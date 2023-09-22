import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

venue_list = []


def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/85.0.4183.83 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', class_='result')


def transform(listing):
    for item in listing:
        try:
            name = item.find('a', class_='business-name').text
        except:
            name = ''
        try:
            address = item.find('div', class_='street-address').text
        except:
            address = ''
        try:
            city_state = item.find('div', class_='locality').text
        except:
            city_state = ''
        try:
            phone = item.find('div', class_='phones phone primary').text
        except:
            phone = ''
        try:
            website = item.find('a', class_="track-visit-website")['href']
        except:
            website = ''
        try:
            photo = item.find('img', class_='no-tracks lazy')['src']
        except:
            photo = ''

        venue = {
            'Photo': photo,
            'Name': name,
            'Address': address,
            'City/State': city_state,
            'Phone': phone,
            'Website': website
        }
        venue_list.append(venue)
    return


def save(state):
    df = pd.DataFrame(venue_list)
    df.to_csv(f'venuelist{state}.csv', index=False)


print("""\
_  _ ____ _  _ _  _ ____    ____ ____ ____ ____ ___  ____ ____ 
|  | |___ |\ | |  | |___    [__  |    |__/ |__| |__] |___ |__/ 
 \/  |___ | \| |__| |___    ___] |___ |  \ |  | |    |___ |  \ 
                                                                                                                                                                
                    """)


search = input("What are your search terms?" + "\n")
location = input("What state would you like to search in?" + "\n")
pages = int(input("How many pages do you want to search?" + "\n")) + 1

for x in range(1, pages):
    print(f"Getting page {x}...")
    listing = extract(
        f'https://www.yellowpages.com/search?search_terms={search}&geo_location_terms={location}&page={x}')
    transform(listing)
    time.sleep(5)

save(location)
print("Saved to csv file")
