import whois
import pandas as pd # open source data analysis and manipulation tool
import time # for execution time calculation
from datetime import datetime
st = time.time() # start time

# reading exported domains
data = pd.read_csv("domain_export.csv")

domain_names = []
exp_dates = []
is_datetimes = []
for name in data.name:
    domain_names.append(name)
    w = whois.whois(name)
    time.sleep(2)
    exp_date = w.expiration_date  # dates converted to datetime object
    if isinstance(exp_date, datetime):
        exp_date = exp_date.strftime("%Y-%m-%d %H:%M:%S") # format unformatted
        is_datetimes.append('yes')
    else:
        is_datetimes.append('no')
    exp_dates.append(exp_date)

data_arr = []
for i in range(0, len(data)):
    data_arr.insert(i, [domain_names[i], exp_dates[i], is_datetimes[i]])

f = open("output.txt", "w")
for i in range(0, len(data_arr)):
    f.write(f"{data_arr[i][0]} {data_arr[i][1]} {data_arr[i][2]}\n")
f.close()

out_csv_header = ['Domain', 'Expiration date', 'Datetime?']
pd_data = pd.DataFrame(data_arr, columns=out_csv_header)
pd_data.to_csv('output.csv', index=False)

et = time.time() # end time
elapsed_time = et - st # execution time
print('Processed', len(domain_names), 'domains')
print('Execution time:', "%.2f" % elapsed_time, 'seconds')

# f = open("output.txt", "r")
# print(f.read())

