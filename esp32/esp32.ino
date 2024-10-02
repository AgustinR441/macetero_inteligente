#include <DHTesp.h>
#include <HTTPClient.h>
#include <LiquidCrystal_I2C.h>
#include <time.h>
#include <WiFi.h>
#include <Wire.h>

// Listas de redes WiFi y servidores
const char* ssids[] = {"INTERNET CASA", "TP-Link_5406_CABAÑAS", "ZEUS"};
const char* passwords[] = {"xR3#9pZu", "52711855", "Olimpo2020*"};
const char* serverNames[] = {"http://192.168.100.8:5000/send-data-esp32", "http://192.168.0.109:5000/send-data-esp32", "http://10.60.1.50:5000/send-data-esp32"};
const int numNetworks = sizeof(ssids) / sizeof(ssids[0]);

// Variable global para almacenar el índice de la red conectada
int connectedNetworkIndex = -1;

// Parámetros para Network Time Protocol (NTP)
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -10800;  // Hora Chile (-3 horas)
const int daylightOffset_sec = 0;   // Horario de verano

// Inicialización de Variables
int pinDHT = 15;
int pinHumedadSub = 34;
float temperatura;
float humedadUp;
float humedadSub;
int humedadAnaloga;
String fecha;
String hora;

// Inicialización módulos
DHTesp dht;                          // DHT21
LiquidCrystal_I2C lcd(0x27, 20, 4);  // Display LCD


void setup() {
  Serial.begin(115200);

  dht.setup(pinDHT, DHTesp::DHT11);
  lcd.init();
  lcd.backlight();

  // Intentar conectar a las redes WiFi disponibles
  bool connected = false;
  for (int i = 0; i < numNetworks; i++) {
    WiFi.begin(ssids[i], passwords[i]);
    int attempt = 0;
    while (WiFi.status() != WL_CONNECTED && attempt < 10) { // Intentar durante 10 segundos
      delay(1000);
      Serial.print("Conectando a WiFi ");
      Serial.print(ssids[i]);
      Serial.println("...");
      lcd.setCursor(0, 0);
      lcd.print("Conectando a WiFi...");
      attempt++;
    }
    if (WiFi.status() == WL_CONNECTED) {
      connected = true;
      connectedNetworkIndex = i;
      break;
    }
  }

  if (connected) {
    Serial.println("Conectado a WiFi");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Conectado a WiFi!");
    delay(1000);

    // Conexión a servidor de tiempo
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    Serial.println("Sincronizando con el servidor NTP...");
    lcd.setCursor(0, 0);
    lcd.print("Obteniendo hora y fecha...");

    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
      Serial.println("Error al sincronizar tiempo");
      return;
    }
    Serial.println("Tiempo sincronizado con éxito");

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Hora y fecha obtenidas!");

    delay(1000);
    lcd.clear();
  } else {
    Serial.println("No se pudo conectar a ninguna red WiFi");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Error de red WiFi");
  }
}

void loop() {
  TempAndHumidity data = dht.getTempAndHumidity();

  if (isnan(data.temperature) || isnan(data.humidity)) {
    Serial.println("Error al leer datos del sensor DHT11.");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Error al leer DHT11");
  } else {
    temperatura = data.temperature;
    humedadUp = data.humidity;
    humedadAnaloga = analogRead(pinHumedadSub);
    humedadSub = map(humedadAnaloga, 0, 4095, 100, 0);

    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.print("°C, Humedad: ");
    Serial.print(humedadUp);
    Serial.print("% ");
    Serial.print("HumedadSub: ");
    Serial.println(humedadSub);

    lcd.setCursor(0, 0);
    lcd.print("Macetero Inteligente");
    lcd.setCursor(0, 1);
    lcd.print("T:");
    lcd.print(temperatura);
    lcd.print(char(223));
    lcd.print("C  H:");
    lcd.print(humedadUp);
    lcd.print("%");

    lcd.setCursor(2, 3);
    lcd.print("por T2");
    lcd.print(char(223));
    lcd.print(" Riquelme");

    obtenerFechaHoraActual();

    enviarDataServidor(temperatura, humedadUp, humedadSub, fecha, hora);
  }

  delay(2000);
}

void enviarDataServidor(float temperatura, float humedadUp, float humedadSub, String fecha, String hora) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    const char* currentServerName = serverNames[connectedNetworkIndex];
    if (strlen(currentServerName) == 0) {
      Serial.println("No se ha definido servidor para la red conectada");
      return;
    }
    http.begin(currentServerName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    String postData = "temperatura=" + String(temperatura) + "&humedadUp=" + String(humedadUp) +
                      "&humedadSub=" + String(humedadSub) + "&fecha=" + fecha + "&hora=" + hora;
    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error en la solicitud POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Error en la conexión WiFi");
  }
}

void obtenerFechaHoraActual() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Error al obtener el tiempo");
    return;
  }

  // Formatear fecha y hora
  char bufferFecha[11];  // YYYY-MM-DD
  char bufferHora[9];    // HH:MM:SS
  strftime(bufferFecha, 11, "%Y-%m-%d", &timeinfo);
  strftime(bufferHora, 9, "%H:%M:%S", &timeinfo);

  fecha = String(bufferFecha);
  hora = String(bufferHora);

  Serial.print("Fecha: ");
  Serial.println(fecha);
  Serial.print("Hora: ");
  Serial.println(hora);
}
