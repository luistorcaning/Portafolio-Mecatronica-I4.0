import time
import random
import json
from datetime import datetime

def generar_datos_motor():
    """Simula datos telemetricos de un motor industrial en condiciones normales."""
    # Temperatura normal: 65°C con variaciones leves.
    temperatura = round(65.0 + random.uniform(-1.5, 1.5), 2)
    
    # Vibracion normal: 2.5 mm/s RMS con ruido.
    vibracion = round(2.5 + random.uniform(-0.3, 0.3), 2)
    
    # Simulación aleatoria de anomalía (1% de probabilidad) para analítica avanzada posterior
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