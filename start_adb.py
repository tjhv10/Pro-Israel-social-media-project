import os
import subprocess
import time


# List of device IPs to connect to (you need to populate this list with actual IPs)
device_ips = [
    # "10.100.102.169",
    # "10.100.102.170",
    # "10.100.102.171",
    # "10.100.102.172",
    # "10.100.102.173",
    "10.100.102.175",
    "10.100.102.176"
]
START_PORT = 5001
NUM_SERVERS = len(device_ips)
def start_adb_server(port):
    """
    Start an ADB server on a specified port.
    """
    # Set the environment variable for the ADB server port
    os.environ["ADB_SERVER_PORT"] = str(port)

    # Start the ADB server on the specified port
    subprocess.run(["adb", "start-server"], check=True)

    print(f"ADB server started on port {port}")

def connect_device(port, device_ip):
    """
    Connect to a device using the specified ADB server port.
    """
    # Run the adb connect command using the custom port
    result = subprocess.run(["adb", "-P", str(port), "connect", device_ip], stdout=subprocess.PIPE)

    # Check the result for success
    if "connected" in result.stdout.decode('utf-8'):
        print(f"Successfully connected to {device_ip} on port {port}")
    else:
        print(f"Failed to connect to {device_ip} on port {port}")
    
def start_and_connect_all_servers():
    """
    Start 60 ADB servers on unique ports and connect to the corresponding devices.
    """
    for i in range(NUM_SERVERS):
        # Calculate the port number (increment from the starting port)
        port = START_PORT + i
        
        # Start the ADB server on this port
        start_adb_server(port)
        
        # Wait briefly before connecting to the device
        time.sleep(1)
        
        # Connect the device with the current ADB server port
        connect_device(port, device_ips[i])
        
        # Wait briefly to avoid overwhelming the system
        time.sleep(1)
