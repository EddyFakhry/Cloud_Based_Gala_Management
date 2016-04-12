import csv
from zipfile import ZipFile
import tempfile


class Ev3Reader():
    TEMP_DIR = "./temp/"

    def __init__(self, file):
        self.file = file
        self.header = []
        self.body = []
        self._parse()

    def _parse(self):
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


# if __name__ == '__main__':
#     ev3_reader = Ev3Reader('MeetEvent.zip')
#     header = ev3_reader.header
#     print(header)
#     print ("Event Title: " + header[0] + " Location: " + header[1] + " Date: " + header[2])
#     for row in ev3_reader.body:
#         print ("Event: #" + row[0] + "    Distance: " + row[8] + "     Category: " + row[5] + "     Event Time: " + row[24])
