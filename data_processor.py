import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

def generate_html():
    game_data_blob = open("gta/gta_data.json")
    data = json.load(game_data_blob)

    for game in data["Games"]:
        html_content = f'''
            <head>
                <link rel="stylesheet" href="css/style.css">
            </head>
            <body>
                <div class = "wrapper" id = "wrapper">
                    <div class="sec-wrapper">
                        <div class = "game-main">
                            <img src="img/{game["Name"].replace(" ","-").replace(":","").lower()}-{game["Year"]}.jpg" alt="">
                        </div>
                        <div class = "game-details">
                                <h1>{game["Name"]} ({game["Year"]}) <span id="small-italic">{game["Producer"]}</span></h1>
                            <div class = "game-details-data">
                                <p id="highlight">Score (IGN)</p>
                                <b>{game["IGN"]}</b>
                            </div>
                            <div class = "game-details-data">
                                <p id="highlight">Copies sold</p>
                                <b>{game["Copies sold"]}</b>
                            </div>
                            <div class = "game-details-data">
                                <p id="highlight">Cost</p>
                                <b>{game["Cost"]}</b>
                            </div>
                            <div class = "game-details-data">
                                <p id="highlight">Revenue</p>
                                <b>{game["Revenue"]}</b>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        '''

        with open(f'html/{game["Name"].replace(" ","-").replace(":","").lower()}-{game["Year"]}.html', 'w') as html_file:
            html_file.write(html_content)


def convert_html_to_img():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the path to the local HTML file (in the same folder as the script)
    html_folder_path = os.path.join(current_dir, 'html')

    for file_name in os.listdir(html_folder_path):

        # Skip files named "css" or "img"
        if file_name.lower() in ["css", "img"]:
            print(f"Skipping file: {file_name}")
            continue

        # Construct the full file path
        full_file_path = os.path.join(html_folder_path, file_name)

        # Set up the Selenium WebDriver (replace with Firefox() if using Firefox)
        options = webdriver.ChromeOptions()

        # Initialize the WebDriver
        driver = webdriver.Chrome(options=options)

        try:
            # Load the local HTML file
            driver.get(f"file://{full_file_path}")

            # Find the specific <div> by its ID
            element = driver.find_element(By.ID, "wrapper")
            
            # Take a screenshot
            screenshot_path = f"gta/{file_name.replace(".html","")}.png"
            element.screenshot(screenshot_path)
            print(f"Screenshot saved at: {screenshot_path}")
        finally:
            # Close the WebDriver
            driver.quit()

# Start script
if __name__ == '__main__':
    generate_html()
    convert_html_to_img()