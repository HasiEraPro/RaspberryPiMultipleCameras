from PyQt5 import QtWidgets
from interface import Ui_MainWindow
import sys
import paho.mqtt.client as mqtt
import time

messageShare = ""
topicOnline = "online/#"
broker = "127.0.0.1"
port = "1883"
client = mqtt.Client("Master")
pub_topic = "shoot/"


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.shootBtn.clicked.connect(self.shoot_btnClicked)
    def shoot_btnClicked(self):
        t = time.time()
        client.publish(pub_topic, int(t))
        print("clicked")


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

def mqttConnect():
    client.on_message = on_message
    print("connecting to broker ", broker)
    try:

        client.connect(broker)  # connect
        print("subscribing ")
        client.subscribe(topicOnline)  # subscribe
        client.loop_start()  # start loop to process received messages


    except:
        print("No mqtt server found")
        disconnec()
        print("Disconnected")

def disconnec():
    client.disconnect() #disconnect
    client.loop_stop() #stop loop


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    mqttConnect()
    application.show()
    sys.exit(app.exec_())

def start_ftp_server:
    print("started FTP server")
    print("IP address of the server")
    print("publish ip address of the server from mqtt")

if __name__ == "__main__":
    main()