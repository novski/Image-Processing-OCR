import os
import time
import subprocess
import easyocr
import paho.mqtt.client as mqtt
import pigpio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MQTT configuration
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")
mqtt_topic_usb = os.getenv("MQTT_TOPIC_USB")
mqtt_topic_picamera = os.getenv("MQTT_TOPIC_PICAMERA")

# Function to flash the LED
def flash_led(pin, duration):
    pi = pigpio.pi()
    pi.set_mode(pin, pigpio.OUTPUT)
    pi.write(pin, 1)
    time.sleep(duration)
    pi.write(pin, 0)
    pi.stop()

# Function to capture an image with USB camera
def capture_usb_image(image_path, flash_pin):
    # Use fswebcam to capture image from USB camera
    subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", image_path])
    flash_led(flash_pin, 0.5)  # Flash LED

# Function to capture an image with PiCamera
def capture_picamera_image(image_path, flash_pin):
    # Initialize PiCamera
    with picamera.PiCamera() as camera:
        # Capture an image
        camera.capture(image_path)
    flash_led(flash_pin, 0.5)  # Flash LED

# Function to process image and send value over MQTT
def process_image_and_send(image_path, mqtt_topic):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Process the image using EasyOCR
    results = reader.readtext(image_path)

    # Extract the recognized text
    recognized_text = ""
    for result in results:
        recognized_text += result[1] + "\n"

    # Initialize MQTT client
    client = mqtt.Client("TextRecognitionClient")

    # Set username and password for MQTT client
    client.username_pw_set(username=mqtt_username, password=mqtt_password)

    # Connect to MQTT broker
    client.connect(mqtt_broker)

    # Publish the recognized text over MQTT
    client.publish(mqtt_topic, recognized_text)

    # Disconnect MQTT client
    client.disconnect()

# Main loop
while True:
    # Check if USB camera is enabled
    if os.getenv("ENABLE_USB_CAMERA") == "true":
        # Capture an image using USB camera
        image_path_usb = os.getenv("PICTURE_PATH_USB")
        capture_usb_image(image_path_usb, int(os.getenv("LED_PIN_USB")))  # Assuming the LED is connected to GPIO pin specified in .env

        # Process image and send value over MQTT for USB camera
        process_image_and_send(image_path_usb, mqtt_topic_usb)

    # Check if PiCamera is enabled
    if os.getenv("ENABLE_PICAMERA") == "true":
        # Capture an image using PiCamera
        image_path_picamera = os.getenv("PICTURE_PATH_PICAMERA")
        capture_picamera_image(image_path_picamera, int(os.getenv("LED_PIN_PICAMERA")))  # Assuming the LED is connected to GPIO pin specified in .env

        # Process image and send value over MQTT for PiCamera
        process_image_and_send(image_path_picamera, mqtt_topic_picamera)

    # Set wake-up timer for 60 minutes using rtcwake
    loop_time = os.getenv("LOOP_TIME")
    subprocess.run(["sudo", "rtcwake", "-m", "mem", "-s", loop_time])
