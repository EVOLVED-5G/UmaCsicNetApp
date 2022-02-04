# Smart Irrigation netApp

## Steps to start the container:

```bash

# 1. 
docker build -t netapp . 

# 2. 
docker run --name=netapp -p 8000:5000 --network=[network-of-nef_emulator]
```

### Try out

After the container is up and running:

- Send requests to http://localhost:8000



<br><br>



## Endpoints

### Cell Management 

#### Get 

http://localhost:8000/api/v1/cells

http://localhost:8000/api/v1/cells/{cell-number}

Sends all the cells data stored in the database by default or data of a specified cell if 
there is a cellNumber in the endpoint

#### Post 

http://localhost:8000/api/v1/cells 

- data = cell_num, crop_type

Creates a new cell entry in the netApp database with data retrieves in the post request

#### Delete

http://localhost:8000/api/v1/cells/{cell-number}

Deletes the cell with the given cellNumber with its historics

#### Put 

http://localhost:8000/api/v1/cells/{cell-number}

- data = cell_num, crop_type

Updates the cell that has the cellNumber given in the endpoint


<br>


### Historic Management 

#### Get 

http://localhost:8000/api/v1/historics

http://localhost:8000/api/v1/historics/{external-id}  

Sends the historics attached to the cell where is placed the UE with that external_id. If not external_id
is defined, sends all the historics in database

#### Post 

http://localhost:8000/api/v1/historics/{external-id}

- data = temperature, humidity

Creates a new historic and attaches it to the cell where is placed the UE (with that external-id)

#### Put 

http://localhost:8000/api/v1/historics/{historic-id}

- data = temperature, humidity, crop

Updates the historic that has the historic_id given in the endpoint

#### Delete 

http://localhost:8000/api/v1/historics/{historic_id}

Deletes the historic which has the historic_id given in the endpoint

