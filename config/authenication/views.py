from datetime import datetime

from django.http.response import HttpResponse
from .models import AuthUserModel
from django.conf import settings
from .utils import make_user_hash, generate_access, generate_refresh, decode_token
from django.core.exceptions import ObjectDoesNotExist


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
            refresh_token = generate_refresh(hash=user_hash)
            response = HttpResponse(status=200)
            response.set_cookie('Access-Token', access_token, httponly=True, path='')
            response.set_cookie('Refresh-Token', refresh_token, httponly=True, path='/refresh')

            return response

        except ObjectDoesNotExist:
            return HttpResponse(status=403)

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

        try:
            exp_time = refresh_token.get('exp', None)

            if not exp_time or exp_time < int(datetime.utcnow().timestamp()):
                return HttpResponse(status=403)

            user_hash = refresh_token.get('user_hash', None)

            if not user_hash:
                return HttpResponse(status=403)

            try:
                user = AuthUserModel.objects.get(hash=user_hash)

                access_token = generate_access(hash=user_hash)
                refresh_token = generate_refresh(hash=user_hash)
                response = HttpResponse(status=200)
                response.set_cookie('Access-Token', access_token, httponly=True)
                response.set_cookie('Refresh-Token', refresh_token, httponly=True)

                return response
            except Exception as e:
                print(e)
                return HttpResponse(status=403)

        except Exception as e:
            print(e)
            return HttpResponse(status=403)

    else:
        return HttpResponse(status=403)

    # else:
    #
    #     reg_data = request.POST.dict()
    #
    #     usr = reg_data.get('usr', None)
    #     pwd = reg_data.get('pwd', None)
    #
    #     print(f'{usr = }')
    #     print(f'{pwd = }')
    #
    #     if all((usr, pwd)):
    #         try:
    #             user_hash = make_user_hash(usr=usr, salt=settings.SALT, pwd=pwd)
    #             user = AuthUserModel.objects.get(hash=user_hash)
    #             if not user:
    #                 return HttpResponse(
    #                     status=400,
    #                     data={
    #                         'error': 'wrong input data'
    #                     }
    #                 )
    #
    #             access_token = generate_refresh(hash=user_hash)
    #             response = HttpResponse(status=200).set_cookie('Refresh-Token', access_token, httponly=True)
    #
    #             return response
    #
    #         except Exception as e:
    #             return HttpResponse(
    #                 status=400,
    #                 data={
    #                     'error': e
    #                 }
    #             )
    #     else:
    #         return HttpResponse(
    #             status=400,
    #             data={
    #                 'error': 'wrong input data'
    #             }
    #         )
