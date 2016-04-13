"""
AUTHOR: EDDY FAKHRY
DATE:   15/10/2016
"""
from time import time
from itsdangerous import URLSafeSerializer
import constants


class LinkGenerator:
    """
    Link to personalised form in email
    """
    DELIMITER = ';'

    def __init__(self, app):
        self._app = app
        self._serializer = URLSafeSerializer(app.config['SECRET_KEY'])

    def generate_payload(self, gala_id, club_id, swimmer_id):
        """
        Include identifiers in payload
        :param gala_id:
        :param club_id:
        :param swimmer_id:
        """
        payload = str(time()) + self.DELIMITER + str(gala_id) + self.DELIMITER + str(club_id) + \
                  self.DELIMITER + str(swimmer_id)
        return self._serializer.dumps(payload, salt=constants.LINK_GENERATOR_SALT)

    def load_payload(self, payload):
        """
        Retrieve identifiers from payload
        :param payload:
        """
        plain_payload = self._serializer.loads(payload, salt=constants.LINK_GENERATOR_SALT)
        try:
            plain_payload = plain_payload.split(self.DELIMITER)
            return {'gala_id': plain_payload[1], 'club_id': plain_payload[2], 'swimmer_id': plain_payload[3]}
        except:
            raise ValueError('Invalid payload format detected.')