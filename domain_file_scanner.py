import pandas as pd  # open source data analysis and manipulation tool
import whois
import file_tools
from datetime import datetime
import sys


def check_date_type(exp_date):
    if isinstance(exp_date, datetime):  # check if dates converted to datetime object
        exp_date = exp_date.strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
        type_of_date = 'datetime'
    elif isinstance(exp_date, list):  # some dates not converted because consists of multiple
        exp_date = exp_date[0].strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
        type_of_date = 'list'
    else:
        type_of_date = 'none'
        exp_date = 'none'
    return exp_date, type_of_date


def whois_main(name):
    try:
        w = whois.whois(name)
        exp_date = w.expiration_date
        exp_date, type_of_date = check_date_type(exp_date)
    except whois.parser.PywhoisError:
        exp_date = 'none'
        type_of_date = 'none'
    return exp_date, type_of_date


def whois_csv(data):
    domain_names = []
    exp_dates = []
    type_of_dates = []
    for name in data.name:
        print('Processing', name)
        domain_names.append(name)
        exp_date, type_of_date = whois_main(name)
        exp_dates.append(exp_date)
        type_of_dates.append(type_of_date)
    return domain_names, exp_dates, type_of_dates


def whois_txt(data):
    domain_names = []
    exp_dates = []
    type_of_dates = []
    for name in data:
        print('Processing', name)
        domain_names.append(name)
        exp_date, type_of_date = whois_main(name)
        exp_dates.append(exp_date)
        type_of_dates.append(type_of_date)
    return domain_names, exp_dates, type_of_dates


def scanner(filename):
    # reading domains
    data = []
    if filename[-4:] == ".csv":
        data = pd.read_csv(filename)
        domain_names, exp_dates, type_of_dates = whois_csv(data)
    elif filename[-4:] == ".txt":
        file = open(filename, "r")
        for line in file:
            data.append(line.rstrip())
        file.close()
        domain_names, exp_dates, type_of_dates = whois_txt(data)
    else:
        print('Wrong filename given. Exiting..')
        sys.exit(0)

    # Push all data into 2D array
    data_arr = []
    for i in range(0, len(data)):
        data_arr.insert(i, [domain_names[i], exp_dates[i], type_of_dates[i]])

    # Write to .txt file
    txt_filename = 'scanned_domains.txt'
    file_tools.write_to_txt(data_arr, txt_filename)

    # Write to .csv file
    out_csv_header = ['Domain', 'Expiration date', 'Date type']
    csv_filename = 'scanned_domains.csv'
    file_tools.write_to_csv(out_csv_header, data_arr, csv_filename)

    # Give some stats after work finishes
    print('\nProcessed', len(domain_names), 'domains')
    print('Results written to', csv_filename + ' and ' + txt_filename)
