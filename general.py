import threading
import time
import tiktokScript as tik
import twitterScript as twi
import instegramScript as inst
import uiautomator2 as u2
from start_adb import *
from concurrent.futures import ThreadPoolExecutor

def run_program(device_id):
    """
    Function to run Twitter and TikTok scripts on a specific phone connected to a custom ADB server port.
    Parameters:
    device_id (str): The IP of the phone.
    """
    print(f"Attempting to connect to device: {device_id}")
    
    # Connect to the device
    d = u2.connect(device_id)
    
    if d is not None:
        print(f"Running Twitter script on device: {device_id}")
        twi.main(d)
        time.sleep(5)  # Delay between scripts
        print(f"Running TikTok script on device: {device_id}")
        tik.main(d)
        time.sleep(5)  # Delay between scripts
        print(f"Running Instagram script on device: {device_id}")
        inst.main(d)
        # time.sleep(0000)
        
    else:
        print(f"Could not connect to device: {device_id}")

def main():
    start_and_connect_all_servers()
    # Define the maximum number of concurrent threads to limit CPU usage
    max_threads = 16  # Adjust this based on your system’s capabilities
    
    # Use ThreadPoolExecutor to manage thread pool
    with ThreadPoolExecutor(max_threads) as executor:
        # Submit each device to the thread pool
        futures = [executor.submit(run_program, dev) for dev in device_ips]
        
        # Wait for all threads to complete
        for future in futures:
            future.result()  # Blocking call to ensure each thread completes

def main_for_1_phone():
    # Run the program on the specified device
    run_program("10.0.0.25")

# Uncomment the function you want to run
main()
# main_for_1_phone()
