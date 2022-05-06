# Home Credit Default Risk Machine Learning App

## 개요
토이 프로젝트로 이런걸 함

## Project Structure
```txt
.
├── README.md
├── app
│ ├── __init__.py
│ ├── config.py
│ ├── data
│ │ ├── __init__.py
│ │ ├── csvdf
│ │ │ ├── __init__.py
│ │ │ ├── application_train_df.py
│ │ │ ├── bureau_df.py
│ │ │ ├── credit_card_df.py
│ │ │ ├── installment_payments_df.py
│ │ │ ├── post_cache_df.py
│ │ │ └── previous_application_df.py
│ │ ├── ingestion.py
│ │ ├── preprocessing.py
│ │ ├── sqldf
│ │ │ └── __init__.py
│ │ └── utils.py
│ ├── feature
│ │ └── __init__.py
│ ├── main.py
│ ├── model
│ │ ├── __init__.py
│ │ ├── lightgbm.py
│ │ └── utils.py
│ └── settins.py
├── data
│ ├── external
│ │ └── ex.txt
│ ├── intermi
│ │ └── inter.txt
│ ├── processed
│ │ └── processed.txt
│ └── raw
│     ├── POS_CASH_balance.csv
│     ├── application_test.csv
│     ├── application_train.csv
│     ├── bureau.csv
│     ├── credit_card_balance.csv
│     ├── installments_payments.csv
│     ├── intent_test_data.csv
│     ├── previous_application.csv
│     └── raw.txt
├── models
│ └── model.txt
├── requirement.txt
├── test
│ ├── __init__.py
│ └── data
│     ├── __init__.py
│     └── ingestion_test.py
```

