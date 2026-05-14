# Assessment 1: Data Set Selection Pre Processing & Exploration Findings

Analysis of U.S. domestic flight delays from 1987 to 2020. Dataset is a 2 million row stratified sample from the BTS Reporting Carrier On-Time Performance database.

## 1. Dataset

Source: [mexwell/carrier-on-time-performance-dataset](https://www.kaggle.com/datasets/mexwell/carrier-on-time-performance-dataset) on Kaggle. Original data from the U.S. Bureau of Transportation Statistics. U.S. Government work, not subject to copyright.

## 2. Get Started

### 2.1. Environment Setup

Requires Python 3.13+, [uv](https://docs.astral.sh/uv/), and Java 11+.

```bash
# 1. Install dependencies
uv sync

# 2. Copy environment template
cp .env.example .env
```

### 2.2. Dataset Download

The dataset is ~850 MB. Choose one of the following options.

| Option A: Direct Download | Option B: Kaggle API |
| :--- | :--- |
| 1. Go to the [Kaggle dataset page](https://www.kaggle.com/datasets/mexwell/carrier-on-time-performance-dataset).<br>2. Click **Download**.<br>3. Extract `airline_2m.csv` into the `data/` folder. | 1. Run `uv run python scripts/download_data.py` |
