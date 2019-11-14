# Repo to try how to deploy basic ML pipeline (for dynamic inference) using Docker and Flask-RESTful
- ref:
    - https://mlinproduction.com/docker-for-ml-part-3/ (batch inference)
    - https://mlinproduction.com/docker-for-ml-part-4/ (dynamic inference)
        + generate predictions by making web requests to the container

# Train model while building docker image
`docker build -t docker-api -f Dockerfile .` 

# run container and inspect trained model
`docker run docker-api cat /home/jovyan/model/metadata.json`

# make (batch) inference in a container from image
`docker run docker-api python3 inference.py`

# future: 
- tagging docker image