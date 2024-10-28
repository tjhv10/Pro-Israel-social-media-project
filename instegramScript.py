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
        num_swipes = random.randint(3,8)
        print(f"Number of swipes: {num_swipes}")

        # Perform the swipe action for the chosen number of times
        for i in range(num_swipes):
            rnd_swipe = random.randint(1000, 1200)  # Pick a random Y-coordinate for the swipe
            d.swipe(500, rnd_swipe, 500, rnd_swipe - 900, duration = 0.05)  # Swipe down
            random_time = random.randint(2, 15)  # Wait for a random number of seconds
            print(f"Waiting {random_time} seconds...")
            time.sleep(random_time)  # Pause between swipes
            print(f"Swiped down {i + 1} time(s).")
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
    d.click(215, 1515)  # Click on the search button
    time.sleep(1)
    d.click(215, 1515)  # Click on the search button
    time.sleep(3)
    # Calculate the coordinates as percentages of the screen resolution
    x = screen_width / 2  # Approximate X coordinate for the search bar
    y = screen_height * (300 / 3168)  # Approximate Y coordinate for the search bar
    d.click(x, y)  # Click on the search bar
      # Click on the search bar
    time.sleep(3)
    # Type each character of the search term with a random delay
    tap_keyboard(d,name)
    time.sleep(1)
    d.press(66)  # Press the search button
    time.sleep(5)
    d.click(245, 225) # Press the accounts button
    time.sleep(5)
    try:
        x,y = search_name(d,name) 
        print("Found account!")
    except:
        search_and_go_to_account(d,random.choice(instagram_accounts))
    d.click(int(x),int(y))
    time.sleep(5)
    num = random.choice([1,2,3])
    if num >=2:
        follow_page(d)
    time.sleep(4)
    d.swipe(500, 1400, 500, 100, duration = 0.02)
    time.sleep(4)
    d.click(120,500)



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
        update_results_file("Likes")
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
    screenshot_path = take_screenshot(d,threading.current_thread().name,"inst")
    
    # Find the best match for the comment icon in the screenshot
    coordinates = find_best_match(screenshot_path, comment_template_path,d)
    time.sleep(2)
    # If the comment icon was found, tap on it
    if coordinates:
        d.click(int(coordinates[0]), int(coordinates[1]))  # Tap the comment button
    else:
        print("Comment not found on the screen.")
    time.sleep(2)
    screenshot_path = take_screenshot(d,threading.current_thread().name,"inst")
    
    # Find the best match for the comment icon in the screenshot
    num_coordinates = find_best_match(screenshot_path, "icons/instagram_icons/num.png",d)
    if num_coordinates != None:
        time.sleep(2)
        tap_keyboard(d,text)
        time.sleep(1)
        d.press(66)
        time.sleep(1)
        update_results_file("Comments")
        time.sleep(1)
        d.press("back")
        time.sleep(1)
    if coordinates !=  None:
        d.press("back")
        time.sleep(2)
    time.sleep(2)

def scroll_like_and_comment(d):
    """
    Scrolls the screen and tries to like a tweet after each scroll by tapping the like button.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    for _ in range(2):
        scroll_once(d)  # Scroll down once
        time.sleep(3)  # Wait 1 second between actions
        num = random.choice([1,2,3,4,5]) 
        if num<=4:
            tap_like_button(d)
            if num>2:
                time.sleep(3)
                comment_text(d,random.choice(israel_support_comments))  # Try to tap the like button to like the post
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
        time.sleep(2)
        update_results_file("Reports")
        time.sleep(4)
        d.app_stop("com.twitter.android")

def follow_page(d, follow_template_path="icons/instagram_icons/follow.png"):
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting follow_page function")
    screenshot_path = take_screenshot(d,threading.current_thread().name,"inst")
    best_match = find_best_match(screenshot_path, follow_template_path,d)
    if not best_match:
        best_match = find_best_match(screenshot_path, "icons/instagram_icons/follow_small.png",d)
    if best_match:
        d.click(int(best_match[0]), int(best_match[1]))
        print(f"{threading.current_thread().name}:{d.wlan_ip} Followed account!")
        time.sleep(2)
        update_results_file("Follows")
    else:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Follow icon not found on the screen.")
    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished follow_page function")

def main(d):
    """
    The main function connects to the Android device and performs various Instagram actions.
    """
    # Connect to the Android device using its IP address (make sure your device is connected via ADB over Wi-Fi)
    d.app_start("com.instagram.android")
    print("Opened Instagram!")
    for _ in range(1):
        time.sleep(7)  # Wait for Instagram to fully load
        scroll_random_number(d)
        time.sleep(2)
        tap_like_button(d)
        time.sleep(7)
        search_and_go_to_account(d,random.choice(instagram_accounts))
        time.sleep(3)
        scroll_like_and_comment(d)
        time.sleep(3)
        scroll_random_number(d)
        tap_like_button(d)
        scroll_random_number(d)
    d.app_stop("com.instagram.android")


# main(u2.connect("10.100.102.178"))
# follow_page(u2.connect("10.100.102.178"))