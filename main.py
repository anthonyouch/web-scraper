from bs4 import BeautifulSoup
import requests
import pandas as pd
url = "https://au.gradconnection.com/internships/computer-science/australia/"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')

title = []

for a_tag in soup.find_all('a', {'class': 'box-header-title'}):
    for h3 in a_tag.find_all('h3'):
        title.append(h3.text)

orgs = soup.find_all('p', {'class': 'box-header-para'})

orgs_list = []
for org in orgs:
    orgs_list.append(org.text)


closing_dates = soup.find_all('span', {'class': 'closing-in'})

date_list = []
for date in closing_dates:
    date_list.append(date.text)

table = pd.DataFrame({'Title': title, 'Organisation': orgs_list, 'Closing Date': closing_dates})

# display only first 50 characters of title for now
table['Title'] = table['Title'].str[:50]

print(table)



