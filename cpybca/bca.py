
import base64
import datetime
import hashlib
import hmac
import json
import urllib.request
import urllib.error

class Bca():
    ''' Module to integrate with BCA API.
    '''

    def __init__(self, api_key, api_secret, host='https://sandbox.bca.co.id'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = ''

        self.host = host
        self.oauth_path = '/api/oauth/token'
        self.get_balance_path = '/banking/v2/corporates/{corporate_id}/accounts/{account_number}'
        self.get_statement_path = '/banking/v2/corporates/{corporate_id}/accounts/' \
            '{account_number}/statements?EndDate={end_date}&StartDate={start_date}'
        self.transfer_path = '/banking/corporates/transfers'

    def _open_url(self, url, data=None, headers=None):
        ''' Helper to call urlopen
        '''
        try:
            if data:
                request = urllib.request.Request(url, data=data, headers=headers)
            else:
                request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                response_data = json.loads(response.read().decode('UTF-8'))
                return response_data
        except urllib.error.HTTPError as err:
            error_content = json.loads(err.read().decode('UTF-8'))
            # print(error_content)
            raise ValueError(error_content['ErrorMessage']['English'])
        except urllib.error.URLError:
            raise ValueError('Something wrong with network connection or server')

    def _generate_signature(self, relative_url, timestamp, http_method='GET', request_body=b''):
        ''' Generate signature to be sent.
        '''
        signature = hmac.new(self.api_secret.encode(), digestmod=hashlib.sha256)
        string_to_sign = http_method + ':' + relative_url + ':' + self.access_token + \
            ':' + hashlib.sha256(request_body.replace(b' ', b'')).hexdigest() + ':' + timestamp
        signature.update(string_to_sign.encode())
        return signature.hexdigest()

    def sign_in(self, client_id, client_secret):
        ''' Signing in client and get access token.
        '''
        url = self.host + self.oauth_path
        data = b'grant_type=client_credentials'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + \
                base64.b64encode(str.encode(client_id + ':' + client_secret)).decode('UTF-8')
        }
        response_data = self._open_url(url, data=data, headers=headers)
        if 'access_token' in response_data:
            self.access_token = response_data['access_token']
            return True
        return response_data

    def get_balance(self, corporate_id, account_number):
        ''' Get balance from account.
        '''
        if isinstance(account_number, list):
            if len(account_number) > 20:
                raise ValueError('Maximum account number is 20')
        relative_url = self.get_balance_path.format(**{
            'corporate_id': corporate_id,
            # Using '%2C' instead ',' because url does not know comma.
            # Avoid using parse.quote to reduce memory consumption.
            'account_number': '%2C'.join(account_number) \
                if isinstance(account_number, list) else account_number
        })
        url = self.host + relative_url

        timestamp = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
        timestamp = timestamp[:23] + timestamp[26:]
        signature = self._generate_signature(relative_url, timestamp)

        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'application/json',
            'Origin': 'cpybca.com',
            'X-BCA-Key': self.api_key,
            'X-BCA-Timestamp': timestamp,
            'X-BCA-Signature': signature
        }

        response_data = self._open_url(url, headers=headers)
        return response_data

    def get_statement(self, corporate_id, account_number, start_date, end_date=None):
        ''' Get account statement.
        '''
        relative_url = self.get_statement_path.format(**{
            'corporate_id': corporate_id,
            'account_number': account_number,
            'start_date': start_date,
            'end_date': end_date if end_date else start_date
        })
        url = self.host + relative_url

        timestamp = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
        timestamp = timestamp[:23] + timestamp[26:]
        signature = self._generate_signature(relative_url, timestamp)

        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'application/json',
            'Origin': 'cpybca.com',
            'X-BCA-Key': self.api_key,
            'X-BCA-Timestamp': timestamp,
            'X-BCA-Signature': signature
        }

        response_data = self._open_url(url, headers=headers)
        return response_data

    def transfer(self, corporate_id, source_account_number, beneficiary_account_number,
                 transaction_id, transaction_date, reference_id, amount, currency_code='IDR',
                 remark1=None, remark2=None):
        ''' Transfer fund to other account.
        '''
        relative_url = self.transfer_path
        url = self.host + relative_url

        timestamp = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
        timestamp = timestamp[:23] + timestamp[26:]
        request_body = {
            'CorporateID': corporate_id,
            'SourceAccountNumber': source_account_number,
            'TransactionID': transaction_id,
            'TransactionDate': transaction_date,
            'ReferenceID': reference_id,
            'CurrencyCode': currency_code,
            'Amount': amount,
            'BeneficiaryAccountNumber': beneficiary_account_number
        }
        if remark1:
            request_body['Remark1'] = remark1
        if remark2:
            request_body['Remark2'] = remark2
        data = json.dumps(request_body, separators=(',', ':')).encode()
        signature = self._generate_signature(relative_url, timestamp, 'POST', data)

        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'application/json',
            'Origin': 'cpybca.com',
            'X-BCA-Key': self.api_key,
            'X-BCA-Timestamp': timestamp,
            'X-BCA-Signature': signature
        }

        response_data = self._open_url(url, data=data, headers=headers)
        return response_data
