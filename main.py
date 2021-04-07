from lxml import etree
import requests
from pathlib import Path
import tempfile

DB_URL = "http://nswdb.com/xml.php"

def download_db():
    r = requests.get(DB_URL, allow_redirects=True)
    f = open("NSWReleases.xml", "wb")
    f.write(r.content)
    f.close()
    return

def updateDatabase():


    if not Path("./NSWReleases.xml").is_file():
        download_db()
    else :
        tmp = open("tmp.xml", "wb")
        tmp.write(requests.get(DB_URL, allow_redirects=True).content)
        tmp.close()

        tmpTree = etree.parse("./tmp.xml")
        currTree = etree.parse("./NSWReleases.xml")

        lastRelease = int(tmpTree.xpath('.//release[last()]/id')[0].text)
        currentRelease = int(currTree.xpath('.//release[last()]/id')[0].text)

        if lastRelease == currentRelease:
            Path("tmp.xml").unlink()
        else:
            Path("./NSWReleases.xml").unlink()
            Path("tmp.xml").rename("./NSWReleases.xml")

    return



if __name__ == "__main__" :

    updateDatabase()

    root = etree.parse("./NSWReleases.xml")
    for release in root.xpath(".//release[languages='ja' and region='JPN']"):
        print(release.xpath(".//name")[0].text.encode("utf-8").decode("utf-8"))



