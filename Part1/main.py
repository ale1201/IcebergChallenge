# Imports.
import requests
from bs4 import BeautifulSoup
import time
import csv

#CONSTANTS
BASE_URL = 'https://www.tripadvisor.com/Hotels-g294074-Bogota-Hotels.html'
HEADERS = {
        'authority': 'www.tripadvisor.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'es-ES,es;q=0.9',
        'referer': 'https://www.tripadvisor.com/',
        'sec-ch-ua': '"Opera GX";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0',
    }

def web_scrapping(file:str) -> None:
    '''
    Writes a CSV file with the information of the hotels of tripadvisor for the city of Bogota.
    This function prints each hotel in order to inform the user which hotel number the program is scraping.
        Parameters:
            file (str): Name of the CSV file
    '''
    with open(file, 'w', newline='') as file:
        writer = csv.writer(file)
        #Headers to identify each column in the CSV file
        data = ['Hotel name','Hotel id','Hotel url_tripadvisor','Address', 'phone', 'Coded hotel link', 'Has email', 'Calification (/50)', 'ranking', 'specific calification', 'time stamp']
        writer.writerow(data)

        counter = 0
        while(True):
            if counter!=0:
                r = requests.get(f'https://www.tripadvisor.com/Hotels-g294074-oa{str(counter)}-Bogota-Hotels.html', headers=HEADERS)
            else:
                r = requests.get(BASE_URL, headers=HEADERS)
            # Only when the request start over from the first page og the hotels list, the while is going to end
            if counter!=0 and r.url == BASE_URL:
                break

            soup = BeautifulSoup(r.content, 'html.parser')
            # Retrieves all the info of the hotels for each page
            list_hotels = soup.find_all('div', attrs={'class': 'prw_rup prw_meta_hsx_listing_name listing-title'})
            for elem in list_hotels:
                # Filter to avoid the sponsored hotels
                if elem.find('span', attrs={'class': 'ui_merchandising_pill sponsored_v2'}) is None:
                    hotel_info = elem.find('a')
                    property_id = hotel_info['id']
                    link_hotel_company = hotel_info['href']
                    hotel_name = hotel_info.text.strip()

                    # Request to get the detail for each hotel
                    res_detail_hotel = requests.get('https://www.tripadvisor.com'+link_hotel_company, headers=HEADERS)
                    soup = BeautifulSoup(res_detail_hotel.content, 'html.parser')

                    # Retrieves the tags where the address is shown
                    find_address = soup.find('span', attrs={'class': 'fHvkI PTrfg'})
                    address = None if find_address is None else find_address.text
                    # Retrieves the tags where a possible phone is shown
                    find_phone = soup.find('span', attrs={'class': 'zNXea NXOxh NjUDn'})
                    phone = None if find_phone is None else find_phone.text
                    # Retrieves the tags where a possible url is shown
                    find_url = soup.find('div', attrs={'data-blcontact': 'URL_HOTEL '})
                    url = None if find_url is None else find_url.find('a')['data-encoded-url']
                    # Retrieves the tags where a possible email is shown
                    find_email = soup.find('div', attrs={'data-blcontact': 'EMAIL '})
                    email = 'No' if find_email is None else 'Yes'
                    # Retrieves the tags where a possible info review is shown
                    find_info_ranking = soup.find('div', attrs={'class': 'Jktgk Mc'})
                    calification=None
                    ranking = None
                    if find_info_ranking is not None:
                        calification = None if find_info_ranking.find('span') is None else find_info_ranking.find('span')['class'][1][-2:]
                        ranking = None if find_info_ranking.find('div') is None else find_info_ranking.find('div').text
                    # Retrieves the tags where a possible detail of review is shown
                    find_specific_calification = soup.find_all('div', attrs={'class': 'WdWxQ'})
                    specific_calification = {}
                    for elem in find_specific_calification:
                        specific_calification[elem.text[:-3]] = elem.text[-3:]
                    ts = time.time()

                    line = [hotel_name, property_id.split('_')[1], 'https://www.tripadvisor.com'+link_hotel_company, address, phone, url, email, str(calification), ranking, specific_calification, ts]
                    writer.writerow(line)
                    print(hotel_name)
            counter+=30

#Uncomment this line to execute the code above
web_scrapping('Part1/data.csv')