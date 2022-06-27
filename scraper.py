from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("project\chromedriver_win32\chromedriver.exe")
browser.get(START_URL)
time.sleep(10)

headers = ["Name","Distance","Mass","Radius"]

def scrape():
    
    star_data = []
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for tr_tag in soup.find_all("tr", attrs={"class", "exoplanet"}):
            th_tags = tr_tag.find_all("th")
            temp_list = []
            for index, th_tag in enumerate(th_tags):
                if index == 0:
                    temp_list.append(th_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(th_tag.contents[0])
                    except:
                        temp_list.append("")
            star_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(star_data)
scrape()


new_data = []

def scrape_more(hyperlink):
    try:
        page = requests.get(hyperlink)

        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in td_tags:
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        
        new_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more(hyperlink)

for index, data in enumerate():
    scrape_more(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_data[0:10])

final_planet_data = []

for index, data in enumerate(data):
    new_planet_data_element = new_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)

with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)

