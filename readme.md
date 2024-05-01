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
4. install pip and git with `sudo apt install python3-pip git`
5. clone this repo with `git clone {{repo_url}}`
5. install the project dependencies with `sudo pip install -r requirements.txt`
6. create the .env file for your system from the sample env file. (add a dot before the filename!)
7. test the script with `python3 ~/image_processing_ocr/image_processing_ocr.py`
8. make an autostartup 
- add the script to /etc/rc.local: `sudo nano /etc/rc.local`
- Add the following line before the exit 0 line in the file: `python3 ~/image_processing_ocr/image_processing_ocr.py &`
- Replace ~/image_processing_ocr/image_processing_ocr.py with the actual path to your Python script.
8.reboot and test if the MQTT topic gets sent out.
