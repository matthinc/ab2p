#!/usr/bin/env python3
import requests
import xmltodict
import time

time.sleep(5)

# Test Audiobook1 XML
ab1 = xmltodict.parse(requests.get("http://ab2p:3000/Audiobook1.xml").content)

assert ab1["rss"]["channel"]["title"] == "Audiobook1"

assert ab1["rss"]["channel"]["item"][0]["title"] == "1.mp3"
assert ab1["rss"]["channel"]["item"][0]["enclosure"]["@url"] == "http://ab2p:3000/Audiobook1/1.mp3"

assert ab1["rss"]["channel"]["item"][1]["title"] == "2.mp3"
assert ab1["rss"]["channel"]["item"][1]["enclosure"]["@url"] == "http://ab2p:3000/Audiobook1/2.mp3"

# Test Audiobook1 Episode
response = requests.get(ab1["rss"]["channel"]["item"][1]["enclosure"]["@url"])
assert response.status_code == 200

# Test Audiobook2 XML
ab2 = xmltodict.parse(requests.get("http://ab2p:3000/Audiobook2.xml").content)

assert ab2["rss"]["channel"]["title"] == "Audiobook2"

assert ab2["rss"]["channel"]["item"][0]["title"] == "2.mp3" 
assert ab2["rss"]["channel"]["item"][1]["title"] == "10.mp3" 

# Test Audiobook2 Episode
response = requests.get(ab2["rss"]["channel"]["item"][1]["enclosure"]["@url"])
assert response.status_code == 200