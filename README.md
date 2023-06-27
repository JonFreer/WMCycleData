# WM CYCLE DATA

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

### Loading in data

Sample data can be loaded in without a vivacity api key. This can be done by navigating to `cyclecounter.localhost/api/docs`, authorizing with the api key set in the .env (EXTERNAL_API_TOKEN) and the using the /load_dummy_counters and /load_dummy_counts requests.

### Utility Scripts

Autoformat code:

    ./dev/autoformat.sh

Install git hooks for running pre-commit checks:

    ./dev/install_git_hooks.sh

## Deployment

- Add the `DOMAIN` environment variable to the .env file and set to your desired domain
