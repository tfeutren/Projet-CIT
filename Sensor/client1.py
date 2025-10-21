import paho.mqtt.client as mqtt
import base64

def on_connect(client, userdata, flags, rc):
    print(f"Connect -> {rc}")

def on_message(client, obj, msg):
    print(f"{msg.topic}({msg.qos})v {msg.payload})")
    image_base64 = msg.payload.decode("utf-8")
    # Convertir les données Base64 en données binaires
    image_data = base64.b64decode(image_base64)

    # Enregistrer les données binaires en tant que fichier image
    with open("received_image.jpg", "wb") as image_file:
        image_file.write(image_data)

def on_publish(client, obj, mid):
    print(f"^ {str(mid)}")

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

url = "10.0.1.13"
port = 1883
topic = "test"
mqttc.username_pw_set("cit","cit")
mqttc.connect(url, port, 60)
mqttc.subscribe(topic, 0)
mqttc.loop_forever()