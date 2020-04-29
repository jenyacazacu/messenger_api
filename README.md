# This is a simple implementation of a messaging API

## Technology stack
- Docker
- Django
- Django Rest Framework
- PostgresSQL
- NGINX

## Functionality
- Users can send a 160 max_length text from a sender to a recipient.
- Users can list the most recent messages from any given sender and to any given recipient.

## Requirements
- You must have Docker installed and running, installation instruction are available [here](https://docs.docker.com/get-docker/)

## How to start and run the API

### Step1: Git clone this repo

### Step 2: From the root directory build the images and start the docker containers

```
messenger_api % docker-compose up
```

or if you prefer 2 steps :)

```
messenger_api % docker-compose build
messenger_api % docker-compose up

```

### Step 3: Done!

### Available API Endpoints:
1. Sending text messages: [http://localhost:1337/api/messages/send/](http://localhost:1337/api/messages/send/) 
```buildoutcfg
POST http://localhost:1337/api/messages/send/
```
```
Request Body
{
    "sender": "string",
    "recipient": "string"
    "message_content": "string"
}
```

2. List recent messages [http://localhost:1337/api/messages/](http://localhost:1337/api/messages/)
```buildoutcfg
GET http://localhost:1337/api/messages/

OPTIONAL query_params: sender, recipient, is_read

EXAMPLE: http://localhost:1337/api/messages/?sender=bob?recipient=alice?is_read=false
```

## Running Tests

### Step 1: Make sure the messenger services are up and running
```
messenger_api % docker-compose up
```

### Step 2: Exec into the `web` service container
```
messenger_api % docker-compose exec web sh
```

### Step 3: Run the tests
```
web % python manage.py test
```

## Future Improvements:
- Replicated DB for reliability and availability.
- Caching of the most recent messages
- Load Balancing of the web server to distribute the load evenly
- Breaking down sending and reading of messages into separate microservices or serverless functions.
- Implementing Web Sockets connection to support asynchronous communication between two users.
- Message received confirmations
- More filtering capabilities based on input from the Client