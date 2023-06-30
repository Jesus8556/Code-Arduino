import serial
import paho.mqtt.client as mqtt
import requests

mqtt_broker = "54.91.96.242"
mqtt_port = 1883
mqtt_username = "usuario_mqtt"
mqtt_password = "contraseña_mqtt"
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)
serial_port = 'COM4'  # Reemplaza 'COM1' con el puerto serie correcto
baud_rate = 9600

codigo = ""  # Variable para almacenar el código recibido

# Obtener códigos de curso desde la API
url = 'http://54.91.96.242:8000/api/admin/curso/'
response = requests.get(url)
codigos_curso = []

if response.status_code == 200:
    data = response.json()
    codigos_curso = [e['id'] for e in data]

try:
    ser = serial.Serial(serial_port, baud_rate)
    while True:
        data = ser.readline().decode().strip()
        # Guardar el dato en un archivo
        with open('datos.txt', 'a') as file:
            file.write(data + '\n')
        print(f"Dato recibido: {data}")
        topic = "examen4a"
        message = data
        client.publish(topic, message)
        
                
            

except serial.SerialException as e:
    print(f"Error al abrir el puerto serie: {e}")
