import os
import cv2
import numpy as np
import uiautomator2 as u2
import time
import random

def take_screenshot(d, filename='screenshot_tik.png'):
    """
    Takes a screenshot of the current screen and saves it to the 'Screenshots' directory.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    filename (str): The name of the screenshot file (default: 'screenshot_tik.png').

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

def find_best_and_second_best_match(image_path, users_template_path):
    """
    Finds the best and second best match of a users button icon in the screenshot using template matching (color images).

    Parameters:
    image_path (str): Path to the screenshot image.
    users_template_path (str): Path to the users button template image.

    Returns:
    tuple or None: Coordinates (x, y) of the best and second-best matches and their values, or None if not found.
    """
    # Load the screenshot and users button template images
    img = cv2.imread(image_path)
    template = cv2.imread(users_template_path)

    if img is None or template is None:
        print("Error loading images.")
        return None, None

    # Get the dimensions of the like button template
    h, w = template.shape[:2]

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Minimum threshold for a match
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

    print(f"Best match found with value: {best_value} at {best_coordinates}")

    return (best_coordinates, best_value)

def tap_users(d, users_template_path="icons/tiktok_icons/users.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    users_template_path (str): Path to the like button template image.
    """
    screenshot_path = take_screenshot(d)
    best_match = find_best_and_second_best_match(screenshot_path, users_template_path)

    # If the Users button was found, tap on it
    if best_match:
        best_coordinates, best_value = best_match
        print(f"Users button found at {best_coordinates} with match value: {best_value}, tapping...")
        # Check if the second-best match is close enough to the best match
        d.click(int(best_coordinates[0]), int(best_coordinates[1]))  # Tap the best match
    else:
        print("Users button not found on the screen.")


def search(d, text):
    """
    Searches for a specific user on TikTok by simulating clicks and typing.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to search for.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    # Calculate the coordinates as percentages of the screen resolution
    x = screen_width * (650 / 720)  # Approximate X coordinate for the search button
    y = screen_height * (100 / 1560)  # Approximate Y coordinate for the search bar
    d.click(x, y)  # Click on the search bar
    time.sleep(2)
    # Type each character of the search term with a random delay
    for char in text:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay to mimic human typing
    time.sleep(2)
    d.press(66)  # Press the search button
    time.sleep(5)
    
    # Click to go to users
    tap_users(d)  # Coordinates for users tab
    time.sleep(3)
    
    # Click to go into the first result
    d.click(700, 300)  # Coordinates for the first user result
    time.sleep(3)


def click_like(d):
    """
    Clicks the like button for an old account.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    d.click(660, 870)
    print("Clicked on the like button.")



def comment_text(d, text):
    """
    Comments on a post.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to comment.
    """
    d.click(670, 1000)
    print("Clicked on the comment button.")

    d.click(310, 1500)  # Click on the comment input
    print(f"Commenting: {text}")
    time.sleep(2)
    # Type the comment character by character with random delays
    # for char in text:
    #     d.send_keys(char, clear=False)
    #     time.sleep(random.uniform(0.1, 0.3))  # Random delay to mimic human typing speed
    d.set_input_ime(True)  # Enable fast input method
    d.send_keys(text, clear=False)  # Send the comment text directly
    d.set_input_ime(False)  # Revert to the default input method after typing

    time.sleep(1)

    # Click the submit button for the comment
    d.click(1300 / 1440, 2700 / 3168)

def scroll_random_number(d):
    """
    Scrolls down a random number of times in a scrollable view.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    if d(scrollable=True).exists:
        print("Found a scrollable view! Swiping down...")
        
        # Generate a random number of swipes between 3 and 6
        num_swipes = random.randint(3, 6)
        print(f"Number of swipes: {num_swipes}")

        for i in range(num_swipes):
            # Swipe down coordinates
            x_start = screen_width * (500 / 720)  # Start X coordinate
            y_start = screen_height * (1200 / 1560)  # Start Y coordinate
            x_end = screen_width * (500 / 720)  # End X coordinate
            y_end = screen_height * (300 / 1560)  # End Y coordinate
            d.swipe(x_start, y_start, x_end, y_end, duration = 0.05)  # Swipe down
            random_time = random.randint(2, 15)  # Random wait time between swipes
            time.sleep(random_time)
            print(f"Swiped down {i + 1} time(s).")
    else:
        print("No scrollable view found!") 

def scroll_and_like(d):
    """
    Scrolls the view and likes posts.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    click_like(d)  # Click like button
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    for i in range(100):
        if d(scrollable=True).exists:
            # Swipe down coordinates
            x_start = screen_width * (500 / 720)  # Start X coordinate
            y_start = screen_height * (1200 / 1560)  # Start Y coordinate
            x_end = screen_width * (500 / 720)  # End X coordinate
            y_end = screen_height * (300 / 1560)  # End Y coordinate
            d.swipe(x_start, y_start, x_end, y_end, duration = 0.05)  # Swipe down
            random_time = random.randint(2, 15)  # Random wait time between swipes
            time.sleep(random_time)
            print(f"Swiped down {i + 1} time(s).")
        else:
            print("No scrollable view found!")
        
        # Click the like button again after scrolling
        click_like(d) 

def like_the_page(d, page):
    """
    Likes the specified page and comments on a post.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    page (str): The name of the page to like.
    """
    search(d, page)  # Search for the page
    d.click(120, 1300)  # Click on the specified page
    time.sleep(2)
    scroll_and_like(d)  # Scroll and like posts

def main(d):
    """
    Main function to connect to the device and perform actions on TikTok.
    """
    time.sleep(1)
    d.app_start("com.zhiliaoapp.musically")  # Open TikTok app
    print("Opened TikTok!")
    time.sleep(15)

    if "com.zhiliaoapp.musically" in d.app_list_running():
        print("TikTok is running!")
        # Uncomment this line to scroll randomly
        scroll_random_number(d)
        time.sleep(1)
        click_like(d)
        time.sleep(1)  # Click the like button for an old account
        comment_text(d, "go Israel")  # Comment on the post
    else:
        print("TikTok is not running!")

# Run the main function to start the process
# main()

# Connect to the device and like the specified page
d = u2.connect("10.100.102.169")  # Use the IP address of your device
time.sleep(1)
like_the_page(d,"idf")
