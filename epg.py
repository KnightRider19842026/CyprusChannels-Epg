import requests
import xml.etree.ElementTree as ET

SOURCE_URL = "https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml"

KEYWORDS = [
    "rik 1",
    "rik1",
    "rik 2",
    "rik2",
    "rik sat",
    "ant1",
    "sigma",
    "omega",
    "alpha"
]

def download_epg():
    r = requests.get(SOURCE_URL, timeout=30)
    with open("full.xml", "wb") as f:
        f.write(r.content)

def match_channel(name):
    name = name.lower()
    return any(k in name for k in KEYWORDS)

def filter_epg():
    tree = ET.parse("full.xml")
    root = tree.getroot()

    new_tv = ET.Element("tv")

    valid_ids = set()

    # channels
    for ch in root.findall("channel"):
        names = [dn.text for dn in ch.findall("display-name") if dn.text]

        if any(match_channel(n) for n in names):
            new_tv.append(ch)
            valid_ids.add(ch.attrib["id"])

    # programmes
    for prog in root.findall("programme"):
        if prog.attrib.get("channel") in valid_ids:
            new_tv.append(prog)

    ET.ElementTree(new_tv).write("epg.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    download_epg()
    filter_epg()
