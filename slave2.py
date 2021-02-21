import paho.mqtt.client as mqtt #import the client1
import time
############
messageGlob = "";
def on_message(client, userdata, message):
    global messageGlob
    messageGlob  = str(message.payload.decode("utf-8"))
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
########################################
broker_address="127.0.0.1"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P2") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","house/bulb1")
client.subscribe("house/bulb1")
client.publish("online/slave2/1")
while(1):
    time.sleep(4) # wait
    print(messageGlob)



#client.loop_stop() #stop the loop