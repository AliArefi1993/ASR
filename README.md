# TaskOrchestrator
Managing and directing tasks across the ASR and translation services, making it clear that it coordinates multiple processing steps to deliver a final response

## Dependencies

#### Project Requirements
Install project requirements with this command.
```
pip install -r app/requirements.txt
```

### Run microservice
To run the microservice and listen to RabbitMQ management, execute this command from the microservice root directory.
```
python app/queue_listener.py
```
