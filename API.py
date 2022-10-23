import requests_html



class Librus:

    def __init__(self):
        self.session = requests_html.HTMLSession()
        self.login_url = 'https://api.librus.pl/OAuth/Authorization?client_id=46'
        self.host_url = 'https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata' 
        self.auth_url = 'https://api.librus.pl/OAuth/Authorization/2FA?client_id=46'

        self.timetable = dict()
        self.hours = set()
        self.grades = []

    def login(self, usr, pwd):
        payload = {
                'action'    : 'login',
                'login'     : usr,
                'pass'      : pwd,
        }

        self.session.get(url=self.host_url)
        self.session.post(self.login_url, data = payload)
        self.session.get(url = self.auth_url)


    def gen_timetable(self):

        payload = {
            #'requestkey' : 'MC4yNTM4MTMwMCAxNjY2MzUyMzg2X2RiYjJmMGIyMGM4ZDA3ZWRiMGI5NzkwNWNlNjc0ZWIy',
            'tydzien'    : '2022-10-24_2022-10-30', }

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

        temp = dict()
        for i in list(self.timetable.keys())[:-2]:
            temp[i] =[]
            for j in self.timetable[i]:
                entry = j.replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('s.', '\ns.').split('\n')

                if 'konwersatorium' in entry:
                    entry[0] += ' konwersatorium'
                    entry.pop(1)
                temp[i].append(entry)

        self.timetable = temp


    def ttout(self):
        for i in self.timetable:
            print(i)
            c= 0 
            for j in self.timetable[i]:
                print(self.hours[c], j)
                c += 1
            print()

    def get_grades(self):
        self.grades = []

        req = self.session.get('https://synergia.librus.pl/przegladaj_oceny/uczen')
        #temp = req.html.find('tr.line0')[2::2]
        req_desc = req.html.find('a.ocena')

        for i in req_desc:
            grade = self.session.get('https://synergia.librus.pl' + list(i.links)[0])
            temp = grade.html.find('tr.line1')[1:] + grade.html.find('tr.line0')[2:]
            toAdd = dict()

            for j in temp:
                line = j.text.split('\n')
                if len(line)==2:
                    toAdd[line[0]] = line[1] 

            print(toAdd)
            self.grades.append(toAdd)

