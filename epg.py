import requests
import xml.etree.ElementTree as ET

SOURCE_URL = "https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml"

CHANNEL_IDS = {
    "rik1.cy",
    "rik2.cy",
    "riksat.cy",
    "ant1.cy",
    "sigma.cy",
    "omega.cy",
    "alpha.cy"
}

def download_epg():
    r = requests.get(SOURCE_URL, timeout=30)
    with open("full.xml", "wb") as f:
        f.write(r.content)

def filter_epg():
    tree = ET.parse("full.xml")
    root = tree.getroot()

    new_tv = ET.Element("tv")

    # channels
    for ch in root.findall("channel"):
        if ch.attrib.get("id") in CHANNEL_IDS:
            new_tv.append(ch)

    # programmes
    for prog in root.findall("programme"):
        if prog.attrib.get("channel") in CHANNEL_IDS:
            new_tv.append(prog)

    ET.ElementTree(new_tv).write("epg.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    download_epg()
    filter_epg()
