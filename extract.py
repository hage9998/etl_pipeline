#Libraries used
import requests
from bs4 import BeautifulSoup
import json

def extraction():
    url = "https://www.tripadvisor.com/RestaurantSearch-g303631-a_date.2021__2D__01__2D__13-a_people.2-a_time.20%3A00%3A00-a_zur.2021__5F__01__5F__13-Sao_Paulo_State_of_Sao_Paulo.html#EATERY_LIST_CONTENTS"
    site = requests.get(url) #Get the first page
    soup = BeautifulSoup(site.content, 'html.parser')
    list_of_links = []
    next_page = 30

    for i in range(5): #Scrapping 5 pages
        print('1', i)
        link = []
        restaurants = soup.find_all('div', class_='_1llCuDZj')
        link = ['https://www.tripadvisor.com' + rest.find('a')['href'] for rest in restaurants if rest.get('data-test') != 'SL_list_item']
        list_of_links.extend(link) #Save all links to do the scrapper after
        new_link = ''
        restaurants = soup.find('div', class_='pageNumbers')
        new = restaurants.find_all('a')
        for j in range(len(new)):
            if new[j]['data-offset'] == str(next_page):
                new_link = new[j]['href'] #Get the link to new page
                break
        url = 'https://www.tripadvisor.com' + new_link 
        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        next_page += 30

    data = {}
    data2 = {}
    for i in range(len(list_of_links)): #Iterate over the links list saved before
        url = list_of_links[i]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        site = requests.get(url, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        
        # Get all features needed on the pages
        Details = soup.find_all('div', class_= [['_14zKtJkz'], ['_1XLfiSsv'], ['o3o2Iihq'], ['_2170bBgV']])
        details_list = [det.text.strip() for det in Details]
        Local_Contact = soup.find_all(['span', 'a'], class_= [['_2saB_OSe'], ['href']])
        Local_Contact_list = [loc_con.text.strip() for loc_con in Local_Contact]
        Ratings = soup.find_all('div', class_='_3-W4EexF')
        Rate = soup.find_all('span', class_='r2Cf69qf')
        Reviews = soup.find_all('a', class_='_10Iv7dOs')
        Comments = soup.find_all('p', class_='partial_entry')
        #Save the features in a dict
        try:
            data2 = {
                "Site" + str(i + 1): {
                    "Link": list_of_links[i],
                    "Price": details_list[details_list.index('PRICE RANGE') + 1] if 'PRICE RANGE' in details_list else 'none',
                    "Cuisines": details_list[details_list.index('CUISINES') + 1] if 'CUISINES' in details_list else 'none',
                    "Address": Local_Contact_list[0],
                    "Phone": Local_Contact_list[-1] if (any(map(str.isdigit, Local_Contact_list[-1]))) else 'none',
                    "Rating": Rate[0].text if len(list(Rate)) >= 1 else 'none',
                    "Position1": Ratings[0].text if len(list(Ratings)) >= 1 else 'none',
                    "Position2": Ratings[1].text if len(list(Ratings)) >= 2 else 'none',
                    "Reviews": Reviews[0].text if len(list(Reviews)) >= 1 else 'none'
                }
            }
        except:
            print('Continue')
        data.update(data2)

    with open("extracted_data.json", "w") as write_file:
        json.dump(data, write_file, indent=4) #Create a json file containg all the features fromthe links
    write_file.close()

