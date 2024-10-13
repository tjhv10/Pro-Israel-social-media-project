import os
import uiautomator2 as u2
import time
import cv2
import random

def scroll_random_number(d):
    # Check if a scrollable view exists before swiping
        if d(scrollable=True).exists:
            print("Found a scrollable view! Swiping down...")

            # Generate a random number of swipes between 1 and 10
            num_swipes = random.randint(1, 3)
            print(f"Number of swipes: {num_swipes}")

            for i in range(num_swipes):
                # Swipe down from (x1, y1) to (x2, y2)
                rnd_swipe = random.randint(1000, 1200)
                d.swipe(500, rnd_swipe, 500, rnd_swipe-900)
                random_time = random.randint(2, 15)
                print("waiting " + str(random_time)+ " seconds...")  # Adjusted swipe parameters
                time.sleep(random_time)  # Wait between swipes
                print(f"Swiped down {i + 1} time(s).")
            d.swipe(500, rnd_swipe-900, 500, rnd_swipe)
        
        else:
            print("No scrollable view found!") 

def search(d, text_to_type):
    # Perform the click action to open the search bar
    d.click(180, 1500)
    print("Clicked on the search button.")
    time.sleep(1)
    # Perform another click on the text input field (if necessary)
    d.click(360, 140)
    time.sleep(2)
    # Type the desired text character by character with random delays to simulate natural typing
    for char in text_to_type:
        d.send_keys(char, clear=False)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay between 100ms and 300ms to mimic human typing speed
    
    print(f"Typed '{text_to_type}' in the search bar naturally.")


def take_screenshot(d, filename='screenshot.png'):
    # Create the directory if it does not exist
    screenshot_dir = 'Screenshots'
    
    # Ensure the directory exists
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    # Full path to save the screenshot
    screenshot_path = os.path.join(screenshot_dir, filename)
    
    # Take a screenshot and save it with a filename
    d.screenshot(screenshot_path)  # Save the screenshot with the specified filename
    print(f"Screenshot saved to: {screenshot_path}")
    return screenshot_path


def find_best_match_in_image(image_path, heart_template_path):
    # Load the images
    img = cv2.imread(image_path)
    template = cv2.imread(heart_template_path)

    # Check if both images were loaded successfully
    if img is None:
        print("Error loading screenshot image.")
        return None
    if template is None:
        print("Error loading heart template image.")
        return None

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Get dimensions of the template
    h, w = template_gray.shape
    new_h, new_w = h, w

    # Check if template is larger than the image
    if h > img_gray.shape[0] or w > img_gray.shape[1]:
        print("Heart template is larger than the screenshot, resizing template.")
        scale_factor = min(img_gray.shape[0] / h, img_gray.shape[1] / w)
        new_h = int(h * scale_factor)
        new_w = int(w * scale_factor)
        template_gray = cv2.resize(template_gray, (new_w, new_h))

    # Match the template
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Find the best match position using minMaxLoc
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Apply a threshold to filter weak matches
    threshold = 0.4  # Adjust this threshold as necessary
    if max_val >= threshold:
        # Return the center of the best matching region
        best_match_center = (max_loc[0] + new_w // 2, max_loc[1] + new_h // 2)
        print(f"Best match found with value: {max_val} at {best_match_center}")
        return best_match_center
    else:
        print(f"No match found above the threshold. Best match value: {max_val}")
        return None




def tap_heart(d, heart_template_path = "twitter_heart.png"):
    # Take a screenshot
    screenshot_path = take_screenshot(d)

    # Find the heart in the screenshot
    coordinates = find_best_match_in_image(screenshot_path, heart_template_path)

    if coordinates:
        print(f"Heart found at {coordinates}, tapping...")
        d.click(coordinates[0], coordinates[1])  # Tap the heart
    else:
        print("Heart not found on the screen.")

def main():
    d = u2.connect("10.100.102.168")  # Use the IP address of your device
    time.sleep(1)

    # Start the Twitter app
    d.app_start("com.twitter.android")
    print("Opened Twitter!")

    # Wait for the app to load
    time.sleep(7)  # Increased wait time

    # Call the function to tap the heart
    tap_heart(d)


def main():
    d = u2.connect("10.100.102.168")  # Use the IP address of your device
    # Wait for a moment to ensure connection
    time.sleep(1)

    # Start the Twitter app
    d.app_start("com.twitter.android")
    print("Opened Twitter!")

    # Wait for the app to load
    time.sleep(7)  # Increased wait time
    d.click(70, 1500)
    time.sleep(2)
    scroll_random_number(d)
    search(d,"israel")