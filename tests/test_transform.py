from io import BytesIO

import pandas as pd
import pytest

from ingest_taxi_data import transform_data


def _to_parquet_buffer(df: pd.DataFrame) -> BytesIO:
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    return buffer


def test_transform_yellow_basic_shape_and_columns() -> None:
    source = pd.DataFrame(
        {
            "VendorID": [1, 2],
            "tpep_pickup_datetime": ["2024-01-01 10:00:00", "2024-01-02 11:00:00"],
            "tpep_dropoff_datetime": ["2024-01-01 10:20:00", "2024-01-02 11:25:00"],
            "passenger_count": [1, 2],
            "trip_distance": [2.3, 4.2],
            "payment_type": [1, 2],
            "fare_amount": [12.0, 18.5],
            "tip_amount": [2.0, 3.5],
            "total_amount": [15.0, 23.0],
        }
    )

    transformed = transform_data(_to_parquet_buffer(source), "yellow")

    assert len(transformed) == 2
    assert "pickup_day_of_week" in transformed.columns
    assert "pickup_year" in transformed.columns
    assert "pickup_month" in transformed.columns
    assert "taxi_type" in transformed.columns
    assert transformed["taxi_type"].eq("yellow").all()


def test_transform_green_drops_non_positive_total_amount() -> None:
    source = pd.DataFrame(
        {
            "VendorID": [1, 2],
            "lpep_pickup_datetime": ["2024-01-01 10:00:00", "2024-01-02 11:00:00"],
            "lpep_dropoff_datetime": ["2024-01-01 10:20:00", "2024-01-02 11:25:00"],
            "passenger_count": [1, 2],
            "trip_distance": [2.3, 4.2],
            "payment_type": [1, 2],
            "fare_amount": [12.0, 18.5],
            "tip_amount": [2.0, 3.5],
            "total_amount": [15.0, -1.0],
        }
    )

    transformed = transform_data(_to_parquet_buffer(source), "green")

    assert len(transformed) == 1
    assert transformed["total_amount"].gt(0).all()


def test_transform_rejects_invalid_taxi_type() -> None:
    source = pd.DataFrame(
        {
            "VendorID": [1],
            "tpep_pickup_datetime": ["2024-01-01 10:00:00"],
            "tpep_dropoff_datetime": ["2024-01-01 10:20:00"],
            "passenger_count": [1],
            "trip_distance": [2.3],
            "payment_type": [1],
            "fare_amount": [12.0],
            "tip_amount": [2.0],
            "total_amount": [15.0],
        }
    )

    with pytest.raises(ValueError, match="taxi_type"):
        transform_data(_to_parquet_buffer(source), "blue")
