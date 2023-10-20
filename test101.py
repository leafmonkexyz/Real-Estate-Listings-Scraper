from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

initial_url = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?enteredFrom='

addresses = []
prices = []
sizes = []
room_counts = []

num_pages = 100


for page in range(1, num_pages + 1):
    
    current_url = f"{initial_url}{page}"
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")

    
    listings = soup.find_all('li', class_='result-list__listing result-list__listing--xl-new')

    
    for listing in listings:
        address = listing.find('button', class_='result-list-entry__map-link link-text-secondary font-normal font-ellipsis')
        if address:
            address = address.text.strip()
            addresses.append(address)
        else:
            addresses.append("Address not found")

        price_element = listing.find('dd', class_='font-highlight font-tabular')
        if price_element:
            price = price_element.text.strip()
        else:
            price = "Price not found"
        prices.append(price)

        size_elements = listing.find_all('dd', class_='font-highlight font-tabular')
        if len(size_elements) > 1:
            size = size_elements[1].text.strip()
        else:
            size = "Size not found"
        sizes.append(size)

        room_count = listing.find('span', class_='onlyLarge')
        room_counts.append(room_count)

    
    time.sleep(1)

data = {
    'Address': addresses,
    'Price': prices,
    'Size': sizes,
    'Room Count': room_counts,
}


df = pd.DataFrame(data)


df.to_csv('listings.csv', index=False)

print(df)
