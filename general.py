import threading
import time
import tiktokScript as tik
import twitterScript as twi
import uiautomator2 as u2
from start_adb import *

def run_program(device_id):
    """
    Function to run Twitter and TikTok scripts on a specific phone connected to a custom ADB server port.
    Parameters:
    device_id (str): The IP of the phone.
    """
    print(f"Attempting to connect to device: {device_id}")
    
    # Connect to the device
    d = u2.connect(f"{device_id}:5555")
    
    if d is not None:
        print(f"Running Twitter script on device: {device_id}")
        # twi.main(d)
        # time.sleep(5)  # Delay between scripts
        print(f"Running TikTok script on device: {device_id}")
        tik.main(d)
    else:
        print(f"Could not connect to device: {device_id}")

def main():
    start_and_connect_all_servers()
    # List of device IPs
    
    # Starting ADB server port number
    threads = []
    for dev in device_ips:
        # Start a new thread to run the program for each device
        thread = threading.Thread(target=run_program, args=(dev,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


def main_for_1_phone():
    # Run the program on the specified device
    run_program("10.0.0.25")

# Uncomment the function you want to run
main()
# main_for_1_phone()
