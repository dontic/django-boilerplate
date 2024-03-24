# django-boilerplate

# Introduction

This is a django boilerplate code was made to help you spin up REST backends SUPER fast.

It runs on devcontainers so that you never have an issue colaborating or deploying in different platforms.

It comes with a `Dockerfile` and a sample `docker-compose.yml` so you can deploy FAST.

It already has the following set up:
1. API Configuration
2. Logging
3. Authentication
4. Notifications
5. Celery

# Configuration

## 1. API Configuration

The django project has already everything set up for you.

You can modify it as follows:
### 1.1 API Connections

### 1.2 REST framework

## 2. Logging

By default this project logs both to console and to a log file called `django.log` in the `./data/logs` directory.

You can modify the `.env` file

## 3. Authentication

This project looks to simplify authentication as much as possible, this is why it uses `allauth` as the main authentication library.

It also uses `dj-rest-auth` to handle REST authentication requests.

## 4. Notifications
