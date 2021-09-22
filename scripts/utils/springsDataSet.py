from bs4 import BeautifulSoup
import csv

csv_file = open('datasetSptrings.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['2020x', '2020y', '2010x', '2010y', '2000x', '2000y'])

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True
    
def findIndex(str):
    number = ''
    for s in str:
        if(is_number(s)):
            number += s
        if(s == '-'):
            number += s
        if(s == '.'):
            number += s
    if (len(number) < 4):
        return "error"
    else:
        return number
            
with open("/data/dataset.html", "r") as f:
    
    contents = f.read()
 
    soup = BeautifulSoup(contents, 'lxml')

    list_of_tables = soup.find_all('table')
    
    for table in list_of_tables:
    
        data_table = table.find('table')
        
        try:
            print("placemark")
            dataset = data_table.find_all('tr')
            row = []
            for data in dataset:
                number = str(data.find_all('td')[1:2])
                
                response = findIndex(number)
                if(response != "error"):
                    print(response)
                    row.append(response)
            csv_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
                
        except Exception:
            print("error")

