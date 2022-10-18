from datetime import datetime
import whois


class Domain:
    exp_date = ""
    type_of_date = ""
    registrar = ""

    def __init__(self, name):
        self.name = name

    def check_date_type(self, exp_date):
        if isinstance(exp_date, datetime):  # check if dates converted to datetime object
            self.exp_date = exp_date.strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
            self.type_of_date = 'datetime'
        elif isinstance(exp_date, list):  # some dates not converted because consists of multiple
            self.exp_date = exp_date[0].strftime("%Y-%m-%d %H:%M:%S")  # format unformatted
            self.type_of_date = 'list'
        else:
            self.type_of_date = 'none'
            self.exp_date = 'none'

    def whois_extract(self, name):
        try:
            w = whois.whois(name)
            exp_date = w.expiration_date
            self.check_date_type(exp_date)
            self.registrar = w.registrar
        except whois.parser.PywhoisError:
            self.exp_date = 'none'
            self.type_of_date = 'none'
            self.registrar = 'none'
