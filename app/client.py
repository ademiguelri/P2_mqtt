import time
import docker.config as config
from warnings import catch_warnings;
import psycopg2
import random
import paho.mqtt.client as mqtt

CONNECTION = "postgres://"+config.username+":"+config.password+"@"+config.host+":"+config.port+"/"+config.dbName
query_create_table = "CREATE TABLE therm (id VARCHAR (10), datetime TIMESTAMP, temp FLOAT, state VARCHAR (10), target INTEGER);"
query_create_hypertable = "SELECT create_hypertable('therm', 'datetime');"
drop_table = "DROP TABLE therm;"

broker_address = 'localhost'

id = ''
temp = ''
state = ''
target = ''

def start_client(count):
    global id
    global temp
    global state
    global target

    def on_message(client, userdata, msg):
        global id
        global temp
        global state
        global target

        if str(msg.topic).find('TH/id'):
            print(msg.topic+' '+str(msg.payload))
            id = msg.payload
        elif str(msg.topic).find('TH/temp'):
            print(msg.topic+' '+str(msg.payload))
            temp = msg.payload
        elif str(msg.topic).find('TH/state'):
            print(msg.topic+' '+str(msg.payload))
            state = msg.payload
        elif str(msg.topic).find('TH/target'):
            print(msg.topic+' '+str(msg.payload))
            target = msg.payload
            insert_value(id, temp, state, target)
            
    def on_connect(client, userdata, flags, rc):
        client.subscribe('TH/#')

    try:
        # Create client instance
        client =mqtt.Client('stateMachine_client_subscriber')
        client.on_connect = on_connect
        client.on_message = on_message
        print('Client instance created')

        # Connect client to broker
        client.connect(broker_address, 1883, 60)
        print('Client connected to broker')

    except:
        print('Error connecting to server')
    else:
        with psycopg2.connect(CONNECTION) as conn:
            cursor = conn.cursor()
            cursor.execute(drop_table)
            cursor.execute(query_create_table)
            conn.commit()
            cursor.execute(query_create_hypertable)
            conn.commit()
            cursor.close()

        client.loop_forever()



def insert_value(id, temp, state, target):
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state, target) VALUES ('"+str(id)+"', current_timestamp,"+str(temp)+",'"+str(state)+"',"+str(target)+")")
    conn.commit()
    cursor.close()
