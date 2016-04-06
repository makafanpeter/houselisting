import requests
from bs4 import BeautifulSoup
from geocode import geocode
from models import *
import re


def format_address():
    houses = House.query.filter_by(formatted=False).all()
    print("Number of house(s) to process =>", len(houses))
    for house in houses:
        try:
            formatted_address = geocode(house.address)
            if formatted_address:
                house.formattedAddress = formatted_address.get("formatted_address")
                house.latitude = formatted_address.get("lat")
                house.longitude = formatted_address.get("lng")
                house.formatted = True
                db.session.add(house)
                db.session.commit()
        except Exception as e:
            print(e)


def crawl():
    site_url = 'https://www.nigeriapropertycentre.com'
    base_url = "https://www.nigeriapropertycentre.com/for-rent"
    page_number = 0
    page_size = 15
    query_string = "?limitstart={0}"
    offset = 0
    try:
        session = requests.Session()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Cache - Control': 'max-age = 0',
            'Upgrade-Insecure-Requests': '1',
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36'
                          '(KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'Host': 'www.nigeriapropertycentre.com:443'
        }

        response = session.get(url=base_url, headers=headers)
        if response.status_code == requests.codes.ok:
            content = response.text
            soup = BeautifulSoup(content, 'lxml')
            headline_results = soup.find(class_="pagination-results")
            result_count_text = headline_results.text.strip()
            index = result_count_text.find('of')
            result_count = int(re.sub("[^0-9.]*", '', result_count_text[index:]))
            number_of_request = int(result_count / page_size)
            print("Number of Search Result -> ", number_of_request)
            for offset in range(0, number_of_request + 1):
                url = base_url
                if offset != 0:
                    page_number += page_size
                    url += query_string.format(page_number)
                response = session.get(url)
                if response.status_code == requests.codes.ok:
                    content = response.text
                    new_soup = BeautifulSoup(content, 'lxml')
                    property_list = new_soup.find_all('div', class_='property-list')
                    for k, v in enumerate(property_list):
                        title = v.find("div", class_='wp-block-title')
                        title = title.text.strip()
                        link = v.find('a', attrs={'hidefocus': 'true'})
                        link = link.get('href')
                        link = site_url + link
                        price = v.find('span', class_='price')
                        price = price.text.strip()
                        price = re.sub("[^0-9.]*", '', price)
                        if not price:
                            price = 0
                        else:
                            price = float(price)
                        aux = v.find(class_='aux-info')
                        features = [i.text.strip() for i in aux]
                        address = v.find('strong')
                        address = address.text.strip()
                        image_url = v.find('img')
                        image_url = image_url.get('src')
                        house = House.query.filter_by(url=link).first()
                        if not house:
                            house = House(name=title, url=link, address=address, price=price, image_url=image_url)
                            db.session.add(house)
                            db.session.commit()
                            for feature in features:
                                if feature:
                                    f = HouseFeature(name=feature, house_id=house.id)
                                    db.session.add(f)
                                    db.session.commit()
    except Exception as e:
        print(e)


crawl()
