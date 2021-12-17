from validator import InputValidator
from db import QueryDatabase

class Events:
    """This class interact with validator class
    and database class to access methods"""

    def __init__(self, **kwargs):
        """
        :param: 
                **kwargs -> dict
                {
                    event -> str 
                    from_timestamp -> timestamp
                    to_timestamp -> timestamp    
                }
        """
        self.input_validator = InputValidator(**kwargs)
        self.kwargs = kwargs
    
    def get_events(self):
        """
        This function calls validator to check
        if all the input params are correct
        and return error message else data

        :return:
                 data -> dict or err -> dict         
        """
        err = self.input_validator.validate_params()
        if err:
            return {'err': err}
        else:
            # get object to access methods
            # prepare query while passing input args
            # execute query and fetch result

            query_db = QueryDatabase()
            query = query_db.get_query(**self.kwargs)
            data = query_db.query_db(query)
            return {'data': data}
    
