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

keyboard_dic = {
    "q": (40, 1200),
    "w": (110, 1200),
    "e": (180, 1200),
    "r": (250, 1200),
    "t": (320, 1200),
    "y": (390, 1200),
    "u": (460, 1200),
    "i": (530, 1200),
    "o": (600, 1200),
    "p": (670, 1200),
    "a": (70, 1285),
    "s": (140, 1285),
    "d": (210, 1285),
    "f": (280, 1285),
    "g": (350, 1285),
    "h": (420, 1285),
    "j": (490, 1285),
    "k": (560, 1285),
    "l": (630, 1285),
    "z": (150, 1400),
    "x": (220, 1400),
    "c": (290, 1400),
    "v": (360, 1400),
    "b": (430, 1400),
    "n": (500, 1400),
    "m": (570, 1400),
    ".": (570,1500),
    ",": (150,1500),
    " ": (400,1500)
}


def tap_keyboard(d, text, keyboard = keyboard_dic):
    """
    Simulates tapping on the screen using the keyboard coordinates for each character in the text.
    """
    for char in text.lower():  # Convert the text to lowercase to match the dictionary keys
        if char in keyboard:
            x, y = keyboard[char]
            d.click(x, y)  # Simulate a tap on the screen at the corresponding coordinates
            time.sleep(random.uniform(0.04,0.07))  # Add a small delay between taps
        else:
            print(f"Character '{char}' not found in keyboard dictionary!")


def take_screenshot(d,thread):
    filename="Screenshots/"+thread+'-screenshot_tik.png'
    print(f"{thread}:{d.wlan_ip} Taking screenshot...")
    d.screenshot(filename)
    print(f"Screenshot saved as {filename}.")
    return filename

def find_best_and_second_best_match(image_path, users_template_path, d):
    """
    Finds the best match of a user's button icon in the screenshot using template matching.
    """
    time.sleep(0.5)
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting find_best_match function")
    
    img = cv2.imread(image_path)
    template = cv2.imread(users_template_path)

    if img is None or template is None:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Error loading images.")
        return None

    h, w = template.shape[:2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.65
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

    print(f"{threading.current_thread().name}:{d.wlan_ip} Best match found with value: {best_value} at {best_coordinates}")

    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished find_best_match function")
    
    return (best_coordinates, best_value)

    

def tap_users(d, users_template_path="icons/tiktok_icons/users.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.
    """
    screenshot_path = take_screenshot(d,threading.current_thread().name)
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
    tap_keyboard(d,text)
    time.sleep(2)
    d.press(66)  # Press the search button
    time.sleep(5)

    tap_users(d)  # Click to go to users
    time.sleep(3)

    d.click(700, 300)  # Click to go into the first result
    time.sleep(3)
    
        

def tap_like_button(d, like_button_template_path="icons/tiktok_icons/like.png"):
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting tap_like_button function")
    screenshot_path = take_screenshot(d,threading.current_thread().name)
    best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path,d)
    if best_match:
        best_coordinates = best_match[0]
        print(f"{threading.current_thread().name}:{d.wlan_ip} Like button found at {best_coordinates}, tapping...")
        d.click(int(best_coordinates[0]), int(best_coordinates[1]))
        print(f"{threading.current_thread().name}:{d.wlan_ip} Tapped best match at {best_coordinates}.")
        time.sleep(1)
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Like button not found on the screen.")
    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished tap_like_button function")

def comment_text(d, text):
    """
    Comments on a post using the regular keyboard.
    """
    d.click(670, 1000)  # Click on the comment button
    print(f"{threading.current_thread().name}:{d.wlan_ip} Clicked on the comment button.")
    time.sleep(3)
    d.click(310, 1500)  # Click on the comment input field
    print(f"{threading.current_thread().name}:{d.wlan_ip} Commenting: {text}")
    
    time.sleep(4)  # Wait for the input field to be ready
    
    tap_keyboard(d,text)
    
    time.sleep(1)  # Give some time for the input to be registered
    
    d.click(650, 1000)  # Click the submit button for the comment
    print(f"{threading.current_thread().name}:{d.wlan_ip} Comment submitted.")
    d.press("back")




def scroll_random_number(d):
    """
    Scrolls down a random number of times in a scrollable view.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    if d(scrollable=True).exists:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Found a scrollable view! Swiping down...")
        num_swipes = random.randint(3, 6)
        print(f"{threading.current_thread().name}:{d.wlan_ip} Number of swipes: {num_swipes}")

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


def scroll_like_and_comment(d):
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
        num = random.choice([1, 2, 3, 4, 5])
        if  num <= 2:
            print("like")
            tap_like_button(d)
            time.sleep(1)
        elif num>2 and num<=4:
            print("like and comment")
            tap_like_button(d)
            time.sleep(1)
            comment_text(d,random.choice(israel_support_comments))
            time.sleep(1)
        else:
            print("none")
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
    d.click(120, 1300) # Get in the first page
    time.sleep(2)
    scroll_like_and_comment(d)

def main(d):
    """
    Main function to connect to the device and perform actions on TikTok.
    """
    d.app_start("com.zhiliaoapp.musically")  # Open TikTok app
    print(f"{threading.current_thread().name}:{d.wlan_ip} :Opened TikTok!")
    time.sleep(15)
    if "com.zhiliaoapp.musically" in d.app_list_running():
        print(f"{threading.current_thread().name}:{d.wlan_ip} TikTok is running!")
        for _ in range(3):
            scroll_random_number(d)
            time.sleep(1)
            tap_like_button(d)
            time.sleep(1)
            like_the_page(d,random.choice(tiktok_accounts))
            scroll_random_number(d)
            time.sleep(10)
        d.app_stop("com.zhiliaoapp.musically")
        time.sleep(4)
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} TikTok is not running!")
    print(f"{threading.current_thread().name}:{d.wlan_ip} done")
