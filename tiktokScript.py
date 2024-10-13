import uiautomator2 as u2
import time
import random

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
    
    # Type each character of the search term with a random delay
    for char in text:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay to mimic human typing
    
    d.press(66)  # Press the search button
    time.sleep(3)
    
    # Click to go to users
    d.click(400 / 1440, 450 / 3168)  # Coordinates for users tab
    time.sleep(3)
    
    # Click to go into the first result
    d.click(700 / 1440, 700 / 3168)  # Coordinates for the first user result

def click_like_old_account_like_button(d):
    """
    Clicks the like button for an old account.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    x = screen_width * (650 / 720)  # Approximate X coordinate for the like button (old account)
    y = screen_height * (900 / 1560)  # Approximate Y coordinate
    
    d.click(x, y)
    print("Clicked on the like button for old account.")

def click_like_new_account_button(d):
    """
    Clicks the like button for a new account.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    x = screen_width * (650 / 720)  # Approximate X coordinate for the like button (new account)
    y = screen_height * (1100 / 1560)  # Approximate Y coordinate

    d.click(x, y)
    print("Clicked on the like button for new account.")

def comment_text(d, text):
    """
    Comments on a post.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    text (str): The text to comment.
    """
    click_comment_button(d)
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    x = screen_width / 2  # Center X coordinate for the comment input
    y = screen_height * (1500 / 1560)  # Approximate Y coordinate for the comment input

    d.click(x, y)  # Click on the comment input
    print(f"Commenting: {text}")
    
    # Type the comment character by character with random delays
    for char in text:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay to mimic human typing speed
    time.sleep(1)
    
    # Click the submit button for the comment
    d.click(1300 / 1440, 2700 / 3168)

def click_comment_button(d):
    """
    Clicks the comment button on a post.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    """
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']
    
    x = screen_width * (670 / 720)  # Approximate X coordinate for the comment button
    y = screen_height * (1000 / 1560)  # Approximate Y coordinate
    
    d.click(x, y)
    print("Clicked on the comment button.")

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
    click_like_old_account_like_button(d)  # Click like button for the old account
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
            random_time = random.randint(2, 4)  # Random wait time between swipes
            time.sleep(random_time)
            print(f"Swiped down {i + 1} time(s).")
        else:
            print("No scrollable view found!")
        
        # Click the like button again after scrolling
        click_like_old_account_like_button(d) 

def like_the_page(d, page):
    """
    Likes the specified page and comments on a post.

    Parameters:
    d (uiautomator2.Device): The connected device object from uiautomator2.
    page (str): The name of the page to like.
    """
    search(d, page)  # Search for the page
    d.click(260 / 1440, 3000 / 3168)  # Click on the specified page
    time.sleep(2)
    scroll_and_like(d)  # Scroll and like posts

def main():
    """
    Main function to connect to the device and perform actions on TikTok.
    """
    d = u2.connect("10.100.102.102")  # Use the IP address of your device
    time.sleep(1)

    d.app_start("com.zhiliaoapp.musically")  # Open TikTok app
    print("Opened TikTok!")
    time.sleep(15)

    if "com.zhiliaoapp.musically" in d.app_list_running():
        print("TikTok is running!")
        # Uncomment this line to scroll randomly
        scroll_random_number(d)
        time.sleep(1)
        click_like_old_account_like_button(d)
        time.sleep(1)  # Click the like button for an old account
        comment_text(d, "go Israel")  # Comment on the post
    else:
        print("TikTok is not running!")

# Run the main function to start the process
main()

# Connect to the device and like the specified page
# d = u2.connect("10.100.102.102")  # Use the IP address of your device
# time.sleep(1)
# scroll_random_number(d)  # Like the page "israel"
