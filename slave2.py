#-------------------------------------------------------
################ Includes ###################
#-------------------------------------------------------

import paho.mqtt.client as mqtt
import ftplib
from time import sleep
import time
import logging
#-------------------------------------------------------
################ user settings  ###################
#-------------------------------------------------------

#set this to your master rpi address
broker_address = "192.168.1.200"
#this is the id of this module,used to be renamed the photos
client_ID = "Slave-02"
#mqtt subscription topic,the master will send command from this topic
sub_topic = "shoot/"
pub_topic = "online/" + client_ID
client = mqtt.Client(client_ID)
#ftp server address ,this is same as the master rpi(static ip)
ftp_server_address = "192.168.1.200"
#ftp seteuped to use the local user login username
ftp_user = "pi"
#ftp seteuped to use the local user login password
ftp_passwd = "GoatHotel77)$"
#ftp port
ftp_port = 21



#-------------------------------------------------------
############# Global variables  ###################
#-------------------------------------------------------
messageGlob = ""

timeInterval = 0
recivedTime = 0
#camera = PiCamera()





def main():
    client.on_message = on_message
    client.on_connect = on_connect
    client.will_set(pub_topic, 0, qos=0, retain=True)  # set will
    print("connecting to broker")
    try:
        client.connect(broker_address)  # connect to broker

        print("Subscribing to topic", sub_topic)
        client.subscribe(sub_topic)

    except:
        print("connection to MQTT broker failed")

    loop()


def on_message(client, userdata, message):
    global messageGlob
    messageGlob = str(message.payload.decode("utf-8"))
    global timeInterval, recivedTime
    recivedTime, timeInterval = int(messageGlob.split(',')[0]), int(messageGlob.split(',')[1])
    nowTime = time.time()

    print(timeInterval)
    print(recivedTime)

    if ((nowTime - recivedTime) >= 0):
        timeToTake = timeInterval - (nowTime - recivedTime)
        take_photo(timeToTake)
        send_photo_ftp()
    else:
        take_photo(1)
        send_photo_ftp()

    # print("message received " ,str(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)


def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags" + str(flags) + "result code " \
                  + str(rc) + "client1_id")
    if rc == 0:
        client.connected_flag = True
        client.publish(pub_topic, 1, retain=True)
    else:
        client.bad_connection_flag = True


def loop():
    while (1):
        client.loop_start()  # start the loop


def disconnect():
    client.loop_stop()  # stop the loop
    client.publish(pub_topic, 0, retain=True)
    client.disconnect()


def take_photo(delay):
    global camera
    sleep(delay)
    #camera.capture('/home/pi/ProgramSlave/images/pic' + str(recivedTime) + '.jpg')
    print("Took photo")


def send_photo_ftp():
    session = ftplib.FTP()
    session.connect(ftp_server_address, ftp_port)
    session.login(ftp_user, ftp_passwd)
    file = open('/home/pi/ProgramSlave/images/pic' + str(recivedTime) + '.jpg', "rb")  # file to send

    try:
        session.storbinary('STOR image' + str(recivedTime) + '_' + client_ID + '.jpg', file)  # send the file
        file.close()  # close file and FTP
        session.quit()
        print("Sent photo FTP Success")
    except:
        print("Sent photo FTP Failed")
        file.close()  # close file and FTP
        session.quit()
    finally:
        file.close()  # close file and FTP
        session.quit()


if __name__ == "__main__":
    main()