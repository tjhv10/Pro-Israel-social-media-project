import uiautomator2 as u2
import time
import random
def main():
    d = u2.connect("10.100.102.102")  # Use the IP address of your device
    # Wait for a moment to ensure connection
    time.sleep(1)

    # Start the Instegram app
    d.app_start("com.instagram.android")
    print("Opened Instegram!")

    # # Wait for the app to load
    time.sleep(15)  # Increased wait time
    print(d.app_list_running())
    # Check if Instegram is running
    if "com.instagram.android" in d.app_list_running():
        print("Instegram is running!")
    else:
        print("Instegram is not running!")
main()