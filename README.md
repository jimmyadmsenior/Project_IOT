# 🌱 Sistema de Controle de Estufa IoT - Cyclamen persicum

<div align="center">
  
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-MicroPython-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20Pico-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

</div>

## 📋 Sobre o Projeto

Sistema IoT inteligente para **monitoramento e controle automatizado** de estufas para cultivo de **Cyclamen persicum**. O projeto monitora condições ambientais essenciais (temperatura, umidade e luminosidade) e fornece alertas visuais através de LEDs indicadores quando os parâmetros estão fora dos valores ideais.

### 🎯 **Por que Cyclamen persicum?**

O Cyclamen persicum foi escolhido estrategicamente por sua capacidade única de **florescer no inverno e outono**, períodos de menor concorrência no mercado de plantas ornamentais. Com o setor brasileiro alcançando **R$ 19,9 bilhões** em faturamento (2023), este projeto oferece vantagem competitiva para produtores.

## ⚡ Funcionalidades

- 🌡️ **Monitoramento de Temperatura** (15°C - 20°C ideal)
- 💧 **Controle de Umidade** (50% - 60% ideal)  
- ☀️ **Sensor de Luminosidade** (detecta luz excessiva)
- 🚨 **Sistema de Alertas Visuais** (LEDs coloridos)
- 📊 **Feedback em Tempo Real** (via console)
- 🔄 **Monitoramento Contínuo** (leituras a cada 5 segundos)

## 🛠️ Hardware Necessário

### 📦 **Lista de Componentes:**

| Componente | Quantidade | Função |
|------------|------------|---------|
| **Raspberry Pi Pico** | 1x | Microcontrolador principal |
| **Sensor DHT22** | 1x | Temperatura e umidade |
| **LDR (Photoresistor)** | 1x | Sensor de luminosidade |
| **LED Verde** | 1x | Indicador condições OK |
| **LED Vermelho** | 1x | Alerta temperatura/umidade |
| **LED Azul** | 1x | Alerta luminosidade |
| **Resistores 220Ω** | 3x | Limitadores para LEDs |
| **Resistor 10kΩ** | 1x | Pull-up para LDR |
| **Protoboard** | 1x | Montagem do circuito |
| **Jumpers** | Vários | Conexões |

## 🔌 Diagrama de Pinagem

```
Raspberry Pi Pico          Componentes
┌─────────────────┐
│  3V3  ●─────────┼──── DHT22 VCC + LDR (via 10kΩ)
│  GND  ●─────────┼──── DHT22 GND + LEDs GND
│  GP15 ●─────────┼──── DHT22 DATA
│  GP16 ●──[220Ω]─┼──── LED Verde (+)
│  GP17 ●──[220Ω]─┼──── LED Vermelho (+)
│  GP18 ●──[220Ω]─┼──── LED Azul (+)
│  GP26 ●─────────┼──── LDR + Resistor 10kΩ para GND
└─────────────────┘
```

### 📋 **Tabela de Conexões:**

| Pino Pico | Componente | Observação |
|-----------|------------|------------|
| **3V3** | DHT22 VCC, LDR | Alimentação 3.3V |
| **GND** | DHT22 GND, LEDs GND | Terra comum |
| **GP15** | DHT22 DATA | Dados digitais |
| **GP16** | LED Verde | via Resistor 220Ω |
| **GP17** | LED Vermelho | via Resistor 220Ω |
| **GP18** | LED Azul | via Resistor 220Ω |
| **GP26** | LDR | Entrada ADC |

## 🚀 Como Executar

### 1. **Clone o Repositório:**
```bash
git clone https://github.com/jimmyadmsenior/Project_IOT.git
cd Project_IOT
```

### 2. **Monte o Circuito:**
- Conecte os componentes conforme o diagrama de pinagem
- Verifique todas as conexões antes de alimentar

### 3. **Carregue o Código:**
- Copie o arquivo `Project/main.py` para o Raspberry Pi Pico
- Use Thonny IDE ou similar para upload

### 4. **Execute:**
```python
python main.py
```

## 🧪 Testando no Wokwi

Este projeto pode ser testado virtualmente no [Wokwi](https://wokwi.com):

1. Acesse [wokwi.com](https://wokwi.com)
2. Crie um novo projeto com Raspberry Pi Pico
3. Monte o circuito conforme o diagrama
4. Cole o código do `main.py`
5. Execute a simulação

### 🎮 **Cenários de Teste:**

| Cenário | Temperatura | Umidade | Luz | LED Esperado |
|---------|-------------|---------|-----|--------------|
| **Ideal** | 18°C | 55% | 300 | 🟢 Verde |
| **Temp. Alta** | 25°C | 55% | 300 | 🔴 Vermelho |
| **Umidade Baixa** | 18°C | 30% | 300 | 🔴 Vermelho |
| **Luz Excessiva** | 18°C | 55% | 800 | 🔵 Azul |

## 📊 Parâmetros de Cultivo

### 🌿 **Condições Ideais para Cyclamen persicum:**

- **🌡️ Temperatura:** 15°C - 20°C
- **💧 Umidade:** 50% - 60%  
- **☀️ Luminosidade:** Indireta durante o dia, ausente à noite

### ⚠️ **Condições Críticas:**

- **Umidade > 70%:** Risco de fungos e mofo
- **Temperatura > 30°C:** Estresse térmico nas plantas
- **Luz noturna:** Interfere no fotoperíodo

## 📁 Estrutura do Projeto

```
Project_IOT/
├── 📄 README.md              # Documentação principal
├── 📄 LICENSE                # Licença MIT
├── 📁 Project/
│   ├── 🐍 main.py           # Código principal
│   ├── 📝 doc.md            # Documentação técnica
│   └── 📄 word.txt          # Especificações do projeto
└── 🖼️ assets/               # Imagens e diagramas
```

## 💡 Como Funciona

### 🔄 **Loop Principal:**
1. **Leitura dos Sensores** → DHT22 (temp/umidade) + LDR (luz)
2. **Verificação dos Parâmetros** → Compara com valores ideais
3. **Controle dos LEDs** → Acende indicador apropriado
4. **Log no Console** → Mostra valores atuais
5. **Aguarda 5 segundos** → Repete o ciclo

### 🚦 **Sistema de Alertas:**
- **🟢 LED Verde:** Todas as condições ideais
- **🔴 LED Vermelho:** Temperatura ou umidade fora do ideal
- **🔵 LED Azul:** Luminosidade excessiva detectada

## 👥 Equipe de Desenvolvimento

- **Diego Alves** - Desenvolvedor
- **Isabela Carvalho** - Desenvolvedora  
- **Isadora Moreira** - Desenvolvedora
- **Jimmy Castilho** - Desenvolvedor
- **Lívia Clemente** - Desenvolvedora

## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido como parte do curso de **Internet das Coisas (IoT)**, focando na aplicação prática de sensores e microcontroladores para automação no **setor agrícola**.

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

- 🐛 Reportar bugs
- 💡 Sugerir melhorias
- 🔄 Enviar pull requests
- 📚 Melhorar a documentação

## 📞 Contato

Para dúvidas ou sugestões:
- 📧 **E-mail:** [Contato via GitHub](https://github.com/jimmyadmsenior)
- 🐙 **GitHub:** [@jimmyadmsenior](https://github.com/jimmyadmsenior)

---

<div align="center">
  
**🌱 Cultive o futuro com tecnologia! 🌱**

*Desenvolvido com ❤️ para o setor agrícola brasileiro*

</div>

