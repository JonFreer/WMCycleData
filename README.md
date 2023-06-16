## WM CYCLE COUNTER

This project aims to create an Web App and API to display and make available the Cycle Count Data from the West Midlands Vivacity API

## Development

### Setup

- Generate certificates using [mkcert](https://github.com/FiloSottile/mkcert):

      cd traefik/certs
      mkcert -cert-file dev.cert -key-file dev.pem "cyclecounter.localhost" "*.cyclecounter.localhost"
      
- Create a `.env` file using the `example.env` template:

      cp example.env .env

- Download and build docker image dependencies:

      INFRA=dev make pull
      INFRA=dev make build

- Launch application:

      INFRA=dev make up
      
The infrastructure should now be running at `cyclecounter.localhost`, make sure that
this resolves to `127.0.0.1`!

# Deployment

- Add the DOMAIN environment variable to the .env file and set to your desired domain