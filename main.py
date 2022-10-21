from cred import *
import requests_html

payload = {
        'action'    : 'login',
        'login'     : username,
        'pass'      : password,
}


class Librus:

    def __init__(self):
        self.session = requests_html.HTMLSession()
        self.login_url = 'https://api.librus.pl/OAuth/Authorization?client_id=46'
        self.host_url = 'https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata' 
        self.auth_url = 'https://api.librus.pl/OAuth/Authorization/2FA?client_id=46'

        self.timetable = dict()
        self.hours = set()

    def login(self):
        global payload

        self.session.get(url=self.host_url)
        self.session.post(self.login_url, data = payload)
        self.session.get(url = self.auth_url)



    def gen_timetable(self):
        req = self.session.get(url = 'https://synergia.librus.pl/przegladaj_plan_lekcji')

        lekcje = req.html.find('td.line1')
        for i in lekcje:
            #print(i.attrs['data-date'], i.attrs['data-time_from'], i.attrs['data-time_to'])

            if i.attrs['data-date'] not in self.timetable:
                self.timetable[i.attrs['data-date']] = []

            self.timetable[i.attrs['data-date']].append(i.text)
            self.hours.add(i.attrs['data-time_from'] + ' - ' + i.attrs['data-time_to'])

        self.hours = sorted(self.hours)


    def ttout(self):
        for i in self.timetable:
            print(i)
            c = 0
            for j in self.timetable[i]:
                print(self.hours[c], end = ' ')
                print(j.split('\n')[0])
                c += 1
            print()

librus = Librus()
librus.login()
librus.gen_timetable()
librus.ttout()


#https://api.librus.pl/OAuth/Authorization?client_id=46action=login&login=7036451u&pass=Iriting97
