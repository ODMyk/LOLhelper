from bs4 import BeautifulSoup
from config import *
import requests


class RequestError(Exception):
    pass

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, features="html.parser")
    else:
        raise RequestError(f"Status code of request is {response.status_code}")

def get_champ_info(champion):
    results = []

    soup = get_soup(url_template.format(champion))
    divs = soup.find_all("div", {"class": "m-1lhmkt7 e1pfij5r6"})[:3]
    for div in divs:
        info = div.find("div", {"class": "m-dme03i ez6mgdl1"}).text
        if info != "Best Synergy (DUO)":
            results.append((x.text for x in div.find_all("p", {"class": "m-1o4xe3x"})))
        else:
            names = (x.text for x in div.find_all("p", {"class": "m-1o4xe3x"}))
            roles_divs = div.find_all("div", {"class": "m-16kzrcn"})
            roles = (x.find("img", {"class": "m-0"})["alt"] for x in roles_divs)
            results.append((f"{name}({role})" for name, role in zip(names, roles)))

    return results

def sort_info(weak, strong, synergy):
    return (", ".join(x) for x in (weak, strong, synergy))

def display_info(weak, strong, synergy):
    print(display_template.format(weak, strong, synergy))

while True:
    champion = input("Champion >> ").lower()
    if champion == "exit":
        break
    temp_var = problematic_champions.get(champion, None)
    if temp_var:
        champion = temp_var
    if champion in champions:
        weak, strong, synergy = sort_info(*get_champ_info(champion.replace(" ", "")))
        display_info(weak, strong, synergy)
    else:
        print("Incorrect input. Please try again.")
