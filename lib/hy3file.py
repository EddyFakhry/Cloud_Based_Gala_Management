from abc import abstractmethod, ABCMeta
from lib.mongo import Mongo
from time import strftime


def checksum(line):
    odd = 0
    even = 0
    for i in range(0, len(line)):
        if i % 2 == 1:
            odd += ord(line[i]) * 2 #sum value of all characters with an odd index and multiply by 2
        else:
            even += ord(line[i])    #sum value of all characters with an even index
    total = (odd + even)            #add the two sums
    raw = (total // 21) + 205       #integer division of addition and add 205
    return str(raw)[-1] + str(raw)[-2] #reverse last two digits of prior operation


class Ev3line:
    __metaclass__ = ABCMeta

    # Padding Constants
    LEFT_PADDING = -1
    NO_PADDING = 0
    RIGHT_PADDING = 1
    # Default values
    SPACE = ' '

    def __init__(self):
        self.LINE_ID = ''

    def _add_padding(self, variable):
        value = str(variable['value'])
        if variable['padding'] is self.NO_PADDING:
            return value
        else:
            padding_required = variable['length'] - len(value)
            if padding_required > 0 and variable['padding'] is self.LEFT_PADDING:
                return self.SPACE * padding_required + value
            elif padding_required > 0 and variable['padding'] is self.RIGHT_PADDING:
                return value + self.SPACE * padding_required
        return value[:variable['length']]

    @abstractmethod
    def as_line(self):
        pass


class FileInformation(Ev3line):

    def __init__(self, date=''):
        self.LINE_ID = 'A102'
        self.line_id = {'value': self.LINE_ID, 'length': 3, 'padding': self.NO_PADDING}
        self.line_description = {'value': 'Meet Entries             Hy-Tek, Ltd', 'length': 36, 'padding': self.NO_PADDING}
        self.version = {'value': '', 'length': 18, 'padding': self.LEFT_PADDING}
        self.date = {'value': date, 'length': 8, 'padding': self.LEFT_PADDING}
        self.end_padding = {'value': '', 'length': 62, 'padding': self.LEFT_PADDING}

    def as_line(self):
        line = self._add_padding(self.line_id) \
                + self._add_padding(self.line_description) \
                + self._add_padding(self.version) \
                + self._add_padding(self.date) \
                + self._add_padding(self.end_padding)
        return line


class MeetInformation(Ev3line):
    def __init__(self, title='', facility='', start_date='', end_date='', age_up_date=''):
        self.LINE_ID = 'B1'
        self.line_id = {'value': self.LINE_ID, 'length': 2, 'padding': self.NO_PADDING}
        self.title = {'value': title, 'length': 45, 'padding': self.RIGHT_PADDING}
        self.facility = {'value': facility, 'length': 45, 'padding': self.RIGHT_PADDING}
        self.start_date = {'value': start_date, 'length': 8, 'padding': self.LEFT_PADDING}
        self.end_date = {'value': end_date, 'length': 8, 'padding': self.LEFT_PADDING}
        self.age_up_date = {'value': age_up_date, 'length': 8, 'padding': self.LEFT_PADDING}
        self.end_padding = {'value': '', 'length': 12, 'padding': self.LEFT_PADDING}

    def as_line(self):
        line = self._add_padding(self.line_id) \
                + self._add_padding(self.title) \
                + self._add_padding(self.facility) \
                + self._add_padding(self.start_date) \
                + self._add_padding(self.end_date) \
                + self._add_padding(self.age_up_date) \
                + self._add_padding(self.end_padding)
        return line


class ClubInformation(Ev3line):

    def __init__(self, club_id='', club_name=''):
        self.LINE_ID = 'C1'
        self.line_id = {'value': self.LINE_ID, 'length': 2, 'padding': self.NO_PADDING}
        self.club_id = {'value': club_id, 'length': 5, 'padding': self.RIGHT_PADDING}
        self.club_name = {'value': club_name, 'length': 30, 'padding':self.RIGHT_PADDING}
        self.end_padding = {'value': '', 'length': 91, 'padding': self.LEFT_PADDING}

    def as_line(self):
        line = self._add_padding(self.line_id) \
                + self._add_padding(self.club_id) \
                + self._add_padding(self.club_name) \
                + self._add_padding(self.end_padding)
        return line


class SwimmerEntry(Ev3line):

    def __init__(self, gender='', event_swimmer_id='', surname='', first_name='', nickname='', uss_number='',
                 team_swimmer_id='', date_of_birth='', age=''):
        super(SwimmerEntry, self).__init__()
        self.LINE_ID = 'D1'
        self.line_id = {'value': self.LINE_ID, 'length': 2, 'padding': self.NO_PADDING}
        self.gender = {'value': gender, 'length': 1, 'padding': self.NO_PADDING}
        self.event_swimmer_id = {'value': event_swimmer_id, 'length': 5, 'padding': self.LEFT_PADDING}
        self.surname = {'value': surname, 'length': 20, 'padding': self.RIGHT_PADDING}
        self.first_name = {'value': first_name, 'length': 20, 'padding': self.RIGHT_PADDING}
        self.nickname = {'value': nickname, 'length': 20, 'padding': self.RIGHT_PADDING}
        self.mi = {'value': self.SPACE, 'length': 1, 'padding': self.NO_PADDING}
        self.uss_number = {'value': uss_number, 'length': 14, 'padding': self.RIGHT_PADDING}
        self.team_swimmer_id = {'value': team_swimmer_id, 'length': 5, 'padding': self.LEFT_PADDING}
        self.date_of_birth = {'value': date_of_birth, 'length': 8, 'padding': self.NO_PADDING}
        self.unknown1 = {'value': self.SPACE, 'length': 1, 'padding': self.NO_PADDING}
        self.age = {'value': age, 'length': 2, 'padding': self.LEFT_PADDING}
        self.end_padding = {'value': '', 'length': 29, 'padding': self.LEFT_PADDING}

    def as_line(self):
        line = self._add_padding(self.line_id) \
                + self._add_padding(self.gender) \
                + self._add_padding(self.event_swimmer_id) \
                + self._add_padding(self.surname) \
                + self._add_padding(self.first_name) \
                + self._add_padding(self.nickname) \
                + self._add_padding(self.mi) \
                + self._add_padding(self.uss_number) \
                + self._add_padding(self.team_swimmer_id) \
                + self._add_padding(self.date_of_birth) \
                + self._add_padding(self.unknown1) \
                + self._add_padding(self.age) \
                + self._add_padding(self.end_padding)
        return line


class EventEntry(Ev3line):
    def __init__(self, gender='', event_swimmer_id='', abbreviated_name='', gender_category='', distance='',
                 stroke='', age_lower='', age_upper='', fee='', event_number='', time1='',
                 course1='', time2='', course2=''):
        self.LINE_ID = 'E1'
        self.line_id = {'value': self.LINE_ID, 'length': 2, 'padding': self.NO_PADDING}
        self.gender1 = {'value': gender, 'length': 1, 'padding': self.NO_PADDING}
        self.event_swimmer_id = {'value': event_swimmer_id, 'length': 5, 'padding': self.LEFT_PADDING}
        self.abbreviated_name = {'value': abbreviated_name[:5], 'length': 5, 'padding': self.RIGHT_PADDING}
        self.gender2 = {'value': gender, 'length': 1, 'padding': self.NO_PADDING}
        self.gender_category = {'value': gender_category, 'length': 1, 'padding': self.NO_PADDING}
        self.unknown1 = {'value': self.SPACE*2, 'length': 2, 'padding': self.NO_PADDING}
        self.distance = {'value': distance, 'length': 4, 'padding': self.LEFT_PADDING}
        self.stroke = {'value': stroke, 'length': 1, 'padding': self.NO_PADDING}
        self.age_lower = {'value': age_lower, 'length': 3, 'padding': self.LEFT_PADDING}
        self.age_upper = {'value': age_upper, 'length': 3, 'padding': self.RIGHT_PADDING}
        self.unknown2 = {'value': self.SPACE*4, 'length': 4, 'padding': self.NO_PADDING}
        self.fee = {'value': fee, 'length': 6, 'padding': self.LEFT_PADDING}
        self.event_number = {'value': event_number, 'length': 3, 'padding': self.LEFT_PADDING}
    # TODO: check if needed and remove at later stage if possible.
        self.unknown3 = {'value': self.SPACE*2, 'length': 2, 'padding': self.NO_PADDING}
        self.time1 = {'value': time1, 'length': 7, 'padding': self.LEFT_PADDING}
        self.course1 = {'value': course1, 'length': 1, 'padding': self.LEFT_PADDING}
        self.unknown4 = {'value': self.SPACE, 'length': 1, 'padding': self.NO_PADDING}
        self.time2 = {'value': time2, 'length': 7, 'padding': self.LEFT_PADDING}
        self.course2 = {'value': course2, 'length': 1, 'padding': self.LEFT_PADDING}
    # End of delete section
        self.end_padding = {'value': '', 'length': 68, 'padding': self.LEFT_PADDING}

    def as_line(self):
        line = self._add_padding(self.line_id) \
                + self._add_padding(self.gender1) \
                + self._add_padding(self.event_swimmer_id) \
                + self._add_padding(self.abbreviated_name) \
                + self._add_padding(self.gender2) \
                + self._add_padding(self.gender_category) \
                + self._add_padding(self.unknown1) \
                + self._add_padding(self.distance) \
                + self._add_padding(self.stroke) \
                + self._add_padding(self.age_lower) \
                + self._add_padding(self.age_upper) \
                + self._add_padding(self.unknown2) \
                + self._add_padding(self.fee) \
                + self._add_padding(self.event_number) \
                + self._add_padding(self.unknown3) \
                + self._add_padding(self.time1) \
                + self._add_padding(self.course1) \
                + self._add_padding(self.unknown4) \
                + self._add_padding(self.time2) \
                + self._add_padding(self.course2) \
                + self._add_padding(self.end_padding)
        return line


class HY3file:

    def __init__(self, gala_id, club_id):
        self.gala_id = gala_id
        self.club_id = club_id
        self.output_lines = []
        self.swimmers = {}
        self.entries = []
        self.add_headers()
        self.add_swimmers_with_entries()
        self.add_checksums()

    def add_headers(self):
        with Mongo() as db:
            gala = db.gala.find_one({'title': self.gala_id, 'club.id': self.club_id})
        self.output_lines.append(FileInformation(strftime("%m%d%Y")).as_line())                 #A line
        self.output_lines.append(MeetInformation(title=self.gala_id,
                                                 facility=gala['location'],
                                                 start_date=gala['date'].strftime("%m%d%Y"),
                                                 end_date=gala['end_date'].strftime("%m%d%Y"),
                                                 age_up_date=gala['age_up_date'].strftime("%m%d%Y")).as_line())    #B line
        self.output_lines.append(ClubInformation(self.club_id, gala['club']['name']).as_line()) #C line

    def add_swimmers_with_entries(self):
        with Mongo() as db:
            swimmers_data = db.swimmers.find({'club_id': self.club_id})
            entries_data = db.entries.find({'gala_id': self.gala_id, 'club_id': self.club_id})
        for swimmer in swimmers_data:
            swimmer_id = swimmer['swimmer_id']
            self.swimmers[swimmer_id] = swimmer
            self.swimmers[swimmer_id]['entry'] = None
        for entry in entries_data:
            swimmer_id = entry['swimmer_id']
            if swimmer_id in self.swimmers:
                self.swimmers[swimmer_id]['entry'] = entry
            else:
                raise Exception('Entry for an unknown swimmer has been detected.')
        for swimmer in self.swimmers.values():
            if swimmer['entry'] and swimmer['entry']['heats']:
                swimmer_entry = SwimmerEntry(gender=swimmer['sex'], event_swimmer_id=swimmer['id'], surname=swimmer['last'],
                                    first_name=swimmer['first'], uss_number=swimmer['swimmer_id'],
                                    date_of_birth=strftime('%m%d%Y', swimmer['dob'].timetuple()))
                self.output_lines.append(swimmer_entry.as_line())
                for heat in swimmer['entry']['heats']:
                    event_entry = EventEntry(gender=swimmer['sex'], event_swimmer_id=swimmer['id'], abbreviated_name=swimmer['last'],
                                             gender_category=heat['gender'], distance=heat['distance'],event_number=heat['id'],
                                             stroke=heat['style'], age_lower=heat['minage'], age_upper=heat['maxage'])
                    self.output_lines.append(event_entry.as_line())

    def add_checksums(self):
        for i, line in enumerate(self.output_lines):
            self.output_lines[i] += checksum(line)

    def to_string(self):
        output = ""
        for line in self.output_lines:
            output += line + '\r\n'
        return output

#for testing purposes
def checksum_file(filename):
    output = ''
    with open(filename) as fd:
        for line in fd:
            line = line.rstrip('\n')[:-2]
            line += checksum(line) + '\n'
            output += line
    with open('new_' + filename, 'w') as fd:
        fd.write(output)
