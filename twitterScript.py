import os
import numpy as np
import uiautomator2 as u2
import time
import cv2
import random
from comments import israel_support_comments

twitter_handles = [
    "@DannyNis",
    "@ElhananMiller",
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
    "@AnshelPfeffer"
]

def scroll_once(d):
    """
    Scrolls down once on a scrollable view in the app in a more natural, human-like manner.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    if d(scrollable=True).exists:
        # Randomize the swipe starting and ending points to make it more natural
        start_x = random.randint(400, 600)  # Random X-coordinate for swipe start (center of screen)
        start_y = random.randint(900, 1200)  # Random Y-coordinate for swipe start (somewhere in middle)
        end_y = start_y - random.randint(400, 600)  # Randomized swipe length (scrolls down by 400 to 600 pixels)
        # Randomize swipe duration to simulate variable human swipe speed (0.2 to 0.5 seconds)
        swipe_duration = random.uniform(0.04, 0.06)
        # Perform the swipe
        d.swipe(start_x, start_y, start_x, end_y, duration=swipe_duration)
        print(f"Scrolled from ({start_x}, {start_y}) to ({start_x}, {end_y}) in {swipe_duration:.2f} seconds.")
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
        num_swipes = random.randint(1, 6)
        print(f"Number of swipes: {num_swipes}")

        # Perform the swipe action for the chosen number of times
        for _ in range(num_swipes):
            scroll_once(d)
            time.sleep(random.randint(2, 10))
        time.sleep(3)
        # Swipe up to return to the previous content
        d.swipe(500, 300, 500, 800, duration = 0.05)
        print("Swipped up!")
        time.sleep(3)
    else:
        print("No scrollable view found!")
    

def take_screenshot(d, filename='screenshot_twi.png'):
    """
    Takes a screenshot of the current screen and saves it to the 'Screenshots' directory.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    filename (str): The name of the screenshot file (default: 'screenshot_twi.png').

    Returns:
    str: The path of the saved screenshot.
    """
    screenshot_dir = 'Screenshots'
    
    # Create the 'Screenshots' directory if it doesn't exist
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    # Create the full path for the screenshot file
    screenshot_path = os.path.join(screenshot_dir, filename)
    
    # Take the screenshot and save it to the specified path
    d.screenshot(screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")
    
    return screenshot_path  # Return the path of the screenshot

def find_best_and_second_best_match(image_path, like_button_template_path):
    """
    Finds the best and second best match of a like button icon in the screenshot using template matching (color images).

    Parameters:
    image_path (str): Path to the screenshot image.
    like_button_template_path (str): Path to the like button template image.

    Returns:
    tuple or None: Coordinates (x, y) of the best and second-best matches and their values, or None if not found.
    """
    # Load the screenshot and like button template images
    img = cv2.imread(image_path)
    template = cv2.imread(like_button_template_path)

    if img is None or template is None:
        print("Error loading images.")
        return None, None

    # Get the dimensions of the like button template
    h, w = template.shape[:2]

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9  # Minimum threshold for a match
    loc = np.where(result >= threshold)  # Get locations where matches exceed the threshold

    # Create a list to store matches with their values and coordinates
    matches = []
    for pt in zip(*loc[::-1]):  # Switch columns and rows
        matches.append((pt, result[pt[1], pt[0]]))  # Append (coordinates, match value)

    if not matches:
        print("No matches found above the threshold.")
        return None, None

    # Sort matches by match value
    matches.sort(key=lambda x: x[1], reverse=True)

    # Get best match
    best_match = matches[0]
    best_coordinates = (best_match[0][0] + w // 2, best_match[0][1] + h // 2)
    best_value = best_match[1]

    # Check for the second-best match
    second_best_coordinates = None
    second_best_value = None
    if len(matches) > 1:
        second_best_match = matches[1]
        second_best_coordinates = (second_best_match[0][0] + w // 2, second_best_match[0][1] + h // 2)
        second_best_value = second_best_match[1]

    print(f"Best match found with value: {best_value} at {best_coordinates}")

    return (best_coordinates, best_value), (second_best_coordinates, second_best_value) if second_best_coordinates else None

def tap_like_button(d, like_button_template_path="icons/twitter_icons/like.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    like_button_template_path (str): Path to the like button template image.
    """
    screenshot_path = take_screenshot(d)
    best_match, second_best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path)

    # If the like button was found, tap on it
    if best_match:
        best_coordinates, best_value = best_match
        print(f"Like button found at {best_coordinates} with match value: {best_value}, tapping...")

        # Check if the second-best match is close enough to the best match
        if second_best_match:
            second_coordinates, second_value = second_best_match
            similarity_tolerance = 0.05  # 5% tolerance for similarity
            if best_value - second_value <= (similarity_tolerance * best_value) and second_coordinates[1]<best_coordinates[1]:
                print(f"Second-best match found at {second_coordinates} with match value: {second_value}, tapping...")
                d.click(int(second_coordinates[0]), int(second_coordinates[1]))  # Tap the second-best match
            else:
                d.click(int(best_coordinates[0]), int(best_coordinates[1]))  # Tap the best match
        else:
            d.click(int(best_coordinates[0]), int(best_coordinates[1]))  # Tap the best match
    else:
        print("Like button not found on the screen.")


def comment_text(d, text, comment_template_path="icons/twitter_icons/comment.png"):
    """
    Takes a screenshot and tries to tap on the comment icon if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    comment_template_path (str): Path to the comment icon template image.
    """
    # Take a screenshot of the current screen
    screenshot_path = take_screenshot(d)
    
    # Find the best match for the comment icon in the screenshot
    coordinates, _ = find_best_and_second_best_match(screenshot_path, comment_template_path)

    # If the comment icon was found, tap on it
    time.sleep(1)
    if coordinates[0]:
        d.click(int(coordinates[0][0]), int(coordinates[0][1]))  # Tap the comment button
        time.sleep(2)
        for char in text:
            d.send_keys(char, clear=False)
            time.sleep(random.uniform(0.1, 0.3))  # Random delay to mimic human typing speed
        time.sleep(1)
    else:
        print("Comment not found on the screen.")
    time.sleep(1)
    d.click(600,125)
    time.sleep(1)


def scroll_and_like(d):
    """
    Scrolls the screen and tries to like a tweet after each scroll by tapping the like button icon.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    for _ in range(30):  # Repeat the process 100 times (or however many times you'd like)
        time.sleep(random.uniform(2, 14))  # Wait 2 seconds after tapping
        scroll_once(d)  # Scroll down once
        time.sleep(random.uniform(1, 14))
        action = random.choice([1,2])  # Wait 1 second between actions
        if action==1:
            print("Pressing like!")
            tap_like_button(d)  # Try to tap the like button icon to like the post
        else:
            print("Not pressing like!")
    time.sleep(2)
    print("Swipped up!")
    d.swipe(500, 300, 500, 800, duration = 0.05)
    time.sleep(2)
        

def scroll_like_and_comment(d):
    """
    Scrolls the screen and randomly likes, comments, both, or neither on each tweet.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to comment.
    """
    actions = ['like', 'comment', 'both', 'none']  # Possible actions

    for _ in range(30):  # Repeat the process 100 times (or however many times you'd like)
        # Random wait between actions
        time.sleep(random.uniform(2, 14))
        scroll_once(d)  # Scroll down once
        time.sleep(random.uniform(2, 14))  # Random wait between scrolls
        # Randomly choose an action
        action = random.choice(actions)
        print(f"Action chosen: {action}")
        text = random.choice(israel_support_comments)
        if action == 'like':
            tap_like_button(d)  # Tap the like button
            print("Liked the post.")
        elif action == 'comment':
            comment_text(d, text)  # Comment on the post
            print(f"Commented: {text}")
        elif action == 'both':
            tap_like_button(d)  # Like the post
            print("Liked the post.")
            time.sleep(2)  # Add a small delay between liking and commenting
            comment_text(d, text)  # Comment on the post
            print(f"Commented: {text}")
    time.sleep(2)
    print("Swipped up!")
    d.swipe(500, 300, 500, 800, duration = 0.05)
    time.sleep(2)    
        
def search_and_go_to_page(d, text):
    """
    Searches for the specified text in Twitter and navigates to the desired page.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to search for.
    """
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
    time.sleep(3)  # Wait for the search results to load

    # Tap on the first result (coordinates may vary)
    d.click(400, 240)
    print("Got into the page!")
    time.sleep(5)


def main(d):
    """
    The main function connects to the Android device and performs various Twitter actions.
    """
    # Start the Twitter app
    d.app_start("com.twitter.android")
    print("Opened Twitter!")
    time.sleep(7)  # Wait for Twitter to fully load
    d.click(75,1500) # Go to home
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

d = u2.connect("10.100.102.170")  # Use the IP address of your device
main(d)