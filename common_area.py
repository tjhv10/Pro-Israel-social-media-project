import random
import threading
import time
import cv2
import numpy as np


israel_support_comments = [
    "Israel has the right to defend itself.",
    "Stand with Israel!",
    "Israel is a beacon of democracy in the Middle East.",
    "Israel's innovation is inspiring.",
    "Support Israel and its quest for peace.",
    "Israel is a land of hope and resilience.",
    "I stand with the people of Israel.",
    "Israel is a vital ally.",
    "The strength of Israel is admirable.",
    "Israel's culture is rich and vibrant.",
    "Israel is a symbol of survival.",
    "Together for Israel!",
    "Israel's achievements in technology are remarkable.",
    "Support Israel's right to exist.",
    "Israel represents freedom and democracy.",
    "The history of Israel is a testament to perseverance.",
    "Israel's contributions to science benefit us all.",
    "Proud to support Israel!",
    "Israel is a land of diverse cultures.",
    "The spirit of Israel is unbreakable.",
    "Israel's military is one of the best in the world.",
    "We must defend Israel's right to self-determination.",
    "Israel's landscapes are breathtaking.",
    "Israel is a sanctuary for many.",
    "The resilience of Israel is inspiring.",
    "Israel's commitment to peace is commendable.",
    "Stand with our friends in Israel!",
    "Israel is a land of opportunity.",
    "The people of Israel deserve peace.",
    "Support Israel's democratic values.",
    "Israel's diversity is its strength.",
    "We will never forget Israel's sacrifices.",
    "Israel is an example of coexistence.",
    "Proud of Israel's cultural contributions.",
    "Israel stands strong against adversity.",
    "Support Israel's innovation and creativity.",
    "Israel is a light unto the nations.",
    "The bond with Israel is unbreakable.",
    "Israel's history is a story of resilience.",
    "The future of Israel is bright.",
    "Support Israel's right to security.",
    "Israel is a hub of knowledge and learning.",
    "Together we can ensure Israel's safety.",
    "Israel's farmers feed the world.",
    "The spirit of Israel lives on.",
    "Support for Israel is support for peace.",
    "Israel's artistic community is vibrant.",
    "Israel's unity is its strength.",
    "We stand with Israel in times of need.",
    "The Israeli people are strong and resilient.",
    "Israel is a land of progress.",
    "The achievements of Israel are commendable.",
    "We cannot ignore Israel's challenges.",
    "Support Israel's quest for lasting peace.",
    "The history of Israel is a testament to hope.",
    "Israel is a model for democracy.",
    "Together, we stand with Israel.",
    "Israel is a haven for many seeking refuge.",
    "Support Israel's right to thrive.",
    "Israel's advancements in medicine save lives.",
    "Proud of Israel's technological leadership.",
    "Israel's spirit of innovation is unmatched.",
    "Stand strong with Israel.",
    "The diversity of Israel enriches us all.",
    "Israel's achievements inspire generations.",
    "We cannot forget Israel's sacrifices for peace.",
    "Support for Israel is support for democracy.",
    "Israel's military innovation is impressive.",
    "Israel is a champion of human rights.",
    "The future of Israel is in our hands.",
    "Israel's agricultural innovations are groundbreaking.",
    "We support Israel's quest for stability.",
    "The culture of Israel is a treasure.",
    "Israel is a land of dreams and possibilities.",
    "The spirit of the Israeli people is incredible.",
    "Support Israel's commitment to peace and security.",
    "Israel is a land of opportunity for all.",
    "Together, we stand with the people of Israel.",
    "Israel's technological advancements benefit humanity.",
    "Proud of Israel's rich history.",
    "Israel's youth are its future.",
    "Support for Israel is support for progress.",
    "Israel is a land where hope thrives.",
    "The achievements of Israel's scientists are remarkable.",
    "Israel is a symbol of strength and courage.",
    "We celebrate Israel's vibrant culture.",
    "Support Israel's democratic processes.",
    "The resilience of Israel is an inspiration.",
    "Together, we can support Israel's growth.",
    "Israel's commitment to peace is unwavering.",
    "Stand with Israel for a better tomorrow.",
    "Israel is a nation of pioneers.",
    "The beauty of Israel is unmatched.",
    "We must advocate for Israel's rights.",
    "Support for Israel is a call for unity.",
    "Israel's heritage is a source of pride.",
    "Together, we celebrate Israel's successes.",
    "The strength of Israel is its people.",
    "Support Israel's efforts for peace and understanding.",
    "Israel is a land of innovation and creativity.",
    "We stand with Israel in solidarity.",
    "The future is bright for Israel.",
    "I stand with Israel!",
    "Solidarity with Israel 🇮🇱",
    "Peace for Israel always.",
    "Israel has my support!",
    "Forever pro-Israel 🇮🇱",
    "Standing strong with Israel.",
    "Israel’s right to defend!",
    "Supporting Israel’s future.",
    "Am Yisrael Chai!",
    "Peace for Israel 🙏",
    "Supporting Israel’s security.",
    "Defending Israel’s sovereignty!",
    "Israel deserves peace.",
    "Proudly pro-Israel!",
    "Strength for Israel.",
    "Backing Israel always!",
    "Unity with Israel 🇮🇱",
    "Israel forever 💙",
    "Israel deserves justice!",
    "Always with Israel."
]

twitter_handles = [
    "YishaiFleisher",
    "DavidMFriedman",
    "Ostrov_A",
    "LahavHarkov",
    "havivrettiggur",
    "Gil_Hoffman",
    "AIPAC",
    "sfrantzman",
    "EylonALevy",
    "FleurHassanN",
    "khaledAbuToameh",
    "rich_goldberg",
    "EVKontorovich",
    "imshin",
    "BarakRavid",
    "MaxAbrahms",
    "mickyrosenfeld",
    "RaphaelAhren",
    "YaakovLappin",
    "ynetnews",
    "HananyaNaftali",
    "AmbDermer",
    "BoothWilliam",
    "AnshelPfeffer",
    "ElhananMiller",
    "GershonBaskin",
    "HonestReporting",
    "issacharoff",
    "JeffreyGoldberg",
    "KhaledAbuToameh",
    "LahavHarkov",
    "DannyNis"
]

tiktok_accounts = [
    "israel",
    "powerisrael",
    "israel_hayom",
    "tbn_official",
    "tbn_fr",
    "tbnua",
    "cbnnewsofficial",
    "cbcnews",
    "newsmaxtv",
    "hananyanaftali",
    "Shaidavidai",
    "noybeyleyb",
    "EylonALevy",
    "yoavdavis",
    "millennialmoor",
    "Jews_of_Ny",
    "noatishby",
    "jewishhistory",
    "houseoflev",
    "melissaschapman",
    "Jewisnews",
    "EndJewHatred",
    "jew_ishcontent",
    "alizalicht"
    ]

instagram_accounts = [
    "rudy_israel",
    "Shaidavidai",
    "adelacojab",
    "EylonALevy",
    "yoavdavis",
    "millennialmoor",
    "Jews_of_Ny",
    "noatishby",
    "jewishhistory",
    "melissaschapman",
    "EndJewHatred",
    "wearetov",
    "idf",
    "fleurhassann",
    "standwithus",
    "israel", 
    "israeltodaymag", 
    "jewishagency", 
    "honestreporting", 
    "beyondtheheadline", 
    "simonwiesenthalcenter", 
    "maccabiusa", 
    "aipac", 
    "Birthrightisraelbeyond", 
    "ariseforisrael",
    "houseoflev"
]


keyboard_dic = {
    "q": (40, 1200),
    "w": (110, 1200),
    "e": (180, 1200),
    "r": (250, 1200),
    "t": (320, 1200),
    "y": (390, 1200),
    "u": (460, 1200),
    "i": (530, 1200),
    "o": (600, 1200),
    "p": (670, 1200),
    "a": (70, 1285),
    "s": (140, 1285),
    "d": (210, 1285),
    "f": (280, 1285),
    "g": (350, 1285),
    "h": (420, 1285),
    "j": (490, 1285),
    "k": (560, 1285),
    "l": (630, 1285),
    "z": (150, 1400),
    "x": (220, 1400),
    "c": (290, 1400),
    "v": (360, 1400),
    "b": (430, 1400),
    "n": (500, 1400),
    "m": (570, 1400),
    ".": (570,1500),
    ",": (150,1500),
    " ": (400,1500)
}

report_tiktok_clicks = {
    'Exploitation and abuse of people under 18': 'd.click(350,390):d.click(350,390):d.click(350,1500):d.click(350,1380)',
    'Physical violence and violent threats': 'd.click(350,390):d.click(350,460):d.click(350,1500):d.click(350,1380)',
    'Sexual exploitation and abuse': 'd.click(350,390):d.click(350,616):d.click(350,1500):d.click(350,1380)',
    'Human exploitation': 'd.click(350,390):d.click(350,710):d.click(350,1500):d.click(350,1380)', 
    'Other criminal activities': 'd.click(350,390):d.click(350,922):d.click(350,1500):d.click(350,1380)',
    'Dangerous activities and challenges': 'd.click(350,849):d.click(350,1500):d.click(350,1380)',
    'Shocking and graphic content': 'd.click(350,1058):d.click(350,1500):d.click(350,1380)',
    'Hate speech and hateful behaviors':'d.click(350,460):d.click(350,390):d.click(350,1500):d.click(350,1380)',
    'Harassment and bullying':'d.click(350,460):d.click(350,460):d.click(350,390):d.click(350,1500):d.click(350,1380)',
    'Harmful misinformation':'d.click(350,1149):d.click(350,460):d.click(350,1500):d.click(350,1380)',
    'Deepfakes, synthetic media, and manipulated media':'d.click(350,1149):d.click(350,590):d.click(350,1500):d.click(350,1380)',
    'Child sexual exploitation':'d.swipe(500, 1200, 500, 300, duration=0.05):d.click(350,1213):d.swipe(500, 300, 500, 1200, duration=0.05):d.click(350,390):d.click(350,1500):d.click(350,1380)', 
    'Illegal hate speech':'d.swipe(500, 1200, 500, 300:duration=0.05):d.click(350,1213):d.swipe(500, 300, 500, 1200, duration=0.05):d.click(350,560):d.click(350,1500):d.click(350,1380)', 
    'Content relating to violent or organized crime':'d.swipe(500, 1200, 500, 300, duration=0.05):d.click(350,1213):d.click(350,420):d.click(350,1500):d.click(350,1380)', 
    'Harrassment or threats':'d.swipe(500, 1200, 500, 300, duration=0.05):d.click(350,1213):d.click(350,870):d.click(350,1500):d.click(350,1380)', 
    'Defamation':'d.swipe(500, 1200, 500, 300, duration=0.05):d.click(350,1213):d.click(350,970):d.click(350,1500):d.click(350,1380)',
    'Other': 'd.swipe(500, 1200, 500, 300, duration=0.05):d.click(350,1500):d.click(350,1500):d.click(350,1380)'
}

report_twitter_clicks = {
    "Slurs & Tropes":"d.click(370,670):d.click(370,1450):d.click(370,670):d.click(370,1450):d.click(370,1450)",
    "Hateful References":"d.click(370,670):d.click(370,1450):d.click(370,950):d.click(370,1450):d.click(370,1450)",
    "Dehumanization":"d.click(370,670):d.click(370,1450):d.click(370,1250):d.click(370,1450):d.click(370,1450)",
    "Hateful Imagery":"d.click(370,670):d.click(370,1450):d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,860):d.click(370,1450):d.click(370,1450)",
    "Incitement":"d.click(370,670)::d.click(370,1450)d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,1214):d.click(370,1450):d.click(370,1450)",
    "Unwanted NSFW & Graphic Content":"d.click(370,965):d.click(370,1450):d.click(370,560):d.click(370,1450):d.click(370,1450)",
    "Targeted Harassment":"d.click(370,965):d.click(370,1450):d.click(370,770):d.click(370,1450):d.click(370,1450)",
    "Insults":"d.click(370,965):d.click(370,1450):d.click(370,986):d.click(370,1450):d.click(370,1450)",
    "Violent Event Denial":"d.click(370,965):d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,1450):d.click(370,895):d.click(370,1450):d.click(370,1450)",
    "Inciting Harassment":"d.click(370,965):d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,1450):d.click(370,1200):d.click(370,1450):d.click(370,1450)",
    "Violent Threats":"d.click(370,1180):d.click(370,1450):d.click(370,560):d.click(370,1450):d.click(370,1450)",
    "Glorification of Violence":"d.click(370,1180):d.click(370,1450):d.click(370,980):d.click(370,1450):d.click(370,1450)",
    "Incitement of Violence":"d.click(370,1180):d.click(370,1450):d.click(370,1280):d.click(370,1450):d.click(370,1450)",
    "Wish of Harm":"d.click(370,1180):d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,1450):d.click(370,925):d.click(370,1450):d.click(370,1450)",
    "Coded Incitement of Violence":"d.click(370,1180):d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,1450):d.click(370,1200):d.click(370,1450):d.click(370,1450)",
    "Spam":"d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,1450):d.click(370,363):d.click(370,1450):d.click(370,1450)",
    "Violent & hateful entities":"d.swipe(500, 1200, 500, 300, duration=0.05):d.click(370,1450):d.click(370,1240):d.click(370,1450):d.click(370,1450)"
}

report_instagram_clicks = {
    "bullying or harassment":"d.click(370,750):d.click(370,660):d.click(370,614):d.click(370,1481)",
    "Credible threat to safty":"d.click(370,930):d.click(370,571):d.click(370,1481)",
    "Seems like terrorism or organized crime":"d.click(370,930):d.click(370,658):d.click(370,1481)",
    "Calling for violence":"d.click(370,930):d.click(370,838):d.click(370,1481)",
    "Hate speech or symbols":"d.click(370,930):d.click(370,931):d.click(370,1481)",
    "Showing violence, death or severe injury":"d.click(370,930):d.click(370,1021):d.click(370,1481)",
    "False information-Health":"d.click(370,1286):d.click(370,520):d.click(370,1440)",
    "False information-Politics":"d.click(370,1286):d.click(370,613):d.click(370,1440)",
    "False information-Social issues":"d.click(370,1286):d.click(370,700):d.click(370,1440)",
    "False information-Digitally created or altered":"d.click(370,1286):d.click(370,800):d.click(370,1440)",
}

def tap_keyboard(d, text, keyboard = keyboard_dic):
    """
    Simulates tapping on the screen using the keyboard coordinates for each character in the text.
    """
    for char in text.lower():
        if char == "_":
            char = " "  
        if char in keyboard:
            x, y = keyboard[char]
            d.click(x, y)  # Simulate a tap on the screen at the corresponding coordinates
            time.sleep(random.uniform(0.04, 0.07))  # Add a small delay between taps
        else:
            print(f"{threading.current_thread().name}:{d.wlan_ip} Character '{char}' not found in keyboard dictionary!")


def take_screenshot(d, thread = threading.current_thread().name, app = "inst"):
    time.sleep(2)
    filename = f"Screenshots/{thread}-screenshot_{app}.png"
    print(f"{thread}:{d.wlan_ip} Taking screenshot...")
    d.screenshot(filename)
    print(f"Screenshot saved as {filename}.")
    return filename

def find_best_match(image_path, users_template_path, d):
    """
    Finds the best match of a user's button icon in the screenshot using template matching.
    """
    time.sleep(0.5)
    print(f"{threading.current_thread().name}:{d.wlan_ip} Starting find_best_match function")
    
    img = cv2.imread(image_path)
    template = cv2.imread(users_template_path)

    if img is None or template is None:
        print(f"{threading.current_thread().name}:{d.wlan_ip} Error loading images.")
        return None

    h, w = template.shape[:2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    matches = []
    for pt in zip(*loc[::-1]):
        matches.append((pt, result[pt[1], pt[0]]))

    if matches:
        # Get the best match (highest confidence value)
        best_match = max(matches, key=lambda x: x[1])
        best_coordinates = (best_match[0][0] + w // 2, best_match[0][1] + h // 2)
        best_value = best_match[1]
        print(f"{threading.current_thread().name}:{d.wlan_ip} Best match found with value: {best_value} at {best_coordinates}")
    else:
        # If no matches found above threshold, find the closest match
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        best_coordinates = (max_loc[0] + w // 2, max_loc[1] + h // 2)
        best_value = max_val
        print(f"{threading.current_thread().name}:{d.wlan_ip} No matches above threshold, closest match found with value: {best_value} at {best_coordinates}")
        return None
    
    print(f"{threading.current_thread().name}:{d.wlan_ip} Finished find_best_match function")
    
    return best_coordinates

def handle_user_selection(d,report_dict):
    print("Select a report reason:")
    numbered_report_dict = show_tree(report_dict)

    # User input for selection
    user_choice = input("Enter the number of the report reason you want to select: ")

    if user_choice.isdigit() and int(user_choice) in numbered_report_dict:
        action = numbered_report_dict[int(user_choice)]
        if isinstance(action, dict):  # If the selection has subcategories
            handle_user_selection(action)  # Show subcategories
        else:
            execute_action(d,action,report_dict)  # Execute the action for the selected reason
    else:
        print("Invalid selection. Please enter a valid number.")

def show_tree(report_dict, level=0):
    numbered_dict = {}
    count = 1
    for key in report_dict.keys():
        print("  " * level + f"{count}. {key}")
        numbered_dict[count] = key  # Store the original key for action retrieval
        count += 1
        if isinstance(report_dict[key], dict):
            # Recursive call for subcategories
            sub_count = show_tree(report_dict[key], level + 1)
            numbered_dict.update(sub_count)
    return numbered_dict

def execute_action(d,reason,report_dict):
    # Execute the corresponding action for the selected reason
    if reason in report_dict:
        action = report_dict[reason]
        actions = action.split(':')
        print(f"Executing action for '{reason}': {actions}")
        time.sleep(1)
        for act in actions:
            exec(act)
            time.sleep(3)  
    else:
        print("No action found for this reason.")


file_lock = threading.Lock()

def update_results_file(action_type):
    """
    Updates the results file with the incremented count for the given action.
    
    Parameters:
    action_type (str): The action type to update ('Likes', 'Comments', 'Follows', 'Reports').
    """
    file_path = "results.txt"
    
    with file_lock:  # Ensure only one thread accesses the file at a time
        # Load current values
        with open(file_path, "r") as file:
            data = file.readlines()

        # Parse current counts from the file
        stats = {}
        for line in data:
            key, value = line.strip().split(" - ")
            stats[key] = int(value)
        
        # Increment the relevant action count
        if action_type in stats:
            stats[action_type] += 1

        # Write updated values back to the file
        with open(file_path, "w") as file:
            for key, value in stats.items():
                file.write(f"{key} - {value}\n")
