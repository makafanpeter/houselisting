import requests
import os
API_KEY = os.environ['API_KEY']


def geocode(address):
    url = ("http://maps.googleapis.com/maps/api/geocode/json?"
           "sensor=false&address={0}".format(address.replace(" ", "+")))
    try:
        r = requests.get(url=url)
        r.raise_for_status()
        if requests.codes.ok == r.status_code:
            response = r.json()
            if response.get("status") == u"OK":
                results = response.get("results")[0]
                new_address = dict(formatted_address=results["formatted_address"],
                                   lat=results["geometry"]["location"]["lat"],
                                   lng=results["geometry"]["location"]["lng"])
                return new_address
    except Exception as e:
        print (e)
    return None


def get_services_nearby(latitude, longitude, service_type, radius=1000):
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        "location={0},{1}&radius={2}&type={3}&key={4}".format(latitude, longitude, radius, service_type, API_KEY))
    try:
        r = requests.get(url=url)
        r.raise_for_status()
        if requests.codes.ok == r.status_code:
            response = r.json()
            if response.get("status") == u"OK":
                results = response.get("results")
                services = [{'name': result["name"], 'address': result["vicinity"],
                             'latitude': result["geometry"]["location"]["lat"],
                             'longitude': result["geometry"]["location"]["lng"]}
                            for result in results]
                return services
    except Exception as e:
        print (e)
    return None


