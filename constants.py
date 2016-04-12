import os

UPLOAD_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)),"temp")
DAYS_IN_YEAR = 365.2425
UPLOAD_FILE_TYPES = ['zip', 'mdb']
MAX_UPLOAD_SIZE = 10 * 1024 * 1024 # 10 MB
SUBJECT = "Import gala name maybe" + ": Please subscribe"
DEFAULT_SENDER = "swimautomail@gmail.com" #gala secretary
RECIPIENTS = ["get swimmers emails"]
LINK_GENERATOR_SALT = \
    'N%BRpAfR4Ta80DLEdGdS!rJ1Pb+yII*SL$hZmo*gIpD9w^6+!5wu9@Q!tdD05c0s|=mv3SrVcrembY!$&wxRHusc-t8o4UBw%scDr&8DCiiJHdxW' \
    'HB#Idq6IB5t3frLr8G4ghZ^BV8DH92cT=jP?LsTc6mMt^v$lTo=i8fBcbalGhTmhu$mKWrhxuYWoksyDA^&W9ELSNJr9?ykVHfheeb0FJ4-Vs#9$' \
    'N$JZiMAM##7fp8DV_nddO^32z?^hDs3A'
SERVER = 'http://127.0.0.1:5000'
FORM_ADDRESS = SERVER + '/form/'