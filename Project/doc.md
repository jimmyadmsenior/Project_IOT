from machine import Pin, ADC, PWM
from utime import sleep, ticks_us, ticks_diff
import dht

# ==========================================
# 1) ULTRASSÔNICO HC-SR04 → GP2 / GP3
# ==========================================
trig = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)

def medir_distancia():
    trig.low()
    sleep(0.002)
    trig.high()
    sleep(0.00001)
    trig.low()

    tempo = ticks_us()
    while echo.value() == 0:
        if ticks_diff(ticks_us(), tempo) > 30000:
            return -1

    inicio = ticks_us()
    while echo.value() == 1:
        if ticks_diff(ticks_us(), inicio) > 30000:
            return -1

    fim = ticks_us()
    duracao = ticks_diff(fim, inicio)
    distancia = (duracao / 2) / 29.1
    return distancia


# ==========================================
# 2) DHT22 → GP7
# ==========================================
dht_sensor = dht.DHT22(Pin(7))


# ==========================================
# 3) LDR AO → GP26 (ADC0)
# ==========================================
ldr = ADC(26)


# ==========================================
# 4) LED normal → GP21
# ==========================================
led = Pin(21, Pin.OUT)
led.value(0)


# ==========================================
# 5) Buzzer → GP16
# ==========================================
buzzer = PWM(Pin(16))
buzzer.freq(2000)
buzzer.duty_u16(0)

def beep(t=0.1):
    buzzer.duty_u16(30000)
    sleep(t)
    buzzer.duty_u16(0)


# ==========================================
# 6) LED RGB → R:GP14, G:GP15, B:GP13
# ==========================================
red   = PWM(Pin(14))
green = PWM(Pin(15))
blue  = PWM(Pin(13))

red.freq(1000)
green.freq(1000)
blue.freq(1000)

def rgb(r, g, b):
    red.duty_u16(r)
    green.duty_u16(g)
    blue.duty_u16(b)


# ==========================================
# LOOP PRINCIPAL
# ==========================================
while True:

    # --- ULTRASSÔNICO ---
    distancia = medir_distancia()
    print("Distância:", distancia, "cm")

    # --- TEMPERATURA / UMIDADE ---
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print("Temp:", temp, "°C  | Hum:", hum, "%")
    except:
        print("Erro no DHT22")

    # --- LDR ---
    luz = ldr.read_u16()
    print("Luz:", luz)

    # =======================================
    # AÇÕES DO SISTEMA
    # =======================================

    # 🔴 Se algo está MUITO perto (<15 cm)
    if distancia != -1 and distancia < 15:
        led.value(1)
        rgb(65535, 0, 0)  # VERMELHO
        beep(0.05)

    # 🟡 Meio perto (<30 cm)
    elif distancia != -1 and distancia < 30:
        led.value(1)
        rgb(65535, 20000, 0)  # AMARELO

    else:
        led.value(0)
        rgb(0, 0, 0)  # Desliga RGB

    # 🌞 Luz forte → azul
    if luz > 30000:
        rgb(0, 0, 65535)

    # 🌙 Luz baixa → lilás
    elif luz < 15000:
        rgb(30000, 0, 65535)

    sleep(0.2)
