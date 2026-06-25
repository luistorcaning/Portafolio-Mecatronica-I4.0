import time
import random
import json
from datetime import datetime
import paho.mqtt.client as mqtt

# Configuración de la Red Industrial Local
MQTT_BROKER = "localhost"
MQTT_PUERTO = 1884  # <--- Apunta a nuestro Docker en el puerto libre
MQTT_TOPIC = "fabrica/planta1/motor01/telemetria"

def generar_datos_motor():
    """Simula datos telemétricos de un motor industrial."""
    temperatura = round(65.0 + random.uniform(-1.5, 1.5), 2)
    vibracion = round(2.5 + random.uniform(-0.3, 0.3), 2)
    
    if random.random() < 0.01:
        temperatura += round(random.uniform(15.0, 25.0), 2)
        vibracion += round(random.uniform(2.0, 4.0), 2)
        estado = "ANOMALO"
    else:
        estado = "NORMAL"
        
    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_activo": "MOTOR_BOMBA_01",
        "temperatura_c": temperatura,
        "vibracion_rms": vibracion,
        "estado": estado
    }
    return payload

if __name__ == "__main__":
    print("=== CONFIGURANDO CLIENTE MQTT INDUSTRIAL ===")
    
    # Inicializar cliente MQTT utilizando la API moderna (Callback API v2)
    cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    
    try:
        # Conectar al broker de Docker
        cliente.connect(MQTT_BROKER, MQTT_PUERTO, 60)
        cliente.loop_start() # Inicia un hilo de fondo muy ligero para mantener la conexión
        print(f"Conectado exitosamente al Broker MQTT en {MQTT_BROKER}:{MQTT_PUERTO}")
        print(f"Publicando en el topic: '{MQTT_TOPIC}'\n")
        
        while True:
            datos = generar_datos_motor()
            json_datos = json.dumps(datos)
            
            # Publicar el mensaje JSON en la red local
            cliente.publish(MQTT_TOPIC, json_datos)
            
            print(f"[ENVIADO] -> {json_datos}")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nDeteniendo simulación...")
    except Exception as e:
        print(f"\nError de conexión: {e}")
    finally:
        cliente.loop_stop()
        cliente.disconnect()
        print("Ecosistema desconectado de forma segura.")
    print("=== SIMULADOR DE ACTIVOS INDUSTRIA 4.0 INICIADO ===")
    print("Presiona Ctrl + C en la terminal para detener la simulación.\n")
    
    try:
        while True:
            datos = generar_datos_motor()
            # Convertimos a formato JSON string, que es el estándar de comunicación IoT/Cloud
            json_datos = json.dumps(datos, indent=4)
            print(json_datos)
            print("-" * 40)
            
            # Frecuencia de muestreo industrial: Cada 2 segundos
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSimulación finalizada por el usuario.")