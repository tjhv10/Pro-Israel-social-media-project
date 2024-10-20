import threading
import time
import tiktokScript as tik
import instegramScript as ins
import twitterScript as twi
import uiautomator2 as u2
import subprocess
import start_adb
from comments import israel_support_comments

def run_tiktok_on_phone(device_id, adb_port):
    """
    Function to run TikTok script on a specific phone connected to a custom ADB server port.
    
    Parameters:
    device_id (str): The IP of the phone to run the script on.
    adb_port (int): The ADB server port for this device.
    """
    # Connect to the device using uiautomator2 on a specific ADB port
    d = u2.connect(f"{device_id}:5555")
    
    if d is not None:
        print(f"Running TikTok script on device: {device_id} (ADB port: {adb_port})")
        tik.main(d)
    else:
        print(f"Could not connect to device: {device_id} on ADB port {adb_port}")

def run_twitter_on_phone(device_id, adb_port):
    """
    Function to run Twitter script on a specific phone connected to a custom ADB server port.
    
    Parameters:
    device_id (str): The IP of the phone to run the script on.
    adb_port (int): The ADB server port for this device.
    """
    # Connect to the device using uiautomator2 on a specific ADB port
    d = u2.connect(f"{device_id}:5555")
    
    if d is not None:
        print(f"Running Twitter script on device: {device_id} (ADB port: {adb_port})")
        twi.main(d)
    else:
        print(f"Could not connect to device: {device_id} on ADB port {adb_port}")

def run_program(device_id, adb_port):
    """
    Function to run Twitter and TikTok scripts on a specific phone connected to a custom ADB server port.
    
    Parameters:
    device_id (str): The IP of the phone.
    adb_port (int): The ADB server port for this device.
    """
    print(f"Attempting to connect to device: {device_id} via ADB port {adb_port}")
    
    # Connect to the device
    d = u2.connect(f"{device_id}:5555")
    
    if d is not None:
        for _ in range(100):
            print(f"Running Twitter script on device: {device_id} (ADB port: {adb_port})")
            tik.main(d)
        # time.sleep(5)  # Delay between scripts
        # print(f"Running TikTok script on device: {device_id} (ADB port: {adb_port})")
        # tik.main(d)
    else:
        print(f"Could not connect to device: {device_id} on ADB port {adb_port}")

def main():
    start_adb.start_and_connect_all_servers()
    # List of device IPs
    devices = [
        "10.100.102.173",
        "10.100.102.170",
        "10.100.102.171",
        "10.100.102.169",
        "10.100.102.172"
    ]
    
    # Starting ADB server port number
    base_adb_port = 5001
    threads = []

    for i, device_id in enumerate(devices):
        # Assign a unique ADB server port for each device
        adb_port = base_adb_port + i
        
        # Start a new ADB server instance on the assigned port
        subprocess.run(['adb', '-P', str(adb_port), 'start-server'], stdout=subprocess.PIPE)
        
        # Connect the device to the ADB server running on its specific port
        subprocess.run(['adb', '-P', str(adb_port), 'connect', f"{device_id}"], stdout=subprocess.PIPE)
        
        # Start a new thread to run the program for each device
        thread = threading.Thread(target=run_program, args=(device_id, adb_port))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


def main_for_1_phone():
    # Specify the IP address of the single device you want to connect to
    device_id = "10.100.102.173"
    adb_port = 5038  # Example ADB server port for this device

    # Start a new ADB server on the specified port
    subprocess.run(['adb', '-P', str(adb_port), 'start-server'], stdout=subprocess.PIPE)
    
    # Connect the device to the ADB server running on its specific port
    subprocess.run(['adb', '-P', str(adb_port), 'connect', f"{device_id}:5555"], stdout=subprocess.PIPE)

    # Run the program on the specified device
    run_program(device_id, adb_port)

# Uncomment the function you want to run
# main()
main_for_1_phone()
