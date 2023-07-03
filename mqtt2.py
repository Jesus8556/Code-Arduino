import sys 
import paho.mqtt.client as mqtt
import pymysql
import requests

# Configuración MQTT
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "examen4a" 
curso_id = 0  # Variable para almacenar el ID del alumno
mqtt_client = None
mqtt_loop_started = False 


# Función para manejar los mensajes MQTT
def on_message(client, userdata, msg):
    global curso_id
    # Recibe el mensaje 
    payload = msg.payload.decode("utf-8")
    print("Mensaje recibido: " + payload)
    # Insertar el mensaje en la base de datos
    if curso_id == 0:
        # Insertar el mensaje en la base de datos
        try:
            curso_id = int(payload)
            print("ID del curso: ", curso_id)
            
            # Obtener códigos de curso desde la API
            url = 'http://54.91.96.242:8000/api/admin/inscripcion/'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                codigos_curso = [e['curso'] for e in data]
                
                if curso_id in codigos_curso:
                    print("El ID  pertenece a un código de curso válido")
                    id_curso_existente = 1
                else:
                    print("El ID  no pertenece a ningún código de curso")
                    id_curso_existente = 0 
                    
                    # Reiniciar el valor de curso_id para esperar otro código de aula
                    curso_id = 0
                    
        except ValueError:
            print("Error: el mensaje no es un ID válido")
    else:
        # Acceso al segundo código
        print("Acceso al segundo código")
        print("Leer variable curso_id:", curso_id)
        # Verificar clave del alumno
        clave_alumno = obtener_clave_alumno(curso_id)
        if clave_alumno is not None and payload == clave_alumno:
            print("Clave del alumno válida")
            # Regi strar asistencia
            registrar_asistencia(curso_id)
            curso_id = 0  # Reiniciar el ID del curso
        else:
            print("Clave del alumno inválida")
            curso_id = 0  # Reiniciar el ID del curso
    

# Función para obtener la clave del alumno desde la API
def obtener_clave_alumno(curso_id):
    url = 'http://54.91.96.242:8000/api/admin/keyAlumno/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        alumno = next((x for x in data if x["id"] == curso_id), None)
        if alumno:
            return alumno["clave"]
    
    return None
    

# Función para registrar la asistencia en la base de datos
def registrar_asistencia(curso_id):
    # Conectar a la base de datos
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='12345',
        database='db_asistencia'
    )

    # Obtener el ID del alumno basado en el curso
    query = f"SELECT alumno_id FROM dashboard_inscripcion WHERE curso_id = {curso_id}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        alumno_id = result[0]

    # Verificar si ya existe una asistencia para el alumno en el curso
    query = f"SELECT * FROM dashboard_asistencia WHERE alumno_id = {alumno_id} AND curso_id = {curso_id} AND fecha = CURDATE()"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    if result:
        print("El alumno ya ha registrado su asistencia en este curso hoy")
    else:
        # Insertar la asistencia en la base de datos
        query = f"INSERT INTO dashboard_asistencia (fecha, estado, alumno_id, curso_id) VALUES (CURDATE(), 'A', {alumno_id}, {curso_id})"
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
        print("Asistencia registrada exitosamente")

    # Cerrar la conexión a la base de datos
    connection.close()


# Configuración del cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

def start_mqtt_loop():
    global mqtt_loop_started
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.subscribe(mqtt_topic)
    mqtt_client.loop_start()
    mqtt_loop_started = True
    print("Bucle de recepción de mensajes MQTT iniciado")

def stop_mqtt_loop():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    mqtt_loop_started = False
    print("Bucle de recepción de mensajes MQTT detenido")

# Mantener el programa en ejecución
try:
    while True:
        if not mqtt_loop_started:
            start_mqtt_loop()
        
except KeyboardInterrupt:
    # Detener el bucle y desconectar el cliente MQTT al presionar Ctrl+C
    stop_mqtt_loop()
