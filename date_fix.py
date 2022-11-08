import json
import re
  
def get_month(x):
    month = 0
    
    if (x  == 'Jan'):
        month = 1

    if (x  == 'Feb'):
        month = 2

    if (x  == 'Mar'):
        month = 3

    if (x  == 'Apr'):
        month = 4

    if (x  == 'May'):
        month = 5

    if (x  == 'Jun'):
        month = 6

    if (x  == 'Jul'):
        month = 7

    if (x  == 'Aug'):
        month = 8

    if (x  == 'Sep'):
        month = 9

    if (x  == 'Oct'):
        month = 10

    if (x  == 'Nov'):
        month = 11

    if (x  == 'Dec'):
        month = 12
    
    return month


def FromStringToDate(date):
    x = date.split()

    month = get_month(x[0])
    day = x[1]
    year = x[2]

    result = year + "-" + str(month) + "-" + day

    return(result)

def main():
    output = open("city_inspections_db.json", "w")
    with open('city_inspections.json', 'r+') as f:
        for line in f:
            
            result = re.search('"date":"(.*?)"', line)
            date = (result.group(1))
            
            x = str(line).replace(date , FromStringToDate(date), 1)
            output.write(x)


if __name__ == "__main__":
  main()