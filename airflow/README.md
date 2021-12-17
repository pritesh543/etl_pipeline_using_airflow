
# Airflow Pipeline

This ETL pipeline integrates the API as source and with the use of pyspark transform the data and load in to MySQL database as target database.




## Installation

activate virtual environment with python version >= 3.8.10

```bash
  cd airflow
  pip install -r requirements.txt
```




## Deployment

To deploy this project run

```bash
  export AIRFLOW_HOME="/home/airflow/"
  
  cd /home/airflow
  airflow db init
  airflow webserver -p 8080
```

It runs on 8080 port.


