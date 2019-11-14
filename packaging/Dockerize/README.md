# Repo to try how to deploy basic ML pipeline (for dynamic inference) using Docker and Flask-RESTful
- ref:
    - https://mlinproduction.com/docker-for-ml-part-3/ (batch inference)
    - https://mlinproduction.com/docker-for-ml-part-4/ (dynamic inference)
        + generate predictions by making web requests to the container

# Train model for batch inference while building docker image
`docker build -t docker-api -f Dockerfile .` 
# Or, train model for online inference
`docker build -t docker-model -f Dockerfile .` 

# run container and inspect trained model
`docker run docker-api cat /home/jovyan/model/metadata.json`

# make batch inference in a container from image
`docker run docker-model python3 inference.py`

# Or, for online inference, launch the web server. This lets us issue POST requests to the endpoint and retrieve predictions
`docker run -it -p 5000:5000 docker-api python3 api.py`
# Then, to make a POST request to 127.0.0.1:5000:
```curl -i -H "Content-Type: application/json" -X POST \
    -d '{"CRIM": 15.02, "ZN": 0.0, "INDUS": 18.1, "CHAS": 0.0, "NOX": 0.614, \
         "RM": 5.3, "AGE": 97.3, "DIS": 2.1, "RAD": 24.0, "TAX": 666.0, \
         "PTRATIO": 20.2, "B": 349.48, "LSTAT": 24.9}' \
        127.0.0.1:5000/predict
```



# future: 
- tagging docker image
- use Kubernetes to scale ML 