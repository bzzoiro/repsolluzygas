import requests
import logging

_LOGGER = logging.getLogger(__name__)


class RepsolLuzYGasSensor():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    cookies = {
            'gmid': 'gmid.ver4.AcbHSBMhFw.1PO5AEWAU-E5wcBXeuZT_c_uz5VVE_t3ZPwM8tKdJgOFsVf0lDmNsBlpecXxwdf0.Zo36FXG0Nnu7Dxd6z0ZedVvVW6U-G9DQlNq1ofie-ez5wHw5SuID3P6jzqbLsuL7BIPqFup0n6D4LSsjS7YKPg.sc3',
            'ucid': 'TiA7xpk2tJCJIn50B0CuzQ',
            'hasGmid': 'ver4',
            'gig_bootstrap_3_2MAJfXPA8zGLzfv2TRlhKGs3d6WdNsLU8unCCIGFhXMo9Ry49fG9k-aWG4SQY9_B': 'gigya_ver4',
             }

    def login(self): 

        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '^\\^Google',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': 'https://areacliente.repsolluzygas.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'en-US,en;q=0.9',
            'Market': 'ML',
        }

        data = {
        'loginID': self.username,
        'password': self.password,
        'targetEnv': 'jssdk',
        'includeUserInfo': 'true',
        'lang': 'en',
        'APIKey': '3_2MAJfXPA8zGLzfv2TRlhKGs3d6WdNsLU8unCCIGFhXMo9Ry49fG9k-aWG4SQY9_B',
        'format': 'json'
        }

        response = requests.post('https://gigya.repsolluzygas.com/accounts.login', headers=headers, cookies=self.cookies, data=data)
        data = response.json()
        _LOGGER.debug('Login Data {}'.format(data))
        if not data:
            raise Exception('Invalid Session ID')

        #session_id = data['sessionInfo']['login_token']
        #apikey = data['userInfo']['loginProviderUID']
        uid = data['userInfo']['UID']
        signature = data['userInfo']['UIDSignature']
        tstamp = data['userInfo']['signatureTimestamp']
        return uid, signature, tstamp


    def get_contracts(self, uid, signature, tstamp):

        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '^\\^Google',
            'x-origin': 'WEB',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'UID': uid,
            'signature': signature,
            'signatureTimestamp': tstamp,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://areacliente.repsolluzygas.com/mis-hogares',
            'Accept-Language': 'en-US,en;q=0.9',
            'Market': 'ML',
        }

        response = requests.get('https://areacliente.repsolluzygas.com/api/v2/houses', headers=headers, cookies=self.cookies)
        data = response.json()
        _LOGGER.debug('Contracts Data {}'.format(data))
        contracts = {}

        data = data[0]
        contracts['house_id'] = data['code']
        contracts['number_of_contracts'] = len(data['contracts'])
        contracts['information'] = []
        for contract in data['contracts']:
            info = {}
            info['contract_id'] = contract['code']
            info['type'] = contract['contractType']
            info['active'] = contract['status'] == 'ACTIVE'
            contracts['information'].append(info)

        _LOGGER.debug('Contracts Parsed {}'.format(contracts))

        return contracts
    
    def get_invoices(self, uid, signature, tstamp, house_id, contract_id):
        
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '^\\^Google',
            'x-origin': 'WEB',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'UID': uid,
            'signature': signature,
            'signatureTimestamp': tstamp,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://areacliente.repsolluzygas.com/mis-hogares',
            'Accept-Language': 'en-US,en;q=0.9',
            'Market': 'ML',
        }

        response = requests.get('https://areacliente.repsolluzygas.com/api/v2/houses/{}/products/{}/invoices?limit=1'.format(house_id, contract_id), headers=headers, cookies=self.cookies)
        response = response.json()

        _LOGGER.debug('Invoices Data {}'.format(response))
        return response

    def get_costs(self, uid, signature, tstamp, house_id, contract_id):
        
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '^\\^Google',
            'x-origin': 'WEB',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'UID': uid,
            'signature': signature,
            'signatureTimestamp': tstamp,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://areacliente.repsolluzygas.com/mis-hogares',
            'Accept-Language': 'en-US,en;q=0.9',
            'Market': 'ML',
        }

        response = requests.get('https://areacliente.repsolluzygas.com/api/v2/houses/{}/products/{}/consumption/accumulated'.format(house_id, contract_id), headers=headers, cookies=self.cookies)
        response = response.json()
         
        vars = ['totalDays', 'consumption', 'amount', 'amountVariable', 'amountFixed', 'averageAmount'] 
        data = {}

        for var in vars:
            data[var] = response.get(var, 0)

        _LOGGER.debug('Costs Data {}'.format(data))
        return data

    def get_next_invoice(self, uid, signature, tstamp, house_id, contract_id):
        
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '^\\^Google',
            'x-origin': 'WEB',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'UID': uid,
            'signature': signature,
            'signatureTimestamp': tstamp,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://areacliente.repsolluzygas.com/mis-hogares',
            'Accept-Language': 'en-US,en;q=0.9',
            'Market': 'ML',
        }

        response = requests.get('https://areacliente.repsolluzygas.com/api/v2/houses/{}/products/{}/consumption/invoice-estimate'.format(house_id, contract_id), headers=headers, cookies=self.cookies)
        response = response.json()
         
        vars = ['amount', 'amountVariable', 'amountFixed'] 
        data = {}

        for var in vars:
            data[var] = response.get(var, 0)

        _LOGGER.debug('Next Invoice Estimated Cost Data {}'.format(data))
        return data

    def update(self):

        uid, signature, tstamp = self.login()
        contracts = self.get_contracts(uid, signature, tstamp)
        
        data = {'consumption': 0, 'amount': 0, 'amountVariable': 0, 'amountFixed': 0, 'averageAmount': 0}
        for contract in contracts['information']:
            if not contract['active']:
                continue
            response = self.get_costs(uid, signature, tstamp, contracts['house_id'], contract['contract_id'])
            for var in data:
                data[var] += response[var]

        if response['totalDays'] > 0:
            data['totalDays'] = response['totalDays']
            data['averageAmount'] = response['averageAmount']
            data['number_of_contracts'] = contracts['number_of_contracts']

        if contracts and contracts['information']:
            invoices = self.get_invoices(uid, signature, tstamp, contracts['house_id'], contracts['information'][0]['contract_id'])
            if invoices:
                if invoices[0].get('amount'):
                    data['last_invoice_amount'] = invoices[0]['amount']
                if invoices[0].get('status'):
                    data['last_invoice_paid'] = invoices[0]['status'] == 'PAID'
                    
            next_invoice = self.get_next_invoice(uid, signature, tstamp, contracts['house_id'], contracts['information'][0]['contract_id'])
            if next_invoice:
                data['nextInvoice'] = next_invoice['amount']

        self.data = data

        _LOGGER.debug('Sensor Data {}'.format(self.data))
        return True
