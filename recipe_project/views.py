from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:list')
        else:
            error_message = 'Something went wrong, Please try again'

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')


def media(request, file_path=None):
    from django.conf import settings as cfg
    media_root = getattr(cfg, 'MEDIA_ROOT', None)

    if not media_root:
        return HttpResponseBadRequest('Invalid Media Root Configuration')
    if not file_path:
        return HttpResponseBadRequest('Invalid File Path')

    with open(os.path.join(media_root, file_path), 'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/doc')
        response['Content-Disposition'] = 'filename=%s' % (file_path.split('/')[-1])
        return response