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

        payload = {
            #'requestkey' : 'MC4yNTM4MTMwMCAxNjY2MzUyMzg2X2RiYjJmMGIyMGM4ZDA3ZWRiMGI5NzkwNWNlNjc0ZWIy',
            'tydzien'    : '2022-10-17_2022-10-23',
        }

        req = self.session.post(url = 'https://synergia.librus.pl/przegladaj_plan_lekcji', data = payload)

        lekcje = req.html.find('td.line1')
        for i in lekcje:

            #print(i.attrs['data-date'], i.attrs['data-time_from'], i.attrs['data-time_to'])

            if i.attrs['data-date'] not in self.timetable:
                self.timetable[i.attrs['data-date']] = []

            self.timetable[i.attrs['data-date']].append(i.text)
            self.hours.add(i.attrs['data-time_from'] + ' - ' + i.attrs['data-time_to'])

            if 'zastępstwo' in i.text:
                rooms = i.html.split('.')

                if len(rooms) < 3: continue

                roomshift = rooms[0][-1] + '.' + rooms[1][:2] + ' -> ' + rooms[1][-1] + '.' + rooms[2][:2]
                self.timetable[i.attrs['data-date']][-1] += ' s. ' + roomshift

        self.hours = sorted(self.hours)

    def ttout(self):
        for i in list(self.timetable.keys())[:-2]:
            print(i)
            c = 0
            for j in self.timetable[i]:
                print(self.hours[c], end = ' ')
                entry = j.replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('s.', '\ns.').split('\n')

                if 'konwersatorium' in entry:
                    entry[0] += ' konwersatorium'
                    entry.pop(1)
                print(entry)
                c += 1
            print()

    def get_grades(self):

        req = self.session.get('https://synergia.librus.pl/przegladaj_oceny/uczen')

librus = Librus()
librus.login()
librus.gen_timetable()
librus.ttout()



