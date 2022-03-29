import paho.mqtt.client as mqtt
import time

broker_address = 'localhost'

def start_mqtt_client(state_machine, count):

    # Create client instance
    client =mqtt.Client('stateMachine_client_publisher')
    print('Client instance created')

    # Connect client to broker
    client.connect(broker_address, 1883, 60)
    print('Client connected to broker')

    while True:
        # Create publications for all PLC
        for i in range(int(count)):
            # Publish state machine data in the broker
            client.publish('TH/id'+ str(i+1), state_machine[i].id)
            client.publish('TH/time'+ str(i+1), state_machine[i].temp)
            client.publish('TH/state'+ str(i+1), state_machine[i].state)
            client.publish('TH/target'+ str(i+1), state_machine[i].target)
        time.sleep(5)
