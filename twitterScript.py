import os
import uiautomator2 as u2
import time
import cv2
import random

def scroll_once(d):
    if d(scrollable=True).exists:
        # Generate a random number of swipes between 1 and 3
        rnd_swipe = random.randint(1000, 1200)
        d.swipe(500, rnd_swipe, 500, rnd_swipe-500)
        random_time = random.randint(1, 6)
        print(f"Waiting {random_time} seconds...")  # Adjusted swipe parameters
    else:
        print("No scrollable view found!") 

def scroll_random_number(d):
    """Scrolls a random number of times between 1 and 3."""
    if d(scrollable=True).exists:
        print("Found a scrollable view! Swiping down...")

        # Generate a random number of swipes between 1 and 3
        num_swipes = random.randint(1, 3)
        print(f"Number of swipes: {num_swipes}")

        for i in range(num_swipes):
            # Swipe down from (x1, y1) to (x2, y2)
            rnd_swipe = random.randint(1000, 1200)
            d.swipe(500, rnd_swipe, 500, rnd_swipe-900)
            random_time = random.randint(2, 15)
            print(f"Waiting {random_time} seconds...")  # Adjusted swipe parameters
            time.sleep(random_time)  # Wait between swipes
            print(f"Swiped down {i + 1} time(s).")
        
        # Swipe up to go back to previous content
        d.swipe(500, rnd_swipe-900, 500, rnd_swipe)
    else:
        print("No scrollable view found!") 

def search(d, text_to_type):
    """Searches for the given text in the Twitter search bar."""
    d.click(180, 1500)
    print("Clicked on the search button.")
    time.sleep(1)
    
    # Click on the search input field
    d.click(360, 140)
    time.sleep(2)
    
    # Type the desired text character by character with random delays
    for char in text_to_type:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay to mimic human typing speed
    
    print(f"Typed '{text_to_type}' in the search bar naturally.")

def take_screenshot(d, filename='screenshot.png'):
    """Takes a screenshot and saves it to a directory."""
    screenshot_dir = 'Screenshots'
    
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    screenshot_path = os.path.join(screenshot_dir, filename)
    d.screenshot(screenshot_path)  # Save the screenshot with the specified filename
    print(f"Screenshot saved to: {screenshot_path}")
    return screenshot_path

def find_best_match_in_image(image_path, heart_template_path):
    """Finds the best match of the heart icon in the screenshot using template matching (color images)."""
    # Load the images in color (default is color when using cv2.imread)
    img = cv2.imread(image_path)
    template = cv2.imread(heart_template_path)

    # Check if both images were loaded successfully
    if img is None:
        print("Error loading screenshot image.")
        return None
    if template is None:
        print("Error loading heart template image.")
        return None

    # Get the dimensions of the template
    h, w = template.shape[:2]  # Get height and width of the template
    new_h, new_w = h, w

    # Check if the template is larger than the image
    if h > img.shape[0] or w > img.shape[1]:
        print("Heart template is larger than the screenshot, resizing template.")
        scale_factor = min(img.shape[0] / h, img.shape[1] / w)
        new_h = int(h * scale_factor)
        new_w = int(w * scale_factor)
        template = cv2.resize(template, (new_w, new_h))  # Resize the template to fit the image

    # Perform template matching on the color images
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # Find the best match location
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Set a threshold for a good match
    threshold = 0.8  # Adjust this threshold as necessary
    if max_val >= threshold:
        # Calculate the center of the best match region
        best_match_center = (max_loc[0] + new_w // 2, max_loc[1] + new_h // 2)
        print(f"Best match found with value: {max_val} at {best_match_center}")
        return best_match_center
    else:
        print(f"No match found above the threshold. Best match value: {max_val}")
        return None


def tap_heart(d, heart_template_path="twitter_heart.png"):
    """Takes a screenshot and taps the heart if found."""
    screenshot_path = take_screenshot(d)
    coordinates = find_best_match_in_image(screenshot_path, heart_template_path)

    if coordinates:
        print(f"Heart found at {coordinates}, tapping...")
        d.click(coordinates[0], coordinates[1])  # Tap the heart
    else:
        print("Heart not found on the screen.")

def scroll_and_like(d):
    """Scrolls and tries to like (tap the heart) after each scroll."""
    for i in range(100):
        scroll_once(d)  # Scroll randomly
        time.sleep(1)
        tap_heart(d)  # Tap heart after scroll
        time.sleep(2)
def search_and_go_to_page(d,text):
    search(d,text)
    d.press(66)
    time.sleep(3)
    d.click(400, 240)
    time.sleep(5)
    d.click(400, 400)
    time.sleep(5)
    

def main():
    d = u2.connect("10.100.102.168")  # Use the IP address of your device
    time.sleep(1)

    # Start the Twitter app
    d.app_start("com.twitter.android")
    print("Opened Twitter!")

    time.sleep(7)  # Wait for the app to load

    # Search for the desired text
    search_and_go_to_page(d, "israel adsenya")
    scroll_and_like(d)

if __name__ == "__main__":
    main()
    # d = u2.connect("10.100.102.168")  # Use the IP address of your device
    # time.sleep(1)
    # scroll_and_like(d)