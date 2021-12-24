from requests import Session
from datetime import datetime
from random import choice, randint
from string import ascii_lowercase
from urllib3 import disable_warnings
from json import dumps
from os import makedirs
from os.path import exists

disable_warnings()

def get_non_empty_rows(items):
    rows = []
    for row in items:
        if row['PhysicalName'] != None: rows.append(row)

    return rows

class Theater():
    def __init__(self, movie: str, time: str, format: str, link: str, seats: list):
        self.movie = movie
        self.time = time
        self.format = format
        self.link = link
        self.seats = seats

    def get_movie(self):
        return self.movie
    
    def get_time(self):
        return self.time

    def get_format(self):
        return self.format

    def get_link(self):
        return self.link

    def get_desc(self):
        return 'Movie: ' + self.movie + '\nFormat: ' + self.format + '\nTime: ' + self.time + '\nLink: ' + self.link

    def get_all_rows(self):
        return sorted(list(set([seat.get_row() for seat in self.seats])), reverse=False)

    def get_row(self, row: str):
        return [seat for seat in self.seats if seat.get_row() == row]

    def get_largest_row_length(self):
        rows = self.get_all_rows()
        longest = 0
        for row in rows:
            row = self.get_row(row)
            if len(row) > longest: longest = len(row)
        return longest

    def save_table(self):
        longest = self.get_largest_row_length()

        top = ['X']
        table = ''
        divider = '+---+'

        numbers = list(range(1, longest + 1))
        for x in numbers:
            if x >= 10: divider += '----+'
            else: divider += '---+'
            top.append(f'{x}')

        divider += '\n'
        table += divider + '| ' + ' | '.join(top) + ' |\n' + divider
        
        for name in self.get_all_rows():
            row = self.get_row(name)
            table += '| ' + name + ' | '

            for number in numbers:
                found = False
                
                for seat in row:
                    if number == seat.get_number():
                        if number >= 10: table += ' ' + seat.get_desc() + ' | '
                        else: table += seat.get_desc() + ' | '
                        found = True

                if not found and number >= 10: table += ' ! | '
                elif not found: table += '! | '
            table += '\n' + divider
        
        table += '\nLegend\nUnavailable Seat: !\nEmpty Seat: -\nTaken Seat: #\nSocial Distancing Seat: ~\nAccessibility Seat: @\nCompanion Seat: ^'

        if not exists('Movies'): makedirs('Movies')
        if not exists(f'Movies//{self.get_movie()}'): makedirs(f'Movies//{self.get_movie()}')

        with open(f'Movies//{self.get_movie()}//[{self.get_format()}] {self.get_time()}.txt', 'w') as f: f.write(self.get_desc() + '\n' + table)

class Seat():
    def __init__(self, row: str, number: int, status: int):
        self.row = row
        self.number = number
        self.tag = row + number
        self.status = status

        self.available = status in [0, 3, 4, 7]
        self.accessible = status == 3
        self.companionable = status == 7
    
    def get_row(self):
        return self.row
    
    def get_number(self):
        return int(self.number)

    def get_status(self):
        return int(self.status)

    def get_tag(self):
        return self.tag

    def get_desc(self):
        #'✅' Empty - 0 4 7
        #'❌' Taken - 1
        #'🦠' Social - 2
        #'🦽' Wheelchair - 3
        #'C'  Companion - 7
        #Abandoned using emojis because using them with letters and numbers in the table made it difficult to display all the results perfectly alligned.
        if self.status in [0, 4]: return '-'
        elif self.status == 1: return '#'
        elif self.status == 2: return '~'
        elif self.status == 3: return '@'
        elif self.status == 7: return '^'

    def is_available(self):
        return self.available
    
    def is_accessible(self):
        return self.accessible
    
    def is_companionable(self):
        return self.companionable

def gen_id():
    s = 'RWEB'
    for char in '1f80e3c0467cb263e9fdc522420e':
        if char.isalpha() : s+= choice(ascii_lowercase)
        else: s+= str(randint(0, 9))
    return s

def get_viewings():
    s = Session()

    headers_a = {'accept': 'application/json;charset=utf-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
            'accept-language': 'en-US,en;q=0.9'}
    
    with s.get(f'https://www.regmovies.com/us/data-api-service/v1/quickbook/10110/cinema-events/with-film/{MOVIE_ID}/at-date/{DATE}?attr=&ids={CINEMA_ID}&lang=en_US', headers=headers_a, verify=False) as a:
        events = a.json()['body']['events']
        details = []
        for event in events:
            if '4dx' in event['attributeIds']: formatting = '4DX'
            elif 'screenx' in event['attributeIds']: formatting = 'ScreenX'
            elif '3d' in event['attributeIds']: formatting = '3D'
            elif 'imax' in event['attributeIds']: formatting = 'IMAX'
            elif 'rpx' in event['attributeIds']: formatting = 'RPX'
            else: formatting = '2D'

            details.append({'ID': event['id'],
            'Time': datetime.strptime(event['eventDateTime'][0:-3].split('T')[1], '%H:%M').strftime("%I:%M %p"),
            'Link': event['bookingLink'],
            'Formatting': formatting})

        
        return details

def get_seatings():
    screenings = get_viewings()
    for screening in screenings:
        s = Session()

        headers_a = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
                'accept-language': 'en-US,en;q=0.9'}
        with s.get(screening['Link'], headers=headers_a, verify=False) as a:
            session_id = gen_id()
            headers_b = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15', 'accept-language': 'en-US,en;q=0.9'}
            params_b = (('theatreCode', CINEMA_ID), ('vistaSession', screening['ID']), ('date', DATE), ('cartId', session_id), ('apiSiteCode', CINEMA_ID))
            
            with s.get('https://experience.regmovies.com/api/TicketTypes', headers=headers_b, params=params_b, verify=False) as b:
                headers_c = {'accept': '*/*', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://experience.regmovies.com', 'accept-language': 'en-US,en;q=0.9', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15'}
                data_c = {"UserSessionId": session_id, "CinemaId": CINEMA_ID, "SessionId": screening['ID'], "TicketTypes": [{"TicketTypeCode": b.json()['Tickets'][0]['TicketTypeCode'], "Qty": 1}], "ReturnDiscountInfo": True, "ReturnOrder": True}
                
                with s.post('https://experience.regmovies.com/api/AddTickets', headers=headers_c, data=dumps(data_c), verify=False) as c:
                    if 'SeatsUnavailable' in c.text: print(f'Time {screening["Time"]} had no seats available.')

                    data_d = {"CinemaId": CINEMA_ID, "SessionId": screening['ID'], "UserSessionId": session_id, "IncludeBrokenSeats": True, "IncludeHouseSpecialSeats": True, "IncludeGreyAndSofaSeats": True, "IncludeAllSeatPriorities": True, "IncludeSeatNumbers": True, "IncludeCompanionSeats": True}
                    params_d = (('theatreCode', CINEMA_ID), ('vistaSession', screening['ID']))
                    
                    with s.post('https://experience.regmovies.com/api/SeatPlan', headers=headers_c, data=dumps(data_d), params=params_d, verify=False) as d:
                        rows = d.json()['SeatLayoutData']['Areas'][0]['Rows']
                        rows = get_non_empty_rows(rows)

                        seats = []
                        for row in rows:
                            for seat in row['Seats']:
                                seats.append(Seat(row['PhysicalName'], seat['Id'], seat['Status']))
             

                        s = Theater(MOVIE, screening['Time'], screening['Formatting'], screening['Link'], seats)
                        s.save_table()

DATE = datetime.now().strftime('%Y-%m-%d')

CINEMA_ID = input('Cinema ID\n').strip()
MOVIE_ID = input('Movie ID\n').strip()
MOVIE = input('Movie Name\n').strip()
DATE = input(f'Date (ex: {DATE})\n').strip()

get_seatings()
