###################################
###     MQTT INSERTA A MYSQL    ###
###################################

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
    #Recibe el mensaje 
    payload = msg.payload.decode("utf-8")
    print("Mensaje recibido: " + payload)
    # Insertar el mensaje en la base de datos
    try:
        if curso_id ==0:
            curso_id = int(payload)
            print("ID del alumno: ", curso_id)
            # Obtener códigos de curso desde la API
            url = 'http://54.91.96.242:8000/api/admin/inscripcion/'
            response = requests.get(url)
            codigos_curso = []

            if response.status_code == 200:
                data = response.json()
                codigos_curso = [e['curso'] for e in data]
            
                id
                if curso_id in codigos_curso:
                    print("El ID del alumno pertenece a un código de curso válido")
            
                else:
                    print("El ID del alumno no pertenece a ningún código de curso")
        else:
            print("Acceso al segundo codigo")
            print("leer varaible curso_id: ", curso_id)
            

        
        
    
    except ValueError:
        print("Error: el mensaje no es un ID válido")
    

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

