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

## A1. Data Set Selection Pre Processing & Exploration Findings

Analysis of U.S. domestic flight delays from 1987 to 2020. Dataset is a 2 million row stratified sample from the BTS Reporting Carrier On-Time Performance database.

***Dataset Source:***
[mexwell/carrier-on-time-performance-dataset](https://www.kaggle.com/datasets/mexwell/carrier-on-time-performance-dataset) on Kaggle. Original data from the U.S. Bureau of Transportation Statistics. U.S. Government work, not subject to copyright.

### A1.1. Get Started

#### A1.1.1. Environment Setup

Requires Python 3.13+, [uv](https://docs.astral.sh/uv/), and [Java 21](https://www.oracle.com/ca-en/java/technologies/downloads/#jdk21-windows).

```bash
# Install dependencies
uv sync
```

#### A1.1.2. Dataset Download

The dataset is ~850 MB. Choose one of the following options.

| Option A: Direct Download                                                                                                                                                                          | Option B: Kaggle API                            |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| 1. Go to the [Kaggle dataset page](https://www.kaggle.com/datasets/mexwell/carrier-on-time-performance-dataset).<br>2. Click **Download**.<br>3. Extract `airline_2m.csv` into the `data/` folder. | 1. Run `uv run python scripts/download_data.py` |

#### A1.1.3. Hadoop `winutils` Setup (Windows Only)

Required for Spark to write to the local filesystem on Windows. The repository mirror used here publishes `hadoop-3.3.6` Windows binaries, so the helper downloads that release. Run the following command to download and set up `winutils`:

```bash
uv run python scripts/setup_winutils.py
```

### A1.2. Run Notebooks

Based on your environment and preference, choose one of the following options to run the notebooks for data processing and exploration.

***Option A: Python-based Execution (Non-Spark):*** Open `notebooks/01_eda_with_pandas.ipynb` and execute the cells sequentially to perform Python-based data processing and exploration.

***Option B: Spark-based Execution:*** Open `notebooks/01_eda_with_spark.ipynb` and execute the cells sequentially to perform Spark-based data processing and exploration.

## A2. Labelling and Insight Generation using LLMs

Zero-shot semantic labeling of carrier delay-risk profiles using [`MoritzLaurer/deberta-v3-large-zeroshot-v2.0`](https://huggingface.co/MoritzLaurer/deberta-v3-large-zeroshot-v2.0) ([Laurer et al., 2024](https://arxiv.org/abs/2312.17543)), the current state-of-the-art open-source NLI classifier, benchmarked across 28 tasks against the widely commercially adopted 2019 model [`facebook/bart-large-mnli`](https://huggingface.co/facebook/bart-large-mnli) baseline.

Each carrier's delay-cause statistics (2003–2020) are serialized to natural language and classified across four label set iterations (binary → cause-focused → business framing → anchor-based) to document prompt sensitivity and justify the final choice.

Labels are attached back to the full dataset as `delay_risk_label` and carried forward as a feature in Assessment 3.

### A2.1. Environment Setup

```bash
# Sync dependencies
uv sync
```

### A2.2. Run Notebook

Open `notebooks/02_llm_labeling.ipynb` and execute the cells sequentially to perform LLM-based labeling of the airline delay data.

### Outputs

- `output/llm_labels/labels_v1_binary.csv`
- `output/llm_labels/labels_v2_cause_focused.csv`
- `output/llm_labels/labels_v3_business_framing.csv`
- `output/llm_labels/labels_v4_anchor_based.csv`
- `output/llm_labels/hypothesis_per_carrier.png`
- `output/airline_labeled.parquet`
