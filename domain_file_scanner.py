import pandas as pd  # open source data analysis and manipulation tool
import file_tools
import sys
from Domain import Domain

domain_names = []
exp_dates = []
registrars = []
availabilities = []


def append(domain):
    domain_names.append(domain.name)
    exp_dates.append(domain.exp_date)
    registrars.append(domain.registrar)
    availabilities.append(domain.availability)


def case_csv(data):
    for name in data.name:
        domain = Domain(name)
        print('Processing', name)
        domain.whois_extract(name)
        append(domain)


def case_txt(data):
    for name in data:
        domain = Domain(name)
        print('Processing', name)
        domain.whois_extract(name)
        append(domain)


def scanner(filename):
    data = []
    if filename[-4:] == ".csv":
        try:
            data = pd.read_csv(filename)
            case_csv(data)
        except Exception as e:
            print('Error while scanning csv file. Info below. Exiting.. \n')
            print(e)
            sys.exit(0)
    elif filename[-4:] == ".txt":
        try:
            file = open(filename, "r")
            for line in file:
                data.append(line.rstrip())
            case_txt(data)
            file.close()
        except Exception as e:
            print('Error while scanning txt file. Info below. Exiting.. \n')
            print(e)
            sys.exit(0)
    else:
        print('Unsupported filename given. Exiting..')
        sys.exit(0)

    # Push all data into 2D array
    data_arr = []
    for i in range(0, len(data)):
        data_arr.insert(i, [domain_names[i], exp_dates[i],
                            registrars[i], availabilities[i]])

    # Write to .txt file
    txt_filename = 'scanned_domains.txt'
    file_tools.write_to_txt(data_arr, txt_filename)

    # Write to .csv file
    out_csv_header = ['Domain', 'Expiration date',
                      'Registrar', 'Availability']
    csv_filename = 'scanned_domains.csv'
    file_tools.write_to_csv(out_csv_header, data_arr, csv_filename)

    # Give some stats after work finishes
    print('\nProcessed', len(domain_names), 'domains')
    print('Results written to', csv_filename + ' and ' + txt_filename)
