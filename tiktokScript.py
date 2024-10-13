import uiautomator2 as u2
import time
import random
def click_search_bar(d):
    screen_width = d.info['displayWidth']
    # Calculate the coordinates for the top right corner
    x = screen_width - 75  # Right edge (1 pixel from the right)
    y = 100  # Top edge (0 pixel from the top)

    # Perform the click action
    d.click(x, y)
    print("Clicked on the search bar.")
def click_like_old_account_button(d):
    screen_width = d.info['displayWidth']
    # Calculate the coordinates for the top right corner
    x = screen_width - 75  # Right edge (1 pixel from the right)
    y = 800  # Top edge (0 pixel from the top)
    # Perform the click action
    d.click(x, y)
    print("Clicked on the like button.")
def click_like_new_account_button(d):
    screen_width = d.info['displayWidth']
    # Calculate the coordinates for the top right corner
    x = screen_width - 75  # Right edge (1 pixel from the right)
    y = 1100  
    # Perform the click action
    d.click(x, y)
    print("Clicked on the like button.")
def comment_text(d, text):
    click_comment_button(d)
    screen_width = d.info['displayWidth']
    # Calculate the coordinates for the top right corner
    x = screen_width/2  # Right edge (1 pixel from the right)
    y = 1500 
    # Perform the click action
    #TODO type the text as needed
    d.click(x, y)

def click_comment_button(d):
    screen_width = d.info['displayWidth']
    # Calculate the coordinates for the top right corner
    x = screen_width - 50  # Right edge (1 pixel from the right)
    y = 1000  # Top edge (0 pixel from the top)

    # Perform the click action
    d.click(x, y)
    print("Clicked on the comment button.")
def scroll_random_number(d):
    # Check if a scrollable view exists before swiping
        if d(scrollable=True).exists:
            print("Found a scrollable view! Swiping down...")

            # Generate a random number of swipes between 1 and 10
            num_swipes = random.randint(3, 6)
            print(f"Number of swipes: {num_swipes}")

            for i in range(num_swipes):
                # Swipe down from (x1, y1) to (x2, y2)
                d.swipe(500, 1200, 500, 300)
                random_time = random.randint(2, 15)  # Adjusted swipe parameters
                time.sleep(random_time)  # Wait between swipes
                print(f"Swiped down {i + 1} time(s).")
        
        else:
            print("No scrollable view found!") 
def main():
    d = u2.connect("10.100.102.168")  # Use the IP address of your device

    # Wait for a moment to ensure connection
    time.sleep(1)

    # Start the TikTok app
    d.app_start("com.zhiliaoapp.musically")
    print("Opened TikTok!")

    # Wait for the app to load
    time.sleep(15)  # Increased wait time

    # Check if TikTok is running
    if "com.zhiliaoapp.musically" in d.app_list_running():
        print("TikTok is running!")
        # click_comment_button(d)
        scroll_random_number(d)
        # click_search_bar(d)
        # comment_text(d,"go Israelllllll")
        click_like_new_account_button(d)
    else:
        print("TikTok is not running!")
main()
# d = u2.connect("10.100.102.168")  # Use the IP address of your device

#     # Wait for a moment to ensure connection
# time.sleep(1)
