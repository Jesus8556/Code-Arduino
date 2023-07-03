import requests
'''
url = 'http://54.91.96.242:8000/api/admin/curso/'
data = requests.get(url)
if data.status_code == 200:
    data = data.json()
    for e in data:
        print(e['id'])
'''


url = 'http://54.91.96.242:8000/api/admin/inscripcion/'  # Reemplaza 'url-de-tu-api' con la URL real de tu API

variable_inicial = 1

response = requests.get(url)
data = response.json()

alumnos_curso_1 = [registro['alumno'] for registro in data if registro['curso'] == variable_inicial]
if len(alumnos_curso_1) > 0:
    print(alumnos_curso_1)
else:
    print("Curso no encontrado")



url = 'http://54.91.96.242:8000/api/admin/keyAlumno/'
variable_clave = "123"

response = requests.get(url)
data = response.json()

alumno_id = None
global clave_alumno 

for registro in data:
    if registro['clave'] == variable_clave:
        alumno_id = registro['alumno']
        clave_alumno = alumno_id
        break

print(alumno_id)

if clave_alumno in alumnos_curso_1:
    print("Aqui estoy :)")
else:
    print("No estoy aqui :(")
