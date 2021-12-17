from datetime import date, datetime
exp_date_format = "%Y-%m-%d %H:%M:%S"

class InputValidator:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def validate_timestamp(self, timestamp):
        try:
            timestamp = timestamp.split(".")[0].strip()
            return datetime.strptime(timestamp, exp_date_format)
        except Exception as e:
            return None

    def validate_params(self):
        err = []
        if not self.validate_timestamp(self.kwargs["from_timestamp"]):
            err.append("{} - required in format {}".\
                format(self.kwargs["from_timestamp"], exp_date_format))

        if not self.validate_timestamp(self.kwargs["to_timestamp"]):
            err.append("{} - required in format {}".\
                format(self.kwargs["to_timestamp"], exp_date_format))

        return err