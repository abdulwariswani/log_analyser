import re

# opens and read file line-by-line 
def ReadFile():
    line_list = []
    with open('./log_file.txt','r') as file :
        for line in file:
           line_list.append(line.strip())
    return line_list 




# extraction: matches regex and stores them into the list of dictionaries
def Regex(store_1):
    parsed_log =[]
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



       

store_1 = ReadFile()
print(Regex(store_1))

