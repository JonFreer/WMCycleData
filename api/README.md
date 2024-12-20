# API

This API is built upon SQLAlchemy and FastAPI. It interfaces with the timescale DB. Upon creation, it should automatically create the appropriate tables. To create the hypertables and continous aggregates view [create-view.sh](create-view.sh)

# Schedule 

Scheduling is handled by ofelia. It is set up to execute a post request on the API every hour.

The logs for this are saved in the data/ofelia