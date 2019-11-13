# Repo to try how to deploy basic ML pipeline (for batch inference) using Docker
- ref: https://mlinproduction.com/docker-for-ml-part-3/

# Train model while building docker image
`docker build -t docker-model -f Dockerfile .`
```
 ---> ac196e35d071
Successfully built ac196e35d071
Successfully tagged docker-model:latest
```

# run container and inspect trained model
`docker run docker-model cat /home/jovyan/model/metadata.json`

# make (batch) inference in a container from image
`docker run docker-model python3 inference.py`

# future: 
- online inference - expose model as REST API
- tagging docker image