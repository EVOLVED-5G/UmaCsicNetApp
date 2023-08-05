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

Login to the admin dashboard NEF and import scenary

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

#### [GET] 

http://localhost:10001/api/cells

http://localhost:10001/api/cells/{cell-number}

Sends all the cells data stored in the database by default or data of a specified cell if there is a cellNumber in the endpoint

http://localhost:10001/api/cells?verbose=yes

http://localhost:10001/api/cells/{cell-number}?verbose=yes

Verbose option sends a more detailed description about the cell

#### [POST] 

http://localhost:10001/api/cells 

- data = cell_num

Creates a new cell entry in the netApp database with the retrieved data in the post request

#### [PUT] 

http://localhost:10001/api/cells/{cell-number}

- data = cell_num

Updates the cell that has the cellNumber given in the endpoint

#### [DELETE]

http://localhost:10001/api/cells/{cell-number}

Deletes the cell with the given cellNumber with its historics

### Historic Management 

These endpoints provide access to the data stored in the netapp. They can be used by any Vertical App

#### [GET] 

http://localhost:10001/api/historics

http://localhost:10001/api/historics?from={index}

From parameter is used to requests historics from the given index to the last.

#### [POST] 

http://localhost:10001/api/historics

- data = HS10_0, HS10_1, HS10_2, HS30_0, HS30_1, HS30_2, HS50_0, HS50_1, HS50_2, FullBR, AirTC, RH, timestamp

#### [PUT] 

http://localhost:10001/api/historics/{historic-id}

- data = HS10_0, HS10_1, HS10_2, HS30_0, HS30_1, HS30_2, HS50_0, HS50_1, HS50_2, FullBR, AirTC, RH

Updates the historic that has the historic_id given in the endpoint

#### [DELETE] 

http://localhost:10001/api/historics/{historic_id}

Deletes the historic which has the historic_id given in the endpoint

### Database utils

#### [GET] 

http://localhost:10001/api/database/utils/clear

Clear the database of the netApp

### Multiespectralcam Api

#### [POST]

http://localhost:10001/api/images/{band}?process={process}

Save an image with required band. Process not required to apply to the image

#### [GET]

http://localhost:10001/api/images/normal/{nameimage}

Retrieve an image with required name

#### [DELETE]

http://localhost:10001/api/images/normal/{nameimage}

Delete the image with the specified name

#### [GET]

http://localhost:10001/api/images/processed/{nameimage}

Retrieve a processed image

#### [DELETE]

http://localhost:10001/api/images/processed/{nameimage}

Delete a processed image

#### [GET]

http://localhost:10001/api/images/normal

Retrieve the name of all stored normal images

#### [GET]

http://localhost:10001/api/images/processed

Retrieve the name of all stored processed images

# Validate NetApp

Create a POST type request using Postman

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

If no environment is set, it will use by default Athens kubernetes

Check the state of the request