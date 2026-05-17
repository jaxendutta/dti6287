# DTI 6287: Business Intelligence & Big Data Analytics


## Course Information

|     Course | Business Intelligence & Big Data Analytics |
| ---------: | :----------------------------------------- |
|       Code | DTI 6287                                   |
| Instructor | Dr. Nour El Kadri                          |
|       Term | Spring/Summer 2026                         |

## Group 23

|   #   | Member              | ID                                     |
| :---: | :------------------ | :------------------------------------- |
|   1   | Jaxen Anirban Dutta | [adutt042](mailto:adutt042@uottawa.ca) |
|   2   | Yifei Yu            | [yyu039](mailto:yyu039@uottawa.ca)     |
|   3   |                     |                                        |
|   4   |                     |                                        |
|   5   |                     |                                        |

## Assessment 1: Data Set Selection Pre Processing & Exploration Findings

Analysis of U.S. domestic flight delays from 1987 to 2020. Dataset is a 2 million row stratified sample from the BTS Reporting Carrier On-Time Performance database.

***Dataset Source:***
[mexwell/carrier-on-time-performance-dataset](https://www.kaggle.com/datasets/mexwell/carrier-on-time-performance-dataset) on Kaggle. Original data from the U.S. Bureau of Transportation Statistics. U.S. Government work, not subject to copyright.

### 1. Get Started

#### 1.1. Environment Setup

Requires Python 3.13+, [uv](https://docs.astral.sh/uv/), and [Java 21](https://www.oracle.com/ca-en/java/technologies/downloads/#jdk21-windows).

```bash
# Install dependencies
uv sync
```

#### 1.2. Dataset Download

The dataset is ~850 MB. Choose one of the following options.

| Option A: Direct Download                                                                                                                                                                          | Option B: Kaggle API                            |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| 1. Go to the [Kaggle dataset page](https://www.kaggle.com/datasets/mexwell/carrier-on-time-performance-dataset).<br>2. Click **Download**.<br>3. Extract `airline_2m.csv` into the `data/` folder. | 1. Run `uv run python scripts/download_data.py` |

#### 1.3. Hadoop `winutils` Setup (Windows Only)

Required for Spark to write to the local filesystem on Windows. The repository mirror used here publishes `hadoop-3.3.6` Windows binaries, so the helper downloads that release. Run the following command to download and set up `winutils`:

```bash
uv run python scripts/setup_winutils.py
```

### 2. Run

#### 2.1. Python-based Execution (Non-Spark)

Go through the cells of the following notebook to execute the Python-based data processing and exploration notebook:

```plain
notebooks/01_eda.ipynb
```

#### 2.2. Spark-based Execution

Go through the cells of the following notebook to execute the Spark-based data processing and exploration script:

```plain
notebooks/02_spark_pipeline.ipynb
```
