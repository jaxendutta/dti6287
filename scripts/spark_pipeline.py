"""
Spark Preprocessing Pipeline
Loads the raw CSV, cleans it, engineers features, and writes
a partitioned Parquet file ready for analysis and ML modeling.

USAGE:
    uv run python scripts/spark_pipeline.py
"""

import os

from bi.config import (
    RAW_CSV, SPARK_PARQUET, OUTPUT_DIR, SPARK_CSV_ENCODING,
    SPARK_APP_NAME, SPARK_DRIVER_MEMORY, SPARK_SHUFFLE_PARTITIONS,
    SPARK_PYTHON, DROP_COLS, CORE_COLS, INT_COLS, DOUBLE_COLS,
    DELAY_MIN_MINUTES, DELAY_MAX_MINUTES,
)

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType


def build_spark() -> SparkSession:
    os.environ["PYSPARK_PYTHON"]        = SPARK_PYTHON
    os.environ["PYSPARK_DRIVER_PYTHON"] = SPARK_PYTHON
    return (
        SparkSession.builder
        .appName(SPARK_APP_NAME)
        .config("spark.driver.memory", SPARK_DRIVER_MEMORY)
        .config("spark.sql.shuffle.partitions", SPARK_SHUFFLE_PARTITIONS)
        .getOrCreate()
    )


def load(spark: SparkSession) -> DataFrame:
    print(f"> Loading: {RAW_CSV}")
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "false")
        .option("nullValue", "")
        .option("encoding", SPARK_CSV_ENCODING)
        .csv(str(RAW_CSV))
    )
    print(f"  > Raw shape: {df.count():,} rows × {len(df.columns)} columns")
    return df


def drop_columns(df: DataFrame) -> DataFrame:
    return df.drop(*[c for c in DROP_COLS if c in df.columns])


def cast_types(df: DataFrame) -> DataFrame:
    # INT_COLS: values like "0.00" need float intermediary before int
    for col in INT_COLS:
        if col in df.columns:
            df = df.withColumn(col, F.col(col).cast(DoubleType()).cast(IntegerType()))
    for col in DOUBLE_COLS:
        if col in df.columns:
            df = df.withColumn(col, F.col(col).cast(DoubleType()))
    return df


def clean(df: DataFrame) -> DataFrame:
    before = df.count()
    df = df.dropna(subset=[c for c in CORE_COLS if c in df.columns])
    df = df.filter(
        F.col("ArrDelay").isNull() |
        F.col("ArrDelay").between(DELAY_MIN_MINUTES, DELAY_MAX_MINUTES)
    ).filter(
        F.col("DepDelay").isNull() |
        F.col("DepDelay").between(DELAY_MIN_MINUTES, DELAY_MAX_MINUTES)
    )
    print(f"  > Removed {before - df.count():,} invalid rows")
    return df


def engineer_features(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn("Decade",    (F.floor(F.col("Year") / 10) * 10).cast(IntegerType()))
        .withColumn("Season",
            F.when(F.col("Month").isin(12, 1, 2), 1)
             .when(F.col("Month").isin(3, 4, 5),  2)
             .when(F.col("Month").isin(6, 7, 8),  3)
             .otherwise(4)
             .cast(IntegerType())
        )
        .withColumn("IsWeekend", F.when(F.col("DayOfWeek").isin(6, 7), 1).otherwise(0).cast(IntegerType()))
        .withColumn("DepHour",   (F.col("CRSDepTime") / 100).cast(IntegerType()))
        .withColumn("IsDelayed", F.coalesce(F.col("ArrDel15"), F.lit(0)).cast(IntegerType()))
    )


def write_summary(df: DataFrame) -> None:
    total = df.count()
    null_exprs = [
        F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
        for c in df.columns
    ]
    null_counts = df.select(null_exprs).collect()[0]

    rows = [
        (c, total - null_counts[c], null_counts[c], round(null_counts[c] / total * 100, 2))
        for c in df.columns
    ]
    stats = df.sparkSession.createDataFrame(rows, ["column", "valid", "missing", "missing_pct"])
    out = str(OUTPUT_DIR / "summary_stats")
    stats.coalesce(1).write.mode("overwrite").option("header", "true").csv(out)
    print(f"  > Summary stats -> {out}")


def main() -> None:
    spark = build_spark()
    spark.sparkContext.setLogLevel("WARN")

    df = load(spark)
    df = drop_columns(df)
    df = cast_types(df)
    df = clean(df)
    df = engineer_features(df)

    print(f"  > Final shape: {df.count():,} rows × {len(df.columns)} columns")

    write_summary(df)

    df.write.mode("overwrite").partitionBy("Year").parquet(str(SPARK_PARQUET))
    print(f"  > Parquet saved -> {SPARK_PARQUET}")

    spark.stop()


if __name__ == "__main__":
    main()