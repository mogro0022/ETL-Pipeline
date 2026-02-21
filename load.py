import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from models import EconomicObservation


def load_data_to_postgres(df: pd.DataFrame, db_url: str):
    if df.empty:
        print("No data to load.")
        return

    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)

    records = df.to_dict(orient="records")

    with Session() as session:
        try:
            stmt = insert(EconomicObservation).values(records)
            update_dict = {"value": stmt.excluded.value}
            upsert_stmt = stmt.on_conflict_do_update(
                constraint="uq_series_date", set_=update_dict
            )
            session.execute(upsert_stmt)
            session.commit()
            print(f"Successfully loaded {len(records)} records into the database.")

        except Exception as e:
            session.rollback()
            print(f"Failed to load data: {e}")
        finally:
            session.close()
