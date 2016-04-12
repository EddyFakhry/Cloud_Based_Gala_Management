import pytest

from lib.mongo import Mongo
from lib.email import Mailer
from lib.linkgenerator import LinkGenerator
import  datetime
import  constants

from flask import render_template, url_for

class TestApp:
    swimmers = [
        {'class': '7',
         'club_id': 'CCRR',
         'dob': datetime.datetime(1988, 1, 1, 0, 0),
         'email': None,
         'first': 'Arrianne',
         'group': 'G',
         'inactive': False,
         'id': 85,
         'last': 'Weisner',
         'mailTo': 'Patrick & Wendi Weisner',
         'sex': 'F',
         'swimmer_id': '010188ARRNWEIS'},
        {'class': '9',
         'club_id': 'CCRR',
         'dob': datetime.datetime(1986, 1, 2, 0, 0),
         'email': 'test1@test.com',
         'first': 'Robert',
         'group': 'G',
         'inactive': False,
         'id': 75,
         'last': 'Orbison',
         'mailTo': 'Andrew & Susan Orbison',
         'sex': 'M',
         'swimmer_id': '010286ROBAORBI'},
        {'class': '6',
         'club_id': 'CCRR',
         'dob': datetime.datetime(1989, 1, 10, 0, 0),
         'email': 'test@test.com',
         'first': 'Kelly',
         'group': 'G',
         'id': 311,
         'inactive': False,
         'last': 'Walton',
         'mailTo': 'Dana & Trey Walton',
         'sex': 'F',
         'swimmer_id': '011089KELBWALT'}]




###############CREATE ############################"



    def test_create_unauthorized(self, client, mocker):

        mocker.patch('Mongo.swimmers', return_value={"find": self.swimmers})
        mocker.patch.object(Mailer, 'send_email', return_value="")
        mocker.patch.object(LinkGenerator, 'generate_payload', return_value="")

        expected_got_email = []
        expected_no_email = []

        for swimmer in self.swimmers:
            if swimmer["email"] is None:
                expected_no_email.append({"swimmer" : swimmer, "link" : constants.FORM_ADDRESS})
            else :
                expected_got_email.append({"swimmer" : swimmer, "link" : constants.FORM_ADDRESS})

        expected = render_template("sentemail.html", got_email=expected_got_email,
                                                no_email=expected_no_email, gala_id="Gala ID")
        result = client.get(url_for("send_emails",club_id="CCRR", gala_id="Gala ID"))

        assert expected == result