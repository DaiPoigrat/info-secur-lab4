import time

import requests


class AuthTest:
    def __init__(self, usr: str, pwd: str):
        self.usr = usr
        self.pwd = pwd

        self.access_token = ''
        self.refresh_token = ''

    def registrate(self):
        print('REGISTRATE')
        r = requests.post(
            url='http://127.0.0.1:80/registrate',
            data={
                'usr': self.usr,
                'pwd': self.pwd
            }
        )

        result = r.status_code
        print(f'{result = }')

    def get_auth(self):
        print('GET AUTH TOKENS')
        r = requests.post(
            url='http://127.0.0.1:80/auth',
            data={
                'usr': self.usr,
                'pwd': self.pwd
            }
        )

        result = r.status_code
        print(f'{result = }')
        if result == 200:
            cookies = r.cookies
            self.access_token = cookies.get('Access-Token')
            self.refresh_token = cookies.get('Refresh-Token')
            print(f'{self.access_token = }')
            print(f'{self.refresh_token = }')

    def refresh(self):
        print('REFRESH AUTH TOKENS')
        r = requests.post(
            url='http://127.0.0.1:80/refresh',
            cookies={
                'Refresh-Token': self.refresh_token
            }
        )

        result = r.status_code
        print(f'{result = }')
        if result == 200:
            print('PREV')
            print(f'{self.access_token = }')
            print(f'{self.refresh_token = }')
            print('NOW')
            cookies = r.cookies
            self.access_token = cookies.get('Access-Token')
            self.refresh_token = cookies.get('Refresh-Token')
            print(f'{self.access_token = }')
            print(f'{self.refresh_token = }')


if __name__ == '__main__':
    auth = AuthTest(usr='uuff_user', pwd='12345')
    # auth.registrate()
    time.sleep(3)
    auth.get_auth()
    time.sleep(5)
    auth.refresh()

