import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
import time
import requests
import json

# ---- Configuración InfluxDB ----
url = "http://influxdb:8086"
token = "vqdjNj8tjQAPlBweIuGmLNffxTFWYB3a6E1brI70Reyl5gvAuk5w6XTT-iZFRssJNYhpf2new2A2eBkByJCJCA=="
org = "IoT"
bucket = "sensores"

# ---- Configuración MQTT ----
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPICS = [("temp", 0), ("hum", 0), ("battery", 0), ("distancia", 0)]

# ---- Esperar servicios ----
def wait_for_services():
    print("⏳ Iniciando listener...")
    
    # Esperar InfluxDB
    print("⏳ Esperando InfluxDB...")
    for i in range(30):
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200 and response.json().get('status') == 'pass':
                print("✅ InfluxDB listo")
                break
        except:
            if i == 29:
                print("❌ TIMEOUT: InfluxDB no responde")
                return False
            time.sleep(2)
    
    # Esperar Mosquitto
    print("⏳ Esperando Mosquitto...")
    for i in range(30):
        try:
            client = mqtt.Client()
            client.connect(MQTT_BROKER, MQTT_PORT, 5)
            client.disconnect()
            print("✅ Mosquitto listo")
            break
        except:
            if i == 29:
                print("❌ TIMEOUT: Mosquitto no responde")
                return False
            time.sleep(2)
    
    return True

# ---- Callbacks MQTT ----
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado a MQTT")
        for topic, qos in MQTT_TOPICS:
            client.subscribe(topic, qos)
            print(f"📡 Suscrito: {topic}")
    else:
        print(f"❌ Error MQTT código: {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("🔌 Desconectado inesperadamente, reconectando...")
        time.sleep(5)
        try:
            client.reconnect()
        except:
            pass

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode().strip()
        topic = msg.topic
        
        print(f"📨 Mensaje: {topic} = {payload}")
        
        # Convertir a float
        value = float(payload)
        
        # Crear punto para InfluxDB
        point = Point("sensor") \
            .tag("device", "NB-IoT-Node") \
            .field(topic, value) \
            .time(time.time_ns())
        
        # Escribir en InfluxDB
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"💾 Guardado: {topic} = {value}")
        
    except ValueError:
        print(f"⚠️  Payload no numérico: {payload}")
    except Exception as e:
        print(f"❌ Error guardando: {e}")

# ---- Main ----
def main():
    if not wait_for_services():
        return
    
    # Configurar InfluxDB
    global write_api
    try:
        influx_client = InfluxDBClient(url=url, token=token, org=org, timeout=30_000)
        write_api = influx_client.write_api()
        print("🔌 Conectado a InfluxDB")
    except Exception as e:
        print(f"❌ Error InfluxDB: {e}")
        return
    
    # Configurar MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Reconexión automática
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    
    try:
        print(f"🔗 Conectando a {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("🚀 Listener activo")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo listener...")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        time.sleep(10)
        main()  # Reiniciar

if __name__ == "__main__":
    main()
