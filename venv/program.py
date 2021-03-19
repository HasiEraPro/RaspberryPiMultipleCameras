from PyQt5 import QtWidgets
from interface import Ui_MainWindow
import sys
import paho.mqtt.client as mqtt
import time
import ntplib
from datetime import  datetime



messageShare = ""
topicOnline = "online/#"
#broker = "127.0.0.1"
broker = "192.168.1.200"
port = "1883"
client = mqtt.Client("Master")
pub_topic = "shoot/"



cur_hour = 0
cur_minute = 0
cur_second = 0


onlineList = []

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.shootBtn.clicked.connect(self.shoot_btnClicked)
    def shoot_btnClicked(self):
        t = time.time()
        time_interval = 5
        sendTime =str(int(t)) + "," + str(time_interval)
        client.publish(pub_topic,sendTime )
        print("clicked")


app = QtWidgets.QApplication(sys.argv)
application = ApplicationWindow()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/broker/clients/connected")


def on_message(client, userdata, msg):
    global onlineList


    global messageShare
    messageShare = msg.topic
    topic = msg.topic.split("/")
    print(topic[1])


    if int(msg.payload) == 0:
        if len(onlineList) > 0:
            if topic[1] in onlineList:
                onlineList.remove(topic[1])
    else:
        if topic[1] not in onlineList:
            onlineList.append(topic[1])

    print(msg.topic+" "+str(msg.payload))

    if len(onlineList) > 0:
        application.ui.listWidget.clear()
        for item in onlineList:
            print ("item>>>"+item)
            application.ui.listWidget.addItem(item)
    else:
        application.ui.listWidget.clear()

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
    global app, application
    mqttConnect()
    application.show()
    sys.exit(app.exec_())




if __name__ == "__main__":
    main()