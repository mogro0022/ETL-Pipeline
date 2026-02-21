import os
from dotenv import load_dotenv

from extract import extract_fred_data
from transform import transform_fred_data
from load import load_data_to_postgres


def main():
    print("Starting FRED Economic Data ETL Pipeline...")

    load_dotenv()
    api_key = os.environ.get("FRED_API_KEY")
    db_url = os.environ.get("AZURE_PG_URL")

    if not api_key or not db_url:
        raise ValueError(
            "Missing critical environment variables. Check your .env file."
        )

    series_id = "DGS10"

    try:
        print(f"\n[1/3] Extracting data for {series_id}...")
        raw_data = extract_fred_data(series_id=series_id, api_key=api_key)

        if not raw_data:
            print("No data extracted. Exiting pipeline.")
            return

        print(f"\n[2/3] Transforming data for {series_id}...")
        clean_df = transform_fred_data(raw_data=raw_data, series_id=series_id)

        if clean_df.empty:
            print("Transformation resulted in an empty dataset. Exiting pipeline.")
            return

        print("\n[3/3] Loading data to Azure PostgreSQL...")

        load_data_to_postgres(df=clean_df, db_url=db_url)

        print("\nPipeline execution completed successfully!")

    except Exception as e:
        print(f"\nPipeline failed with error: {e}")


if __name__ == "__main__":
    main()
