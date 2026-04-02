import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

CHANNELS = {
    "rik1.cy": "RIK 1",
    "rik2.cy": "RIK 2",
    "riksat.cy": "RIK SAT",
    "ant1.cy": "ANT1 Cyprus",
    "sigma.cy": "SIGMA",
    "omega.cy": "OMEGA",
    "alpha.cy": "ALPHA Cyprus"
}

def generate_programmes():
    programmes = []
    now = datetime.now()

    for cid in CHANNELS:
        for d in range(3):
            date = now + timedelta(days=d)

            slots = [
                ("06:00", "09:00", "Morning Show"),
                ("09:00", "12:00", "Entertainment"),
                ("12:00", "14:00", "News"),
                ("14:00", "18:00", "Series"),
                ("20:00", "21:00", "Main News"),
                ("21:00", "23:00", "Prime Time")
            ]

            for start, stop, title in slots:
                start_dt = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {start}", "%Y-%m-%d %H:%M")
                stop_dt = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {stop}", "%Y-%m-%d %H:%M")
                programmes.append({
                    "channel": cid,
                    "start": start_dt.strftime("%Y%m%d%H%M%S +0300"),
                    "stop": stop_dt.strftime("%Y%m%d%H%M%S +0300"),
                    "title": title
                })
    return programmes

def build_xml():
    tv = ET.Element("tv")

    for cid, name in CHANNELS.items():
        ch = ET.SubElement(tv, "channel", id=cid)
        dn = ET.SubElement(ch, "display-name")
        dn.text = name

    for p in generate_programmes():
        prog = ET.SubElement(tv, "programme", {
            "channel": p["channel"],
            "start": p["start"],
            "stop": p["stop"]
        })
        title = ET.SubElement(prog, "title")
        title.text = p["title"]

    ET.ElementTree(tv).write("epg.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    build_xml()
