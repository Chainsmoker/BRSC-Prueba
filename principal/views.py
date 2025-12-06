from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from apps.centro_costos.models import NuevoGasto

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.db import connection

User = get_user_model()

##########################################################################
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def forgot_password(request):
    if request.method == 'POST':
        print("POST")
        email = request.POST['email']
        print(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            print(user)
            # send reset password email
            mail_subject = 'Restablecer su contraseña'
            email_template = 'email/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'email/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Por favor restablezca su contraseña')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'email/reset_password.html')
##########################################################################


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Cambia según el nombre de tu vista home
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos.'})

    return render(request, 'login.html')

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.control_expediente.models import Seguimiento


# @login_required
# def home(request):
#     # ✅ Si el usuario tiene rol LEGAL (role = 2)
#     if hasattr(request.user, 'role') and request.user.role == 2:
    
#         with connection.cursor() as cursor:
#             # Ejecutamos el SP pasando request.user.id como parámetro
#             cursor.execute("EXEC dbo.sp_get_alertas_expedientes @responsable=%s", [request.user.id])
            
#             columns = [col[0] for col in cursor.description]
#             resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         print(resultados)
#         print(type(resultados))

#         #return render(request, 'home_legal_original.html', {
#         return render(request, 'home_legal_modificado.html', {
#             'pendientes': resultados
#         })


#     # ✅ Otros roles → home normal
#     return render(request, 'home.html')



@login_required
def home(request):

    if hasattr(request.user, 'role') and request.user.role == 2:

        with connection.cursor() as cursor:
            cursor.execute("EXEC dbo.sp_get_alertas_expedientes @responsable=%s", [request.user.id])
            columns = [col[0] for col in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Filtrar según tipo_alerta
        expedientes = [r for r in resultados if r["tipo_alerta"] == "EXPEDIENTE"]
        tramites = [r for r in resultados if r["tipo_alerta"] == "TRAMITE"]
        exp_penal = [r for r in resultados if r["tipo_alerta"] in ("CPENAL", "CFISCAL")]

        return render(request, 'home_legal_modificado.html', {
            'expedientes': expedientes,
            'tramites': tramites,
            'exp_penal': exp_penal
        })

    return render(request, 'home.html')




def int_art(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'sistemas/test.html')
    
@login_required(login_url='login')
def perfil_user(request):
    user = request.user

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PerfilUsuarioForm(instance=user)

    return render(request, 'sistemas/perfil_user.html', {'form': form, 'user': user})


@login_required
def lista_usuarios(request):
    usuarios = User.objects.filter(is_active=True).order_by('username')
    ccs = NuevoGasto.objects.filter(flag=True)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])  # Hashea la contraseña
            usuario.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UserForm()

    return render(request, 'administrador/home.html', {
        'usuarios': usuarios,
        'form': form,
        'ccs': ccs
    })


@login_required
def editar_usuario(request):
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=request.POST.get('id'))
        form = UserEditForm(request.POST, instance=usuario)

        if form.is_valid():
            print(form)
            print(form.is_valid())
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Usuario actualizado correctamente.")
        else:
            print("Errores del formulario:", form.errors)  # Aquí se imprimen los errores
            messages.error(request, "Hubo un error al actualizar el usuario.")

    return redirect('lista_usuarios')

from apps.centro_costos.forms import NuevoGastoForm

@login_required
def editar_CC(request):
    if request.method == 'POST':
        cc = get_object_or_404(NuevoGasto, id=request.POST.get('id'))
        form = NuevoGastoForm(request.POST, instance=cc)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Actualizado correctamente.")
        else:
            messages.error(request, "Hubo un error al actualizar.")

    return redirect('lista_usuarios')

@login_required
def eliminar_CC(request, id):
    cc = get_object_or_404(NuevoGasto, id=id)
    cc.flag = False
    cc.nombre = ''
    cc.save()  # Guardar los cambios en la base de datos
    return redirect('lista_usuarios')

@login_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.is_active = False   # ← DESACTIVA EL USUARIO
    usuario.save()              # ← GUARDA CAMBIO
    return redirect('lista_usuarios')


def cambiar_password_usuario(request):
    if request.method == "POST":
        user_id = request.POST.get("id")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        print(user_id)
        print(password)
        print(confirm_password)
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('lista_usuarios')

        try:
            user = User.objects.get(id=user_id)
            user.password = make_password(password)  # Hashear la contraseña
            user.save()
            messages.success(request, "Contraseña actualizada correctamente.")
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")

    return redirect('lista_usuarios')