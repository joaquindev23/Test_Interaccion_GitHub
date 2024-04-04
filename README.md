# LegalIA_Main
El objetivo de este repositorio es estructurar un sistema de IA para lecturas de documentos, aprendizaje continuo, respuestas optimas y lectura de imagenes. Mediante esta estructuracion se podra obtener las especificaciones de los requerimientos en el BackEnd, FrontEnd, DataBase, DataBase, API's, claves, como asi tambien todos los pasos desde la creacion del repositorio.

# Problema
Unificacion de codificacion en un solo archivo ignorando los archivos .gitignore para la separacion de carpetas y archivos que no deben subirse y que deben estar solo en su red local.

# Solucion
Comenzar de 0 un repositorio y compartir los conocimientos de git, github y comandos para trabajar de manera remota y con desicion sobre el codigo como equipo proesional de trabajo

# ¡COMENCEMOS!

1. Creare un nuevo repositorio con los archivos README y LICENSE, esto hará automaticamente el primer commit
2. Creare una clave SSH en mi ordenador dependiendo del sistema operativo que estas usando (en mi caso Linux Ubuntu)
3. Guardare la clave SSH en un fichero 
4. Creare una nueva configuracion de clave SSH en mi cuenta de GIT HUB/Setting/SSH and GPG keys/New SSH key/ "Ttle = Cualquie rtitulo" ; "Key = SSH guardada en fichero"
5. Confirmar cambios

# ¡CLONAR REPOSITORIOS Y PRIMER COMMIT!
Habiendo configurado la clave SSH de GITHUB con la del ordenador configuraremos la cuenta en VS CODE

1. Dirigase al area CUENTAS en la parte inferior izquierda y vinculese con su cuenta de GitHub.
2. Autorice la sesion para vincular Vs code con Cuenta para poder controlar los cambios en las ramificaciones correspondientes mediante su ordenador y cuenta configurada.
3. Para no cometer errores graves en la unica rama del momento llamada MAIN (rama principal del codigo) realice lo siguiente:

4. Verifique si su ordenador esta en condiciones sin errores de vinculacion para realizar el primer commit (cambio en la rama principal sin autorizacion)

5. Desde la terminal de VS CODE ejecute:
    Posisionese en el escritorio y ejecute:
    1. git clone "git@github.com:joaquindev23/LegalIA_Main.git"
    
    2. Aprende los comandos git status, git add . y tambien git commit -m "mensaje" en el siguiente link --> https://www.youtube.com/watch?v=CLpuAyr4Ol0

    3. Mediante el video anterior, pruebe los comandos de git recien aprendidos para mejorar la aplicacion remota en el repositorio

    4. Edite el archivo README.md agregandole lineas de texto en el siguiente espacio

        1. Edite esta seccion y deje su huella para realizar el primer"

        2. Guarde el archivo

        3. git commit - m "mensaje" 



# VIDEOS DE REFENCIA QUE ME HAN SERVIDO PARA PODER RESUMIR ESTA ACTIVIDAD

1. https://www.youtube.com/watch?v=niPExbK8lSw
2. https://www.youtube.com/watch?v=1eEnboVooiY
3. https://www.youtube.com/watch?v=tFr0Vg1q9Eg
4. https://www.youtube.com/watch?v=CLpuAyr4Ol0
5. https://www.youtube.com/watch?v=5us1oHTmPHs

6. DOCUMENTACION OFICIAL GIT --> https://git-scm.com/doc


# ¡A COMENZAR!

1. **En primer lugar empezamos a ramificar el proyecto en partes**: Creamos la rama de carpetas para el Back-End/Front-End/API's Key y demas.



# ¡Instancia Back-End!

2. **Creamos un Entorno Virtual dentro de su raiz Back-End**: Actualmente estoy usando Python 3.10.12 ```python -m venv EntornoVirtual```

3. **Actualizam el paquete de pip**: ```pip install --upgrade pip```

4. **Por el momento no es posible ejecutar la Instalacion de los Requirimientoss, se esta creando el archivo**: ```pip install -r requirements.txt``` 

5. **DATO IMPORRTANTE**: Evite que la carpeta ENTORNOVIRTUAL se suba y se actualice cuando realice los comandos de git, para eso cree un archivo .gitignore y dentro de ella con / asigne la direccion que quiero opacar para que no los suba al repositorio de git hub.



# ¡Instancias Front-End!

