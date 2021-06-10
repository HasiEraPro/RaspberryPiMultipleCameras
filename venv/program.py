from PyQt5 import QtWidgets
from interface import Ui_MainWindow
import sys
import os
import paho.mqtt.client as mqtt
import time
import ntplib
from datetime import  datetime
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
#-------------------------------------------------------
################ user settings  ###################
#-------------------------------------------------------
messageShare = ""
topicOnline = "online/#"
topic_photo_recived = "photoTaken/"
broker = "192.168.1.200"
port = "1883"
client = mqtt.Client("Master")
pub_topic = "shoot/"


ftp_images_folder = "/home/$USER/ftp/"


#-------------------------------------------------------
############# Global variables  ###################
#-------------------------------------------------------
cur_hour = 0
cur_minute = 0
cur_second = 0

time_interval = 1

onlineList = []

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        global ftp_images_folder
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.labelShowFilePath.setText(ftp_images_folder)
        self.ui.shootBtn.clicked.connect(self.shoot_btnClicked)
        self.ui.spinBox.valueChanged.connect(self.spin_valueChanged)
        self.ui.btnFileDialog.clicked.connect(self.btnFileDialog_clicked)
    def btnFileDialog_clicked(self):
        try:

            directoryName = QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
            if directoryName:

                self.ui.labelShowFilePath.setText(directoryName)
                global ftp_images_folder
                ftp_images_folder = directoryName + "/"
                print(ftp_images_folder)

        except:
            print(sys.exc_info()[0])



    def spin_valueChanged(self):
        global time_interval
        time_interval = self.ui.spinBox.value()
        print(time_interval)
    def shoot_btnClicked(self):
        global ftp_images_folder
        if(os.path.isdir(ftp_images_folder)):
            t = time.time()
            global time_interval
            print("timeinterval=:")
            print(time_interval)
            sendTime =str(int(t)) + "," + str(time_interval)+","+str(ftp_images_folder)
            client.publish(pub_topic,sendTime )



        else:
            try:
                print("else")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Photo Manager")
                msg.setText("Please set a Folder to save Photos First!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            except:
                print(sys.exc_info()[0])

app = QtWidgets.QApplication(sys.argv)
application = ApplicationWindow()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/broker/clients/connected")

def onPhoto_message(client, userdata, msg):
    print("Photo recived")
    msgRaw = str(msg.payload)
    picFullPath = str(ftp_images_folder + "image" + msgRaw[2:-1])
    print(picFullPath)

    if (path.isfile(picFullPath)):
        print("Photo Set")
        pixmap = QPixmap(picFullPath)
        application.ui.pictureLabel.setPixmap(pixmap)



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
        client.subscribe(topic_photo_recived)


        client.message_callback_add(topic_photo_recived, onPhoto_message)
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