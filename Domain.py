from datetime import datetime
import json
import whois


class Domain:
    name = ""
    exp_date = ""
    registrar = ""
    availability = ""
    con = object
    domainr_url = ""
    domainr_key = ""

    def __init__(self, name, con, domainr_url, domainr_key):
        self.name = name
        self.con = con
        self.domainr_url = domainr_url
        self.domainr_key = domainr_key

    def check_date_type(self, exp_date):
        if isinstance(exp_date, datetime):  # check if dates converted to datetime object
            self.exp_date = exp_date.strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
        elif isinstance(exp_date, list):  # some dates not converted because consists of multiple
            self.exp_date = exp_date[0].strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
        else:
            self.exp_date = 'none'

    def whois_extract(self, name):
        # getting general whois info
        try:
            w = whois.whois(name)
            exp_date = w.expiration_date
            self.check_date_type(exp_date)
            self.registrar = w.registrar
        except Exception as e:
            self.exp_date = 'none'
            self.registrar = 'none'
            print(e)
        # getting domain availability info
        try:
            res, json_data = self.http(name)
            status = json_data['status'][0]['status']
            if res.status == 200:
                if "inactive" in status:
                    self.availability = "available"
                elif "active" in status:
                    self.availability = "taken"
                elif "unknown" in status:
                    self.availability = "unknown"
                else:
                    self.availability = "unknown"
            else:
                self.availability = "error"
        except Exception as e:
            self.availability = "error " + e

    def http(self, name):
        self.con.request('GET',
                         self.domainr_url + self.domainr_key +
                         '&domain=' + name)
        res = self.con.getresponse()
        res_data = res.read()
        json_data = json.loads(res_data)
        return res, json_data
