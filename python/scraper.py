from data.user import UserPreview
from view.console import print_warning, print_info
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests, re, time, random

def search_profiles(search, session, debug=False):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    url = search.get_main_url()
    if debug: print_info(f"Reaching: {url}")
    response_main = session.get(url, headers=headers)
    
    soup = BeautifulSoup(response_main.text, "html.parser")

    div = soup.find('div', class_='resultC2')
    if div:
        children = div.find_all(recursive=False)
        if len(children) == 2 and children[0].name == 'link' and children[1].name == 'h1':
            print_warning("No results")
            return False

    if response_main.status_code == 403:
        print_warning("Only Swedish IPs allowed")
        return False
    
    #time.sleep(15)
    return load_next_page(session, 1, 0, debug=debug)

def load_profile(search=None):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    session = requests.Session()
    response = session.get(search.get_user_url(), headers=headers)

    if response.status_code == 403:
        print_warning("Only Swedish IPs allowed")
        return False
    
def load_next_page(session, index, tries, max=3, debug=False):
    results = []

    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    if debug: print_info(f"Loading index [{index}] attempt [{tries}]")
    url = f"https://mrkoll.se/loadResult/?p={index}"
    if debug: print_info(f"Reaching: {url}")
    response_page = session.get(url, headers=headers)
    
    if response_page.status_code == 403:
        print_warning("Only Swedish IPs allowed")
        return False

    if response_page.url == "https://mrkoll.se/":
        print_warning("No people found, use a broader search term")
        return False

    response_page.encoding = "utf-8"

    if response_page.text.strip() == '<p class=maxLoad>Hela sökresultatet visas nu</p>':
        tries += 1
        if tries == max:
            if debug: print_warning("Failed, attempt limit reached")
            print_warning("No results > Refine search | Wait a bit | No more pages")
            return False
        delay = random.uniform(2, 10)
        if debug: print_info(f"Failed, retrying in {delay} seconds")
        time.sleep(delay)
        return load_next_page(session, index, tries, max)
    
    soup = BeautifulSoup(response_page.text, "html.parser")
    people = soup.find_all('a')

    for person in people:
        full_name = person.find('span', class_='namnSpan').get_text(strip=True) + person.find_all("strong")[1].get_text(strip=True)
        full_name = re.sub(r"([a-zA-ZåäöÅÄÖ])([A-ZÅÄÖ])", r"\1 \2", full_name)
        age_spanM = person.find("span", class_="distance spanKille")

        age = ""
        gender = "Man"
        if age_spanM:
            age = age_spanM.getText(strip=True).split(" ")[0]
        else:
            gender = "Woman"
            age = person.find("span", class_="distance spanTjej").getText(strip=True).split(" ")[0]

        address_span = person.find("span", class_="stText")
        address = "N/A"
        zip = "N/A"
        city = "N/A"
        lived_here = "N/A"

        if address_span.getText(strip=True):
            full_address = address_span.decode_contents().split("<br/>")
            zip_city = full_address[1].split("\xa0")
            zip = zip_city[0]
            city = zip_city[1]
            address = full_address[0]

            content_div = person.find("div", class_="resBlockContent_result")
            if content_div:
                info_span = person.find("div", class_="resBlockContent_result").find("span", class_=re.compile(r"infoSpan"))
                if info_span:
                    lived_here = info_span.get_text(strip=True)[-4:]
                    if not lived_here.isdigit(): lived_here = "N/A"

        birthday = person.find("span", class_="persnr").get_text(strip=True)[:8]
        birthday = birthday[:4] + '/' + birthday[4:6] + '/' + birthday[6:8]
        id = person['href'].split('/')[-1]
        results.append(UserPreview(full_name, age, address, zip, city, birthday, lived_here, gender, id))
    return results