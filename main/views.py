from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import RandomNumber, State, Token
from requests_oauthlib import OAuth2Session
import jsonpickle

client_id = "0f608ff5be0866cb348b"
secret = "25e330b41fff48eebe9ed8154bf6ce2390f9aa2b"
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


# Create your views here.

def is_authenticated(request):
    try:
        token = Token.objects.get(token=request.COOKIES.get('github_token', None))
        return True
    except ObjectDoesNotExist:
        return False


def index(request):
    if is_authenticated(request):
        context = {
            'number': RandomNumber.objects.get(pk=1).number
        }
        response = render(request, 'index.html', context)
    else:
        github = OAuth2Session(client_id)
        authorization_url, state = github.authorization_url(authorization_base_url)
        # session = Session.objects.create(session=jsonpickle.encode(github))
        state_object = State.objects.create(state=state)
        context = {
            'link': authorization_url + '&redirect_uri=http://{}/main/authorize'.format(request.get_host())
        }
        response = render(request, 'index.html', context)

        response.set_cookie('validation_number', state_object.pk)
    return response


def authorize(request):
    if request.GET.get('code', False):
        code = request.GET['code']
    else:
        return HttpResponse('Please pass a code')
    if request.GET.get('state', False):
        state = request.GET['state']
    else:
        return HttpResponse('Please pass a state')
    if request.COOKIES.get('validation_number', False):
        valid_num = request.COOKIES['validation_number']
        real_state = State.objects.get(pk=valid_num).state
        github = OAuth2Session(client_id)
        if state == real_state:
            github.authorization_url(authorization_base_url, real_state)
            try:
                github.fetch_token(token_url, client_secret=secret,
                                   authorization_response="https://{}".format(request.get_host()) + request.path + "?" + request.META[
                                       'QUERY_STRING'])
            except ValueError as e:
                print(type(e))
            if github.authorized:
                token = Token.objects.create(token=github.token)
                context = {
                    'number': RandomNumber.objects.get(pk=1).number
                }
                response = redirect('index')
                response.set_cookie('github_token', github.token)
                response.delete_cookie('validation_number')
                return response
        else:
            return HttpResponse("wrong state")
    else:
        return HttpResponse('You have no cookie "validation_number"')


@require_POST
def get_rnd_number(request):
    if is_authenticated(request):
        return JsonResponse({'number': RandomNumber.objects.get(pk=1).number})
    else:
        return JsonResponse({'error': 'unauthorized'}, code=401)
