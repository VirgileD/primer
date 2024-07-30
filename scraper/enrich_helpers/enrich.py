from math import e
import lxml.html as html

def enrich_show(show, html_string):
    # with open("test.html", "w") as f:
    #     f.write(test)
    tree = html.fromstring(html_string)
    show.update({ "rating": None, "duration": None, "rating": -1.0, "release_year": None,
                 "genres": [ "N/A"], "moods": ["N/A"],
                 "starring": ["N/A"], "directors": ["N/A"], "synopsis": "N/A", "included": True })
    
    rating = tree.xpath("//span[@data-automation-id='imdb-rating-badge']/text()")
    if rating:
        show["rating"] = float(rating[0].replace("IMDb ", ""))

    if show["type"] == "Movie":
        duration = tree.xpath("//span[@data-automation-id='runtime-badge']/text()")
    else:
        duration = tree.xpath("//div[@data-testid='episode-metadata']/div[@data-testid='episode-runtime']/text()")
        seasons = tree.xpath("//div[@class='dv-node-dp-seasons']//li")
        if seasons:
            show["seasons"] = len(seasons)
        else:
            show["seasons"] = 1
        episodes = tree.xpath("//div[@class='dv-node-dp-badges']//span[contains(@aria-label, 'episode')]/text()")
        if episodes:
            show["episodes"] = int(episodes[0].split(" ")[0])
    if duration:
        try:
            duration_h_m = duration[0]
            duration_h = 0
            duration_m = 0
            if "h" in duration_h_m:
                duration_h = int(duration_h_m.split("h")[0])
                if "min" in duration_h_m:
                    duration_m = int(duration_h_m.split("h")[1].split("min")[0])
            else:
                duration_m = int(duration_h_m.split("min")[0])
            show["duration"] = duration_h*60 + duration_m
        except:
            show["duration"] = "N/A"

    release_year = tree.xpath("//span[@data-automation-id='release-year-badge']/text()")
    if release_year:
        show["release_year"] = int(release_year[0])

    genres_and_moods = tree.xpath("//div[@data-testid='genresMetadata']")
    if genres_and_moods: # probably useless
        genres = genres_and_moods[0].xpath(".//span[@data-testid='genre-texts']/@aria-label")
        if genres:
            show["genres"] = genres
        moods = genres_and_moods[0].xpath(".//span[@data-testid='mood-texts']/@aria-label")
        if moods:
            show["moods"] = moods

    starring = tree.xpath("//span[contains(text(), 'Starring')]/../../dd")
    if starring:
        show["starring"] = starring[0].text_content().split(", ")
    
    directors = tree.xpath("//span[contains(text(), 'Directors')]/../../dd")
    if directors:
        show["directors"] = directors[0].text_content().split(", ")

    synopsis = tree.xpath("//div[contains(@class, 'dv-dp-node-synopsis')]")
    if synopsis:
        show["synopsis"] = synopsis[0].text_content()

    show["price"] = 0
    included = tree.xpath("//span[contains(text(), 'Watch with Prime')]")
    if included:
        show["included"] = True
    else:
        show["included"] = False
        # find the rent button and crap the price - unfortunately, there is no direct catch.
        # So first find all spans that contain "Rent"
        rent = tree.xpath("//span[contains(text(), 'Rent ')]")
        if rent:
            # and for each span, look if we found a "€" inside
            found = None
            for x in rent:
                if "€" in x.text_content():
                    found = x.text_content().split("€")[1]
                    break
            if found:
                show["price"] = float(found)
            else:
                # go gross, parse the script that is popped up when you click on the "More purchase options" button
                rent = tree.xpath("//script[contains(text(), 'Rent ')]")
                if rent:
                    script = rent[0].text_content()
                    # find the first "Rent" and then the first "€" after that
                    rent_pos = script.find("Rent ")
                    euro_pos = script.find("€", rent_pos)
                    if rent_pos != -1 and euro_pos != -1:
                        # now find the next duble-quote after that
                        dq = script.find('"', euro_pos)
                        show["price"] = float(script[euro_pos+1:dq])

    return show