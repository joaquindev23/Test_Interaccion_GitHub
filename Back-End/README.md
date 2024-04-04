**Instancia Back-End**


1. **Creamos un Entorno Virtual dentro de su raiz Back-End**: Actualmente estoy usando Python 3.10.12 ```python -m venv EntornoVirtual```

2. **Actualizamos el paquete de pip**: ```pip install --upgrade pip```

3. **DATO IMPORRTANTE**: Evite que la carpeta ENTORNOVIRTUAL se suba y se actualice cuando realice los comandos de git, para eso cree un archivo .gitignore y dentro de ella con / asigne la direccion que quiero opacar para que no los suba al repositorio de git hub.

4. **Activar el entorno Virtual y hacer las instalaciones de todos los requerimientos**: Back-End/EntornoVirtual/bin --> source activate (en linux)

4. **Instalar los Requerimientos**: Se esta creando el archivo es por eso que no se podra hacerlo de manera directa todos los frameowrk y librerias a usar en el proyecto generalizado 

5. **Creamos un proyecto Django**: django-admin startproject "LegalIA"

    1. python manage.py makemigrations --> se encarga de la creación de nuevas migraciones basado en los cambios que ha hecho a sus modelos.
    2. python manage.py migrate --> Sirve para generar y modificar las tablas de la base de datos
