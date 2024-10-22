import os
import numpy as np
import uiautomator2 as u2
import time
import cv2
import random
from common_area import *

def search_and_go_to_account(d, text):
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
    
    # Type each character of the search term with a random delay
    for char in text:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay to mimic human typing
    time.sleep(2)
    d.press(66)  # Press the search button
    time.sleep(3)
    d.click(450 / 1440, 500 / 3168) # Press the accounts button
    time.sleep(3)
    # Click to go into the first result
    d.click(700 / 1440, 600 / 3168)  # Coordinates for the first user result
    time.sleep(2)
    d.click(120,1200)


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


def take_screenshot(d, filename='screenshot_inst.png'):
    """
    Takes a screenshot of the current screen and saves it to the 'Screenshots' directory.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    filename (str): The name of the screenshot file (default: 'screenshot.png').

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

def tap_like_button(d, like_button_template_path="icons\instagram_icons\like.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    like_button_template_path (str): Path to the like button template image.
    """
    screenshot_path = take_screenshot(d)
    best_match, second_best_match = find_best_and_second_best_match(screenshot_path, like_button_template_path)
    if best_match == None:
        print("No like button found.")
        return
    best_coordinates, best_value = best_match
    if second_best_match:
        second_coordinates, second_value = second_best_match
    if best_coordinates[0]>170 and second_coordinates[0]>170:
        print("No like button that is unliked") 
        return
    # If the like button was found, tap on it
    if best_match:
        print(f"Like button found at {best_coordinates} with match value: {best_value}, tapping...")
        # Check if the second-best match is close enough to the best match
        if second_best_match:
            similarity_tolerance = 0.05  # 5% tolerance for similarity
            if best_value - second_value <= (similarity_tolerance * best_value) and best_coordinates[1]<second_coordinates[1]:
                print(f"Second-best match found at {second_coordinates} with match value: {second_value}, tapping...")

                d.click(int(second_coordinates[0]), int(second_coordinates[1]))  # Tap the second-best match
            else:
                d.click(int(best_coordinates[0]), int(best_coordinates[1]))  # Tap the best match
        else:
            d.click(int(best_coordinates[0]), int(best_coordinates[1]))  # Tap the best match
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
    coordinates, _ = find_best_and_second_best_match(screenshot_path, comment_template_path)

    # If the comment icon was found, tap on it
    if coordinates[0]:
        d.click(int(coordinates[0][0]), int(coordinates[0][1]))  # Tap the comment button
    else:
        print("Comment not found on the screen.")
    time.sleep(2)
    for char in text:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay between 0.1 and 0.3 seconds
    time.sleep(0.5)
    d.press(66)
    time.sleep(0.5)
    d.press("back")
    d.press("back")

def scroll_and_like(d):
    """
    Scrolls the screen and tries to like a tweet after each scroll by tapping the like button.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    for i in range(100):  # Repeat the process 100 times (or however many times you'd like)
        scroll_once(d)  # Scroll down once
        time.sleep(3)  # Wait 1 second between actions
        tap_like_button(d)  # Try to tap the like button to like the post
        time.sleep(1)  # Wait 2 seconds after tapping


def main():
    """
    The main function connects to the Android device and performs various Instagram actions.
    """
    # Connect to the Android device using its IP address (make sure your device is connected via ADB over Wi-Fi)
    d = u2.connect("10.100.102.168")  # Replace with your device's IP address
    time.sleep(1)

    # Start the Instagram app
    d.app_start("com.instagram.android")
    print("Opened Instagram!")
    time.sleep(7)  # Wait for Instagram to fully load
    search_and_go_to_account(d,"israel")
    time.sleep(3)
    scroll_and_like(d)


# Uncomment this line to run the main function
# main()

# Example of performing a comment action:
# d = u2.connect("10.100.102.168")  # Use the IP address of your device
# time.sleep(1)
# tap_like_button(d)