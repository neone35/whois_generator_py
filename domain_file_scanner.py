import pandas as pd  # open source data analysis and manipulation tool
import whois
import file_tools
from datetime import datetime
import sys


def scanner(filename):
    # reading exported domains
    data = []
    if filename[-4:] == ".csv":
        data = pd.read_csv(filename)
    elif filename[-4:] == ".txt":
        file = open(filename, "r")
        for line in file:
            data.append(line.rstrip())
            print(line.rstrip())
        file.close()
    else:
        print('Wrong filename given. Exiting..')
        sys.exit(0)

    domain_names = []
    exp_dates = []
    type_of_date = []
    for name in data:
        print('Processing', name)
        domain_names.append(name)
        try:
            w = whois.whois(name)
            exp_date = w.expiration_date
            if isinstance(exp_date, datetime):  # check if dates converted to datetime object
                exp_date = exp_date.strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
                type_of_date.append('datetime')
            elif isinstance(exp_date, list):  # some dates not converted because consists of multiple
                exp_date = exp_date[0].strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
                type_of_date.append('list')
            else:
                type_of_date.append('none')
            exp_dates.append(exp_date)
        except whois.parser.PywhoisError:
            exp_dates.append('none')

    # Push all data into 2D array
    data_arr = []
    for i in range(0, len(data)):
        data_arr.insert(i, [domain_names[i], exp_dates[i], type_of_date[i]])

    # Write to .txt file
    file_tools.write_to_txt(data_arr, 'scanned_domains.txt')

    # Write to .csv file
    out_csv_header = ['Domain', 'Expiration date', 'Date type']
    filename = 'scanned_domains.csv'
    file_tools.write_to_csv(out_csv_header, data_arr, filename)

    # Give some stats after work finishes
    print('\nProcessed', len(domain_names), 'domains')
    print('Results written to', filename)
