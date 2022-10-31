import pandas as pd  # open source data analysis and manipulation tool
import file_tools
import sys
import mail
from Domain import Domain
from http.client import HTTPSConnection
import os
from dotenv import load_dotenv

domain_names = []
exp_dates = []
registrars = []
availabilities = []
con = object
domainr_key = ""
domainr_url = ""


def append(domain):
    domain_names.append(domain.name)
    exp_dates.append(domain.exp_date)
    registrars.append(domain.registrar)
    availabilities.append(domain.availability)


def switch_to_rapidapi():
    global con
    global domainr_key
    global domainr_url
    con = HTTPSConnection('domainr.p.rapidapi.com')
    domainr_key = os.getenv('DOMAINR_RAPIDAPI_KEY')
    domainr_url = "/v2/status?mashape-key="


def switch_to_domainrapi():
    global con
    global domainr_key
    global domainr_url
    con = HTTPSConnection('api.domainr.com')
    domainr_key = os.getenv('DOMAINR_CLIENT_ID')
    domainr_url = "/v2/status?client_id="


# switch api url from limited rapidAPI to domainrAPI if successful response
def switch_domainr_api():
    if os.getenv('DOMAINR_CLIENT_ID') is not None:
        switch_to_domainrapi()
        print("Using unlimited Domainr API")
    elif os.getenv('DOMAINR_RAPIDAPI_KEY') is not None:
        switch_to_rapidapi()
        print("Switched to limited Domainr RapidAPI (10K/month)")
    else:
        print("No API key found in .env file. Please add DOMAINR_CLIENT_ID or DOMAINR_RAPIDAPI_KEY")


def case_csv(data):
    switch_domainr_api()
    for name in data.name:
        domain = Domain(name, con, domainr_url, domainr_key)
        print('Processing', name)
        domain.whois_extract(name)
        append(domain)


def case_txt(data):
    switch_domainr_api()
    for name in data:
        domain = Domain(name, con, domainr_url, domainr_key)
        print('Processing', name)
        domain.whois_extract(name)
        append(domain)


def scanner(src_file_name, out_file_name, mail_to):
    load_dotenv()
    data = []
    if src_file_name[-4:] == ".csv":
        try:
            data = pd.read_csv(src_file_name)
            case_csv(data)
        except Exception as e:
            print('Error while scanning csv file. Info below. Exiting.. \n')
            print(e)
            sys.exit(0)
    elif src_file_name[-4:] == ".txt":
        try:
            file = open(src_file_name, "r")
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
    txt_filename = out_file_name + '.txt'
    file_tools.write_to_txt(data_arr, txt_filename)

    # Write to .csv file
    out_csv_header = ['Domain', 'Expiration date',
                      'Registrar', 'Availability']
    csv_filename = out_file_name + '.csv'
    file_tools.write_to_csv(out_csv_header, data_arr, csv_filename)

    # Give some stats after work finishes
    print('\nProcessed', len(domain_names), 'domains')
    print('Results written to', csv_filename + ' and ' + txt_filename)

    # Send email
    abs_output_dir = file_tools.abs_output_dir
    mail_from = "artur@whoisgen.ga"
    try:
        mail.send_mail(mail_from, mail_to,
                       "Whois generator results", "Result files attached",
                       [abs_output_dir + txt_filename, abs_output_dir + csv_filename])
        print('\nEmail sent to', mail_to + ' with those files attached')
    except Exception as e:
        print('Error while sending email. Info below. Exiting.. \n')
        print(e)
        sys.exit(0)
