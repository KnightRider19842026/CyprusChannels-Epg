from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import xml.etree.ElementTree as ET
import time

driver = webdriver.Chrome()

driver.get("https://www.rik.cy/el/tv-programma")
time.sleep(5)

programs = driver.find_elements(By.CLASS_NAME, "schedule-item")

tv = ET.Element("tv")

# Channels
for ch in ["RIK1", "RIK2"]:
    c = ET.SubElement(tv, "channel", id=ch)
    ET.SubElement(c, "display-name").text = ch

for p in programs:
    try:
        time_text = p.find_element(By.CLASS_NAME, "time").text
        title = p.find_element(By.CLASS_NAME, "title").text

        start = datetime.now().strftime("%Y%m%d") + time_text.replace(":", "") + "00 +0300"

        prog = ET.SubElement(tv, "programme", channel="RIK1", start=start, stop=start)
        ET.SubElement(prog, "title").text = title

    except:
        pass

driver.quit()

tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
