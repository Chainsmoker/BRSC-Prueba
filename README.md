# Despliegue de la app - Usando Docker

# CREDENCIALES
username: alejandro
pass: test12345

# Construir la imagen
docker build -t django-app .

# Ejecutar el contenedor
docker run -p 8000:8000 django-app

# Ingresar
Ingresar a localhost:8000 o http://0.0.0.0:8000 (el host que brinda el contenedor)

# Despliegue de la app - Forma tradicional

## Crear entorno virtual
```
python -m venv .venv
```

## Activar entorno (Windows Powershell)
```
.\.venv\Scripts\activate 
```

## Instalar las dependencias
```
pip install -r requirements.txt
```

## Realizar las migraciones
```
python manage.py migrate
```

## Ejecución de la app
```
python manage.py runserver
```


