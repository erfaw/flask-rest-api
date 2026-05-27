# Simple RESTful api with Flask

This is a project which outputed from **[elasti_py](https://github.com/erfaw/elasti_py/tree/master/Day066-erf/1.%20introdoce%20to%20RESTful%20APIs)** repo.

to make `CRUD` operations on Cafes on a city!

# Endpoints

1. `/` : Returns all Cafes.
2. `random/`: Return a random Cafe from DB.
3. `add/`: Insert a Cafe record to DB.
4. `update-price/<int:cafe_id>/`: Update an existing Cafe record.
5. `/report-closed/<int:cafe_id>`: Delete an existing Cafe record.

# Cafe Model

* id : Primary Key Integer
* name : String(255) Unique
* map_url : String(500), nullable=False
* img_url : String(500), nullable=False
* location : String(500), nullable=False
* seats : String(250), nullable=False
* has_toilet : Boolean, nullable=False
* has_wifi : Boolean, nullable=False
* has_sockets : Boolean, nullable=False
* can_take_calls : Boolean, nullable=False
* coffee_price : String(250), nullable=True