"""
AUTHOR: EDDY FAKHRY
DATE:   15/10/2016
"""
import csv
from zipfile import ZipFile
import tempfile


class Ev3Reader:
    """
    Retrieve the data from the EV3 file
    """
    TEMP_DIR = "./temp/"

    def __init__(self, file):
        self.file = file
        self.header = []
        self.body = []
        self._parse()

    def _parse(self):
        """
        Find and parse EV3 file after unzipping invitation folder
        """
        zf = ZipFile(self.file, 'r')
        suffix = "ev3"
        tempdir = tempfile.TemporaryDirectory()
        for ev3_file in zf.namelist():
            if ev3_file.endswith(suffix):
                zf.extract(ev3_file, self.TEMP_DIR)
                with open(self.TEMP_DIR + ev3_file, 'r', newline='') as csvfile:
                    eventreader = csv.reader(csvfile, delimiter=';')
                    self.header = next(eventreader)
                    for row in eventreader:
                        self.body.append(row)

