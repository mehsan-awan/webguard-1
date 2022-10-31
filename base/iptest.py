IP_lst = []
for line in open('/var/log/apache2/newlog.log.1'):
    line  = line.split()
    IP_lst.append(line[0])

finallst = []

for val in IP_lst:
    if val in finallst:
        pass
    else:
        finallst.append(val)

for val in finallst:
    print(val)
    #ip = line.split(' ')[0]
    #IP_lst.append(ip)

    #temp_list = []
    #for i in IP_lst:
    #    if i not in temp_list:
    #       temp_list.append(i)

   # my_list = temp_list

  #  print(my_list)