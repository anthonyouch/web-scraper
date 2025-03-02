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

boxes = soup.find_all('div', class_ = 'outer-container')

for box in boxes:
    title = box.find('h3').text.strip()
    org = box.find('p', class_ = 'box-header-para').text.strip()
    closing_date = box.find('span', class_ = 'closing-in').text.strip()
    job_type = box.find('p', class_ = 'ellipsis-text-paragraph').text.strip()

    
    # job_discipline_tag = box.find('div', class_ = 'ellipsis-text-paragraph')
    # job_discipline = job_discipline_tag.find(text=True, recursive=False).strip()

    titles.append(title)
    orgs.append(org)
    closing_dates.append(closing_date)
    job_types.append(job_type)
    # job_disciplines.append(job_discipline)


table = pd.DataFrame({'Title': titles, 'Organisation': orgs, 'Closing Date': closing_dates, 'Job Type': job_types})

table['Title'] = table['Title'].str[:50]

print(table)


