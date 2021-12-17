from pymysql import connections
import pymysql.cursors
import configparser
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

# db details from config
db_params = {
    'host' : config['database']['host'],
    'port' : int(config['database']['port']),
    'db' : config['database']['db'],
    'user' : config['database']['username'],
    'password' : config['database']['password']
}

# table level info
tablename = config["database"]["tablename"]
columns = config["table-"+tablename]["columns"]

class QueryDatabase:
    def __init__(self):
        pass

    def get_query(self, **kwargs):
        query_parms = {
            **kwargs,
            "table" : tablename,
            "columns" : columns
        }

        # prepare query
        query = """ SELECT 
                        {columns}
                    FROM 
                        {table} 
                    WHERE 
                        EVENT='{event}' 
                            AND 
                    PROPERTIES_TIME 
                        BETWEEN '{from_timestamp}' AND '{to_timestamp}';""".\
            format(**query_parms)
        return query
    
    def connect_db(self):
        # Connect to the database
        connection = None
        try:
            connection = pymysql.connect(**db_params, cursorclass=pymysql.cursors.DictCursor)
        except ConnectionError as con_error:
            pass
        except Exception as e:
            pass

        return connection

    def query_db(self, query):
        # get connection object
        connection = self.connect_db()
        
        data = []
        try:
            with connection.cursor() as cursor:
                # Read events
                cursor.execute(query)

                for item in cursor.fetchall():
                    # creating nested dict for properties
                    tmp_dict = {}
                    tmp_dict["event"] = item["event"]
                    del item["event"]
                    tmp_dict["properties"] = item
                    
                    # converting datetime object to string here
                    tmp_dict["properties"]["time"] = str(item["time"])
                    data.append(tmp_dict)
        finally:
            connection.close()
        
        return data