"""
Sistema de Controle de Estufa para Cyclamen persicum
Projeto IoT - Setor Agrícola

Equipe: Diego Alves, Isabela Carvalho, Isadora Moreira, Jimmy Castilho, Lívia Clemente

Este sistema monitora e controla as condições ambientais de uma estufa,
garantindo que a temperatura, umidade e luminosidade permaneçam nos
parâmetros ideais para o cultivo de Cyclamen persicum.

Parâmetros ideais:
- Temperatura: 15°C a 20°C
- Umidade: 50% a 60%
- Luminosidade: Indireta durante o dia, ausente à noite
"""

import machine
import time
import dht
import network
import urequests
from machine import Pin, ADC, PWM, I2C
import json
from time import sleep
import gc

# ===============================================
# CONFIGURAÇÕES DE HARDWARE - PINAGEM
# ===============================================

# Sensores
DHT22_PIN = 15          # Sensor de temperatura e umidade
LDR_PIN = 26            # Sensor de luminosidade (ADC)

# LEDs indicadores
LED_VERDE_PIN = 16      # Condições normais
LED_VERMELHO_PIN = 17   # Alerta temperatura/umidade
LED_AZUL_PIN = 18       # Alerta luminosidade

# Buzzer para alertas sonoros
BUZZER_PIN = 19

# Display I2C (SSD1306)
SDA_PIN = 20
SCL_PIN = 21

# ===============================================
# CONFIGURAÇÕES DO SISTEMA
# ===============================================

# Parâmetros ideais para Cyclamen persicum
TEMP_MIN = 15.0         # Temperatura mínima (°C)
TEMP_MAX = 20.0         # Temperatura máxima (°C)
UMID_MIN = 50.0         # Umidade mínima (%)
UMID_MAX = 60.0         # Umidade máxima (%)
UMID_CRITICA = 70.0     # Umidade crítica - risco de fungos (%)
TEMP_CRITICA = 30.0     # Temperatura crítica - estresse térmico (°C)

# Configurações de luminosidade
LDR_THRESHOLD_DIA = 500     # Limite para considerar "dia"
LDR_THRESHOLD_NOITE = 100   # Limite para considerar "noite"

# Intervalos de tempo (em segundos)
INTERVALO_LEITURA = 10      # Intervalo entre leituras dos sensores
INTERVALO_DISPLAY = 2       # Intervalo para atualizar display
DURACAO_ALERTA = 5          # Duração dos alertas sonoros

# ===============================================
# CONFIGURAÇÃO DOS COMPONENTES
# ===============================================

class EstufaController:
    def __init__(self):
        """Inicializa todos os componentes do sistema de controle."""
        self.setup_hardware()
        self.status = {
            'temperatura': 0.0,
            'umidade': 0.0,
            'luminosidade': 0,
            'condicoes_ok': False,
            'alertas_ativos': []
        }
        
    def setup_hardware(self):
        """Configura todos os componentes de hardware."""
        print("Inicializando sistema de controle de estufa...")
        
        # Sensor DHT22
        self.dht_sensor = dht.DHT22(Pin(DHT22_PIN))
        
        # Sensor LDR (luminosidade)
        self.ldr = ADC(Pin(LDR_PIN))
        
        # LEDs indicadores
        self.led_verde = Pin(LED_VERDE_PIN, Pin.OUT)
        self.led_vermelho = Pin(LED_VERMELHO_PIN, Pin.OUT)
        self.led_azul = Pin(LED_AZUL_PIN, Pin.OUT)
        
        # Buzzer para alertas
        self.buzzer = PWM(Pin(BUZZER_PIN))
        self.buzzer.freq(1000)  # Frequência de 1kHz
        self.buzzer.duty_u16(0)  # Inicialmente desligado
        
        # Display I2C
        try:
            self.i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
            self.setup_display()
        except Exception as e:
            print(f"Erro ao inicializar display: {e}")
            self.display = None
        
        # Desliga todos os LEDs inicialmente
        self.desligar_todos_leds()
        
        print("Hardware inicializado com sucesso!")
        
    def setup_display(self):
        """Configura o display OLED SSD1306."""
        try:
            import ssd1306
            self.display = ssd1306.SSD1306_I2C(128, 64, self.i2c)
            self.display.fill(0)
            self.display.text('Sistema Estufa', 0, 0)
            self.display.text('Cyclamen persicum', 0, 10)
            self.display.text('Inicializando...', 0, 30)
            self.display.show()
        except ImportError:
            print("Biblioteca ssd1306 não encontrada. Display desabilitado.")
            self.display = None
            
    def ler_sensores(self):
        """Lê todos os sensores e atualiza o status do sistema."""
        try:
            # Leitura do sensor DHT22
            self.dht_sensor.measure()
            temperatura = self.dht_sensor.temperature()
            umidade = self.dht_sensor.humidity()
            
            # Leitura do sensor LDR
            luminosidade = self.ldr.read_u16()
            
            # Atualiza status
            self.status.update({
                'temperatura': temperatura,
                'umidade': umidade,
                'luminosidade': luminosidade
            })
            
            print(f"Leituras - Temp: {temperatura}°C, Umidade: {umidade}%, Luz: {luminosidade}")
            
            return True
            
        except Exception as e:
            print(f"Erro ao ler sensores: {e}")
            return False
            
    def verificar_condicoes(self):
        """Verifica se as condições estão dentro dos parâmetros ideais."""
        temp = self.status['temperatura']
        umid = self.status['umidade']
        luz = self.status['luminosidade']
        
        alertas = []
        
        # Verificação de temperatura
        if temp < TEMP_MIN:
            alertas.append("TEMPERATURA BAIXA")
        elif temp > TEMP_MAX:
            alertas.append("TEMPERATURA ALTA")
        elif temp > TEMP_CRITICA:
            alertas.append("TEMPERATURA CRÍTICA - ESTRESSE TÉRMICO")
            
        # Verificação de umidade
        if umid < UMID_MIN:
            alertas.append("UMIDADE BAIXA")
        elif umid > UMID_MAX:
            alertas.append("UMIDADE ALTA")
        elif umid > UMID_CRITICA:
            alertas.append("UMIDADE CRÍTICA - RISCO DE FUNGOS")
            
        # Verificação de luminosidade (detecta se há luz artificial à noite)
        hora_atual = time.localtime()[3]  # Hora atual (0-23)
        is_noite = hora_atual < 6 or hora_atual > 18  # Considera noite das 18h às 6h
        
        if is_noite and luz > LDR_THRESHOLD_NOITE:
            alertas.append("LUZ ARTIFICIAL NOTURNA - INTERFERINDO NO FOTOPERÍODO")
        elif not is_noite and luz < LDR_THRESHOLD_DIA:
            alertas.append("LUMINOSIDADE INSUFICIENTE DURANTE O DIA")
            
        self.status['alertas_ativos'] = alertas
        self.status['condicoes_ok'] = len(alertas) == 0
        
        return self.status['condicoes_ok']
        
    def controlar_leds(self):
        """Controla os LEDs baseado nas condições atuais."""
        self.desligar_todos_leds()
        
        if self.status['condicoes_ok']:
            # Condições ideais - LED verde
            self.led_verde.on()
        else:
            alertas = self.status['alertas_ativos']
            
            # Verifica tipo de alerta para escolher LED apropriado
            tem_alerta_temp_umid = any('TEMPERATURA' in alerta or 'UMIDADE' in alerta 
                                     for alerta in alertas)
            tem_alerta_luz = any('LUZ' in alerta for alerta in alertas)
            
            if tem_alerta_temp_umid:
                self.led_vermelho.on()
                
            if tem_alerta_luz:
                self.led_azul.on()
                
    def desligar_todos_leds(self):
        """Desliga todos os LEDs."""
        self.led_verde.off()
        self.led_vermelho.off()
        self.led_azul.off()
        
    def emitir_alerta_sonoro(self, duracao=2):
        """Emite alerta sonoro por um período determinado."""
        if not self.status['condicoes_ok']:
            print("Emitindo alerta sonoro...")
            # Liga buzzer
            self.buzzer.duty_u16(32768)  # 50% duty cycle
            sleep(duracao)
            # Desliga buzzer
            self.buzzer.duty_u16(0)
            
    def atualizar_display(self):
        """Atualiza as informações no display OLED."""
        if self.display is None:
            return
            
        try:
            self.display.fill(0)
            
            # Título
            self.display.text('Estufa Cyclamen', 0, 0)
            
            # Dados dos sensores
            temp_text = f'Temp: {self.status["temperatura"]:.1f}C'
            umid_text = f'Umid: {self.status["umidade"]:.1f}%'
            luz_text = f'Luz: {self.status["luminosidade"]}'
            
            self.display.text(temp_text, 0, 15)
            self.display.text(umid_text, 0, 25)
            self.display.text(luz_text, 0, 35)
            
            # Status geral
            if self.status['condicoes_ok']:
                self.display.text('Status: OK', 0, 50)
            else:
                self.display.text('Status: ALERTA!', 0, 50)
                
            self.display.show()
            
        except Exception as e:
            print(f"Erro ao atualizar display: {e}")
            
    def log_dados(self):
        """Registra dados para monitoramento histórico."""
        timestamp = time.time()
        log_entry = {
            'timestamp': timestamp,
            'temperatura': self.status['temperatura'],
            'umidade': self.status['umidade'],
            'luminosidade': self.status['luminosidade'],
            'condicoes_ok': self.status['condicoes_ok'],
            'alertas': self.status['alertas_ativos']
        }
        
        # Aqui poderia salvar em arquivo ou enviar para servidor
        print(f"LOG: {json.dumps(log_entry)}")
        
    def enviar_notificacao_wifi(self):
        """Envia notificações via WiFi quando há alertas críticos."""
        if not self.status['condicoes_ok']:
            try:
                # Aqui seria implementado envio para API/servidor
                # Por enquanto apenas simula o envio
                alertas_criticos = [alerta for alerta in self.status['alertas_ativos'] 
                                  if 'CRÍTICA' in alerta or 'CRÍTICO' in alerta]
                
                if alertas_criticos:
                    print(f"ENVIANDO NOTIFICAÇÃO CRÍTICA: {alertas_criticos}")
                    # Simulação de envio HTTP
                    # urequests.post('https://api.exemplo.com/alertas', 
                    #               json={'alertas': alertas_criticos})
                    
            except Exception as e:
                print(f"Erro ao enviar notificação: {e}")
                
    def imprimir_status_detalhado(self):
        """Imprime status detalhado do sistema."""
        print("\n" + "="*50)
        print("STATUS DETALHADO DA ESTUFA - CYCLAMEN PERSICUM")
        print("="*50)
        print(f"Temperatura: {self.status['temperatura']:.1f}°C (Ideal: {TEMP_MIN}-{TEMP_MAX}°C)")
        print(f"Umidade: {self.status['umidade']:.1f}% (Ideal: {UMID_MIN}-{UMID_MAX}%)")
        print(f"Luminosidade: {self.status['luminosidade']} (ADC)")
        
        if self.status['condicoes_ok']:
            print("✅ CONDIÇÕES IDEAIS - Sistema funcionando perfeitamente")
        else:
            print("⚠️  ALERTAS ATIVOS:")
            for alerta in self.status['alertas_ativos']:
                print(f"   • {alerta}")
                
        print("="*50)

# ===============================================
# PROGRAMA PRINCIPAL
# ===============================================

def main():
    """Função principal do sistema de controle."""
    
    print("Iniciando Sistema de Controle de Estufa para Cyclamen persicum")
    print("Desenvolvido por: Diego, Isabela, Isadora, Jimmy, Lívia")
    print("-" * 60)
    
    # Inicializa o controlador da estufa
    estufa = EstufaController()
    
    # Variáveis de controle de tempo
    ultimo_log = 0
    ultima_notificacao = 0
    contador_ciclos = 0
    
    try:
        while True:
            # Lê sensores
            if estufa.ler_sensores():
                
                # Verifica condições
                estufa.verificar_condicoes()
                
                # Controla LEDs
                estufa.controlar_leds()
                
                # Atualiza display
                estufa.atualizar_display()
                
                # Log periódico (a cada 60 segundos)
                tempo_atual = time.time()
                if tempo_atual - ultimo_log > 60:
                    estufa.log_dados()
                    ultimo_log = tempo_atual
                
                # Status detalhado a cada 10 ciclos
                contador_ciclos += 1
                if contador_ciclos >= 10:
                    estufa.imprimir_status_detalhado()
                    contador_ciclos = 0
                
                # Alertas sonoros para condições críticas
                if not estufa.status['condicoes_ok']:
                    alertas_criticos = [alerta for alerta in estufa.status['alertas_ativos'] 
                                      if 'CRÍTICA' in alerta or 'CRÍTICO' in alerta]
                    
                    if alertas_criticos:
                        estufa.emitir_alerta_sonoro(3)
                        
                        # Notificação WiFi para alertas críticos (máximo 1 por minuto)
                        if tempo_atual - ultima_notificacao > 60:
                            estufa.enviar_notificacao_wifi()
                            ultima_notificacao = tempo_atual
                
                # Gerenciamento de memória
                gc.collect()
                
            # Aguarda próximo ciclo
            sleep(INTERVALO_LEITURA)
            
    except KeyboardInterrupt:
        print("\nSistema interrompido pelo usuário")
    except Exception as e:
        print(f"Erro crítico no sistema: {e}")
    finally:
        # Cleanup - desliga todos os componentes
        estufa.desligar_todos_leds()
        estufa.buzzer.duty_u16(0)
        if estufa.display:
            estufa.display.fill(0)
            estufa.display.text('Sistema', 0, 20)
            estufa.display.text('Desligado', 0, 30)
            estufa.display.show()
        print("Sistema finalizado com segurança")

# ===============================================
# FUNÇÕES AUXILIARES PARA TESTES
# ===============================================

def simular_condicoes_teste():
    """Função para simular diferentes condições para teste."""
    print("Modo de simulação ativado - testando diferentes cenários")
    
    estufa = EstufaController()
    
    # Simula diferentes condições
    cenarios = [
        {'temp': 18.0, 'umid': 55.0, 'luz': 300, 'descricao': 'Condições ideais'},
        {'temp': 12.0, 'umid': 45.0, 'luz': 200, 'descricao': 'Temperatura baixa'},
        {'temp': 25.0, 'umid': 75.0, 'luz': 800, 'descricao': 'Temp. alta e umidade alta'},
        {'temp': 35.0, 'umid': 80.0, 'luz': 600, 'descricao': 'Condições críticas'},
        {'temp': 18.0, 'umid': 55.0, 'luz': 900, 'descricao': 'Luz artificial noturna'}
    ]
    
    for i, cenario in enumerate(cenarios):
        print(f"\n--- TESTE {i+1}: {cenario['descricao']} ---")
        
        # Simula leituras dos sensores
        estufa.status.update({
            'temperatura': cenario['temp'],
            'umidade': cenario['umid'],
            'luminosidade': cenario['luz']
        })
        
        # Processa condições
        estufa.verificar_condicoes()
        estufa.controlar_leds()
        estufa.atualizar_display()
        estufa.imprimir_status_detalhado()
        
        sleep(3)

def configurar_wifi():
    """Configura conexão WiFi para notificações remotas."""
    try:
        # Configuração WiFi (ajustar credenciais conforme necessário)
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        
        # sta_if.connect('NOME_DA_REDE', 'SENHA')
        # 
        # while not sta_if.isconnected():
        #     print("Conectando ao WiFi...")
        #     sleep(1)
        #     
        # print(f"WiFi conectado: {sta_if.ifconfig()}")
        
        print("WiFi configurado (simulado)")
        
    except Exception as e:
        print(f"Erro ao configurar WiFi: {e}")

# ===============================================
# EXECUÇÃO DO PROGRAMA
# ===============================================

if __name__ == "__main__":
    # Opções de execução
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        # Modo de teste/simulação
        simular_condicoes_teste()
    else:
        # Execução normal
        configurar_wifi()
        main()