
# Airflow ETL pipeline (Python, PySpark, Flask)

This pipeline is orchestrated with Airflow which schedules the pipeline at defined interval and trigger to fetch data from api (with basic auth), store in data lake (/mount), transform it and later push it to data warehouse.





## Installation

There are two parts of this.

```bash
  cd airflow
  cd api
```
A separate readme is avaiable for both in respective directories.

## Deployment

airflow setup
```
cd airflow
pip install -r requirements.txt
```

api setup
```
cd api
pip install -r requirements.txt
```


Run the server now.
```bash
  python server.py
```

It runs on 8000 port.



## Demo

Check here to see the demo.

http://localhost:8000/ (api)\
http://localhost:3000/ (airflow)
## Documentation

[API Design](https://github.com/pritesh543/etl_pipeline_using_airflow/blob/main/API_Design.docx) \
[Airflow Design](https://github.com/pritesh543/etl_pipeline_using_airflow/blob/main/Airflow_Design_Implementation.docx) \
[DDL Queries](https://github.com/pritesh543/etl_pipeline_using_airflow/blob/main/DDL_Queries.docx)

