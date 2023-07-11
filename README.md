# [Access NEF](https://github.com/EVOLVED-5G/NEF_emulator)

Add the endpoints in the /etc/hosts file of the NEF and CAPIF

To do this step it is necessary to run Notepad++ with administrator permissions. Once started, open the file located in the path:

`C:\Windows\System32\drivers\etc\hosts`

Add the endpoints provided by Telefonica and save the file

Open a browser and search for:

http://umacsic-nef.apps.ocp-epg.hi.inet:80

Import escenario

# [Smart Irrigation NetApp](https://github.com/EVOLVED-5G/UmaCsicNetApp)

Postgres

`kubectl apply -f environment.yaml`

`kubectl apply -f pv.yaml`

`kubectl apply -f pvc.yaml`

`kubectl apply -f deployment.yaml`

`kubectl apply -f service.yaml`

NetApp

`kubectl apply -f environment.yaml`

`kubectl apply -f deployment.yaml`

`kubectl apply -f service.yaml`

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

# the dirIp is the one provided by the kubernetes cluster

response = post("http://dirIp:10001/api/cells",data={'cell_num' : '...'})

print(response.content)
```

`python datalogger.py`

## Endpoints

### Cell Management 

#### Get 

http://localhost:10001/api/cells

http://localhost:10001/api/cells/{cell-number}

Sends all the cells data stored in the database by default or data of a specified cell if there is a cellNumber in the endpoint

http://localhost:10001/api/cells?verbose=yes

http://localhost:10001/api/cells/{cell-number}?verbose=yes

Verbose option sends a more detailed description about the cell

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

These endpoints provide access to the data stored in the netapp. They can be used by any Vertical App

#### Get 

http://localhost:10001/api/historics

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

Create a post type request using Postman

```json
{
    "action": "validation",
    "parameters": {
        "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/UmaCsicNetApp",
        "GIT_NETAPP_BRANCH": "evolved5g",
        "VERSION_NETAPP": "1.0.8",
        "ENVIRONMENT": "..."
    }
}
```

If no environment is set, it will use by default athenas kubernetes

Check the state of the request