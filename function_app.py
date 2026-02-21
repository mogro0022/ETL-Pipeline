import os
import logging
import azure.functions as func

from extract import extract_fred_data
from datalake import save_to_datalake
from transform import transform_fred_data
from load import load_data_to_postgres

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def FredDataPipeline(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Starting FRED Economic Data ETL Pipeline...")

    api_key = os.environ.get("FRED_API_KEY")
    db_url = os.environ.get("AZURE_PG_URL")

    if not api_key or not db_url:
        logging.error("Missing critical environment variables. Pipeline aborted.")
        return

    series_id = "DGS10"

    try:
        logging.info(f"[1/3] Extracting data for {series_id}...")
        raw_data = extract_fred_data(series_id=series_id, api_key=api_key)

        if not raw_data:
            logging.warning("No data extracted. Exiting pipeline.")
            return

        # Need this for BlobStorage
        storage_conn = os.environ["AzureWebJobsStorage"]
        logging.info("Saving raw data to Azure Blob Storage...")
        file_name = save_to_datalake(
            raw_data=raw_data, series_id=series_id, connection_string=storage_conn
        )
        logging.info(f"Successfully backed up as {file_name}")

        logging.info(f"[2/3] Transforming data for {series_id}...")
        clean_df = transform_fred_data(raw_data=raw_data, series_id=series_id)

        if clean_df.empty:
            logging.warning("Transformation resulted in an empty dataset. Exiting.")
            return

        logging.info("[3/3] Loading data to Azure PostgreSQL...")
        load_data_to_postgres(df=clean_df, db_url=db_url)

        logging.info("Pipeline execution completed successfully!")

    except Exception as e:
        logging.error(f"Pipeline failed with error: {e}")

    logging.info("Python timer trigger function executed.")
