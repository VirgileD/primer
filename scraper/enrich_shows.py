from curses import raw
from lxml import html
import requests
import os
from pymongo  import MongoClient
from halo import Halo
from enrich_helpers.enrich import enrich_show
import yaml
import argparse
from utils.logmngt import get_logger

if __name__ == "__main__":
    config = {}
    if 'config.yml' in os.listdir():
        with open("config.yml", "r") as f:
            config = yaml.safe_load(f)
    else:
        print("No config file found")
        exit(1)
    log = get_logger("enrich_shows", cfg=config)

    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--reset_status", action="store_true", help="Reset enriched status")
    args = parser.parse_args()

    spinner = Halo(text='Loading', spinner='dots')
    # set the cookies to enter our session
    # FIXME: use the coolies to setup a session so that "Included with Prime" is set
    # here it doesn't work so we got the un-authenticated page
    # hopefully, there is the "Watch with Prime" that helps
    http_session = requests.Session()
    # with open('cookies.json', 'r') as file:
    #     scookies = json.load(file)
    # for cookie in scookies:
    #     http_session.cookies.set(cookie['name'], cookie['value'])

    client = MongoClient(config['db_uri'])
    shows_db = client.get_default_database("shows")
    enriched_coll = shows_db.enriched
    raw_coll  = shows_db.raw
    if args.reset_status:
        log.info(f"Reseting the enrichment status, all shows will be enriched")
        raw_coll.update_many({}, { "$set": { "enriched": False } } )

    spinner.start()
    shows = list(raw_coll.find({ "enriched":  { "$in": [None, False ] } }))
    idx = 1
    tot = len(shows)
    for show in shows:
        del show['_id']
        if len(show['title']) > 47:
            formatted_title = "'" + show['title'][0:47] + "...'"
        else:
            formatted_title = "{: <52}".format("'" + show['title'] + "'" )

        spinner.text = f"Enrich {formatted_title} ({tot - idx})"
        idx += 1
        html_string = http_session.get(show["url"]).text

        try:
            show = enrich_show(show, html_string)
        except Exception as e:
            spinner.stop()
            log.error(f"Failed to enrich {show['title']} - {show['url']}: {e}")
            spinner.start()
            continue
        raw_coll.update_one({ "id": show["id"] }, { "$set": { "enriched": True } })
        enriched_coll.update_one({ "id": show["id"] }, { "$set": { **show, "enriched": True } }, upsert=True)
    spinner.stop()
    
#https://understandingdata.com/posts/how-to-easily-resize-compress-your-images-in-python/

# res = requests.get(url)
#     if res == 200 and 'jpeg' in res.headers['content-type']:
#         img_arr = np.array(Image.open(BytesIO(res.content)))
#         return img_arr

# image_file = StringIO(open("test.jpg",'rb').read())

# and then send it to Binary(image_file) type in pymongo

# Binary_image_file = Binary(image_file) #pymongo libary

# Then do a normal insert in mongo.

# To read. do a normal find(). Then load the value from key and convert the data stored to image as:

# image_data = StringIO.StringIO(Stringio_image_file)
# image = Image.open(image_data)
