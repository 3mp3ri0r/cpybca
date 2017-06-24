
import os
import unittest

from configparser import ConfigParser

from cpybca.bca import Bca


class TestBca(unittest.TestCase):
    ''' Test BCA API connector module.
    '''

    def setUp(self):
        self.config = ConfigParser(strict=False)
        self.config.read(os.getenv('CONFIG', 'etc/development.ini'))
        self.bca = Bca(
            self.config.get('api', 'api_key'),
            self.config.get('api', 'api_secret', fallback=os.getenv('api_secret'))
        )

    def test_get_access_token(self):
        ''' Ensure module can get access token from BCA server.
        '''
        client_id = self.config.get('auth', 'client_id')
        client_secret = self.config.get(
            'auth', 'client_secret', fallback=os.getenv('client_secret')
        )
        access_token = self.bca.sign_in(client_id, client_secret)

        assert isinstance(access_token, bool)
        assert access_token

    def test_get_access_token_bad_client_id(self):
        ''' Ensure module raise error when user give wrong client_id.
        '''
        client_id = 'asdsad-sadsad-asdsa'
        client_secret = self.config.get(
            'auth', 'client_secret', fallback=os.getenv('client_secret')
        )
        with self.assertRaises(ValueError) as err:
            self.bca.sign_in(client_id, client_secret)

        assert err.exception.args[0] == 'Invalid client_id/client_secret/grant_type'

    def test_get_access_token_bad_client_secret(self):
        ''' Ensure module raise error when user give wrong client_secret.
        '''
        client_id = self.config.get('auth', 'client_id')
        client_secret = 'asdd-asdsd'
        with self.assertRaises(ValueError) as err:
            self.bca.sign_in(client_id, client_secret)

        assert err.exception.args[0] == 'Invalid client_id/client_secret/grant_type'
        self.assertEqual(err.exception.args[0], 'Invalid client_id/client_secret/grant_type')
