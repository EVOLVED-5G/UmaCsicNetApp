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

# [Smart Irrigation netApp](https://github.com/EVOLVED-5G/UmaCsicNetApp)

## Steps to start the container:

`docker compose build`

`docker compose up`

## Try out

After the container is up and running:

- Send requests to http://localhost:10001