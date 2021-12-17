import os
import configparser
import pymysql.cursors
from pyspark.sql import SparkSession

####### global params ##########

#print("===os.getcwd()===", os.getcwd())
config_file = os.path.join(os.getcwd(), "plugins/configs/etl_api")+"/"+'config.ini'
config = configparser.ConfigParser(interpolation=None)
config.read(os.path.join(os.getcwd(), "plugins/configs/etl_api")+"/"+'config.ini')

load_table_name = config['process']['load_table_name']
input_file_name = config['process']['input_file_name']

main_table_name = config["database"]["tablename"]
columns = config["table-"+main_table_name]["columns"]

db_params = {
    'host'      : config['database']['host'],
    'port'      : int(config['database']['port']),
    'db'        : config['database']['db'],
    'user'      : config['database']['username'],
    'password'  : config['database']['password']
}

jdbc_url = "jdbc:mysql://{host}:{port}/{db}?user={user}&password={password}".format(**db_params)


######### spark read/process json and storing to table ##########

def store_db(spark):
    file_path = os.path.join(os.path.join(os.getcwd(),"plugins/datalake/etl_api"),input_file_name)
    df = spark.read.json(file_path)
    df.createOrReplaceTempView(load_table_name)

    query = """SELECT 
                event, 
                properties.time as properties_time, 
                properties.unique_visitor_id as properties_unique_visitor_id, 
                properties.browser as properties_browser, 
                properties.os as properties_os, 
                properties.ha_user_id as properties_ha_user_id, 
                properties.country_code as properties_country_code  
            FROM
                {table}""".format(table=load_table_name)
                
    df_data = spark.sql(query)
    df_data.write.format("jdbc").option("url",jdbc_url).option("dbtable",main_table_name).mode('append').save()

    return True

####### Completed #########

def main():

    spark = SparkSession\
              .builder\
              .master("local[*]")\
              .appName("events")\
              .config("spark.driver.extraClassPath","/usr/local/lib/python3.8/dist-packages/airflow/mysql-connector-java-8.0.23.jar")\
              .getOrCreate()
    
    store_db(spark)
    print("data is stored in db")
