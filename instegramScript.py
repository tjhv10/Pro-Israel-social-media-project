import uiautomator2 as u2
import time
from common_area import *

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
    time.sleep(3)
    # Type each character of the search term with a random delay
    tap_keyboard(d,text)
    time.sleep(1)
    d.press(66)  # Press the search button
    time.sleep(3)
    d.click(245, 225) # Press the accounts button
    time.sleep(3)
    # Click to go into the first result
    d.click(360,300)  # Coordinates for the first user result
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

def main():
    """
    The main function connects to the Android device and performs various Instagram actions.
    """
    # Connect to the Android device using its IP address (make sure your device is connected via ADB over Wi-Fi)
    d = u2.connect("10.100.102.177")  # Replace with your device's IP address
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
main()

# Example of performing a comment action:
# d = u2.connect("10.100.102.168")  # Use the IP address of your device
# time.sleep(1)
# tap_like_button(d)