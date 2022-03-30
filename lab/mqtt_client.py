import paho.mqtt.client as mqtt
import time

broker_address = 'localhost'

def start_mqtt_client(state_machine, count):

    # Create client instance
    client =mqtt.Client('stateMachine_client_publisher')
    print('Client instance created')

    # Connect client to broker
    client.connect(broker_address, 1883, 60)    # Mosquitto broker
    # client.connect(broker_address, 1881, 60)  # Hivemq broker
    print('Client connected to broker')

    while True:
        # Create publications for all PLC
        for i in range(int(count)):
            # Publish state machine data in the broker
            client.publish('TH'+str(i+1)+'/id', state_machine[i].id)
            client.publish('TH'+str(i+1)+'/temp', state_machine[i].temp)
            client.publish('TH'+str(i+1)+'/state', state_machine[i].state)
            client.publish('TH'+str(i+1)+'/target', state_machine[i].target)
        time.sleep(5)
