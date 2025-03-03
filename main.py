from bs4 import BeautifulSoup
import requests
import pandas as pd
url = "https://au.gradconnection.com/jobs/?page=1"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')

titles = []
orgs = []
closing_dates = []
job_types = []
job_disciplines = []
locations = []

boxes = soup.find_all('div', class_ = 'outer-container')

for box in boxes:
    title = box.find('h3').get_text(strip=True)
    org = box.find('p', class_ = 'box-header-para').get_text(strip=True)
    closing_date = box.find('span', class_ = 'closing-in').get_text(strip=True)
    job_type = box.find('p', class_ = 'ellipsis-text-paragraph').get_text(strip=True)

    # find location and job_discipline,
    # in grad connect when theres only 1 location its in a <p> but if theres more than 1 its in a <div>
    # but disciplines are always in divs even if only 1. 
    paragraphs = box.find_all('div', class_='ellipsis-text-paragraph')
    if len(paragraphs) == 2:
        location_list_items = paragraphs[0].find_all('li')
        location = [li.get_text(strip=True) for li in location_list_items]

    elif len(paragraphs) == 1:
        # this means only 1 location 

        location = [box.find('p', class_ = 'location-name').get_text(strip=True)]
        
    else:
        print("This shouldn't happen!")
    
    #discipline always in last paragraph
    # For now just get the main discipline, not the ones in the span
    #if its generalist, its in a span 
    generalist_span = paragraphs[-1].find('span', class_ = 'generalist')
    if generalist_span:
        discipline = generalist_span.get_text(strip=True)
    else:
        discipline = paragraphs[-1].find(text=True, recursive=False).strip()

    titles.append(title)
    orgs.append(org)
    closing_dates.append(closing_date)
    job_types.append(job_type)
    job_disciplines.append(discipline)
    locations.append(location)


table = pd.DataFrame({'Title': titles, 'Organisation': orgs, 'Closing Date': closing_dates, 'Job Type': job_types, 'Discipline': job_disciplines, 'Location': locations})

table['Title'] = table['Title'].str[:50]

print(table['Location'])


