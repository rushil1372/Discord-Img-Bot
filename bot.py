import os
import discord
from dotenv import load_dotenv

import selenium
from selenium import webdriver
import time
import random 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

DRIVER_PATH = "C:/Users/RUSHIL/Desktop/chromedriver.exe"
wd = webdriver.Chrome(executable_path=DRIVER_PATH)

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver=wd, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    wd.get(search_url.format(q=query))

    image_urls = []
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print("Found: {} search results".format(number_results))
        
        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue
    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.append(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
 
        results_start = len(thumbnail_results)
        result = random.choice(image_urls)
    return result

@client.event
async def on_ready():
    print('{} has connected to Discord!'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content=='$hey':
        await message.channel.send("Hey! How can I help?")

    if message.content.startswith('$im'):
        def check(m):
            final = fetch_image_urls(m.content.strip("$im"),20)
            return final 

        await message.channel.send(check(message))
        
        

client.run(TOKEN)
