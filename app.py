import json
import requests

places = ["quán bia", "quán nhậu", "quán bar", "nhà hàng"]
radius = 2000
lat, lng = 21.012985, 105.821839
api = ""
N = 50


def get_data(place):
    r = requests.get(
        "https://discover.search.hereapi.com/v1/"
        + "discover"
        + "?in=circle:{},{};r={}".format(lat, lng, radius)
        + "&q={}".format(place)
        + "&apiKey={}".format(api)
    )

    return r.json()


def get_50_places(N, place):
    result = []

    for p in place:
        data = get_data(p)
        result.extend(data["items"])

    return result[:N]


def location(N, place):
    geoMap = {"type": "FeatureCollection", "features": []}

    for data in get_50_places(N, place):
        la = data["position"]["lat"]
        lo = data["position"]["lng"]
        add = data["address"]["label"]
        name = data["title"]
        info = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lo, la]},
            "properties": {"Address": add, "name": name},
        }
        geoMap["features"].append(info)

    return geoMap


def solve(N, place):
    data = location(N, place)

    with open("pymi_beer.geojson", "wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    n = N
    place = places
    solve(n, place)


if __name__ == "__main__":
    main()
