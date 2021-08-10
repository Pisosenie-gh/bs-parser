import requests
from bs4 import BeautifulSoup
import csv
#Начальный url
url = 'https://zakup.kbtu.kz/zakupki/sposobom-zaprosa-cenovyh-predlozheniy&page=1'



items_url = []
urls = 42

def get_data(url):
    
    #Сбор ссылок
    with open('result.csv', 'a', encoding='utf-8' ) as file:

        writer = csv.writer(file)
        writer.writerow(
            (
                'Название',
                "Организатор",
                'Начало',
                'Окончание',
                'СТАТУС'

            )
            )
    
    for slug in range(1, urls + 1):
        
        newUrl = url.replace('1', str(slug))
        response = requests.get(newUrl)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all("div", class_='card-body')

       


        #Запись новых ссылок в массив
        for item in items:
            item_url = 'https://zakup.kbtu.kz' + item.find('h5', class_='card-title').find('a').get("href")
            items_url.append(item_url)
            
   #Сбор данных
    for item_url in items_url:
        
        response = requests.get(item_url)
        soup = BeautifulSoup(response.text, 'lxml')
        item_data = soup.find("div", class_='content')
        item_name = item_data.find('h4', class_= 'card-title').text
        item_td = item_data.find('tr').find_all_next('td')
        organizer = item_td[1].text
        start = item_td[3].text
        end = item_td[5].text
        status = item_td[7].text
       
        with open('result.csv', 'a', encoding='utf-8' ) as file:

            writer = csv.writer(file)
            writer.writerow(
                (
                item_name,
                organizer,
                start,
                end,
                status

                )
            )
      


get_data(url)


