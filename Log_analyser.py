import re 
import sys
import logging 

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')  
logger = logging.getLogger(__name__)   

if len(sys.argv) < 2:     
    logger.error("Usage: python log_analyser.py <auth.log>")     
    sys.exit(1) 

filename = sys.argv[1]       

def parsed_failed_log(filename):     
    # Fixed literal spaces by replacing them with \s+ or \s
    pattern = re.compile(r'''
        ^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) # Timestamp (handles single/double digit days)
        .*?\bFailed\s+password\s+for\s+(?:invalid\s+user\s+)? # Main trigger phrase
        (\S+)                                          # Username
        \s+from\s+(\d{1,3}(?:\.\d{1,3}){3})            # IP Address
        (?:\s+port\s+(\d+))?                           # Optional Port
    ''', re.VERBOSE)                

    try:          
        with open(filename, 'r') as f:             
            for line in f:                 
                for match in pattern.finditer(line):                     
                    ip = match.group(3)                     
                    assert ip.count(".") == 3, f'INVALID IP: {ip}'                     
                    yield {                         
                        'timestamp': match.group(1),                         
                        'username': match.group(2),                         
                        'IP_address': ip,                         
                        'port': match.group(4) # Might be None                      
                    }     
    except FileNotFoundError:         
        logger.error(f'Error: File {filename} not found')         
        sys.exit(1)                                                                   

def IP_count(parsed_log):     
    result = {}     
    for entry in parsed_log:         
        ip = entry['IP_address']         
        if ip not in result:             
            result[ip] = {'count': 0, 'users': set(), 'timestamps': []}         
        
        result[ip]['count'] += 1         
        result[ip]['users'].add(entry['username']) 
        result[ip]['timestamps'].append(entry['timestamp'])     
    return result             

if __name__ == '__main__':
    store_1 = parsed_failed_log(filename) 
    store_3 = IP_count(store_1) 
    logger.info(store_3)

