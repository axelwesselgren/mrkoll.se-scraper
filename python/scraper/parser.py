import re

NAME_REGEX = r"([a-zA-ZåäöÅÄÖ])([A-ZÅÄÖ])"

class Parser:
    def __init__(self, person):
        self.person = person

    def get_name(self) -> str:
        full_name = (
            self.person.find('span', class_='namnSpan').get_text(strip=True) +
            self.person.find_all("strong")[1].get_text(strip=True)
        )
        return re.sub(NAME_REGEX, r"\1 \2", full_name)

    def get_age(self) -> str:
        age_span = self.person.find("span", class_="distance spanKille")
        if age_span:
            return age_span.getText(strip=True).split(" ")[0]
        return self.person.find("span", class_="distance spanTjej").getText(strip=True).split(" ")[0]

    def get_gender(self) -> str:
        if self.person.find("span", class_="distance spanKille"):
            return "Man"
        return "Woman"

    def get_birthday(self) -> str:
        birthday = self.person.find("span", class_="persnr").get_text(strip=True)[:8]
        return f"{birthday[:4]}/{birthday[4:6]}/{birthday[6:8]}"

    def get_pid(self) -> str:
        return self.person['href'].split('/')[-1]

    def get_address(self) -> str:
        address_span = self.person.find("span", class_="stText")
        if address_span:
            return address_span.decode_contents().split("<br/>")[0]
        return "N/A"

    def get_address_details(self) -> tuple:
        address_span = self.person.find("span", class_="stText")
        address = zip_code = city = lived_here = "N/A"

        if address_span and address_span.getText(strip=True):
            address, zip_code, city = self._extract_address_details(address_span)
            lived_here = self._get_time_lived_here()
        
        return address, zip_code, city, lived_here

    def _get_time_lived_here(self) -> str:
        content_div = self.person.find("div", class_="resBlockContent_result")
        if content_div:
            info_span = content_div.find("span", class_=re.compile(r"infoSpan"))
            if info_span:
                lived_here = info_span.get_text(strip=True)[-4:]
                if lived_here.isdigit():
                    return lived_here
        return "N/A"

    def _extract_address_details(self, address_span) -> tuple:
        full_address = address_span.decode_contents().split("<br/>")
        zip_code, city = full_address[1].split("\xa0")
        address = full_address[0]
        return address, zip_code, city
