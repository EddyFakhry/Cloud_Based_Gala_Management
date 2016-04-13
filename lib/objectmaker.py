"""
AUTHOR: EDDY FAKHRY
DATE:   15/10/2016
"""
from .galaparser import GalaParser
from .ev3utils import Ev3Reader
from .mdbextractor import mdbextractor

MDB_FILE = "test.mdb"
ZIP_FILE = "MeetEvent.zip"


class Objectmaker:
    """
    Construct complete gala/swimmers/club object
    """
    def __init__(self, mdbfile, zipfile):
        self._mdbfile = mdbfile
        self._zipfile = zipfile
        self._ev3reader = Ev3Reader(zipfile)
        self._galaparser = GalaParser(self._ev3reader.header, self._ev3reader.body)

    def _extract_swimmers(self, club_id):
        with mdbextractor(self._mdbfile) as cur:
            SQL = '''SELECT
                                Athlete as id,
                                First,
                                Last,
                                Sex,
                                Age,
                                Class,
                                ID_NO as Swimmer_id,
                                Group,
                                MailTo,
                                EMail,
                                Birth,
                                Inactive
                    FROM Athlete'''
            rows = cur.execute(SQL).fetchall()
            swimmers = {}
            for row in rows:
                swimmers[row[6]] = {
                    'id'        : row[0],
                    'first'     : row[1],
                    'last'      : row[2],
                    'sex'       : row[3],
                    'class'     : row[5],
                    'swimmer_id': row[6],
                    'group'     : row[7],
                    'mailTo'    : row[8],
                    'email'     : row[9],
                    'dob'       : row[10],
                    'inactive'  : row[11],
                    'club_id'   : club_id,
                }
            return swimmers


    def _extract_club(self):
        with mdbextractor(self._mdbfile) as cur:
            SQL = '''SELECT
                                TCode,
                                TName
                    FROM TEAM;'''
            rows = cur.execute(SQL).fetchone()
            club = {
                    'id': rows[0],
                    'name': rows[1],
            }
            return club

    def get_data(self):
        self._galaparser.parse()
        gala = self._galaparser.gala
        gala["club"] = self._extract_club()
        gala["swimmers"] = self._extract_swimmers(gala["club"]["id"])
        return gala