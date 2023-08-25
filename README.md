# selogerbot

# Projeto de Automação de Trading

Este documento fornece uma documentação completa para o meu bot de automação de trading baseado em Python. O projeto utiliza as bibliotecas Telethon e IQ Option API para automatizar operações de trading em opções binárias e digitais. O objetivo principal é receber sinais de trading do Telegram, interpretá-los e executar automaticamente as operações de acordo com os sinais recebidos.

!!projeto de estudo!!

## Índice

- [Requisitos](#requisitos)
- [Configuração](#configuração)
- [Funcionalidades](#funcionalidades)
  - [Conexão com a IQ Option](#conexão-com-a-iq-option)
  - [Verificação de Sinais](#verificação-de-sinais)
  - [Execução de Operações](#execução-de-operações)
  - [Gestão de Saldo e Controle](#gestão-de-saldo-e-controle)
- [Instruções de Uso](#instruções-de-uso)
- [Aviso Legal](#aviso-legal)

## Requisitos <a name="requisitos"></a>

- Python 3.6 ou superior
- Pacotes: `telethon`, `iqoptionapi`, `dotenv`

## Configuração <a name="configuração"></a>

1. Instale as bibliotecas necessárias usando o seguinte comando:

```bash
pip install telethon iqoptionapi python-dotenv
```

2. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

```dotenv
API_ID=YOUR_TELEGRAM_API_ID
API_HASH=YOUR_TELEGRAM_API_HASH
CHAT_ID=YOUR_CHAT_ID
email=YOUR_IQOPTION_EMAIL
senha=YOUR_IQOPTION_PASSWORD
```

Substitua `YOUR_TELEGRAM_API_ID`, `YOUR_TELEGRAM_API_HASH`, `YOUR_CHAT_ID`, `YOUR_IQOPTION_EMAIL` e `YOUR_IQOPTION_PASSWORD` pelas informações apropriadas.

## Funcionalidades <a name="funcionalidades"></a>

### Conexão com a IQ Option <a name="conexão-com-a-iq-option"></a>

O projeto inicia uma conexão com a plataforma IQ Option usando as credenciais fornecidas no arquivo `.env`. Após a conexão ser estabelecida, as informações da conta, como saldo, são exibidas.

### Verificação de Sinais <a name="verificação-de-sinais"></a>

O projeto verifica continuamente as mensagens em um grupo do Telegram especificado pelo `CHAT_ID`. Ele procura por mensagens que contenham sinais de trading no formato "TRADERZISMO FREE". Quando um sinal é detectado, as informações do sinal, como par, direção e horário, são extraídas da mensagem.

### Execução de Operações <a name="execução-de-operações"></a>

Após a detecção de um sinal válido, o projeto verifica se o par de trading tem um payout suficientemente alto. Dependendo do tipo de operação (binária ou digital) e do payout, ele executará a operação correspondente.

### Gestão de Saldo e Controle <a name="gestão-de-saldo-e-controle"></a>

O projeto implementa funcionalidades de gestão de saldo, incluindo verificações de Stop Loss e Take Profit. Ele também suporta a estratégia de Martingale para operações perdidas. As configurações de Stop Loss, Take Profit, número de Martingales e multiplicador são ajustáveis.

## Instruções de Uso <a name="instruções-de-uso"></a>

1. Complete os passos de configuração conforme mencionado acima.

2. Execute o script Python:

```bash
python selogerRefactored.py
```

Substitua `selogerRefactored.py` pelo nome do arquivo que contém o código.

3. O projeto começará a monitorar as mensagens no grupo do Telegram. Quando um sinal válido for detectado, ele executará as operações de acordo com as condições especificadas.

## Aviso Legal <a name="aviso-legal"></a>

Este projeto é fornecido apenas para fins educacionais e informativos. A negociação de ativos financeiros, como opções binárias e digitais, envolve riscos substanciais. Você deve entender os riscos e considerar cuidadosamente suas decisões de investimento. O autor e a OpenAI não assumem qualquer responsabilidade por perdas ou danos decorrentes do uso deste projeto. Use por sua própria conta e risco. Sempre faça sua própria pesquisa e consulte profissionais financeiros antes de tomar decisões de investimento.
