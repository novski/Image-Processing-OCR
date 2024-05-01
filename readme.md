# Image processing OCR
This is a verry basic script to make a picture been interpreted to text and sent out over MQTT.

It's tested with:
- Raspberry Pi Zero V2 and Raspberry Pi Camera 2.1

## install
1. create an sd card with raspbian os lite and ssh connection
2. update the system sudo apt update && sudo apt upgrade -Y
3. create aditional power saveing conditions in /boot/firmware/config.txt
```
# Disable HDMI
hdmi_blanking=1
# Disable Bluetooth (optional)
dtoverlay=disable-bt
```
4. install pip, git and because picamera2 breaks by now we cannot install it with pip so execute `sudo apt install git python3-venv python3-picamera2 --no-install-recommends -y`
5. clone this repo with `git clone {{repo_url}}`
6. change directory in to the cloned repo `cd Image-Processing-OCR`
7. make your virtual environement and activate it `python -m venv .venv && source .venv/bin/activate`
8. install the project dependencies with `sudo pip install -r requirements.txt`
9. check if picamera2 is in the pip list else `deactivate` and `python3 -m venv --system-site-packages .venv`
10. create the .env file for your system from the sample env file. (add a dot before the filename!)
11. test the script with `python3 image_processing_ocr.py`
12. make an autostartup script
    create a file with:
    ```
    #!/bin/bash

    # Activate the virtual environment
    source ~/Image-Processing-OCR/.venv/bin/activate

    # Run your Python script
    python ~/Image-Processing-OCR/image_processing_ocr.py

    ```
    - add the script to /etc/rc.local: `sudo nano /etc/rc.local`
    - Add the following line before the exit 0 line in the file: `Image-Processing-OCR/run_script.sh &`
    - Replace `Image-Processing-OCR/run_script.sh` with the actual path to your shell script.
13. reboot and test if the MQTT topic gets sent out.

## debug
check if camera takes picture: `libcamera-still -o test.jpg`