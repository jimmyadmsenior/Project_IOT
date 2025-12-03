# Sistema de Controle de Estufa para Cyclamen persicum

## Descrição

Este projeto desenvolve um sistema IoT para monitoramento e controle automatizado de estufas de cultivo de **Cyclamen persicum**. O sistema monitora temperatura, umidade e luminosidade, fornecendo alertas visuais e sonoros quando as condições ambientais estão fora dos parâmetros ideais para o desenvolvimento saudável da planta.

O **Cyclamen persicum** foi escolhido por sua capacidade única de florescer no inverno e outono, períodos em que a demanda por plantas ornamentais tende a ser menor. Isso representa uma oportunidade estratégica para empresas do setor, permitindo ampliar as vendas em épocas de menor concorrência no mercado brasileiro de flores e plantas ornamentais, que alcançou um faturamento de R$ 19,9 bilhões em 2023.

## Hardware - Lista de Materiais

### Sensores:
- **1x DHT22** - Sensor digital de temperatura e umidade
- **1x LDR** - Sensor de luminosidade (Light Dependent Resistor)

### Atuadores:
- **3x LEDs RGB** - Indicadores visuais de status
  - LED Verde: Condições adequadas
  - LED Vermelho: Alerta de temperatura/umidade
  - LED Azul: Alerta de iluminação incorreta

### Componentes Adicionais:
- **1x Visor/Display** - Para exibição de leituras de temperatura e umidade
- **1x Buzzer/Alto-falante** - Para alertas sonoros
- **1x Microcontrolador** - Placa de controle principal
- **1x Caixa de controle** - Para abrigar os componentes eletrônicos
- **Resistores e cabos de conexão**

### Placa:
- Microcontrolador compatível com sensores DHT22 e LDR (ex: Arduino, Raspberry Pi Pico, ESP32)

## Pinagem

| Componente | Pino/Conexão | Descrição |
|------------|-------------|-----------|
| DHT22 - VCC | 3.3V/5V | Alimentação |
| DHT22 - GND | GND | Terra |
| DHT22 - DATA | GP15 | Dados digitais |
| LDR - Terminal 1 | GP26 (ADC) | Entrada analógica |
| LDR - Terminal 2 | 3.3V | Alimentação (via resistor pull-up) |
| LED Verde | GP16 | Condições normais |
| LED Vermelho | GP17 | Alerta temperatura/umidade |
| LED Azul | GP18 | Alerta luminosidade |
| Buzzer | GP19 | Alertas sonoros |
| Display SDA | GP20 | Dados I2C |
| Display SCL | GP21 | Clock I2C |

## Parâmetros Ideais de Cultivo

### Cyclamen persicum:
- **Temperatura**: 15°C a 20°C
- **Umidade**: 50% a 60%
- **Luminosidade**: 
  - Luz indireta durante o dia
  - Ausência de luz durante a noite (respeitar fotoperíodo)

### Condições Críticas:
- **Umidade > 70%**: Risco de fungos e mofo nas sementes
- **Temperatura > 30°C**: Perda de viabilidade das sementes, estresse térmico
- **Luz artificial noturna**: Interfere no fotoperíodo e floração

## Funcionamento do Sistema

### Monitoramento:
1. **DHT22**: Monitora temperatura e umidade continuamente
2. **LDR**: Detecta intensidade luminosa no ambiente
3. **Sistema de alertas**: Compara valores lidos com parâmetros ideais

### Respostas do Sistema:
- **LED Verde**: Todas as condições dentro dos parâmetros ideais
- **LED Vermelho**: Temperatura ou umidade fora dos limites seguros
- **LED Azul**: Detecção de luz inadequada (iluminação noturna)
- **Alertas Sonoros**: Notificações audíveis para condições críticas
- **Visor**: Exibição em tempo real das leituras dos sensores

## Posicionamento dos Sensores

### Na Estufa:
- **DHT22**: Instalado no teto, suspenso sobre as plantas para captar condições gerais da estufa
- **LDR**: Fixado na lateral da estufa para monitorar incidência luminosa

### Externa:
- **Caixa de Controle**: Localizada fora da estufa, no chão, contendo LEDs de alerta
- **Visor**: Instalado em caixa separada ao lado da estufa para fácil visualização

## Instruções de Configuração

### Pré-requisitos:
1. Microcontrolador configurado com ambiente de desenvolvimento
2. Bibliotecas necessárias instaladas
3. Componentes conectados conforme pinagem especificada

### Passos para Execução:
1. Clone este repositório
2. Conecte os componentes seguindo a tabela de pinagem
3. Carregue o código `main.py` no microcontrolador
4. Posicione os sensores conforme especificação do projeto
5. Alimente o sistema e verifique funcionamento dos LEDs
6. Monitore as leituras no visor

### Calibração:
- Ajuste os thresholds de temperatura e umidade conforme necessidade
- Teste o sensor LDR em diferentes condições de luminosidade
- Verifique a resposta dos alertas sonoros e visuais

## Equipe de Desenvolvimento

- Diego Alves
- Isabela Carvalho  
- Isadora Moreira
- Jimmy Castilho
- Lívia Clemente

---

*Este projeto foi desenvolvido como parte do curso de IoT, focando no setor agrícola e controle automatizado de estufas.*