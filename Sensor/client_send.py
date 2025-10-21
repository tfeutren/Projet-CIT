import subprocess
import cv2
import paho.mqtt.client as mqtt
import base64
import numpy as np
import time
import os

broker = "localhost"
topic = "camera/image"

# MQTT setup
client = mqtt.Client()
client.connect(broker, 1883, 60)

# Temporary image file
tmp_file = "/tmp/frame.jpg"

def capture_image():
    # capture from camera (no preview, reduced size)
    subprocess.run([
        "raspistill",
        "-n",              # no preview
        "-o", tmp_file,    # output file
        "-w", "640",       # width
        "-h", "480",       # height
        "-q", "40"         # compression quality (0–100, lower = smaller)
    ])

def optimize_and_encode():
    img = cv2.imread(tmp_file)
    if img is None:
        raise RuntimeError("Capture failed")

    # resize smaller if needed
    max_width = 480
    if img.shape[1] > max_width:
        ratio = max_width / img.shape[1]
        img = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)

    # extra compression to keep payload small (<150 kB)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
    _, buf = cv2.imencode(".jpg", img, encode_param)
    return base64.b64encode(buf).decode("utf-8")

while True:
    capture_image()
    encoded = optimize_and_encode()
    client.publish(topic, encoded)
    print(f"Image sent ({len(encoded)//1024} KB)")
    time.sleep(5)  # send every 5 s
