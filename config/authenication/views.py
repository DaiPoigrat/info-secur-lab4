from django.http.response import HttpResponse
from .models import AuthUserModel
from django.conf import settings
from .utils import make_user_hash, generate_access, generate_refresh, decode_token


# Create your views here.

def registrate(request):
    reg_data = request.POST.dict()

    usr = reg_data.get('usr', None)
    pwd = reg_data.get('pwd', None)

    print(f'{usr = }')
    print(f'{pwd = }')

    if all((usr, pwd)):
        try:
            user = AuthUserModel(
                usr=usr,
                hash=make_user_hash(usr=usr, salt=settings.SALT, pwd=pwd)
            )
            user.save()

        except Exception as e:
            return HttpResponse(
                status=400,
                data={
                    'error': e
                }
            )

        return HttpResponse(status=201)

    return HttpResponse(
        status=400,
        data={
            'error': 'wrong input data'
        }
    )


def auth(request):
    reg_data = request.POST.dict()

    usr = reg_data.get('usr', None)
    pwd = reg_data.get('pwd', None)

    print(f'{usr = }')
    print(f'{pwd = }')

    if all((usr, pwd)):
        try:
            user_hash = make_user_hash(usr=usr, salt=settings.SALT, pwd=pwd)
            user = AuthUserModel.objects.get(hash=user_hash)
            if not user:
                return HttpResponse(
                    status=400,
                    data={
                        'error': 'wrong input data'
                    }
                )

            access_token = generate_access(hash=user_hash)
            response = HttpResponse(status=200).set_cookie('Access-Token', access_token, httponly=True)

            return response

        except Exception as e:
            return HttpResponse(
                status=400,
                data={
                    'error': e
                }
            )
    else:
        return HttpResponse(
            status=400,
            data={
                'error': 'wrong input data'
            }
        )


def refresh(request):
    cookie = request.COOKIES.get('Refresh-Token', None)

    if cookie:
        refresh_token = decode_token(token=cookie)
        print(f'DECODED {refresh_token = }')

    else:

        reg_data = request.POST.dict()

        usr = reg_data.get('usr', None)
        pwd = reg_data.get('pwd', None)

        print(f'{usr = }')
        print(f'{pwd = }')

        if all((usr, pwd)):
            try:
                user_hash = make_user_hash(usr=usr, salt=settings.SALT, pwd=pwd)
                user = AuthUserModel.objects.get(hash=user_hash)
                if not user:
                    return HttpResponse(
                        status=400,
                        data={
                            'error': 'wrong input data'
                        }
                    )

                access_token = generate_refresh(hash=user_hash)
                response = HttpResponse(status=200).set_cookie('Refresh-Token', access_token, httponly=True)

                return response

            except Exception as e:
                return HttpResponse(
                    status=400,
                    data={
                        'error': e
                    }
                )
        else:
            return HttpResponse(
                status=400,
                data={
                    'error': 'wrong input data'
                }
            )
