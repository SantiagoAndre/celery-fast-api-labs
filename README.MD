

# FastAPI & Celery Learning Labs

Welcome to my collection of hands-on labs designed to take you from zero to intermediate proficiency in using FastAPI with Celery. This repository contains five progressive labs, each building upon the knowledge and skills developed in the previous one. 

## Overview

These labs offer a practical approach to learning the integration of FastAPI, a modern, fast web framework for building APIs with Python, with Celery, a powerful distributed task queue system. Each lab is structured to enhance your understanding incrementally, starting from basic concepts to more advanced implementations. Each lab has its own README and diagrams to easily understand each one, all labs are over docker and docker-compose to run each one in your machine without any problem.

### Lab Summaries

- **Lab 1: Basic FastAPI Celery Application**  
  Introduction to FastAPI, setting up a simple API.

- **Lab 2: Project Factory and SqlAlChemy integration**  
  Refactoring to a more scalable structure and SQLAlCHemy integration

- **Lab 3:  User Management and Chatroom Module**  
  Implementing user roles, routes decorators to protect them, and a chatroom feature.

- **Lab 4: Real-Time Chat Application**  
  Enhancing the chatroom application with real-time messaging capabilities.

- **Lab 5: WebSocket with Celery**  
  Incorporating WebSocket for live updates on Celery task statuses.

## Installation

You need to have docker and docker-compose configured in your machine. To run each lab you need to follow the next steps:

1. `cd labfolfer`
2. `docker-compose up`

Note: if the lab has database models, after the last command you have to run

```bash
docker-compose exec web bash
alembic revision --autogenerate
alembic upgrade head
```

These commands migrate the models to the database 


## Contribution

If you like my work and you want to contribute with a new lab, go ahead, please flow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.




