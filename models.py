import datetime
from sqlalchemy import String, Date, Float, UniqueConstraint, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class EconomicObservation(Base):
    __tablename__ = "economic_observations"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    series_id: Mapped[str] = mapped_column(String(50), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("series_id", "date", name="uq_series_date"),
        Index("idx_series_date", "series_id", "date"),
    )
