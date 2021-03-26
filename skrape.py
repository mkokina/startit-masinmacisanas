import requests
from bs4 import BeautifulSoup as bs
import csv
import time


URL = 'https://www.ss.lv/lv/transport/cars/today-5/sell/'
LAPAS = 'lapas/'
DATI = 'dati/'


def saglaba (url, datne):
    rezultats = requests.get(url)
    if rezultats.status_code == 200:
        with open(datne, 'w', encoding='UTF-8') as f:
            f.write(rezultats.text)

# saglaba(URL, LAPAS + "pirma_lapa.html")


def info(datne):
    dati = []
    with open(datne, 'r', encoding='UTF-8') as f:
        html = f.read()

    zupa = bs(html, "html.parser")
    galvena = zupa.find(id = 'page_main')
    tabulas = galvena.find_all("table")
    auto_tabula = tabulas[2]
    rindas = auto_tabula.find_all("tr")

    for rinda in rindas[1:-1]:
        lauki = rinda.find_all("td")

        auto = {}

        auto["saite"] = lauki[1].find("a")["href"]
        auto["bilde"] = lauki[1].find("img")["src"]
        auto["apraksts"] = lauki[2].find("a").text.replace("\n", " ")
        if lauki[3].br:
            lauki[3].br.replace_with('!')

            auto["marka"] = lauki[3].text.replace("!", " ")
            auto["razotajs"] = lauki[3].text.split("!")[0]
            auto["modelis"] = lauki[3].text.split("!")[1]
        else: 
            auto["marka"] = lauki[3].text
            auto["razotajs"] = lauki[3].text
            auto["modelis"] = lauki[3].text

        auto["gads"] = lauki[4].text

        tilpums = lauki[5].text
        if tilpums[-1] == "D":
            auto["dzinejs"] = "Dīzelis"
            auto["tilpums"] = tilpums[:-1]
        elif tilpums[-1] == "H":
            auto["dzinejs"] = "Hibrīds"
            auto["tilpums"] = tilpums[:-1]
        elif tilpums[-1] == "E":
            auto["dzinejs"] = "Elektro"
            auto["tilpums"] = 0
        else:
            auto["dzinejs"] = "Benzīns"
            auto["tilpums"] = tilpums

        if not lauki[6].text == '-':
            auto["nobraukums"] =  lauki[6].text.replace(" tūkst.", "")
        else:
            continue
# apstrādāt nobraukumus, kur "-"

        auto["cena"] = lauki[7].text.replace("  €", "").replace(",","")

        # print(auto)
        # print("============================")

        dati.append(auto)

    return dati



def saglaba_datus(dati):
    with open(DATI + 'ss_auto.csv', 'w', encoding='utf-8', newline="") as f:
        kolonnu_nosaukumi = ['razotajs', 'modelis', 'marka', 'gads', 'dzinejs', 'tilpums', 'nobraukums', 'cena', 'apraksts', 'bilde', 'saite']
        w = csv.DictWriter(f, fieldnames = kolonnu_nosaukumi)
        w.writeheader()
        for auto in dati:
            w.writerow(auto)

def atvelkam_lapas(cik):
    # pirma_lapa = "{}page1.html".format(LAPAS)
    # saglaba(URL, pirma_lapa)
    for i in range(1, cik+1):
        url = "{}page{}.html".format(URL,i)
        datne ="{}page{}.html".format(LAPAS, i)
        saglaba(url,datne)
        time.sleep(1)

# atvelkam_lapas(5)

# d3 = info(LAPAS+"page3.html")
# print(d3)
# saglaba_datus(d1)


def izvelkam_datus(cik):
    visi_dati = []
    for i in range (1, cik+1):
        datne ="{}page{}.html".format(LAPAS, i)

        datnes_dati = info(datne)
        visi_dati += datnes_dati

    saglaba_datus(visi_dati)

izvelkam_datus(5)
