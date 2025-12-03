# Sistema de Controle de Estufa para *Cyclamen persicum*

## Equipe de Desenvolvimento
- Diego Alves  
- Isabela Carvalho  
- Isadora Moreira  
- Jimmy Castilho  
- Lívia Clemente  

## Descrição

Este projeto desenvolve um sistema IoT para monitoramento e controle automatizado de estufas de cultivo de *Cyclamen persicum*. O sistema monitora temperatura, umidade e luminosidade, fornecendo alertas visuais e sonoros quando as condições ambientais estão fora dos parâmetros ideais para o desenvolvimento saudável da planta.

O *Cyclamen persicum* foi escolhido por sua capacidade de florescer no inverno e no outono, períodos em que a demanda por plantas ornamentais tende a ser menor. Isso representa uma oportunidade estratégica para empresas do setor, permitindo ampliar as vendas em épocas de menor concorrência no mercado brasileiro de flores e plantas ornamentais, que alcançou faturamento de R$ 19,9 bilhões em 2023.

## Hardware — Lista de Materiais

### Sensores
- **1x DHT22** — Sensor digital de temperatura e umidade
- **1x LDR** — Sensor de luminosidade (Light Dependent Resistor)

### Atuadores
- **LEDs RGB** — Indicadores visuais de status
  - LED Verde: condições ambientais adequadas
  - LED Vermelho: alerta de temperatura ou umidade fora do limite seguro
  - LED Azul: alerta de iluminação incorreta (luz artificial/incidência noturna)

### Componentes Adicionais
- **1x Display** — Utilizado para exibição de leituras de temperatura e umidade
- **1x Buzzer** — Utilizado para alertas sonoros
- **1x Microcontrolador** — Utilizado para controle principal
- **1x Caixa** — Utilizada como abrigo para os componentes eletrônicos
- **Resistores e cabos** — Utilizados para conexões

### Placa
- **Raspberry Pi Pico 2W** — Placa microcontroladora compacta e de baixo custo, criada pela Raspberry Pi Foundation para uso em projetos eletrônicos, automação, robótica e educação.

## Pinagem

- **DHT22**
  - VCC : 3.3V/5V — Alimentação  
  - GND : GND — Terra  
  - DATA : GP15 — Dados digitais  

- **LDR**
  - Terminal 1 : GP26 (ADC) — Entrada analógica  
  - Terminal 2 : 3.3V — Alimentação (via resistor pull-up)  

- **LEDs**
  - LED Verde : GP16 — Condições normais  
  - LED Vermelho : GP17 — Alerta temperatura/umidade  
  - LED Azul : GP18 — Alerta luminosidade  

- **Buzzer**
  - Buzzer : GP19 — Alertas sonoros  

- **Display I2C**
  - SDA : GP20 — Dados I2C  
  - SCL : GP21 — Clock I2C  

## Parâmetros Ideais

### *Cyclamen persicum*
- **Temperatura:** 15°C a 20°C  
- **Umidade:** 50% a 60%  
- **Luminosidade:**
  - Luz indireta durante o dia  
  - Ausência de luz durante a noite (fotoperíodo)  

### Condições Críticas
- **Umidade > 70%:** risco de fungos e mofo  
- **Temperatura > 30°C:** perda de viabilidade e estresse térmico  
- **Luz noturna:** interfere no fotoperíodo e na floração  

## Funcionamento do Sistema

1. Ler temperatura e umidade pelo DHT22.  
2. Ler intensidade de luz pelo LDR.  
3. Comparar leituras com os valores ideais.  

### Ações e Respostas do Sistema
- Se tudo estiver dentro dos parâmetros: acende LED VERDE.  
- Se temperatura ou umidade estiver fora do ideal: acende LED VERMELHO.  
- Se a iluminação estiver inadequada: acende LED AZUL.  
- Em condições críticas: buzzer é ativado.  
- O display sempre mostra as medições em tempo real.  

## Posicionamento dos Sensores

- **DHT22:** no teto da estufa, acima das plantas.  
- **LDR:** na lateral da estufa.  
- **LEDs e buzzer:** na caixa de controle, fora da estufa.  
- **Display:** ao lado da estufa para fácil visualização.  

## Instruções de Configuração

### Pré-requisitos
1. Microcontrolador configurado com ambiente de desenvolvimento.  
2. Bibliotecas necessárias instaladas.  
3. Componentes conectados conforme pinagem.  

### Passos para Execução
1. Clone este repositório.  
2. Conecte os componentes conforme pinagem.  
3. Carregue main.py no microcontrolador.  
4. Posicione os sensores.  
5. Alimente o sistema.  
6. Verifique o funcionamento dos LEDs e do display.  

### Calibração
- Ajuste limites de temperatura e umidade conforme necessidade.  
- Teste o LDR em diferentes condições de iluminação.  
- Verifique alertas sonoros e visuais.  