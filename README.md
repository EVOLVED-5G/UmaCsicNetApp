# Smart Irrigation netApp

## Steps to start the container:

```bash

# 1. 
docker compose build 

# 2. 
docker compose up
```

### Try out

After the container is up and running:

- Send requests to http://localhost:10001


<br><br>

## Create cell and historics

### By python file

Create an environment 

`python -m venv venv`

Activate environment

`.\venv\Scripts\activate`

`pip install requests`

```python
# datalogger.py
import json
from requests import post, get, delete
from datetime import datetime

response = post("http://localhost:10001/api/cells",data={'cell_num' : 'AAAAA1001'})

print(response.content)

# json structure based on the historic model

# timestamp not required

message = {
    "HS10_0" : "123456789",
    "HS10_1" : "1234567890",
    "HS10_2" : "12345678901",
    "HS30_0" : "123456789012",
    "HS30_1" : "1234567890123",
    "HS30_2" : "12345678901234",
    "HS50_0" : "123456789012345",
    "HS50_1" : "1234567890123456",
    "HS50_2" : "12345678901234567",
    "FullBR" : "123456789012345678",
    "AirTC"  : "1234567890123456789",
    "RH"     : "12345678901234567890"
}

response = post("http://localhost:10001/api/historics/",json=message) 

print(response.content)
```

`python datalogger.py`

## Endpoints

### Cell Management 

#### Get 

http://localhost:10001/api/cells

http://localhost:10001/api/cells/{cell-number}

Sends all the cells data stored in the database by default or data of a specified cell if 
there is a cellNumber in the endpoint

http://localhost:10001/api/cells?verbose=yes

http://localhost:10001/api/cells/{cell-number}?verbose=yes

verbose option sends a more detailed description about the cell

#### Post 

http://localhost:10001/api/cells 

- data = cell_num

Creates a new cell entry in the netApp database with the retrieved data in the post request

#### Put 

http://localhost:10001/api/cells/{cell-number}

- data = cell_num

Updates the cell that has the cellNumber given in the endpoint

#### Delete

http://localhost:10001/api/cells/{cell-number}

Deletes the cell with the given cellNumber with its historics


<br>


### Historic Management 

#### Get 

http://localhost:10001/api/historics

http://localhost:10001/api/historics/{external-id}  

Sends the historics attached to the cell where is placed the UE with that external_id. If not external_id
is defined, sends all the historics in database

http://localhost:10001/api/historics?from={index}

From parameter is used to requests historics from the given index to the last.

#### Post 

http://localhost:10001/api/historics/publish/{external-id}

- data = HS10_0, HS10_1, HS10_2, HS30_0, HS30_1, HS30_2, HS50_0, HS50_1, HS50_2, FullBR, AirTC, RH, timestamp

Creates a new historic and attaches it to the cell where is placed the UE (with that external-id)

#### Put 

http://localhost:10001/api/historics/{historic-id}

- data = HS10_0, HS10_1, HS10_2, HS30_0, HS30_1, HS30_2, HS50_0, HS50_1, HS50_2, FullBR, AirTC, RH

Updates the historic that has the historic_id given in the endpoint

#### Delete 

http://localhost:10001/api/historics/{historic_id}

Deletes the historic which has the historic_id given in the endpoint



<br>



### Database utils

#### Get 

http://localhost:10001/api/database/utils/clear

Clear the database of the netApp