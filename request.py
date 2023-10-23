import requests


class AuthTest:
    def __init__(self, usr: str, pwd: str):
        self.usr = usr
        self.pwd = pwd

        self.access_token = ''
        self.refresh_token = ''

    def registrate(self):
        r = requests.post(
            url='http://127.0.0.1:8000/registrate',
            data={
                'usr': self.usr,
                'pwd': self.pwd
            }
        )

        result = r.status_code
        print(f'{result = }')


if __name__ == '__main__':
    auth = AuthTest(usr='kira', pwd='uffff_password')
    auth.registrate()
