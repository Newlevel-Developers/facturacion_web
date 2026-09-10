1. Crear el entorno virtual
Si no existe la carpeta .venv o deseas recrearla:

python3 -m venv .venv


2. Activar el entorno virtual
En Linux / macOS:

Bash
source .venv/bin/activate
En Windows (CMD / PowerShell):

DOS
.venv\Scripts\activate
3. Instalar las dependencias del proyecto
Una vez activado el entorno virtual, instala las librerías listadas en requirements.txt:

Bash
pip install -r requirements.txt
pip install xhtml2pdf   
pip install openpyxl
4. Ejecutar las migraciones de la base de datos
Aplica la estructura de datos en la base de datos local (db.sqlite3):

o modificar la conexion

Bash
python manage.py migrate
5. Crear un usuario Administrador (Opcional)
Si necesitas acceder al panel de administración:

Bash
python manage.py createsuperuser
6. Iniciar el servidor de desarrollo
Ejecuta el servidor local de Django:

Bash
python manage.py runserver


como correr seeder:

python3 manage.py seed_tech