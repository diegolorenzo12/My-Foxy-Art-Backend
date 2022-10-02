import json
import random
import requests
from model import Model
from flask import Flask, request
m = Model()

app = Flask(__name__)


@app.route('/generateImage', methods=['GET'])
def generate_image():
    searchword = request.args.get('key', '')
    url = "https://images-api.nasa.gov/search?q=" + searchword + "&media_type=image"

    res = requests.get(url)
    response = json.loads(res.text)

    res_art = requests.get("https://openaccess-api.clevelandart.org/api/artworks/")
    response_art = json.loads(res_art.text)
    art_url = str(response_art["data"][random.randint(0, 999)]["images"]["web"]["url"])

    # art_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallpaperset.com%2Fw%2Ffull%2F2%2F2%2F9%2F207342.jpg&f=1&nofb=1&ipt=2fda1fa6e3b7fd801376864f512323acd52519acb2711b81b5fcc18ae8889151&ipo=images"
    if len(response["collection"]["items"]) == 0:
        searchword = "space"
        url = "https://images-api.nasa.gov/search?q=" + searchword + "&media_type=image"
        res = requests.get(url)
        response = json.loads(res.text)

    index = random.randint(0, len(response["collection"]["items"])) - 1
    imagen_url = str(response["collection"]["items"][index]["links"][0]["href"])

    print('Content: {content}'.format(content=imagen_url))
    print('Style: {style}'.format(style=art_url))

    # image = m.generate_image(str(random.randint(0, 999)) + ".jpg",
    #                        "https://images-assets.nasa.gov/image/PIA16667/PIA16667~thumb.jpg",
    #                        str(random.randint(0, 999)) + ".jpg",
    #                        "https://openaccess-cdn.clevelandart.org/1980.79/1980.79_web.jpg")
    image = m.generate_image(str(random.randint(0, 999)) + ".jpg",
                             imagen_url,
                             str(random.randint(0, 999)) + ".jpg",
                             art_url)
    image.show()

    return 'oki'


app.run(debug=True)