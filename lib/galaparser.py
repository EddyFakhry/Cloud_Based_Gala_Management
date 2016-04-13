"""
AUTHOR: EDDY FAKHRY
DATE:   15/10/2016
"""
from datetime import datetime


class GalaParser():
    """
    Retrieve all relevant information about the gala event
    """
    def __init__(self, header, body):
        self._header = header
        self._body = body
        self.gala = {}

    def parse(self):
        self._parse_header()
        self._parse_body()

    def _parse_header(self):
        """
        Parse first line of the EV3 file
        """
        self.gala['title'] = self._header[0]
        self.gala['location'] = self._header[1]
        self.gala['date'] = datetime.strptime(self._header[2], '%m/%d/%Y')
        self.gala['end_date'] = datetime.strptime(self._header[3], '%m/%d/%Y')
        self.gala['age_up_date'] = datetime.strptime(self._header[4], '%m/%d/%Y')
        self.gala['deleted'] = False

    def _parse_body(self):
        """
        Parse all lines in the EV3 file other than the first one
        """
        self.gala['heats'] = []
        for row in self._body:
            heat = {
                'id'                : row[0],
                'type'              : row[2],
                'dives'             : row[3],
                'individual/relay'  : row[4],
                'gender'            : row[5],
                'minage'            : row[6],
                'maxage'            : row[7],
                'distance'          : row[8],
                'style'             : row[9],
                'time'              : row[24],
            }
            self.gala['heats'].append(heat)
