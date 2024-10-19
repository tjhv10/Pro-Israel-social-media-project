import os
import subprocess
import cv2
import numpy as np
import uiautomator2 as u2
import time
import random
import threading
from comments import israel_support_comments

# Global variables
tiktok_accounts = []
adb_reset_event = threading.Event()
action_lock = threading.Lock()

def acquire_action_lock():
    """
    Acquire the action lock.
    """
    action_lock.acquire()

def release_action_lock():
    """
    Release the action lock.
    """
    action_lock.release()


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
        print("starting to restart")
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


def take_screenshot(d, filename='screenshot_tik.png'):
    """
    Takes a screenshot of the current screen and saves it to the 'Screenshots' directory.
    """
    screenshot_dir = 'Screenshots'
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, filename)
    d.screenshot(screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")
    return screenshot_path

def find_best_and_second_best_match(image_path, users_template_path):
    """
    Finds the best and second best match of a users button icon in the screenshot using template matching.
    """
    time.sleep(2)
    print("Starting find_best_and_second_best_match function")
    if adb_reset_event.is_set():
            print("Paused2 due to ADB reset event.")
            time.sleep(10)
    img = cv2.imread(image_path)
    template = cv2.imread(users_template_path)

    if img is None or template is None:
        print("Error loading images.")
        return None

    h, w = template.shape[:2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    matches = []
    for pt in zip(*loc[::-1]):
        matches.append((pt, result[pt[1], pt[0]]))

    if not matches:
        print("No matches found above the threshold.")
        return None

    matches.sort(key=lambda x: x[1], reverse=True)
    best_match = matches[0]
    best_coordinates = (best_match[0][0] + w // 2, best_match[0][1] + h // 2)
    best_value = best_match[1]

    print(f"Best match found with value: {best_value} at {best_coordinates}")

    print("Finished find_best_and_second_best_match function")
    return (best_coordinates, best_value)
    

def tap_users(d, users_template_path="icons/tiktok_icons/users.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.
    """
    
    screenshot_path = take_screenshot(d)
    best_match = find_best_and_second_best_match(screenshot_path, users_template_path)

    
    if best_match:
        best_coordinates, best_value = best_match
        print(f"Users button found at {best_coordinates} with match value: {best_value}, tapping...")
        d.click(int(best_coordinates[0]), int(best_coordinates[1]))
    else:
        print("Users button not found on the screen.")
   

def search(d, text):
    """
    Searches for a specific user on TikTok by simulating clicks and typing.
    """
    if adb_reset_event.is_set():
        print("Paused4 due to ADB reset event.")
        time.sleep(10)
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    x = screen_width * (650 / 720)
    y = screen_height * (100 / 1560)

    acquire_action_lock()
    try:
        d.click(x, y)  # Click on the search bar
        time.sleep(2)

        for char in text:
            d.send_keys(char, clear=False)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(2)
        d.press(66)  # Press the search button
        time.sleep(5)

        tap_users(d)  # Click to go to users
        time.sleep(3)

        d.click(700, 300)  # Click to go into the first result
        time.sleep(3)
    finally:
        release_action_lock()
        

def tap_like_button(d, like_button_template_path="icons/tiktok_icons/like.png"):
    print("Starting tap_like_button function")
    
    if adb_reset_event.is_set():
        print("Paused2 due to ADB reset event.")
        time.sleep(13)

    acquire_action_lock()
    try:
        screenshot_path = take_screenshot(d)
        best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path)
        print(best_match)
        if best_match:
            best_coordinates = best_match[0]
            print(f"Like button found at {best_coordinates}, tapping...")
            d.click(int(best_coordinates[0]), int(best_coordinates[1]))
            print(f"Tapped best match at {best_coordinates}.")
        else:
            print("Like button not found on the screen.")
    finally:
        release_action_lock()

    print("Finished tap_like_button function")

# def comment_text(d, text):
#     """
#     Comments on a post.
#     """
#     if adb_reset_event.is_set():
#         print("Paused6 due to ADB reset event.")
#         time.sleep(10)
#     acquire_action_lock()  # Acquire the lock
#     try:
#         d.click(670, 1000)
#         print("Clicked on the comment button.")

#         d.click(310, 1500)  # Click on the comment input
#         print(f"Commenting: {text}")
#         time.sleep(2)
#         d.set_input_ime(True)  # Enable fast input method
#         d.send_keys(text, clear=False)  # Send the comment text directly
#         d.set_input_ime(False)  # Revert to the default input method after typing

#         time.sleep(1)
#         d.click(1300 / 1440, 2700 / 3168)  # Click the submit button for the comment
#     finally:
#         release_action_lock()  # Ensure the lock is released

def scroll_random_number(d):
    """
    Scrolls down a random number of times in a scrollable view.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    if adb_reset_event.is_set():
        print("Paused7 due to ADB reset event.")
        time.sleep(10)
    acquire_action_lock()  # Acquire the lock
    try:
        if d(scrollable=True).exists:
            print("Found a scrollable view! Swiping down...")
            num_swipes = random.randint(3, 6)
            print(f"Number of swipes: {num_swipes}")

            for i in range(num_swipes):
                x_start = screen_width * (500 / 720)
                y_start = screen_height * (1200 / 1560)
                x_end = screen_width * (500 / 720)
                y_end = screen_height * (300 / 1560)
                d.swipe(x_start, y_start, x_end, y_end, duration=0.05)
                random_time = random.randint(2, 15)
                time.sleep(random_time)
                print(f"Swiped down {i + 1} time(s).")
        else:
            print("No scrollable view found!")
    finally:
        print("relesed6")
        release_action_lock()  # Ensure the lock is released





def scroll_and_like(d):
    """
    Scrolls the view and likes posts.
    """
    tap_like_button(d)
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']

    for i in range(1):
        if adb_reset_event.is_set():
            print("Paused8 due to ADB reset event.")
            time.sleep(10)
        acquire_action_lock()  # Acquire the lock
        if d(scrollable=True).exists:
            x_start = screen_width * (500 / 720)
            y_start = screen_height * (1200 / 1560)
            x_end = screen_width * (500 / 720)
            y_end = screen_height * (300 / 1560)
            d.swipe(x_start, y_start, x_end, y_end, duration=0.05)
            random_time = random.randint(2, 15)
            time.sleep(random_time)
            print(f"Swiped down {i + 1} time(s).")
        else:
            print("No scrollable view found!")
        release_action_lock()
        if random.choice([1, 2, 3, 4, 5]) < 5:
            tap_like_button(d)
    acquire_action_lock()
    d.press("back")
    d.press("back")
    time.sleep(2)
    d.press("back")
    time.sleep(2)
    d.press("back")
    time.sleep(4)
    d.press("back")
    release_action_lock()

def like_the_page(d, page):
    """
    Likes the specified page and comments on a post.
    """
    search(d, page)
    acquire_action_lock()
    d.click(120, 1300)
    time.sleep(2)
    release_action_lock()
    scroll_and_like(d)

def main(d):
    """
    Main function to connect to the device and perform actions on TikTok.
    """
    connect_to_devices()
    adb_restart_thread = threading.Thread(target=restart_adb_periodically, daemon=True)
    adb_restart_thread.start()
    time.sleep(1)
    d.app_start("com.zhiliaoapp.musically")  # Open TikTok app
    print("Opened TikTok!")
    if adb_reset_event.is_set():
        print("Paused1 due to ADB reset event.")
        time.sleep(10)
    time.sleep(15)
    
    if "com.zhiliaoapp.musically" in d.app_list_running():
        print("TikTok is running!")
        scroll_random_number(d)
        time.sleep(1)
        tap_like_button(d)
        time.sleep(1)
        like_the_page(d,"hananyaNaftali")
        scroll_random_number(d)
        if adb_reset_event.is_set():
            print("Paused9 due to ADB reset event.")
            time.sleep(10)
        time.sleep(10)
        d.app_stop("com.zhiliaoapp.musically")
        time.sleep(4)
    else:
        print("TikTok is not running!")

# Example usage (make sure to uncomment when running)
# d = u2.connect("10.100.102.171")  # Use the IP address of your device
# time.sleep(1)
# main(d)
