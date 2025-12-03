"""
Sistema de Controle de Estufa - Cyclamen persicum
Projeto IoT Simplificado para Wokwi

Equipe: Diego, Isabela, Isadora, Jimmy, Lívia

Monitoramento básico de temperatura, umidade e luz para cultivo de Cyclamen.
Parâmetros ideais: Temp 15-20°C, Umidade 50-60%, Luz controlada
"""

from machine import Pin, ADC
import dht
import time

# Configuração dos pinos
DHT_PIN = 15        # Sensor DHT22
LDR_PIN = 26        # Sensor de luz (ADC)
LED_VERDE = 16      # LED verde - condições OK
LED_VERMELHO = 17   # LED vermelho - problema temp/umidade
LED_AZUL = 18       # LED azul - problema de luz

# Parâmetros ideais para Cyclamen persicum
TEMP_MIN = 15.0     # Temperatura mínima
TEMP_MAX = 20.0     # Temperatura máxima
UMID_MIN = 50.0     # Umidade mínima
UMID_MAX = 60.0     # Umidade máxima
LUZ_LIMITE = 500    # Limite para detectar luz excessiva

# Configuração dos componentes
sensor_dht = dht.DHT22(Pin(DHT_PIN))
sensor_luz = ADC(Pin(LDR_PIN))
led_verde = Pin(LED_VERDE, Pin.OUT)
led_vermelho = Pin(LED_VERMELHO, Pin.OUT)
led_azul = Pin(LED_AZUL, Pin.OUT)

def desligar_leds():
    """Desliga todos os LEDs"""
    led_verde.off()
    led_vermelho.off()
    led_azul.off()

def ler_sensores():
    """Lê os sensores e retorna os valores"""
    try:
        sensor_dht.measure()
        temperatura = sensor_dht.temperature()
        umidade = sensor_dht.humidity()
        luz = sensor_luz.read_u16()
        
        print(f"Temp: {temperatura}°C, Umidade: {umidade}%, Luz: {luz}")
        return temperatura, umidade, luz
    except:
        print("Erro ao ler sensores")
        return None, None, None

def verificar_condicoes(temp, umid, luz):
    """Verifica se as condições estão adequadas"""
    temp_ok = TEMP_MIN <= temp <= TEMP_MAX
    umid_ok = UMID_MIN <= umid <= UMID_MAX
    luz_ok = luz < LUZ_LIMITE  # Luz não muito intensa
    
    return temp_ok, umid_ok, luz_ok

def controlar_leds(temp_ok, umid_ok, luz_ok):
    """Controla os LEDs baseado nas condições"""
    desligar_leds()
    
    if temp_ok and umid_ok and luz_ok:
        # Tudo OK - LED verde
        led_verde.on()
        print("✅ Condições ideais!")
    else:
        # Problema de temperatura ou umidade
        if not temp_ok or not umid_ok:
            led_vermelho.on()
            if not temp_ok:
                print("⚠️ Temperatura fora do ideal!")
            if not umid_ok:
                print("⚠️ Umidade fora do ideal!")
        
        # Problema de luz
        if not luz_ok:
            led_azul.on()
            print("⚠️ Muita luz detectada!")

def main():
    """Programa principal"""
    print("=== Sistema de Controle de Estufa ===")
    print("Monitorando Cyclamen persicum...")
    print("Pressione Ctrl+C para parar")
    print()
    
    contador = 0
    
    while True:
        try:
            # Lê os sensores
            temp, umid, luz = ler_sensores()
            
            if temp is not None:
                # Verifica condições
                temp_ok, umid_ok, luz_ok = verificar_condicoes(temp, umid, luz)
                
                # Controla LEDs
                controlar_leds(temp_ok, umid_ok, luz_ok)
                
                # Status a cada 10 leituras
                contador += 1
                if contador >= 10:
                    print(f"\n--- STATUS ESTUFA ---")
                    print(f"Temperatura: {temp}°C (Ideal: 15-20°C)")
                    print(f"Umidade: {umid}% (Ideal: 50-60%)")
                    print(f"Luz: {luz}")
                    print("-------------------\n")
                    contador = 0
            
            # Aguarda 5 segundos
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\nSistema parado pelo usuário")
            break
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)
    
    # Desliga tudo ao finalizar
    desligar_leds()
    print("Sistema finalizado")

# Executa o programa
if __name__ == "__main__":
    main()