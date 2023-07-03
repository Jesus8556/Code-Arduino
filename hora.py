import time

def cronometro():
    tiempo_inicial = time.time()
    
    while True:
        palabra = input("Ingresa una palabra: ")
        tiempo_transcurrido = time.time() - tiempo_inicial

        if tiempo_transcurrido <= 20:
            print("Estás a tiempo!")
            print("Tiempo transcurrido:", tiempo_transcurrido)
        else:
            print("Tardón!")
            print("Tiempo transcurrido:", tiempo_transcurrido)

cronometro()
