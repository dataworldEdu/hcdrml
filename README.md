# Home Credit Default Risk Machine Learning App

## 개요
토이 프로젝트로 이런걸 함

## Project Structure
```txt
.
|-- README.md
|-- __pycache__
|   `-- main.cpython-39.pyc
|-- app
|   |-- __init__.py
|   |-- __pycache__
|   |   |-- __init__.cpython-39.pyc
|   |   |-- decorator.cpython-39.pyc
|   |   `-- enums.cpython-39.pyc
|   |-- data
|   |   |-- __init__.py
|   |   |-- __pycache__
|   |   |   |-- __init__.cpython-39.pyc
|   |   |   |-- ingestion.cpython-39.pyc
|   |   |   |-- preprocessing.cpython-39.pyc
|   |   |   `-- utils.cpython-39.pyc
|   |   |-- csvdf
|   |   |   |-- __init__.py
|   |   |   |-- __pycache__
|   |   |   |   |-- __init__.cpython-39.pyc
|   |   |   |   |-- application_train_df.cpython-39.pyc
|   |   |   |   |-- bureau_df.cpython-39.pyc
|   |   |   |   |-- credit_card_df.cpython-39.pyc
|   |   |   |   |-- installment_payments_df.cpython-39.pyc
|   |   |   |   |-- post_cache_df.cpython-39.pyc
|   |   |   |   `-- previous_application_df.cpython-39.pyc
|   |   |   |-- application_train_df.py
|   |   |   |-- bureau_df.py
|   |   |   |-- credit_card_df.py
|   |   |   |-- installment_payments_df.py
|   |   |   |-- post_cache_df.py
|   |   |   `-- previous_application_df.py
|   |   |-- ingestion.py
|   |   |-- preprocessing.py
|   |   |-- sqldf
|   |   |   |-- __init__.py
|   |   |   `-- __pycache__
|   |   |       `-- __init__.cpython-39.pyc
|   |   `-- utils.py
|   |-- decorator.py
|   |-- enums.py
|   |-- feature
|   |   `-- __init__.py
|   `-- model
|       |-- __init__.py
|       |-- __pycache__
|       |   |-- __init__.cpython-39.pyc
|       |   `-- lightgbm.cpython-39.pyc
|       |-- lightgbm.py
|       `-- utils.py
|-- data
|   |-- external
|   |   `-- ex.txt
|   |-- intermi
|   |   `-- inter.txt
|   |-- processed
|   |   `-- processed.txt
|   `-- raw
|       |-- POS_CASH_balance.csv
|       |-- application_test.csv
|       |-- application_train.csv
|       |-- bureau.csv
|       |-- credit_card_balance.csv
|       |-- installments_payments.csv
|       |-- intent_test_data.csv
|       |-- previous_application.csv
|       `-- raw.txt
|-- main.py
|-- models
|   `-- model.txt
|-- profile.py
|-- profile_result.txt
|-- requirement.txt
|-- test
|   |-- __init__.py
|   |-- data
|   |   |-- __init__.py
|   |   |-- collect_test.py
|   |   |-- ingestion_test.py
|   |   `-- save_test.py
|   `-- setting_test.py
```

