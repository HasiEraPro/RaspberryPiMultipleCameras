import paho.mqtt.client as mqtt
import time

messageShare = ""
topicOnline = "online/#"
broker = "127.0.0.1"
port = "1883"
client = mqtt.Client("client-001")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/broker/clients/connected")


def on_message(client, userdata, msg):
    global messageShare
    messageShare = msg.topic
    topic = msg.topic.split("/")
    print(topic[1])
    print(msg.topic+" "+str(msg.payload))

def main():
    client.on_message = on_message
    print("connecting to broker " ,broker)
    try:

        client.connect(broker)#connect
        print("subscribing ")
        client.subscribe(topicOnline)  # subscribe
        client.loop_start() #start loop to process received messages


    except:
        print("except")


def loop():
    time.sleep(2)
    print("publishing ")
    while(True):
        #client.publish("house/bulb1","off")#publish
        #time.sleep(4)
        #client.publish("house/bulb1", "on")  # publish
        time.sleep(4)
        print(messageShare)
def disconnec():
    client.disconnect() #disconnect
    client.loop_stop() #stop loop

if __name__ == "__main__":
    main()

