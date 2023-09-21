import requests
from bs4 import BeautifulSoup

url = 'https://www.yellowpages.com/search?search_terms=music+venue&geo_location_terms=oregon'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/85.0.4183.83 Safari/537.36'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

listing = soup.find_all('div', class_='result')

for item in listing:
    name = item.find('a', class_='business-name').text
    address = item.find('div', class_='street-address').text
    city_state = item.find('div', class_='locality').text
    phone = item.find('div', class_='phones phone primary').text
    try:
        website = item.find('a', class_="track-visit-website")['href']
    except:
        website = ''

    venue = {
        'Name': name,
        'Address': address,
        'City/State': city_state,
        'Phone': phone,
        'Website': website
    }
    print(venue)
