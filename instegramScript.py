import uiautomator2 as u2
import time
from common_area import *
from fuzzywuzzy import fuzz
import easyocr

def scroll_once(d):
    """
    Scrolls down once on a scrollable view in the app if it exists.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    if d(scrollable=True).exists:
        # Generate a random starting point for the swipe within a range of 1000 to 1200 on the Y-axis
        rnd_swipe = random.randint(1000, 1200)
        # Swipe down by dragging from the point (500, rnd_swipe) to (500, rnd_swipe-500)
        d.swipe(500, rnd_swipe, 500, rnd_swipe - 500, duration = 0.05)
        # Wait for a random number of seconds between 1 and 6
        random_time = random.randint(1, 6)
        print(f"Waiting {random_time} seconds...")  # Display the wait time
    else:
        print("No scrollable view found!")  # If the screen is not scrollable, display a message

def scroll_random_number(d):
    """
    Scrolls down a random number of times between 1 and 3 and then scrolls up.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    if d(scrollable=True).exists:
        print("Found a scrollable view! Swiping down...")

        # Randomly choose how many times to swipe (between 1 and 3)
        num_swipes = random.randint(1,3)
        print(f"Number of swipes: {num_swipes}")

        # Perform the swipe action for the chosen number of times
        for i in range(num_swipes):
            rnd_swipe = random.randint(1000, 1200)  # Pick a random Y-coordinate for the swipe
            d.swipe(500, rnd_swipe, 500, rnd_swipe - 900, duration = 0.05)  # Swipe down
            random_time = random.randint(2, 15)  # Wait for a random number of seconds
            print(f"Waiting {random_time} seconds...")
            time.sleep(random_time)  # Pause between swipes
            print(f"Swiped down {i + 1} time(s).")
        
        # Swipe up to return to the previous content
        d.swipe(500, rnd_swipe - 900, 500, rnd_swipe, duration = 0.05)
    else:
        print("No scrollable view found!")

def search_name(d, name, tolerance=20):
    screen_shot = take_screenshot(d, threading.current_thread().name, "inst")
    print(f"Searching for name: {name}")
    
    # Initialize the OCR reader
    reader = easyocr.Reader(['en'])  # You can add more languages if needed

    # Perform OCR
    result = reader.readtext(screen_shot, detail=1)  # detail=1 provides bounding box and text

    best_match = None
    best_similarity = 0  # Initialize with the lowest possible score (0%)

    # Ensure both name and detected text retain special characters like '@'
    processed_name = name.strip()  # Keep special characters, but strip unnecessary spaces

    # Iterate over detected texts
    for detection in result:
        bbox, text, _ = detection
        top_left, _, bottom_right, _ = bbox
        # Skip any detected text that is above y=200
        if top_left[1] < 180:
            continue  # Ignore this text since it's above the desired y position
        # Compare using fuzzy matching
        similarity_score = fuzz.ratio(processed_name, text)
        # Check if the similarity score is the highest and within tolerance
        if similarity_score > best_similarity and similarity_score >= (100 - tolerance):
            best_similarity = similarity_score
            best_match = bbox

    if best_match:
        # Bounding box gives four points (top-left, top-right, bottom-right, bottom-left)
        top_left, _, bottom_right, _ = best_match

        # Calculate the center position of the bounding box
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2
        return (center_x, center_y)

    print("No sufficiently similar text was found.")
    return None

def search_and_go_to_account(d, name):
    """
    Searches for a specific user on TikTok by simulating clicks and typing.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to search for.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    # Calculate the coordinates as percentages of the screen resolution
    x = screen_width * (434 / 1440)  # Approximate X coordinate for the search bar
    y = screen_height * (2900 / 3168)  # Approximate Y coordinate for the search bar
    d.click(x, y)  # Click on the search bar
    time.sleep(2)
    # Calculate the coordinates as percentages of the screen resolution
    x = screen_width / 2  # Approximate X coordinate for the search bar
    y = screen_height * (300 / 3168)  # Approximate Y coordinate for the search bar
    d.click(x, y)  # Click on the search bar
    time.sleep(3)
    # Type each character of the search term with a random delay
    tap_keyboard(d,name)
    time.sleep(1)
    d.press(66)  # Press the search button
    time.sleep(3)
    d.click(245, 225) # Press the accounts button
    time.sleep(3)
    x,y = search_name(d,name) 
    d.click(int(x),int(y))
    time.sleep(2)
    d.click(120,1200)



def tap_like_button(d, like_button_template_path="icons\instagram_icons\like.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    like_button_template_path (str): Path to the like button template image.
    """
    screenshot_path = take_screenshot(d,threading.current_thread().name,'inst')
    best_match = find_best_match(screenshot_path, like_button_template_path,d)

    # If the like button was found, tap on it
    if best_match and best_match[0] < 170:
        print(f"Like button found at {best_match} with match value: {best_match}, tapping...")
        d.click(int(best_match[0]), int(best_match[1]))  # Tap the best match
    else:
        print("Like button not found on the screen.")


def comment_text(d,text, comment_template_path="icons\instagram_icons\comment.png"):
    """
    Takes a screenshot and tries to tap on the comment icon if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    comment_template_path (str): Path to the comment icon template image.
    """
    # Take a screenshot of the current screen
    screenshot_path = take_screenshot(d)
    
    # Find the best match for the comment icon in the screenshot
    coordinates, _ = find_best_match(screenshot_path, comment_template_path)

    # If the comment icon was found, tap on it
    if coordinates[0]:
        d.click(int(coordinates[0][0]), int(coordinates[0][1]))  # Tap the comment button
    else:
        print("Comment not found on the screen.")
    time.sleep(2)
    tap_keyboard(d,text)
    time.sleep(1)
    d.press(66)
    time.sleep(1)
    d.press("back")
    time.sleep(1)
    d.press("back")
    time.sleep(1)

def scroll_and_like(d):
    """
    Scrolls the screen and tries to like a tweet after each scroll by tapping the like button.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    for i in range(10):  # Repeat the process 100 times (or however many times you'd like)
        scroll_once(d)  # Scroll down once
        time.sleep(3)  # Wait 1 second between actions
        tap_like_button(d)  # Try to tap the like button to like the post
        time.sleep(1)  # Wait 2 seconds after tapping
    d.press("back")
    time.sleep(1)
    d.press("back")
    time.sleep(1)
    d.press("back")
    time.sleep(1)
    d.press("back")
    time.sleep(1)

def report(d, link):
    # Open Twitter app
    d.app_start("com.instagram.android")
    print(f"{threading.current_thread().name}:{d.wlan_ip} :Opened Instagram!")
    # time.sleep(15)

    if "com.instagram.android" in d.app_list_running():
        print(f"{threading.current_thread().name}:{d.wlan_ip} Instagram is running!")

        # Open the tweet in the Twitter app
        d.shell(f"am start -a android.intent.action.VIEW -d '{link}'")
        print(f"{threading.current_thread().name}:{d.wlan_ip} Opened: {link}")
        time.sleep(3)
        # Click on the share button
        d.click(685, 210)
        time.sleep(3)

        # # Click on the report button
        d.click(370, 1500)
        time.sleep(8)
        handle_user_selection(d,report_instagram_clicks)
        time.sleep(4)
        d.app_stop("com.twitter.android")

def main():
    """
    The main function connects to the Android device and performs various Instagram actions.
    """
    # Connect to the Android device using its IP address (make sure your device is connected via ADB over Wi-Fi)
    d = u2.connect("10.100.102.178")  # Replace with your device's IP address
    time.sleep(1)

    # Start the Instagram app
    d.app_start("com.instagram.android")
    print("Opened Instagram!")
    time.sleep(7)  # Wait for Instagram to fully load
    scroll_random_number(d)
    time.sleep(2)
    tap_like_button(d)
    time.sleep(7)
    search_and_go_to_account(d,"idf")
    time.sleep(3)
    scroll_and_like(d)
    time.sleep(3)
    scroll_random_number(d)
    tap_like_button(d)
    scroll_random_number(d)
    d.app_stop("com.instagram.android")


# Uncomment this line to run the main function
# main()

# Example of performing a comment action:
d = u2.connect("10.100.102.178")  # Use the IP address of your device
time.sleep(1)
report(d,"https://www.instagram.com/p/DAUlsozStez/?igsh=ZG9xbncxajNwNmRv")
