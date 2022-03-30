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
therm_num = 3
lap = 5

class data:
    def __init__(self):
        self.id = 0
        self.temp = 0
        self.state = ''
        self.target = 0

data_list = []

def start_client(count):
    global data_list
    for i in range(therm_num):
        init_data = data()
        data_list.append(init_data)

    def on_connect(client, userdata, flags, rc):
            client.subscribe('TH1/#')
            client.subscribe('TH2/#')
            client.subscribe('TH3/#')

    def on_message(client, userdata, msg):
        global data_list
        print('Message arrived')
        data_list = clasify_values(msg.topic, msg.payload, data_list)
            
    
    try:
        # Create client instance
        client =mqtt.Client('stateMachine_client_subscriber')
        client.on_connect = on_connect
        client.on_message = on_message
        print('Client instance created')

        # Connect client to broker
        client.connect(broker_address, 1883, 60)    # Mosquitto broker
        # client.connect(broker_address, 1881, 60)  # Hivemq broker
        print('Client connected to broker')

    except:
        print('Error connecting to server')
    else:
        client.loop_forever()
        # while True:
        #     print('Loop')
        #     for j in range(therm_num):
        #         insert_value(data_list[i].id, data_list[i].temp, data_list[i].state, data_list[i].target)
        #     time.sleep(lap)

def insert_value(id, temp, state, target):
    print('Sending values to DB')
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state, target) VALUES ('"+str(id)+"', current_timestamp,"+str(temp)+",'"+str(state)+"',"+str(target)+")")
    conn.commit()
    cursor.close()

def clasify_values(topic, payload, list):
    print('Clasifying values')
    print(topic)
    if str(topic).find('TH1')!=-1:
        if topic == 'TH1/id':
            x = str(payload).split("\'")
            print(x[1])
            data_list[0].id = x[1]
        elif topic == 'TH1/temp':
            x = str(payload).split("\'")
            print(x[1])
            data_list[0].temp= x[1]
        elif topic == 'TH1/state':
            x = str(payload).split("\'")
            print(x[1])
            data_list[0].state = x[1]
        elif topic == 'TH1/target':
            x = str(payload).split("\'")
            print(x[1])
            data_list[0].target = x[1]
        print('Id: '+data_list[0].id+' Temp: '+ str(data_list[0].temp)+' State: '+ data_list[0].state+' Target: '+ str(data_list[0].target))
        insert_value(data_list[0].id, data_list[0].temp, data_list[0].state, data_list[0].target)

    elif str(topic).find('TH2')!=-1:
        if topic == 'TH2/id':
            x = str(payload).split("\'")
            print(x[1])
            data_list[1].id = x[1]
        elif topic == 'TH2/temp':
            x = str(payload).split("\'")
            print(x[1])
            data_list[1].temp= x[1]
        elif topic == 'TH2/state':
            x = str(payload).split("\'")
            print(x[1])
            data_list[1].state = x[1]
        elif topic == 'TH2/target':
            x = str(payload).split("\'")
            print(x[1])
            data_list[1].target = x[1]
        print('Id: '+data_list[1].id+' Temp: '+ str(data_list[1].temp)+' State: '+data_list[1].state+' Target: '+ str(data_list[1].target))
        insert_value(data_list[1].id, data_list[1].temp, data_list[1].state, data_list[1].target)

    elif str(topic).find('TH3')!=-1:
        if topic == 'TH3/id':
            x = str(payload).split("\'")
            print(x[1])
            data_list[2].id = x[1]
        elif topic == 'TH3/temp':
            x = str(payload).split("\'")
            print(x[1])
            data_list[2].temp= x[1]
        elif topic == 'TH3/state':
            x = str(payload).split("\'")
            print(x[1])
            data_list[2].state = x[1]
        elif topic == 'TH3/target':
            x = str(payload).split("\'")
            print(x[1])
            data_list[2].target = x[1]
        print('Id: '+data_list[2].id+' Temp: '+ str(data_list[2].temp)+' State: '+ data_list[2].state+' Target: '+ str(data_list[2].target))
        insert_value(data_list[2].id, data_list[2].temp, data_list[2].state, data_list[2].target)
    return list