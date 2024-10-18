import os
import subprocess
import threading
import numpy as np
import uiautomator2 as u2
import time
import cv2
import random
from comments import israel_support_comments
 
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

device_ips = get_connected_devices()

twitter_handles = [
    "@GershonBaskin",
    "@HonestReporting",
    "@Issacharoff",
    "@JeffreyGoldberg",
    "@KhaledAbuToameh",
    "@LahavHarkov",
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
    "@DannyNis"
]

adb_reset_event = threading.Event()
action_lock = threading.Lock()

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

def connect_to_devices():
    print("Starting connect_to_devices function")
    for ip in device_ips:
        result = os.system(f"adb connect {ip}")
        if result == 0:
            print(f"Connected to {ip}")
        else:
            print(f"Failed to connect to {ip}")
    print("Finished connect_to_devices function")


def restart_adb_periodically(interval=600):
    while True:
        time.sleep(interval)
        print("Setting ADB reset event to pause actions...")
        adb_reset_event.set()  # Set the event to signal that ADB is resetting
        
        with action_lock:  # Prevent actions during ADB restart
            print("Restarting ADB server...")
            os.system("adb kill-server")
            time.sleep(2)
            os.system("adb start-server")
            print("ADB server restarted.")
            time.sleep(1)
            connect_to_devices()
            time.sleep(2)

        print("Clearing ADB reset event...")
        adb_reset_event.clear()  # Clear the event to resume actions
        print("Resuming after ADB reset.")


def scroll_once(d):
    print("Starting scroll_once function")
    
    if adb_reset_event.is_set():
        print("Paused1 due to ADB reset event.")
        time.sleep(13)
    
    acquire_action_lock()
    try:
        print("Starting scroll action")
        if d(scrollable=True).exists:
            start_x = random.randint(400, 600)
            start_y = random.randint(900, 1200)
            end_y = start_y - random.randint(400, 600)
            swipe_duration = random.uniform(0.04, 0.06)
            d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
            print(f"Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
        else:
            print("No scrollable view found!")
    finally:
        release_action_lock()

    print("Finished scroll_once function")

def tap_like_button(d, like_button_template_path="icons/twitter_icons/like.png"):
    print("Starting tap_like_button function")
    
    if adb_reset_event.is_set():
        print("Paused2 due to ADB reset event.")
        time.sleep(13)

    acquire_action_lock()
    try:
        screenshot_path = take_screenshot(d)
        best_match, second_best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path)

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
            print("Like button not found on the screen.")
    finally:
        release_action_lock()

    print("Finished tap_like_button function")

def find_best_and_second_best_match(image_path, template_path):
    print("Finding best and second-best match...")
    img = cv2.imread(image_path)
    template = cv2.imread(template_path)

    if img is None or template is None:
        print("Error loading images.")
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
        return best_match, second_best_match
    else:
        print("No matches found.")
        return None, None

def comment_text(d, text, comment_template_path="icons/twitter_icons/comment.png"):
    print("Starting comment_text function")

    if adb_reset_event.is_set():
        print("Paused3 due to ADB reset event.")
        time.sleep(13)

    acquire_action_lock()
    try:
        screenshot_path = take_screenshot(d)
        best_match, _ = find_best_and_second_best_match(screenshot_path, comment_template_path)

        time.sleep(1)
        if best_match:
            d.click(int(best_match[0]), int(best_match[1]))  # Unpack directly
            time.sleep(2)
            for char in text:
                d.send_keys(char, clear=False)
                time.sleep(random.uniform(0.05, 0.1))
            time.sleep(1)
            d.click(600, 125)  # Click the post button
        else:
            print("Comment icon not found on the screen.")
    finally:
        release_action_lock()

    print("Finished comment_text function")

def scroll_and_like(d):
    print("Starting scroll_and_like function")
    for _ in range(30):
        if adb_reset_event.is_set():
            print("Paused7 due to ADB reset event.")
            time.sleep(13)
        time.sleep(random.uniform(2, 14))
        if d(scrollable=True).exists:
            start_x = random.randint(400, 600)
            start_y = random.randint(900, 1200)
            end_y = start_y - random.randint(400, 600)
            swipe_duration = random.uniform(0.04, 0.06)
            d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
            print(f"Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
        else:
            print("No scrollable view found!")
        time.sleep(random.uniform(1, 14))
        action = random.choice([1, 2, 3, 4, 5])
        if action != 1:
            print("Pressing like!")
            tap_like_button(d)
        else:
            print("Not pressing like!")
    print("Finished scroll_and_like function")

def scroll_like_and_comment(d):
    print("Starting scroll_like_and_comment function")
    actions = ['like', 'comment', 'both', 'none']
    for _ in range(30):
        print("start loop")
        time.sleep(2)
        print("stop sleep")
        print(adb_reset_event.is_set())
        if adb_reset_event.is_set():
            print("Paused8 due to ADB reset event.")
            time.sleep(13)
        acquire_action_lock()
        if d(scrollable=True).exists:
            start_x = random.randint(400, 600)
            start_y = random.randint(900, 1200)
            end_y = start_y - random.randint(400, 600)
            swipe_duration = random.uniform(0.04, 0.06)
            d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
            print(f"Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
        else:
            print("No scrollable view found!")
        time.sleep(random.uniform(2, 14))
        action = random.choice(actions)
        print(f"Action chosen: {action}")
        text = random.choice(israel_support_comments)

        if action == 'like':
            release_action_lock()
            tap_like_button(d)
            print("Liked the post.")

        elif action == 'comment':
            release_action_lock()
            comment_text(d, text)
            print(f"Commented: {text}")

        elif action == 'both':
            release_action_lock()
            tap_like_button(d)
            print("Liked the post.")
            time.sleep(2)
            comment_text(d, text)
            print(f"Commented: {text}")
        else:
            release_action_lock()
            if adb_reset_event.is_set():
                print("Paused6 due to ADB reset event.")
                time.sleep(13)
    if adb_reset_event.is_set():
        print("Paused6 due to ADB reset event.")
        time.sleep(13)
    d.press("back")
    d.press("back")
    print("Finished scroll_like_and_comment function")

def take_screenshot(d, filename='screenshot_twi.png'):
    print("Taking screenshot...")
    d.screenshot(filename)
    print(f"Screenshot saved as {filename}.")
    return filename

def scroll_random_number(d):
    """
    Scrolls down a random number of times between 1 and 3 and then scrolls up.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    if adb_reset_event.is_set():
        print("Paused4 due to ADB reset event.")
        time.sleep(13)

    acquire_action_lock()
    try:
        if d(scrollable=True).exists:
            print("Found a scrollable view! Swiping down...")

            # Randomly choose how many times to swipe (between 1 and 3)
            num_swipes = random.randint(1, 6)
            print(f"Number of swipes: {num_swipes}")

            # Perform the swipe action for the chosen number of times
            for _ in range(num_swipes):
                if d(scrollable=True).exists:
                    start_x = random.randint(400, 600)
                    start_y = random.randint(900, 1200)
                    end_y = start_y - random.randint(400, 600)
                    swipe_duration = random.uniform(0.04, 0.06)
                    d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
                    print(f"Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
                else:
                    print("No scrollable view found!")
                time.sleep(random.randint(2, 10))
            time.sleep(3)
            # Swipe up to return to the previous content
            d.swipe(500, 300, 500, 800, duration = 0.05)
            print("Swipped up!")
            time.sleep(3)
        else:
            print("No scrollable view found!")
    finally:
        release_action_lock()

def search_and_go_to_page(d, text):
    """
    Searches for the specified text in Twitter and navigates to the desired page.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to search for.
    """
    if adb_reset_event.is_set():
        print("Paused5 due to ADB reset event.")
        time.sleep(13)
    
    acquire_action_lock()
    try:
        # Perform the search
        d.click(180, 1500)
        print("Clicked on the search button.")
        time.sleep(3)

        # Click on the search input field
        d.click(360, 140)
        time.sleep(5)

        # Type each character of the search term with a random delay to simulate human typing
        for char in text:
            d.send_keys(char, clear=False)
            time.sleep(random.uniform(0.1, 0.3))  # Random delay between 0.1 and 0.3 seconds
        time.sleep(2)
        print(f"Typed '{text}' in the search bar naturally.")
        d.click(350,250)  # Press Enter (key code 66) after typing the search text
        print("Got into the page!")
        time.sleep(5)
    finally:
        release_action_lock()

if __name__ == "__main__":
    def main(d):
        """
        The main function connects to the Android device and performs various Twitter actions.
        """
        connect_to_devices()
        adb_restart_thread = threading.Thread(target=restart_adb_periodically, daemon=True)
        adb_restart_thread.start()
        acquire_action_lock()
        time.sleep(2)
        # Start the Twitter app
        d.app_start("com.twitter.android")
        print("Opened Twitter!")
        time.sleep(7)  # Wait for Twitter to fully load
        d.click(75,1500) # Go to home
        release_action_lock()
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
            d.click(75,1500) # Go to home
            time.sleep(4)
            for _ in range(random.randint(4,10)):
                scroll_random_number(d)
                time.sleep(4)
                tap_like_button(d)
                time.sleep(2)
            time.sleep(5)
        d.app_stop("com.twitter.android")
        time.sleep(4)


d = u2.connect("10.100.102.171")  # Use the IP address of your device
main(d)