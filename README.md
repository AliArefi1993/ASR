# ASR
 The ASR microservice receives an English audio file (in .wav format) and transcribes it into English text.

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
