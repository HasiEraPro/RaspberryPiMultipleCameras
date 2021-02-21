import paho.mqtt.client as mqtt
import time

messageGlob = ""
broker_address = "127.0.0.1"
client_ID = "Slave-01"
sub_topic = "shoot/"
pub_topic = "online/"+client_ID
client = mqtt.Client(client_ID)


def on_message(client, userdata, message):
    global messageGlob
    messageGlob = str(message.payload.decode("utf-8"))
    print(messageGlob)
    # print("message received " ,str(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)


def main():
    client.on_message = on_message
    print("connecting to broker")
    try:
        client.connect(broker_address) # connect to broker
        client.loop_start()  # start the loop
        print("Subscribing to topic", sub_topic)
        client.subscribe(sub_topic)
        client.publish(pub_topic, "on")  # publish
    except:
        print("connection to MQTT broker failed")


def disconnect():
    client.loop_stop()  # stop the loop
    client.disconnect()


def take_photo():
    print("Took photo")


def send_photo_ftp():
    print("Sent photo FTP")


if __name__ == "__main__":
    main()