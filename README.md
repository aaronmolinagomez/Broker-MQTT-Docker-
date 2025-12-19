# IoT Server Stack - Sistema de Monitoreo de Sensores

Stack completo para recepción, almacenamiento y visualización de datos de sensores IoT.

## Características

- MQTT Broker: Mosquitto para recepción de datos de dispositivos IoT
- Base de Datos: InfluxDB v2 para almacenamiento de series de tiempo  
- Dashboard: Grafana para visualización de métricas
- Listener: Servicio Python que procesa MQTT -> InfluxDB

## Servicios y Puertos

| Servicio | Puerto | Acceso | Credenciales |
|----------|--------|--------|--------------|
| Mosquitto (MQTT) | 1883 | mqtt://localhost:1883 | Sin autenticación |
| InfluxDB v2 | 8086 | http://localhost:8086 | usuario: admin<br>password: admin123<br>org: IoT<br>token: vqdjNj8tjQAPlBweIuGmLNffxTFWYB3a6E1brI70Reyl5gvAuk5w6XTT-iZFRssJNYhpf2new2A2eBkByJCJCA== |
| Grafana | 3000 | http://localhost:3000 | usuario: admin<br>password: admin123 |

