
import datetime
import os
import unittest

from configparser import ConfigParser

from cpybca.bca import Bca


class TestFunctionalBca(unittest.TestCase):
    ''' Functional test of BCA API connector module.
    '''

    def setUp(self):
        self.config = ConfigParser(strict=False)
        self.config.read(os.getenv('CONFIG', 'etc/development.ini'))
        self.bca = Bca(
            self.config.get('api', 'api_key'),
            self.config.get('api', 'api_secret', fallback=os.getenv('api_secret'))
        )

        client_id = self.config.get('auth', 'client_id')
        client_secret = self.config.get(
            'auth', 'client_secret', fallback=os.getenv('client_secret')
        )
        self.bca.sign_in(client_id, client_secret)

    def test_get_balance(self):
        ''' Ensure module can get account balance.
        '''
        corporate_id = self.config.get('account', 'corporate_id')
        account_number = self.config.get('account', 'account_number')
        response = self.bca.get_balance(corporate_id, account_number)

        assert 'AccountDetailDataSuccess' in response
        account_detail_data_success = response['AccountDetailDataSuccess'][0]
        assert 'AccountNumber' in account_detail_data_success
        assert account_detail_data_success['AccountNumber'] == '0201245680'
        assert 'Plafon' in account_detail_data_success
        assert account_detail_data_success['Plafon'] == '0.00'
        assert 'Balance' in account_detail_data_success
        assert account_detail_data_success['Balance'] == '118849999.53'
        assert 'AvailableBalance' in account_detail_data_success
        assert account_detail_data_success['AvailableBalance'] == '118849999.53'
        assert 'FloatAmount' in account_detail_data_success
        assert account_detail_data_success['FloatAmount'] == '0.00'
        assert 'Currency' in account_detail_data_success
        assert account_detail_data_success['Currency'] == 'IDR'
        assert 'HoldAmount' in account_detail_data_success
        assert account_detail_data_success['HoldAmount'] == '0.00'

        assert 'AccountDetailDataFailed' in response
        assert not response['AccountDetailDataFailed']

    def test_get_multiple_balance(self):
        ''' Ensure module can get multiple account balance.
        '''
        corporate_id = self.config.get('account', 'corporate_id')
        account_number = self.config.get('account', 'account_number')
        account_number2 = self.config.get('account', 'account_number2')
        response = self.bca.get_balance(corporate_id, [account_number, account_number2])
        response_expected = {
            'AccountDetailDataSuccess': [{
                'AccountNumber': '0201245680',
                'Plafon': '0.00',
                'HoldAmount': '0.00',
                'Balance': '118849999.53',
                'Currency': 'IDR',
                'AvailableBalance': '118849999.53',
                'FloatAmount': '0.00'
            }, {
                'AccountNumber': '0063001004',
                'Plafon': '0.00',
                'HoldAmount': '0.00',
                'Balance': '69942987.27',
                'Currency': 'IDR',
                'AvailableBalance': '69942987.27',
                'FloatAmount': '0.00'
            }],
            'AccountDetailDataFailed': []
        }

        assert response == response_expected

    def test_get_balance_wrong_account(self):
        ''' Ensure module get an error when entering wrong account number.
        '''
        corporate_id = self.config.get('account', 'corporate_id')
        account_number = 'asdsadsad'
        response = self.bca.get_balance(corporate_id, account_number)

        assert 'AccountDetailDataFailed' in response
        account_detail_data_failed = response['AccountDetailDataFailed'][0]
        assert 'English' in account_detail_data_failed
        assert account_detail_data_failed['English'] == 'Invalid AccountNumber'
        assert 'Indonesian' in account_detail_data_failed
        assert account_detail_data_failed['Indonesian'] == 'AccountNumber Tidak Valid'
        assert 'AccountNumber' in account_detail_data_failed

        assert 'AccountDetailSuccess' in response
        assert not response['AccountDetailSuccess']

    def test_get_multiple_balance_right_and_wrong_account(self):
        ''' Ensure module get balance for the right account and fail for the wrong account.
        '''
        corporate_id = self.config.get('account', 'corporate_id')
        account_number = self.config.get('account', 'account_number')
        account_number2 = self.config.get('account', 'account_number2')
        account_number3 = '1111111111'
        response = self.bca.get_balance(
            corporate_id,
            [account_number, account_number2, account_number3]
        )
        response_expected = {
            'AccountDetailDataSuccess': [{
                'AccountNumber': '0201245680',
                'Plafon': '0.00',
                'HoldAmount': '0.00',
                'Balance': '118849999.53',
                'Currency': 'IDR',
                'AvailableBalance': '118849999.53',
                'FloatAmount': '0.00'
            }, {
                'AccountNumber': '0063001004',
                'Plafon': '0.00',
                'HoldAmount': '0.00',
                'Balance': '69942987.27',
                'Currency': 'IDR',
                'AvailableBalance': '69942987.27',
                'FloatAmount': '0.00'
            }],
            'AccountDetailDataFailed': [{
                'English': 'Invalid AccountNumber',
                'Indonesian': 'AccountNumber Tidak Valid',
                'AccountNumber': '1111111111'
            }]
        }

        assert response == response_expected

    def test_get_balance_more_then_20_account(self):
        ''' Ensure module raise error when user check balance for more than 20 account.
        '''
        corporate_id = self.config.get('account', 'corporate_id')
        with self.assertRaises(ValueError) as err:
            self.bca.get_balance(
                corporate_id,
                ['123', '123', '123', '123', '123', '123', '123', '123', '123', '123', '123',
                 '123', '123', '123', '123', '123', '123', '123', '123', '123', '123']
            )

        assert err.exception.args[0] == 'Maximum account number is 20'

    def test_get_statement(self):
        ''' Ensure module can get account statement.
        '''
        corporate_id = self.config.get('account', 'corporate_id')
        account_number = self.config.get('account', 'account_number')
        start_date = '2016-09-01'
        end_date = '2016-09-01'
        response = self.bca.get_statement(corporate_id, account_number, start_date, end_date)
        response_expected = {
            "StartDate": "2016-09-01",
            "EndDate"   : "2016-09-01",
            "Currency" : "IDR",
            "StartBalance" : "94163880.00",
            "Data": [
                {
                    "TransactionDate":"PEND",
                    "BranchCode":"0000",
                    "TransactionType":"D",
                    "TransactionAmount":"100000.00",
                    "TransactionName":"TRSF E-BANKING DB",
                    "Trailer":"0109/FTSCY/WS95051 100000.00 Online Transfer   PT DUMMY2"
                }, {
                    "TransactionDate":"PEND",
                    "BranchCode":"0061",
                    "TransactionType":"C",
                    "TransactionAmount":"3000000.00",
                    "TransactionName":"NK - LLG",
                    "Trailer":""
                }, {
                    "TransactionDate":"PEND",
                    "BranchCode":"0000",
                    "TransactionType":"D",
                    "TransactionAmount":"250000.00",
                    "TransactionName":"TRSF E-BANKING DB",
                    "Trailer":"0109/FTSCY/WS95051 250800.00 Transfer DUMMY1"
                }, {
                    "TransactionDate":"PEND",
                    "BranchCode":"0000",
                    "TransactionType":"D",
                    "TransactionAmount":"100000.00",
                    "TransactionName":"BA JASA E-BANKING",
                    "Trailer":"0109/TRCHG/WS95051BIAYA TRANSFER SME"
                }, {
                    "TransactionDate":"PEND",
                    "BranchCode":"0101",
                    "TransactionType":"C",
                    "TransactionAmount":"10000.00",
                    "TransactionName":"KR OTOMATIS",
                    "Trailer":"DUMMY7  039903811112"
                }, {
                    "TransactionDate":"PEND",
                    "BranchCode":"0038",
                    "TransactionType":"D",
                    "TransactionAmount":"100000.00",
                    "TransactionName":"TARIKAN TUNAI",
                    "Trailer":""
                }
            ]
        }

        assert response == response_expected

    def test_transfer(self):
        ''' Ensure module can transfer fund.
        '''
        corporate_id = self.config.get('account', 'corporate_id')
        source_account_number = self.config.get('account', 'account_number')
        beneficiary_account_number = self.config.get('account', 'beneficiary_account_number')
        transaction_id = '00000021'
        transaction_date = str(datetime.datetime.now(
            datetime.timezone(datetime.timedelta(0, 25200), 'WIB')))
        reference_id = '43287/DP/2017'
        amount = '100000.00'
        currency_code = 'IDR'
        remark1 = 'Transfer Test'
        remark2 = 'Online Transfer'
        response = self.bca.transfer(
            corporate_id, source_account_number, beneficiary_account_number, transaction_id,
            transaction_date, reference_id, amount, currency_code, remark1, remark2
        )
        response_expected = {
            "TransactionID" : transaction_id,
            "TransactionDate" : transaction_date,
            "ReferenceID" : reference_id,
            "Status" : "Success"
        }

        assert response == response_expected

# Check false request to get_statement and transfer. Try to transfer to closed account.