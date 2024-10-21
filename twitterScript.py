import threading
import numpy as np
import time
import cv2
import random
from comments import israel_support_comments

twitter_handles = [
    "yishaifleisher",
    "Israellycool",
    "DavidM_Friedman",
    "Ostrov_A",
    "lahavharkov",
    "havivrettiggur",
    "gil_hoffman",
    "AIPAC",
    "sfrantzman",
    "EylonALevy",
    "FleurHassanN",
    "DemMaj4Israel",
    "khaledAbiToameh",
    "rich goldberg",
    "EVKontorovich",
    "imshin",
    "jtruzmah",
    "barakravid",
    "MaxAbrahms",
    "MickyRosenfeld",
    "RaphaelAhren",
    "YaakovLappin",
    "YnetNews",
    "HananyaNaftali",
    "AmbDermer",
    "BoothWilliam",
    "AnshelPfeffer",
    "ElhananMiller",
    "GershonBaskin",
    "HonestReporting",
    "Issacharoff",
    "JeffreyGoldberg",
    "KhaledAbuToameh",
    "LahavHarkov",
    "DannyNis"
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
            time.sleep(random.uniform(0.04, 0.07))  # Add a small delay between taps
        else:

            print(f"{threading.current_thread().name}:{d.wlan_ip} Character '{char}' not found in keyboard dictionary!")


def tap_like_button(d, like_button_template_path="icons/twitter_icons/like.png"):
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting tap_like_button function")
    
    screenshot_path = take_screenshot(d,threading.current_thread().name)
    
    best_match, second_best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path)    
    
    if best_match:
        best_coordinates = best_match
        print(f"{threading.current_thread().name}:{d.wlan_ip} Like button found at {best_coordinates}, tapping...")
        if second_best_match:
            second_coordinates = second_best_match
            if (best_coordinates[1] < second_coordinates[1]):
                d.click(int(second_coordinates[0]), int(second_coordinates[1]))
                print(f"{threading.current_thread().name}:{d.wlan_ip} Tapped second-best match at {second_coordinates}.")
            else:
                d.click(int(best_coordinates[0]), int(best_coordinates[1]))
                print(f"{threading.current_thread().name}:{d.wlan_ip} Tapped best match at {best_coordinates}.")
        else:
            d.click(int(best_coordinates[0]), int(best_coordinates[1]))
            print(f"{threading.current_thread().name}:{d.wlan_ip} Tapped best match at {best_coordinates}.")
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Like button not found on the screen.")
    
    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished tap_like_button function")

def find_best_and_second_best_match(image_path, template_path):
    print(f"{threading.current_thread().name}: Finding best and second-best match...")
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
        
        return best_match, second_best_match
    else:
        print(f"{threading.current_thread().name}: No matches found.")
        
        return None, None
    

def comment_text(d, text, comment_template_path="icons/twitter_icons/comment.png"):
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting comment_text function")
    screenshot_path = take_screenshot(d,threading.current_thread().name)
    best_match, _ = find_best_and_second_best_match(screenshot_path, comment_template_path)
    if best_match:
        d.click(int(best_match[0]), int(best_match[1]))  # Unpack directly
        time.sleep(2)
        tap_keyboard(d,text) 
        time.sleep(1)
        d.click(600, 125)  # Click the post button
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Comment icon not found on the screen.")
    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished comment_text function")


def scroll_like_and_comment(d):
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting scroll_like_and_comment function")
    actions = ['like', 'comment', 'both', 'none']
    for _ in range(30):
        if d(scrollable=True).exists:
            start_x = random.randint(400, 600)
            start_y = random.randint(900, 1200)
            end_y = start_y - random.randint(400, 600)
            swipe_duration = random.uniform(0.04, 0.06)
            d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
            print(f"{threading.current_thread().name}:{d.wlan_ip} Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
        else:
            print(f"{threading.current_thread().name}:{d.wlan_ip} No scrollable view foun!")
        time.sleep(random.uniform(2, 14))
        action = random.choice(actions)
        print(f"Action chosen: {action}")
        text = random.choice(israel_support_comments)
        if action == 'like':
            tap_like_button(d)
            print(f"{threading.current_thread().name}:{d.wlan_ip} Liked the post.")

        elif action == 'comment':
            comment_text(d, text)
            print(f"{threading.current_thread().name}:{d.wlan_ip} Commented: {text}")

        elif action == 'both':
            tap_like_button(d)
            print(f"{threading.current_thread().name}:{d.wlan_ip} Liked the post.")
            time.sleep(2)
            comment_text(d, text)
            print(f"{threading.current_thread().name}:{d.wlan_ip} Commented: {text}")


    d.press("back")
    d.press("back")
    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished scroll_like_and_comment function")


def take_screenshot(d,thread):
    filename="Screenshots/"+thread + '-screenshot_twi.png'
    print(f"{threading.current_thread().name}:{d.wlan_ip}: Taking screenshot...")
    d.screenshot(filename)
    print(f"{threading.current_thread().name}:{d.wlan_ip} Screenshot saved as {filename}.")
    return filename


def scroll_random_number(d):
    """
    Scrolls down a random number of times between 1 and 3 and then scrolls up.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    if d(scrollable=True).exists:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Found a scrollable view! Swiping down...")

        # Randomly choose how many times to swipe (between 1 and 3)
        num_swipes = random.randint(1, 6)
        print(f"{threading.current_thread().name}:{d.wlan_ip} Number of swipes: {num_swipes}")

        # Perform the swipe action for the chosen number of times
        for _ in range(num_swipes):
            if d(scrollable=True).exists:
                start_x = random.randint(400, 600)
                start_y = random.randint(900, 1200)
                end_y = start_y - random.randint(400, 600)
                swipe_duration = random.uniform(0.04, 0.06)
                d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
                print(f"{threading.current_thread().name}:{d.wlan_ip} Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
            else:
                print(f"{threading.current_thread().name}: No scrollable view founddd!")
            time.sleep(random.randint(2, 10))
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} No scrollable view foundd!")


def search_and_go_to_page(d, text):
    """
    Searches for the specified text in Twitter and navigates to the desired page.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to search for.
    """
    # Swipe up to return to the previous content
    d.swipe(500, 300, 500, 1000, duration = 0.05)
    print(f"{threading.current_thread().name}:{d.wlan_ip} Swipped up!")
    time.sleep(3)
    # Perform the search
    d.click(180, 1500)
    print(f"{threading.current_thread().name}:{d.wlan_ip} Clicked on the search button.")
    time.sleep(3)
    # Click on the search input field
    d.click(360, 140)
    time.sleep(5)
    # Type each character of the search term with a random delay to simulate human typing
    tap_keyboard(d,text)  # Random delay between 0.1 and 0.3 seconds
    time.sleep(2)
    print(f"{threading.current_thread().name}:{d.wlan_ip} Typed '{text}' in the search bar naturally.")
    d.click(350,250)  # Press Enter (key code 66) after typing the search text
    print(f"{threading.current_thread().name}:{d.wlan_ip} Got into the page!")
    time.sleep(5)



def main(d):
    """
    The main function connects to the Android device and performs various Twitter actions.
    """
    # Start the Twitter app
    d.app_start("com.twitter.android")
    print(f"{threading.current_thread().name}:{d.wlan_ip} Opened Twitter!")
    time.sleep(12)  # Wait for Twitter to fully load
    d.click(75,1500) # Go to home
    # for _ in range(random.randint(4,10)):
    #     scroll_random_number(d)
    #     time.sleep(4)
    #     tap_like_button(d)
    #     time.sleep(2)
    time.sleep(2)
    for _ in range(3):
        search_and_go_to_page(d, random.choice(twitter_handles))
        time.sleep(2)
        # Perform scrolling and liking of tweets
        scroll_like_and_comment(d)
        d.click(75,1500) # Go to home
        time.sleep(4)
        # for _ in range(random.randint(4,10)):
        #     scroll_random_number(d)
        #     time.sleep(2)
        #     tap_like_button(d)
        #     time.sleep(2)
        # time.sleep(5)
    d.app_stop("com.twitter.android")
    time.sleep(4)
    