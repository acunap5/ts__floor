from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from .models import topShot, Set
import time
from datetime import datetime
import re
import functools

def scrape(url, day):
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    browser.get(url)
    timeout = 5

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, 
                "//div[@class='Thumbnail__StyledThumbnail-sc-1tojpin-0 kAMKVp']")
            )
        )
    except TimeoutException:
        print("Timed out Loading Page")
        browser.quit()
    

    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height 

    topShot_elements = browser.find_elements_by_xpath(
        "//div[@class='Thumbnail__StyledThumbnail-sc-1tojpin-0 kAMKVp']"
    )
    for element in topShot_elements:
        #retrieve player name and uses regular expression for name capitalization 
        # i.e. TALEN HORTON-TUCKER -> Talen Horton-Tucker
        # check for explanation here: https://docs.python.org/3/library/stdtypes.html#str.title
        # changed [A-Za-z] to [\w] to include foreign letters
        name = element.find_element_by_tag_name("h3")
        player_name_of = name.text
        player_name_of = re.sub(r"[\w]+('[\w]+)?", lambda mo: mo.group(0).capitalize(),player_name_of)

        #retrieve img link
        link = element.find_element_by_tag_name("img")
        pic_of = link.get_attribute("src")

        #get description which includes play_type, team, set_name, series, date
        description = element.find_element_by_tag_name('p')
        description = description.text

        #parses description to make each part of description a variable
        dash_index = description.find('-')
        play_type_of = description[:dash_index - 1]
        description = description[dash_index+1:]
        description = description.split(',')
        date = description[0]
        date = datetime.strptime(date, " %b %d %Y").date()
        set_name_of = description[1]
        team_of = description[2]

        #gets price and converts it from string -> float -> int
        price = element.find_element_by_xpath(
            ".//div[@class='Price__PriceWrapper-sc-14mok7p-2 JKBnr']"
        )
        price = price.text
        dollar_sign_index = price.find('$')
        price_of = str( int ( float ( price[dollar_sign_index+1:].replace(',', '') ) ) )

        #gets rarity i.e. Common, Rare, Legendary
        rarity = element.find_element_by_xpath(
            ".//span[@class='MomentThumbnail__StyledRarityTag-sc-1b051xk-6 dfaslz']"
        )
        rarity_of = rarity.text

        #gets how many of a moment exist and LE/CC tag
        limit_ed = element.find_element_by_xpath(
            ".//span[@class='MomentThumbnail__StyledScarcityTag-sc-1b051xk-5 lgZZBR']"
        )
        if '+' not in limit_ed.text:
            limit = int(limit_ed.text[2:-2])
        else:
            limit = int(limit_ed.text[2:-3])
        edition_of = limit_ed.text[-2:]

        #seeing if this topShot exists in DB if not create
        obj, created = topShot.objects.get_or_create(
            player_name=player_name_of,
            pic=pic_of,
            play_type=play_type_of,
            team=team_of,
            set_name=set_name_of[1:],
            rarity=rarity_of,
            date_game=date,
            defaults={
                'out_of' : limit,
                'edition' : edition_of,
                'curr_price' : int(price_of),
                'open_price' : price_of,
                'close_price': price_of,
                'high_price' : price_of,
                'low_price' : price_of,
                'scrape_date' : day,
                },
        )

        ## if wasn't just created we will update fields
        if created is False:
            obj.curr_price = int(price_of)
            obj.out_of = limit 
            obj.edition = edition_of
            if obj.scrape_date[-10:] != day:
                obj.scrape_date += ',' + day
                obj.low_price += ',' + price_of
                obj.high_price += ',' + price_of
                obj.open_price += ',' + price_of
                obj.close_price += ',' + price_of
            elif ',' in obj.low_price:
                #always replace close price with new price
                c_idx = obj.close_price.rfind(',')
                obj.close_price = obj.close_price[:c_idx+1] + price_of

                #check if new price is a low or high
                h_idx = obj.high_price.rfind(',')
                l_idx = obj.low_price.rfind(',')

                high = int( obj.high_price[h_idx+1:] )
                low = int( obj.low_price[l_idx+1:] )

                if int(price_of) > high :
                    obj.high_price = obj.high_price[:h_idx+1] + price_of
                elif int(price_of) < low:
                    obj.low_price = obj.low_price[:l_idx+1] + price_of
            else:
                #only happens for first day of scrape where theres no ,
                obj.close_price = price_of
                high = int(obj.high_price)
                low = int(obj.low_price)
                
                if int(price_of) > high:
                    obj.high_price = price_of 
                elif int(price_of) < low:
                    obj.low_price = price_of

            #finished updating now we save obj
            obj.save()

        #set image_url logic
        idx = set_name_of.find('(')
        altered_name = set_name_of[:idx-1]
        altered_name = altered_name.replace('-', 'qy')
        altered_name = altered_name.replace(' ', '_')
        altered_name = re.sub(r'\W+', '', altered_name)
        altered_name = altered_name.replace('qy', '-')
        pic_url = 'https://assets.nbatopshot.com/codex/' + rarity_of.lower() + '/co_' + set_name_of[-2] + altered_name.lower() + '_' + rarity_of.lower() + '.jpg'

        #check if set exists if not we create it
        set_obj, created = Set.objects.get_or_create(set_name=set_name_of[1:],defaults={'img_link' : pic_url})

        #simply adds the moment if not in the sets moments
        if created is True:
            set_obj.moments.add(obj)
        else:
            ts_in_set = set_obj.moments.all()
            if obj not in ts_in_set:
                set_obj.moments.add(obj)

        #finished and save changes
        set_obj.save()


    browser.quit()




