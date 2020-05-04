
# ZZ-compute

![alt text][id]

[id]: img/compute.png "Title"

### Description
The compute service is an integral part of ZZ project. It processes on model 
inference tasks, which are received from a broker (Kafka server).
Result is returned back to broker, and processed by other services, for example
the web-service.

The compute service can also execute custom logic (Python) for pre- and post 
processing. This kind of logic is called **runner** in the system.

The service can query different models. HTTP/HTTPS protocols are used for model
inference now, however list is not exhausted and new protocols logic can be 
easily added.


### Main components
 - **models** - this folder contains classes, which represent the main entities 
 in the service. Mostly all of them inherit from 
 [faust.Record](https://faust.readthedocs.io/en/latest/reference/faust.models.record.html).
 The Record class is used for serialization/deserialization of Python objects.
 - **app** - is the main entry point
 - **config** - contains all configuration settings/logic.
 - **agent** - that's the place where all the job is done. It contains only **2** 
 functions, which query a model and send back a result. **compute_agent** function
 can execute runner as well. 
 
### Interaction process

![alt text][schema]

[schema]: img/compute_schema.png "Title"
 
### Run locally
To run locally application requires Kafka broker and at least one model running.

To install seamlessly Kafka broker we recommend 
[Kafka-docker](https://github.com/wurstmeister/kafka-docker) project. In the project 
you can find **docker-compose-single-broker.yml**

We suggest to create next alias
```bash
alias kafka="docker-compose --file {PATH_TO}/kafka-docker/docker-compose-single-broker.yml up"
```
To run the model please visit **zz-ds-artifacts** repository.

### Questions
For questions, please, reach *andras.gyacsok@boehringer-ingelheim.com*
