import csv
import requests
from bs4 import BeautifulSoup

url = input("Insert URL: ")

res = requests.get(url)

PagingString = "?PageIndex="

soup = BeautifulSoup(res.content, 'html.parser')
set_title = soup.head.title.string
set_title = set_title.split(" |")[0]
set_title = set_title.replace(" ", "_") + ".csv"
print("Now Generating: ", set_title)

# Find How many pages

raw_pages = soup.find(
    "ul", {'class': 'pagination justify-content-center flex-wrap'})
pages = len(raw_pages.find_all('a')) - 2
print(f"Number of Pages: {pages}")

page_count = 1

player_list = []
for page in range(1, pages + 1):
    current_page = url + PagingString + str(page_count)
    # print(current_page)
    page_count += 1

    res = requests.get(current_page)
    soup = BeautifulSoup(res.content, 'html.parser')

    # Table Parsing
    table = soup.find_all('table')

    rows = table[4].find_all("tr")
    test = rows[0].find_all("td")
    a = 0

    player_row = []
    for z in rows:
        # for x in test:
        # if(str(x).__contains__("/ViewCard.cfm")):
        data = z.find_all("a")
        for y in data:
            if len(y) == 1:
                player_row.append(y.string)
        player_list.append(player_row)
        player_row = []


for j in player_list:
    # TODO - Fix this, it gives an out-of-bounds error
    if len(j) < 3:
        j[0] = [j[0], " ", " "]
    for i in j:
        print(i, end=",")
    print("")

with open(set_title, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Number', 'Player', 'Team'])

    for card in player_list:
        writer.writerow([card[0], card[1], card[2]])
