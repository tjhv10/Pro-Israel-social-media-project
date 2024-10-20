import os
import subprocess
import cv2
import numpy as np
import uiautomator2 as u2
import time
import random
import threading
from comments import israel_support_comments

tiktok_accounts = [
    "israel",
    "powerisrael",
    "israel_hayom",
    "tbn_official",
    "tbn_fr",
    "tbnua",
    "cbnnewsofficial",
    "cbcnews",
    "newsmaxtv",
    "hananyanaftali",
    "rudy_israel",
    "Shaidavidai",
    "adelacojab",
    "noybeyleyb",
    "EylonALevy",
    "Kami.Soprano",
    "yoavdavis",
    "millennialmoor",
    "Jews_of_Ny",
    "tlvinstitute",
    "noatishby",
    "jewishhistory",
    "houseoflev",
    "melissaschapman",
    "jordyntilchen",
    "Jewishvibes",
    "EndJewHatred",
    "alizalicht",
    "wearetov",
    "Libbyamberwalker",
    "2024newvoices"
]

def take_screenshot(d, filename=f"{threading.current_thread().name}-screenshot_tik.png"):
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

def find_best_and_second_best_match(image_path, users_template_path, d):
    """
    Finds the best match of a user's button icon in the screenshot using template matching.
    """
    time.sleep(2)
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting find_best_match function")
    
    img = cv2.imread(image_path)
    template = cv2.imread(users_template_path)

    if img is None or template is None:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Error loading images.")
        return None

    h, w = template.shape[:2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(result >= threshold)

    matches = []
    for pt in zip(*loc[::-1]):
        matches.append((pt, result[pt[1], pt[0]]))

    if not matches:
        print(f"{threading.current_thread().name}:{d.wlan_ip} No matches found above the threshold.")
        return None

    # Get the best match (highest confidence value)
    best_match = max(matches, key=lambda x: x[1])
    best_coordinates = (best_match[0][0] + w // 2, best_match[0][1] + h // 2)
    best_value = best_match[1]

    print(f"Best match found with value: {best_value} at {best_coordinates}")

    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished find_best_match function")
    
    return (best_coordinates, best_value)

    

def tap_users(d, users_template_path="icons/tiktok_icons/users.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.
    """
    
    screenshot_path = take_screenshot(d)
    best_match = find_best_and_second_best_match(screenshot_path, users_template_path,d)

    
    if best_match:
        best_coordinates, best_value = best_match
        print(f"Users button found at {best_coordinates} with match value: {best_value}, tapping...")
        d.click(int(best_coordinates[0]), int(best_coordinates[1]))
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Users button not found on the screen.")
   

def search(d, text):
    """
    Searches for a specific user on TikTok by simulating clicks and typing.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    x = screen_width * (650 / 720)
    y = screen_height * (100 / 1560)

    
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
    
        

def tap_like_button(d, like_button_template_path="icons/tiktok_icons/like.png"):
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting tap_like_button function")
    screenshot_path = take_screenshot(d)
    best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path,d)
    if best_match:
        best_coordinates = best_match[0]
        print(f"Like button found at {best_coordinates}, tapping...")
        d.click(int(best_coordinates[0]), int(best_coordinates[1]))
        print(f"Tapped best match at {best_coordinates}.")
        time.sleep(1)
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Like button not found on the screen.")
    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished tap_like_button function")

# def comment_text(d, text):
#     """
#     Comments on a post.
#     """
#     if adb_reset_event.is_set():
#         print(f"{threading.current_thread().name}:{d.wlan_ip} Paused6 due to ADB reset event.")
#         time.sleep(10)
#     acquire_action_lock()  # Acquire the lock
#     try:
#         d.click(670, 1000)
#         print(f"{threading.current_thread().name}:{d.wlan_ip} Clicked on the comment button.")

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
    
    if d(scrollable=True).exists:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Found a scrollable view! Swiping down...")
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
            print(f"{threading.current_thread().name}:{d.wlan_ip} Swiped down {i + 1} time(s).")
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} No scrollable view found!")





def scroll_and_like(d):
    """
    Scrolls the view and likes posts.
    """
    tap_like_button(d)
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']

    for i in range(30):
        
        if d(scrollable=True).exists:
            x_start = screen_width * (500 / 720)
            y_start = screen_height * (1200 / 1560)
            x_end = screen_width * (500 / 720)
            y_end = screen_height * (300 / 1560)
            d.swipe(x_start, y_start, x_end, y_end, duration=0.05)
            random_time = random.randint(2, 15)
            time.sleep(random_time)
            print(f"{threading.current_thread().name}:{d.wlan_ip} Swiped down {i + 1} time(s).")
        else:
            print(f"{threading.current_thread().name}:{d.wlan_ip} No scrollable view found!")
        if random.choice([1, 2, 3, 4, 5]) < 5:
            tap_like_button(d)
            time.sleep(1)
    d.press("back")
    d.press("back")
    time.sleep(2)
    d.press("back")
    time.sleep(2)
    d.press("back")
    time.sleep(4)
    d.press("back")

def like_the_page(d, page):
    """
    Likes the specified page and comments on a post.
    """
    search(d, page)
    d.click(120, 1300)
    time.sleep(2)
    scroll_and_like(d)

def main(d):
    """
    Main function to connect to the device and perform actions on TikTok.
    """
    d.app_start("com.zhiliaoapp.musically")  # Open TikTok app
    print(f"{threading.current_thread().name}:{d.wlan_ip} :Opened TikTok!")
    time.sleep(15)
    if "com.zhiliaoapp.musically" in d.app_list_running():
        print(f"{threading.current_thread().name}:{d.wlan_ip} TikTok is running!")
        scroll_random_number(d)
        time.sleep(1)
        tap_like_button(d)
        time.sleep(1)
        like_the_page(d,"hananyaNaftali")
        scroll_random_number(d)
        time.sleep(10)
        d.app_stop("com.zhiliaoapp.musically")
        time.sleep(4)
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} TikTok is not running!")
    print(f"{threading.current_thread().name}:{d.wlan_ip} done")

# Example usage (make sure to uncomment when running)
# d = u2.connect("10.100.102.171")  # Use the IP address of your device
# time.sleep(1)
# main(d)
