import threading
import tiktokScript as tk
import instegramScript as ins
import twitterScript as twi
import uiautomator2 as u2
import subprocess

def get_connected_devices():
    """
    Get the list of all connected devices using ADB.

    Returns:
    list: A list of device IPs or IDs connected via ADB.
    """
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip().splitlines()

    devices = []
    for line in output[1:]:  # Skip the first line ('List of devices attached')
        if 'device' in line:  # Make sure it's a connected device
            device_id = line.split()[0]  # Extract the device ID (first column)
            devices.append(device_id)
    
    return devices

def run_tiktok_on_phone(device_id):
    """
    Function to run TikTok script on a specific phone.
    
    Parameters:
    device_id (str): The ADB device ID of the phone to run the script on.
    """
    # Connect to the device using uiautomator2
    d = u2.connect(device_id)
    
    if d is not None:
        print(f"Running TikTok script on device: {device_id}")
        tk.main(d)
    else:
        print(f"Could not connect to device: {device_id}")


def run_twitter_on_phone(device_id):
    """
    Function to run Twitter script on a specific phone.
    
    Parameters:
    device_id (str): The ADB device ID of the phone to run the script on.
    """
    # Connect to the device using uiautomator2
    d = u2.connect(device_id)
    
    if d is not None:
        print(f"Running Twitter script on device: {device_id}")
        twi.main(d)
    else:
        print(f"Could not connect to device: {device_id}")

def main():
    # Get the list of all connected devices
    devices = get_connected_devices()
    print(devices)

    if not devices:
        print("No devices connected.")
        return

    threads = []

    # Create and start a thread for each connected device
    for device_id in devices:
        thread = threading.Thread(target=run_tiktok_on_phone, args=(device_id,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

main()
