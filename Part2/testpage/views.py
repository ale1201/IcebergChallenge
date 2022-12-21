from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://www.tripadvisor.com'
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

def get_correct_url(city, counter):
    if city.lower() == 'medellin':
        return f'{BASE_URL}/Hotels-g297478-oa{str(counter)}-Medellin_Antioquia_Department-Hotels.html'
    if city.lower() == 'bogota':
        return f'{BASE_URL}/Hotels-g294074-oa{str(counter)}-Bogota-Hotels.html'

def testcase(request, city):
    result = {'data': []}
    counter = 0
    url = 'https://www.tripadvisor.co/Search?q=medellin&ssrc=h'
    r = requests.get(url, headers=HEADERS)
    url_with_session_id = r.url
    while (counter <= 40):
        r = requests.get(get_correct_url(city, counter), headers=HEADERS)

        soup = BeautifulSoup(r.content, 'html.parser')
        list_hotels = soup.find_all('div', attrs={'class': 'prw_rup prw_meta_hsx_listing_name listing-title'})
        for elem in list_hotels:
            if elem.find('span', attrs={'class': 'ui_merchandising_pill sponsored_v2'}) is None:
                hotel_info = elem.find('a')
                property_id = hotel_info['id']
                link_hotel_company = hotel_info['href']
                hotel_name = hotel_info.text.strip()

                res_detail_hotel = requests.get(BASE_URL + link_hotel_company, headers=HEADERS)
                soup = BeautifulSoup(res_detail_hotel.content, 'html.parser')
                find_address = soup.find('span', attrs={'class': 'fHvkI PTrfg'})
                address = None if find_address is None else find_address.text
                find_phone = soup.find('span', attrs={'class': 'zNXea NXOxh NjUDn'})
                phone = None if find_phone is None else find_phone.text
                find_url = soup.find('div', attrs={'data-blcontact': 'URL_HOTEL '})
                url = None if find_url is None else find_url.find('a')['data-encoded-url']
                find_email = soup.find('div', attrs={'data-blcontact': 'EMAIL '})
                email = 'No' if find_email is None else 'Yes'
                find_info_ranking = soup.find('div', attrs={'class': 'Jktgk Mc'})
                calification = None
                ranking = None
                if find_info_ranking is not None:
                    calification = None if find_info_ranking.find('span') is None else \
                    find_info_ranking.find('span')['class'][1][-2:]
                    ranking = None if find_info_ranking.find('div') is None else find_info_ranking.find('div').text
                find_specific_calification = soup.find_all('div', attrs={'class': 'WdWxQ'})
                specific_calification = {}
                for elem in find_specific_calification:
                    specific_calification[elem.text[:-3]] = elem.text[-3:]
                ts = time.time()

                total_hotel_info = {'hotel_name': hotel_name,
                                'hotel_id': property_id,
                                'hotel_url_tripadvisor': BASE_URL+link_hotel_company,
                                'address': address,
                                'phone': phone,
                                'coded_hotel_link': url,
                                'has_email': email,
                                'calification(/50)': str(calification),
                                'ranking':ranking,
                                'specific_calification':specific_calification,
                                'time_stamp':ts}
                result['data'].append(total_hotel_info)
                print(hotel_name)
        counter += 30

    return JsonResponse(result)