import xml.dom.minidom as dom

from pyload.plugins.MultiHoster import MultiHoster


class RealdebridCom(MultiHoster):
    __name__ = "RealdebridCom"
    __version__ = "0.5"
    __type__ = "account"
    __description__ = """Real-Debrid.com account plugin"""
    __author_name__ = ("Devirex, Hazzard")
    __author_mail__ = ("naibaf_11@yahoo.de")

    def loadAccountInfo(self, req):
        page = req.load("http://real-debrid.com/api/account.php")
        xml = dom.parseString(page)
        account_info = {"validuntil": int(xml.getElementsByTagName("expiration")[0].childNodes[0].nodeValue),
                        "trafficleft": -1}

        return account_info

    def login(self, user, data, req):
        page = req.load("https://real-debrid.com/ajax/login.php", get={"user": user, "pass": data["password"]})
        # page = req.load("https://real-debrid.com/login.html",
        #                 post={"user": user, "pass": data["password"]}, cookies=True)

        if "Your login informations are incorrect" in page:
            self.wrongPassword()

    def loadHosterList(self, req):
        page = req.load("http://real-debrid.com/api/hosters.php").replace("\"", "").strip()
        return[x.strip() for x in page.split(",") if x.strip()]
