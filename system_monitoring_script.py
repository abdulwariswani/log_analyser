import os , shutil ,re , time
def get_cpu_percentage():
        with open ('/proc/stat', 'r') as file:
            first_line = file.readline()
            matched_list  = first_line.split()
            matched_list.pop(0)
            idle_time = int(matched_list[3])+ int(matched_list[4])
            total_sum = 0
            for num in matched_list:
                  total_sum += int(num)

        return total_sum, idle_time 


        # read meminfo file
def RAM():
        info= {}
        with open('/proc/meminfo', 'r') as file_1:
            for count , line in enumerate(file_1):
                if count ==5 :
                     break
                lines = line.split()
                if len(lines) >= 2:
                     keys = lines[0].strip(':')
                     # lines.pop(2)
                     value = lines[1]
                info[keys] = value
            print(info)
        
RAM()





store = []
def queue(value):
    if  len(store) < 2:
        store.append(value)
    elif len(store) == 2 :
          store.pop(0)
          store.append(value)
    return None

def formula(store):
    if len(store) <2 :
         return None 
    old_total ,old_idle = store[0]
    new_total , new_idle = store[1]
    total_diff = new_total  - old_total
    idle_diff = new_idle - old_idle
    if total_diff == 0:
        return 0
    cpu_usage = ((total_diff - idle_diff)/total_diff)*100
    return cpu_usage
        

while True:
      store_1 = get_cpu_percentage()
      # print(store_1)
      queue(store_1)
      #print(store)
      print(formula(store))
      time.sleep(1)