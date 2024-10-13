import os
import uiautomator2 as u2
import time
import cv2
import random

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
        d.swipe(500, rnd_swipe, 500, rnd_swipe - 500)
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
        num_swipes = random.randint(1, 3)
        print(f"Number of swipes: {num_swipes}")

        # Perform the swipe action for the chosen number of times
        for i in range(num_swipes):
            rnd_swipe = random.randint(1000, 1200)  # Pick a random Y-coordinate for the swipe
            d.swipe(500, rnd_swipe, 500, rnd_swipe - 900)  # Swipe down
            random_time = random.randint(2, 15)  # Wait for a random number of seconds
            print(f"Waiting {random_time} seconds...")
            time.sleep(random_time)  # Pause between swipes
            print(f"Swiped down {i + 1} time(s).")
        
        # Swipe up to return to the previous content
        d.swipe(500, rnd_swipe - 900, 500, rnd_swipe)
    else:
        print("No scrollable view found!")

def search(d, text_to_type):
    """
    Simulates a search action by typing text in the Twitter search bar.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text_to_type (str): The text to search for.
    """
    # Tap on the search button in the app (coordinates may vary on different devices)
    d.click(180, 1500)
    print("Clicked on the search button.")
    time.sleep(1)

    # Click on the search input field
    d.click(360, 140)
    time.sleep(2)

    # Type each character of the search term with a random delay to simulate human typing
    for char in text_to_type:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay between 0.1 and 0.3 seconds

    print(f"Typed '{text_to_type}' in the search bar naturally.")

def take_screenshot(d, filename='screenshot.png'):
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

def find_best_match_in_image(image_path, like_button_template_path):
    """
    Finds the best match of a like button icon in the screenshot using template matching (color images).

    Parameters:
    image_path (str): Path to the screenshot image.
    like_button_template_path (str): Path to the like button template image.

    Returns:
    tuple or None: Coordinates (x, y) of the center of the best match or None if not found.
    """
    # Load the screenshot and like button template images
    img = cv2.imread(image_path)
    template = cv2.imread(like_button_template_path)

    # Check if both images were loaded successfully
    if img is None:
        print("Error loading screenshot image.")
        return None
    if template is None:
        print("Error loading like button template image.")
        return None

    # Get the dimensions of the like button template (height and width)
    h, w = template.shape[:2]
    new_h, new_w = h, w  # Initialize new height and width for potential resizing

    # If the like button template is larger than the screenshot, resize it
    if h > img.shape[0] or w > img.shape[1]:
        print("Like button template is larger than the screenshot, resizing template.")
        scale_factor = min(img.shape[0] / h, img.shape[1] / w)
        new_h = int(h * scale_factor)
        new_w = int(w * scale_factor)
        template = cv2.resize(template, (new_w, new_h))  # Resize the template to fit

    # Perform template matching to find the best match of the like button icon
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # Find the best match's location and value
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Set a threshold for a "good enough" match (values range from -1 to 1)
    threshold = 0.8  # You can adjust this value based on testing
    if max_val >= threshold:
        # Calculate the center coordinates of the matched area
        best_match_center = (max_loc[0] + new_w // 2, max_loc[1] + new_h // 2)
        print(f"Best match found with value: {max_val} at {best_match_center}")
        return best_match_center  # Return the coordinates of the match center
    else:
        print(f"No match found above the threshold. Best match value: {max_val}")
        return None

def tap_like_button(d, like_button_template_path="twitter_icons/twitter_like_button.png"):
    """
    Takes a screenshot and tries to tap on the like button if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    like_button_template_path (str): Path to the like button template image.
    """
    # Take a screenshot of the current screen
    screenshot_path = take_screenshot(d)
    
    # Find the best match for the like button in the screenshot
    coordinates = find_best_match_in_image(screenshot_path, like_button_template_path)

    # If the like button was found, tap on it
    if coordinates:
        print(f"Like button found at {coordinates}, tapping...")
        d.click(coordinates[0], coordinates[1])  # Tap the like button at the found coordinates
    else:
        print("Like button not found on the screen.")

def comment(d, comment_template_path="twitter_icons/twitter_comment.png"):
    """
    Takes a screenshot and tries to tap on the comment icon if found.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    comment_template_path (str): Path to the comment icon template image.
    """
    # Take a screenshot of the current screen
    screenshot_path = take_screenshot(d)
    
    # Find the best match for the comment icon in the screenshot
    coordinates = find_best_match_in_image(screenshot_path, comment_template_path)

    # If the comment icon was found, tap on it
    if coordinates:
        d.click(coordinates[0], coordinates[1])  # Tap the comment button
    else:
        print("Comment not found on the screen.")

def scroll_and_like(d):
    """
    Scrolls the screen and tries to like a tweet after each scroll by tapping the like button.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    for i in range(100):  # Repeat the process 100 times (or however many times you'd like)
        scroll_once(d)  # Scroll down once
        time.sleep(1)  # Wait 1 second between actions
        tap_like_button(d)  # Try to tap the like button to like the post
        time.sleep(2)  # Wait 2 seconds after tapping

def scroll_and_like(d):
    """
    Scrolls the screen and tries to like a tweet after each scroll by tapping the like button icon.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    for i in range(100):  # Repeat the process 100 times (or however many times you'd like)
        scroll_once(d)  # Scroll down once
        time.sleep(1)  # Wait 1 second between actions
        tap_like_button(d)  # Try to tap the like button icon to like the post
        time.sleep(2)  # Wait 2 seconds after tapping

def search_and_go_to_page(d, text):
    """
    Searches for the specified text in Twitter and navigates to the desired page.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to search for.
    """
    # Perform the search
    search(d, text)
    d.press(66)  # Press Enter (key code 66) after typing the search text
    time.sleep(3)  # Wait for the search results to load

    # Tap on the first result (coordinates may vary)
    d.click(400, 240)
    time.sleep(5)  # Wait for the profile page to load

    # Tap again to go into the page or tweet
    d.click(400, 400)
    time.sleep(5)

def main():
    """
    The main function connects to the Android device and performs various Twitter actions.
    """
    # Connect to the Android device using its IP address (make sure your device is connected via ADB over Wi-Fi)
    d = u2.connect("10.100.102.102")  # Replace with your device's IP address
    time.sleep(1)

    # Start the Twitter app
    d.app_start("com.twitter.android")
    print("Opened Twitter!")
    time.sleep(7)  # Wait for Twitter to fully load

    # Search for a specific text (e.g., a Twitter handle or hashtag) and go to the page
    search_and_go_to_page(d, "israel adsenya")
    
    # Perform scrolling and liking of tweets
    scroll_and_like(d)

if __name__ == "__main__":
    # Uncomment this line to run the main function
    # main()

    # Example of performing a comment action:
    d = u2.connect("10.100.102.168")  # Use the IP address of your device
    time.sleep(1)
    comment(d)  # Try to find and tap on the comment icon
