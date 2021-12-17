
# Events API

This api provides events data for specific events with time durations. So, basically this API expects three input arguments.




## Installation

activate virtual environment with python version >= 3.8.10

```bash
  cd Assessment
  pip install -r requirements.txt
```

use the same environment for Airflow also.


## Deployment

To deploy this project run

```bash
  python server.py
```

It runs on 5000 port by default. keep the same as it is being used by airflow task as well.



## API Reference

#### Get all events

```http
  GET /api/events?
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `event` | `string` | **Required**. event name |
| `from_timestamp` | `string` | **Required**. time duration |
| `to_timestamp` | `string` | **Required**. time duration |


### requires basic auth
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username |
| `password`      | `string` | **Required**. password |


Takes three arguments and returns the events.


## Documentation

Attached in the zip folder.
