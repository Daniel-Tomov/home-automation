import _csv as csv
array = []
num = ''

with open('values.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
        array = array + row
        print(array)
        
   