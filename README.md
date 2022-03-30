# P2-mqtt project

This project is a copy of the P2 project but instead of using OPC UA communication protocol, MQTT protocol is use for communication.

To communicate via MQTT in this project you can use mosquitto or hivemq broker.

Thermostats are simulated using a state machine, helped by python transitions package.

Once timescale is receiving data, these data is visualiced on Grafana.

Thermostat.py creates a instance of the object stateMachine. This instance creates a state machine and will simulate a working thermostat that will warm or cool based on the target temperature.


## Use guide

+ Start docker-compose
    * Browse http://localhost:3000/ for Grafana
    * Browse http://localhost:5050/ for PgAdmin4
    * Browse http://localhost:8080/ for HiveMQ
+ Run lab.py
    * Select cuantity of thermostats
+ Run app.py

## Usefull code

Visualize docker container IDs:

    docker ps

Ispect container info:

    docker inspect <dockerID>

Open postgres terminal inside the docker:

    docker exec -it <dockerID> psql -U postgres
