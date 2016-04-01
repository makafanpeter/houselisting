import requests


def geocode(address):
    url = ("http://maps.googleapis.com/maps/api/geocode/json?"
           "sensor=false&address={0}".format(address.replace(" ", "+")))
    try:
        r = requests.get(url=url)
        r.raise_for_status()
        if requests.codes.ok == r.status_code:
            response = r.json()
            if response["status"] == u"OK":
                results = response.get("results")[0]
                new_address = dict(formatted_address=results["formatted_address"],
                                   lat=results["geometry"]["location"]["lat"],
                                   lng=results["geometry"]["location"]["lng"])
                return new_address
        return None
    except Exception as e:
        print e
