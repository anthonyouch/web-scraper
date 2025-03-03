from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
base_url = "https://au.gradconnection.com/jobs/?page="

titles = []
orgs = []
closing_dates = []
job_types = []
job_disciplines = []
locations = []


page_number = 1
while True:
    url = base_url + str(page_number)
    print(f"Scraping {url}")

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    boxes = soup.find_all('div', class_ = 'outer-container')
    if not boxes:
        break
    for box in boxes:
        title = box.find('h3').get_text(strip=True)
        org = box.find('p', class_ = 'box-header-para').get_text(strip=True)
        
        closing_date_box = box.find('span', class_ = 'closing-in')
        if closing_date_box:
            closing_date = closing_date_box.get_text(strip=True)
        else:
            closing_date = None
        
        job_type = box.find('p', class_ = 'ellipsis-text-paragraph').get_text(strip=True)

        # find location and job_discipline
       
        # find all ellipsis-text-paragraph divs
        all_ellipsis_divs = box.find_all('div', class_='ellipsis-text-paragraph')

        location_div = None
        discipline_div = None

        # Separate location vs discipline by seeing if "location-name" in class
        for div in all_ellipsis_divs:
            classes = div.get('class', [])
            if 'location-name' in classes:
                location_div = div
            else:
                discipline_div = div

         # In grad connect when theres only 1 location its in a <p> but if theres more than 1 its in a <div>
        # --- LOCATION LOGIC ---
        if location_div:
            location_list_items = location_div.find_all('li')
            if location_list_items:
                # multiple locations
                location = [li.get_text(strip=True) for li in location_list_items]
        else:
            # check if its a single location
            # single location
            location_item = box.find('p', class_ = 'location-name')
            if location_item:
                location = [location_item.get_text(strip=True)]
            else:
                location = None

         # Disciplines are always in divs even if only 1. 
        # --- DISCIPLINE LOGIC ---
        if discipline_div:
            discipline_list_items = discipline_div.find_all('li')
            if discipline_list_items:
                # multiple disciplines
                discipline = [li.get_text(strip=True) for li in discipline_list_items]
            else:
                # single discipline
                discipline = [discipline_div.get_text(strip=True)]
        else:
            discipline = None

        titles.append(title)
        orgs.append(org)
        closing_dates.append(closing_date)
        job_types.append(job_type)
        job_disciplines.append(discipline)
        locations.append(location)

    page_number += 1
    time.sleep(1)


table = pd.DataFrame({'Title': titles, 'Organisation': orgs, 'Closing Date': closing_dates, 'Job Type': job_types, 'Discipline': job_disciplines, 'Location': locations})

table.to_csv('gradconnection_jobs.csv')



