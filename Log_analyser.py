import re , sys
from collections import Counter

# opens and read file line-by-line 
def ReadFile():
    line_list = []
    if len(sys.argv) > 1:
        try:
            filename = sys.argv[1]
            with open(filename, 'r') as file :
                for line in file:
                    line_list.append(line.strip())
        except FileNotFoundError:
            print(f'Error:The file {filename} was not found')
    else:
        print("Usage: python script.py <filename>")
    return line_list 




# extraction: matches regex and stores them into the list of dictionaries
def Regex(store_1):
    parsed_log =[] # list of directoires.
    for lines in store_1:
        pattern = r'^([A-Z][a-z]{2}\s+\d{2}\s+\d{2}:\d{2}:\d{2}).*?Failed password for (?:invalid user )?(\S+) from (\d{1,3}(?:\.\d{1,3}){3})'
        found = re.search(pattern,lines)
        if found :
            entry = {
            'timestamp' : found.group(1),
            'username' : found.group(2),
            'IP_address' : found.group(3)
            }
            parsed_log.append(entry)
    return parsed_log 

# simple IP counter
def IP_count(parsed_log):
    result = {}
    for entry in parsed_log:
        ip = entry['IP_address']
        if ip not in result:
            result[ip] = {'count':0 , 'users':set(), 'timestamps': []}
        # update info in nested dictionary
        result[ip]['count'] = +1
        result[ip]['users'].add(entry['username']) # set prevents duplicate usernames
        result[ip]['timestamps'].append(entry['timestamp'])
    return result

       

store_1 = ReadFile()
store_2 = Regex(store_1)
store_3 = IP_count(store_2)
print(store_2)
