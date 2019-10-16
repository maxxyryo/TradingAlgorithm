import requests
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

url = "https://www.investing.com/technical/technical-summary"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36','Accept': 'application/json, text/javascript, */*; q=0.01'}
response = requests.get(url, headers = headers)
print ("Getting url...")

if response.status_code == 200:
	print("HTML webpage loaded successfully.\n")
else:
	print("Error. HTML webpage not loaded.\n")
soup = bs(response.content, 'html.parser')
table = soup.find('table', {'class':'genTbl closedTbl technicalSummaryTbl noHover'})

text, assetType, allColumns, groupedColumns = [], [], [], []
for header in table.find_all('th'):
	text.append(header.get_text())

for asset in table.find_all('a'):
        assetType.append(asset.get_text())

n = 5
for row in table.find_all('tr', {'data-row-type':"summary"}):
        for ele in row.find_all('td'):
                counter = 0
                allColumns.append(ele.get_text())
groupColumns = [allColumns[k:k+n] for k in range(0, len(allColumns), n)]
print(groupColumns[0][1])

x = PrettyTable()
x.field_names, x.padding_width = text, 1
zeroth, first, second, third, fourth = groupColumns[0], groupColumns[1], groupColumns[2], groupColumns[3], groupColumns[4]
x.add_row([assetType[0], zeroth[0], zeroth[1], zeroth[2], zeroth[3], zeroth[4]])
x.add_row([assetType[1], first[0], first[1], first[2], first[3], first[4]])
x.add_row([assetType[2], second[0], second[1], second[2], second[3], second[4]])
x.add_row([assetType[3], third[0], third[1], third[2], third[3], third[4]])
x.add_row([assetType[4], fourth[0], fourth[1], fourth[2], fourth[3], fourth[4]])
print(x)

