# tp-flask_sqlalchemy_spasic_veljko

## Summary
Backend of a hotel room reservation app for a hotel chain. The app allows users to search for available rooms according to their criteria, make reservations, and cancel existing reservations. The app also allows the hotel administration to manage rooms.

/

Backend d'une application de réservation de chambres d'hôtel pour une chaîne d'hôtels. L'application permet aux utilisateurs de rechercher des chambres disponibles selon leurs critères, de faire des réservations, et d'annuler des réservations existantes. L'application également permet à l'administration de l'hôtel de gérer les chambres.

## How to setup

To **setup** the project follow these instructions.

A the **root of the project**:
1. In the terminal:
```sh
docker compose build
docker compose up
```
A/N: If the web service doesn't start when you run `docker compose up` and instead you get output like:
`web-1 exited with code 1` then open a separate terminal and run:
```sh
docker compose restart web
```


2. In second (or third) terminal:
```sh
docker ps
```
This will list all *docker containers*. Look for the **container id** you need (web or db) and run the following command to enter that specific container:
```sh
docker exec -it CONTAINER_ID /bin/bash
```
You need to enter db container to initialize db.
When you enter db container run following commands:
- `cd app/src/hotel`
- `flask db init`
- `flask db migrate`
- `flask db upgrade`

A/N: Inside db container, *if you want* you can proceed to enter **MySQL**. To do so, use the following command:
```sh
mysql -u root -p hotel_db
```
After, you'll be requested to enter root's password. Type **pass** and press enter.

To exit any entered container just run `exit`.