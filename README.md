# [Install CAPIF](https://github.com/EVOLVED-5G/CAPIF_API_Services)

`cd services/`

`./run.sh`

# [Install NEF](https://github.com/EVOLVED-5G/NEF_emulator)

If you dont have install make:

`apt install jq`

Then continue with NEF installation

`make prepare-dev-env`

`make build`

`make up`

Login in NEF and import scenary

# [Smart Irrigation netApp](https://github.com/EVOLVED-5G/UmaCsicNetApp)

## Steps to start the container:

`docker compose build`

`docker compose up`

## Create cell

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

response = post("http://localhost:10001/api/cells",data={'cell_num' : '...'})

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

### Historic Management 

#### Get 

http://localhost:10001/api/historics

http://localhost:10001/api/historics/{external-id}  

http://localhost:10001/api/historics?from={index}

From parameter is used to requests historics from the given index to the last.

#### Post 

http://localhost:10001/api/historics

- data = HS10_0, HS10_1, HS10_2, HS30_0, HS30_1, HS30_2, HS50_0, HS50_1, HS50_2, FullBR, AirTC, RH, timestamp

#### Put 

http://localhost:10001/api/historics/{historic-id}

- data = HS10_0, HS10_1, HS10_2, HS30_0, HS30_1, HS30_2, HS50_0, HS50_1, HS50_2, FullBR, AirTC, RH

Updates the historic that has the historic_id given in the endpoint

#### Delete 

http://localhost:10001/api/historics/{historic_id}

Deletes the historic which has the historic_id given in the endpoint

### Database utils

#### Get 

http://localhost:10001/api/database/utils/clear

Clear the database of the netApp

# Validate netApp
