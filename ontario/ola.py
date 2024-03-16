import requests
from bs4 import BeautifulSoup
from typing import List

nb_of_parliaments = 43
ola_url: str = 'https://www.ola.org/'
parliament_members = lambda number: f'{ola_url}en/members/parliament-{number}'

def extract_member_urls(parliament_number: int) -> dict:
    response = requests.get(parliament_members(parliament_number))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        members = []

        # Find all rows in the table
        rows = soup.find_all('tr')
        count: int = 0
        for row in rows:
            # Find the anchor tag within each row
            anchor = row.find('a')
            if anchor:
                # Extract the href attribute value
                href_value: str = anchor.get('href')
                # Check if it starts with the desired pattern
                if href_value.startswith('/en/members/all/'):
                    members.append(href_value)
                    count += 1

        # Find the div with class view-header
        div_element = soup.find('div', class_='view-header')
        start_date = None
        end_date = None
        if div_element:
            # Find the time elements within the div
            time_elements = div_element.find_all('time', class_='datetime')
            if len(time_elements) >= 2:
                start_date = time_elements[0]['datetime']
                end_date = time_elements[1]['datetime']
            elif len(time_elements) == 1:
                start_date = time_elements[0]['datetime']
                end_date = ''  # Set end_date to empty string if only one date is found
            else:
                print("Dates not found.")
        else:
            print("Header not found.")

        return {'parliament_number': parliament_number, 'members': members, 'count': count, 'start_date': start_date, 'end_date': end_date}
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)


def get_all_members():
    return [extract_member_urls(parliament_number) for parliament_number in range(1, nb_of_parliaments+1)]


print(extract_member_urls(43))

