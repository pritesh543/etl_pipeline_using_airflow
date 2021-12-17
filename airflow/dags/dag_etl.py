
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from random import randint

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),"../../plugins"))

from plugins.scripts.etl_api.store_events import main

print("All modules are Imported !")

# prep api input args
dt_format="%Y-%m-%d %H:%M:%S"
username = "john"
password = "john@123"

input_file_name = "events_data.json" # to take from config
api_endpoint="http://localhost:5000/api/events"
event="event_1"
from_timestamp = "2020-10-22 06:36:00" #datetime.strftime(datetime.now()-timedelta(hours=1), dt_format)
to_timestamp = "2020-10-22 08:36:00" #datetime.strftime(datetime.now(), dt_format

url = "{api_endpoint}?event={event}&from_timestamp={from_timestamp}&to_timestamp={to_timestamp}".\
        format(api_endpoint=api_endpoint, event=event, from_timestamp=from_timestamp, to_timestamp=to_timestamp)


def fetch_events():
    resp = requests.get(url, auth=(username, password))
    return resp.json()

#def store_events():
#    return "Data is stored in db !"

def no_events():
    return "No events data found for this time period !"

def _choose_next_task(ti):
    api_resp = ti.xcom_pull(task_ids=['fetch_events_api'])
    # print("***********api_resp************", api_resp)
    try:
        if api_resp[0].get("data", []):
            file_path = os.path.join(os.path.join(os.getcwd(),"plugins/datalake/etl_api"),input_file_name)
            with open(file_path, "w") as f:
                json.dump(api_resp[0].get("data"), f)
            return 'load_data'
        else:
            return 'no_events'
    except Exception as e:
        print("Exception: {}".format(str(e)))
        return 'no_events'

with DAG("dag_etl",
            start_date=datetime(2021, 12 ,1),
            schedule_interval='0 */2 * * *',
            catchup=False,
            tags=['etl']
        ) as dag:
        
        fetch_events_api = PythonOperator(
            task_id="fetch_events_api",
            python_callable=fetch_events)
        
        choose_next_task = BranchPythonOperator(
            task_id="store_to_datalake",
            python_callable=_choose_next_task) 

        store_event_data = PythonOperator(
            task_id="load_data",
            python_callable=main)

        no_events = PythonOperator(
            task_id="no_events",
            python_callable=no_events)

       
        fetch_events_api >> choose_next_task >> [store_event_data, no_events]
