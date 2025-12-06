from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from apps.control_expediente.models import RegistroActividad
from django.utils import timezone

# Create your views here.
@login_required
def lista_proyectos(request):
    form = ProyectoForm()

    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            RegistroActividad.objects.create(
                nombre = f"{request.user.first_name} {request.user.last_name}".strip(),
                fecha = timezone.now(),
                actividad = f"[CANTA CALLAO] Registró un nuevo proyecto: {form.save().proyecto}",
                user_id = request.user.id,
            )

            return redirect('p_canta_callao:lista_proyectos')
        else:
            print("Errores en el formulario:", form.errors)

    caso_judiciales = Proyecto.objects.all()
    registro_actividad = RegistroActividad.objects.all()


    return render(request, 'proyecto_canta_callao/home.html', {
        'form': form,
        'caso_judiciales': caso_judiciales,
        'registro_actividad': registro_actividad,
    })




def editar_proyecto(request):
    if request.method == 'POST':
        cj_id = request.POST.get('id')
        cj = get_object_or_404(Proyecto, id=cj_id)

        form = ProyectoForm(request.POST, request.FILES, instance=cj)
        
        if form.is_valid():
            form.save()

            return redirect('p_canta_callao:lista_proyectos')
        else:
            return redirect('p_canta_callao:lista_proyectos')
    return redirect('p_canta_callao:lista_proyectos')



def eliminar_proyecto(request, doc_id):
    doc = get_object_or_404(Proyecto, id=doc_id)
    doc.delete()

    return redirect('p_canta_callao:lista_proyectos')

#####################################################################################################



def ver_actividades(request, caso_id):
    caso = get_object_or_404(Proyecto, id=caso_id)

    if request.method == 'POST':
        tipo_formulario = request.POST.get('tipo_formulario')
        seguimiento_id = request.POST.get('seguimiento_id')

        # Editar actividad existente
        if tipo_formulario == 'editar_seguimiento' and seguimiento_id:
            seguimiento = get_object_or_404(Actividad, id=seguimiento_id)
            form = ActividadForm(request.POST, request.FILES, instance=seguimiento)
            if form.is_valid():
                actividad = form.save(commit=False)
                actividad.editor = f"{request.user.first_name} {request.user.last_name}"
                actividad.save()
                return redirect('p_canta_callao:ver_actividades', caso_id=caso.id)
            else:
                print("Errores en formulario de edición:", form.errors)

        # Crear nueva actividad
        else:
            form = ActividadForm(request.POST, request.FILES)
            
            print(request.FILES)
            print(form.errors)
            
            if form.is_valid():
                nueva_actividad = form.save(commit=False)
                nueva_actividad.proyecto = caso  # ✅ nombre correcto
                nueva_actividad.usuario = request.user
                nueva_actividad.editor = f"{request.user.first_name} {request.user.last_name}"
                nueva_actividad.save()
                return redirect('p_canta_callao:ver_actividades', caso_id=caso.id)
            else:
                print("Errores en el formulario de creación:")
                print(form.errors)

    else:
        form = ActividadForm()

    # ✅ Mostrar solo actividades del proyecto actual
    actividades = Actividad.objects.filter(proyecto=caso).order_by('-fecha')

    context = {
        'caso': caso,
        'presupuesto': caso.presupuesto,
        'form': form,
        'nombre_usuario': f"{request.user.first_name} {request.user.last_name}",
        'actividades': actividades,
    }

    return render(request, 'proyecto_canta_callao/lista_actividades.html', context)


def editar_actividad(request):
    if request.method == 'POST':
        seguimiento_id = request.POST.get('id')
        print("ID recibido en POST:", seguimiento_id)

        seguimiento = get_object_or_404(Actividad, id=seguimiento_id)

        form = ActividadForm(request.POST, request.FILES, instance=seguimiento)
        
        if form.is_valid():
            seguimiento_editado = form.save(commit=False)
            seguimiento_editado.save()


            return redirect('p_canta_callao:ver_actividades', caso_id=seguimiento.caso.id)
        else:
            print("Errores al editar seguimiento:", form.errors)
            return redirect('p_canta_callao:ver_actividades', caso_id=seguimiento.caso.id)

    return redirect('p_canta_callao:ver_actividades', caso_id=0)