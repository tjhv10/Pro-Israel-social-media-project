import os
import subprocess
import threading
import numpy as np
import uiautomator2 as u2
import time
import cv2
import random
from comments import israel_support_comments

twitter_handles = [
    "@MaxAbrahms",
    "@MickyRosenfeld",
    "@RaphaelAhren",
    "@YaakovLappin",
    "@YnetNews",
    "@HananyaNaftali",
    "@AmbDermer",
    "@BoothWilliam",
    "@AnshelPfeffer",
    "@ElhananMiller",
    "@GershonBaskin",
    "@HonestReporting",
    "@Issacharoff",
    "@JeffreyGoldberg",
    "@KhaledAbuToameh",
    "@LahavHarkov",
    "@DannyNis"
]

adb_reset_event = threading.Event()
action_lock = threading.Lock()
function_work = threading.Event()
# Global variable to track lock status
lock_acquired = False

def acquire_action_lock():
    global lock_acquired
    print(f"Thread {threading.current_thread().name} attempting to acquire action lock.")
    action_lock.acquire()
    lock_acquired = True
    print(f"Thread {threading.current_thread().name} acquired action lock.")

def release_action_lock():
    global lock_acquired
    action_lock.release()
    lock_acquired = False
    print(f"Thread {threading.current_thread().name} released action lock.")

import threading
import time
import subprocess
import os

# Example of device IPs and their corresponding ports
device_config = {
    "10.100.102.170": 5037,  # Device 1
    "10.100.102.171": 5038,  # Device 2
    # Add more device IPs and ports here
}

# def get_connected_devices():
#     """
#     Get the list of all connected devices using ADB.

#     Returns:
#     list: A list of device IPs or IDs connected via ADB.
#     """
#     result = ''
#     result += subprocess.run(['adb','-P 5038', 'devices'], stdout=subprocess.PIPE)
#     output = result.stdout.decode('utf-8').strip().splitlines()
#     print(output)
#     devices = []
#     for line in output[1:]:  # Skip the first line ('List of devices attached')
#         if 'device' in line:  # Make sure it's a connected device
#             device_id = line.split()[0]  # Extract the device ID (first column)
#             devices.append(device_id)
    
#     return devices

def connect_to_devices():
    print(f"{threading.current_thread().name}: Starting connect_to_devices function")
    for ip, port in device_config.items():
        # Connect to the device on its specific port
        result = os.system(f"adb -P {port} connect {ip}")
        if result == 0:
            print(f"{threading.current_thread().name}: Connected to {ip} on port {port}")
        else:
            print(f"{threading.current_thread().name}: Failed to connect to {ip} on port {port}")
    print(f"{threading.current_thread().name}: Finished connect_to_devices function")


def restart_adb_periodically(port,interval=30):
    while True:
        time.sleep(interval)
        # Assuming function_work is a threading.Event() that's being checked somewhere
        if function_work.is_set():
            print(f"{threading.current_thread().name}: waiting")
            while function_work.is_set():
                print("Sleeping...")
                time.sleep(0.1)
            print(f"{threading.current_thread().name}: done waiting")
        print(f"{threading.current_thread().name}: Setting ADB reset event to pause actions...")
        adb_reset_event.set()  # Set the event to signal that ADB is resetting
        acquire_action_lock()  # Lock the action only for the ADB reset thread.
        try:
            print(f"{threading.current_thread().name} on {port}: Restarting ADB server...")
            os.system("adb -P "+str(port)+" kill-server")
            time.sleep(2)
            os.system("adb -P "+str(port)+" start-server")
            print(f"{threading.current_thread().name}: ADB server restarted.")
            time.sleep(1)
            connect_to_devices()  # Reconnect to devices after restarting ADB
            time.sleep(2)
        finally:
            release_action_lock()

        print(f"{threading.current_thread().name}: Clearing ADB reset event...")
        adb_reset_event.clear()  # Clear the event to resume actions
        print(f"{threading.current_thread().name}: Resuming after ADB reset.")




def tap_like_button(d, like_button_template_path="icons/twitter_icons/like.png"):
    print(f"{threading.current_thread().name}: Starting tap_like_button function")
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused2 due to ADB reset event.")
        time.sleep(13)
    screenshot_path = take_screenshot(d,threading.current_thread().name)
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused2 due to ADB reset event.")
        time.sleep(13)
    best_match, second_best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path)
    time.sleep(1)
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused2 due to ADB reset event.")
        time.sleep(13)
    time.sleep(1)    
    function_work.set()
    if best_match:
        best_coordinates = best_match
        print(f"Like button found at {best_coordinates}, tapping...")
        if second_best_match:
            second_coordinates = second_best_match
            if (best_coordinates[1] < second_coordinates[1]):
                d.click(int(second_coordinates[0]), int(second_coordinates[1]))
                print(f"Tapped second-best match at {second_coordinates}.")
            else:
                d.click(int(best_coordinates[0]), int(best_coordinates[1]))
                print(f"Tapped best match at {best_coordinates}.")
        else:
            d.click(int(best_coordinates[0]), int(best_coordinates[1]))
            print(f"Tapped best match at {best_coordinates}.")
    else:
        print(f"{threading.current_thread().name}: Like button not found on the screen.")
    function_work.clear()
    print(f"{threading.current_thread().name}: Finished tap_like_button function")

def find_best_and_second_best_match(image_path, template_path):
    print(f"{threading.current_thread().name}: Finding best and second-best match...")
    function_work.set()
    img = cv2.imread(image_path)
    template = cv2.imread(template_path)

    if img is None or template is None:
        print(f"{threading.current_thread().name}: Error loading images.")
        return None, None

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    yloc, xloc = np.where(result >= threshold)
    matches = list(zip(xloc, yloc))

    if matches:
        best_match = max(matches, key=lambda coord: result[coord[1], coord[0]])
        matches.remove(best_match)
        second_best_match = max(matches, key=lambda coord: result[coord[1], coord[0]]) if matches else None
        print(f"Best match found at {best_match}, second-best match found at {second_best_match}.")
        function_work.clear()
        return best_match, second_best_match
    else:
        print(f"{threading.current_thread().name}: No matches found.")
        function_work.clear()
        return None, None
    

def comment_text(d, text, comment_template_path="icons/twitter_icons/comment.png"):
    print(f"{threading.current_thread().name}: Starting comment_text function")
    
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused3 due to ADB reset event.")
        time.sleep(13)
    
    screenshot_path = take_screenshot(d,threading.current_thread().name)
    best_match, _ = find_best_and_second_best_match(screenshot_path, comment_template_path)
    time.sleep(1)
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused10 due to ADB reset event.")
        time.sleep(13)
    time.sleep(1)
    function_work.set()
    if best_match:
        d.click(int(best_match[0]), int(best_match[1]))  # Unpack directly
        time.sleep(2)
        if adb_reset_event.is_set():
            print(f"{threading.current_thread().name}: Paused30 due to ADB reset event.")
            time.sleep(13)
        for char in text:
            d.send_keys(char, clear=False)
            time.sleep(random.uniform(0.005, 0.01))
        if adb_reset_event.is_set():
            print(f"{threading.current_thread().name}: Paused30 due to ADB reset event.")
            time.sleep(13)    
        time.sleep(1)
        d.click(600, 125)  # Click the post button
    else:
        print(f"{threading.current_thread().name}: Comment icon not found on the screen.")
    
    function_work.clear()
    print(f"{threading.current_thread().name}: Finished comment_text function")


def scroll_like_and_comment(d):
    print(f"{threading.current_thread().name}: Starting scroll_like_and_comment function")
    actions = ['like', 'comment', 'both', 'none']
    for _ in range(30):
        if adb_reset_event.is_set():
            print(f"{threading.current_thread().name}: Paused8 due to ADB reset event.")
            time.sleep(13)
        function_work.set()
        if d(scrollable=True).exists:
            start_x = random.randint(400, 600)
            start_y = random.randint(900, 1200)
            end_y = start_y - random.randint(400, 600)
            swipe_duration = random.uniform(0.04, 0.06)
            d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
            print(f"Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
        else:
            print(f"{threading.current_thread().name}: No scrollable view found!")
        time.sleep(random.uniform(2, 14))
        action = random.choice(actions)
        print(f"Action chosen: {action}")
        text = random.choice(israel_support_comments)
        function_work.clear()
        if action == 'like':
            tap_like_button(d)
            print(f"{threading.current_thread().name}: Liked the post.")

        elif action == 'comment':
            comment_text(d, text)
            print(f"Commented: {text}")

        elif action == 'both':
            tap_like_button(d)
            print(f"{threading.current_thread().name}: Liked the post.")
            time.sleep(2)
            comment_text(d, text)
            print(f"Commented: {text}")
        else:
            if adb_reset_event.is_set():
                print(f"{threading.current_thread().name}: Paused6 due to ADB reset event.")
                time.sleep(13)
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused6 due to ADB reset event.")
        time.sleep(13)
    function_work.set()
    d.press("back")
    d.press("back")
    function_work.clear()
    print(f"{threading.current_thread().name}: Finished scroll_like_and_comment function")


def take_screenshot(d,thread):
    if adb_reset_event.is_set():
        print(f"{thread}: Paused8 due to ADB reset event.")
        time.sleep(13)
    filename="Screenshots/"+thread + '-screenshot_twi.png'
    print(f"{thread}: Taking screenshot...")
    function_work.set()
    d.screenshot(filename)
    function_work.clear()
    print(f"Screenshot saved as {filename}.")
    return filename

def scroll_random_number(d):
    """
    Scrolls down a random number of times between 1 and 3 and then scrolls up.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused4 due to ADB reset event.")
        time.sleep(13)
    function_work.set()
    if d(scrollable=True).exists:
        print(f"{threading.current_thread().name}: Found a scrollable view! Swiping down...")

        # Randomly choose how many times to swipe (between 1 and 3)
        num_swipes = random.randint(1, 6)
        print(f"Number of swipes: {num_swipes}")

        # Perform the swipe action for the chosen number of times
        for _ in range(num_swipes):
            function_work.set()
            if d(scrollable=True).exists:
                start_x = random.randint(400, 600)
                start_y = random.randint(900, 1200)
                end_y = start_y - random.randint(400, 600)
                swipe_duration = random.uniform(0.04, 0.06)
                d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
                print(f"Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
            else:
                print(f"{threading.current_thread().name}: No scrollable view found!")
            
            time.sleep(random.randint(2, 10))
        time.sleep(3)
        # Swipe up to return to the previous content
        d.swipe(500, 300, 500, 800, duration = 0.05)
        print(f"{threading.current_thread().name}: Swipped up!")
        time.sleep(3)
    else:
        print(f"{threading.current_thread().name}: No scrollable view found!")
    function_work.clear()
def search_and_go_to_page(d, text):
    """
    Searches for the specified text in Twitter and navigates to the desired page.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to search for.
    """
    if adb_reset_event.is_set():
        print(f"{threading.current_thread().name}: Paused5 due to ADB reset event.")
        time.sleep(13)
    function_work.set()
    # Perform the search
    d.click(180, 1500)
    print(f"{threading.current_thread().name}: Clicked on the search button.")
    time.sleep(3)

    # Click on the search input field
    d.click(360, 140)
    time.sleep(5)
    print("hi")
    # Type each character of the search term with a random delay to simulate human typing
    for char in text:
        print("hix")
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay between 0.1 and 0.3 seconds
    time.sleep(2)
    print(f"Typed '{text}' in the search bar naturally.")
    d.click(350,250)  # Press Enter (key code 66) after typing the search text
    print(f"{threading.current_thread().name}: Got into the page!")
    function_work.clear()
    time.sleep(5)



def main(d,port):
    """
    The main function connects to the Android device and performs various Twitter actions.
    """
    # connect_to_devices()
    adb_restart_thread = threading.Thread(target=restart_adb_periodically, args=(port), daemon=True)
    adb_restart_thread.start()
    time.sleep(2)
    function_work.set()
    # Start the Twitter app
    d.app_start("com.twitter.android")
    print(f"{threading.current_thread().name}: Opened Twitter!")
    time.sleep(7)  # Wait for Twitter to fully load
    d.click(75,1500) # Go to home
    function_work.clear()
    for _ in range(random.randint(4,10)):
        scroll_random_number(d)
        time.sleep(4)
        tap_like_button(d)
        time.sleep(2)
    time.sleep(2)
    for page in twitter_handles:
        search_and_go_to_page(d, page)
        time.sleep(2)
        # Perform scrolling and liking of tweets
        scroll_like_and_comment(d)
        if adb_reset_event.is_set():
            print(f"{threading.current_thread().name}: Paused11 due to ADB reset event.")
            time.sleep(13)
        function_work.set()
        d.click(75,1500) # Go to home
        time.sleep(4)
        function_work.clear()
        for _ in range(random.randint(4,10)):
            scroll_random_number(d)
            time.sleep(4)
            tap_like_button(d)
            time.sleep(2)
        time.sleep(5)
    if adb_reset_event.is_set():
            print(f"{threading.current_thread().name}: Paused11 due to ADB reset event.")
            time.sleep(13)
    d.app_stop("com.twitter.android")
    time.sleep(4)


# d = u2.connect("10.100.102.171")  # Use the IP address of your device
# main(d)