from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegisterForm
from .models import User
from .tokens import account_activation_token


def register(request):
    form = RegisterForm()
    error = ''

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Подтверждение регистрации - NoteApp'
            current_context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            html_content = get_template('registration/acc_active_email.html').render(current_context)
            to_email = form.cleaned_data.get('email')
            from_email = 'Note App <NoteAppTPU@yandex.ru>'
            msg = EmailMultiAlternatives(mail_subject, '', from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, 'registration/accept_sent.html', {})
        else:
            error = 'Ошибка при регистрации'
    context = {'form': form, 'error': error}
    return render(request, 'register/register.html', context)


def activate(request, uidb64, token):
    context = {'respond': ''}
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context['respond'] = 'Спасибо за подтверждение электронной почты. Теперь вы можете войти в свою учетную запись.'
        return render(request, 'registration/accept_respond.html', context)
    else:
        context['respond'] = 'Ссылка активации недействительна!'
        return render(request, 'registration/accept_respond.html', context)
