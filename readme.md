# Food-delivery

Food delivery app created with Django Rest Framework.

## Description

Users can authorize and authenticate. There are three roles with their own set of accesses: superusers, restorators and
customers. To
register, you need to provide a login and a password.

The app also includes restaurant, dishes, orders and order details. Customers can search for their favorite restaurants
and dishes, make orders and watch status of delivery. Restaurants could see information about orders, change status,
create/update/delete dishes.

## Tech stack

- Python 3.10
- Django 4.2.1
- Django Rest Framework 3.14.0
- Djoser 2.2.0
- PostgreSQL
- pip
- drf-spectacular 0.26.2

## Run

Start web application and database in Docker

### Clone project from git via ssh

```commandline
git clone git@github.com:kolaxy/food-delivery.git
```

### Cd into project folder

```commandline
cd food_delivery
```

### Build application Docker image

```commandline
docker build -t kolaxy/food:1.0 .
```

### Run application and database containers

```commandline
docker compose --profile backend up -d
```

### Swagger documentation

http://0.0.0.0:8000/api/v1/schema/docs/