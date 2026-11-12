# 📊 Observacao-Homelab

**Laboratório de observabilidade, monitoramento de infraestrutura e automação DevOps.**

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Zabbix](https://img.shields.io/badge/Zabbix-7.4-red)
![Grafana](https://img.shields.io/badge/Grafana-13-orange?logo=grafana)
![Proxmox](https://img.shields.io/badge/Proxmox-VE-orange)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## 🌐 Dashboard ao Vivo

Este projeto disponibiliza um dashboard Grafana com métricas reais de um ambiente Proxmox VE, coletadas pelo Zabbix.

### [📊 Visualizar Dashboard ao Vivo](https://grafana.alighierizz.com.br/public-dashboards/a2e427c9b8c84355b499319a0beb28eb)

**Métricas disponíveis:**
- Utilização de CPU
- Consumo de memória RAM
- Utilização de armazenamento
- Uptime do servidor

O dashboard público disponibiliza métricas selecionadas, enquanto o acesso administrativo ao Grafana permanece protegido pelo Cloudflare Access.

> As métricas são provenientes de um homelab real e podem ficar temporariamente indisponíveis durante manutenções.

---

## 🎯 Sobre o Projeto

O **Observacao-Homelab** foi desenvolvido para aplicar conceitos de monitoramento de infraestrutura, observabilidade, segurança, automação e integração contínua.

O ambiente utiliza o Proxmox VE como plataforma de virtualização, o Zabbix para coleta e monitoramento de recursos e o Grafana para visualização das métricas.

Além disso, foram implementados scripts Python para verificações HTTP de disponibilidade, testes automatizados com pytest e uma pipeline GitHub Actions.

### Objetivos

- Monitorar recursos e disponibilidade da infraestrutura.
- Centralizar informações de VMs e containers LXC.
- Visualizar métricas históricas e indicadores operacionais.
- Detectar indisponibilidades por meio de triggers.
- Enviar notificações automáticas por e-mail.
- Automatizar verificações de disponibilidade com Python.
- Validar alterações de código por integração contínua.
- Documentar incidentes e procedimentos de recuperação.

---

## 🏗️ Arquitetura

```text
                 Proxmox VE
                 (Hypervisor)
                      |
                      v
                 Zabbix Server
              (Coleta e alertas)
                      |
                      v
                 Grafana
            (Dashboards e métricas)
                      |
                      v
               Cloudflare Tunnel
                      |
                      v
              Dashboard Público
                      |
                      v
                Visitante GitHub


          LXC Debian - Desenvolvimento
                      |
                      v
              Python Health Check
                      |
                      v
               Testes com pytest
                      |
                      v
               GitHub Repository
                      |
                      v
                GitHub Actions
```

O Cloudflare Tunnel permite disponibilizar o dashboard por HTTPS sem necessidade de abrir portas no roteador.

A pipeline GitHub Actions realiza testes automatizados independentemente da disponibilidade da rede doméstica.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Proxmox VE | Virtualização de máquinas e containers |
| Debian Linux | Sistema operacional dos containers e ambiente de desenvolvimento |
| Zabbix | Monitoramento, descoberta automática e alertas |
| Grafana | Visualização das métricas |
| Cloudflare Tunnel | Publicação HTTPS do dashboard |
| Cloudflare Access | Proteção dos acessos administrativos |
| Python | Scripts de verificação de disponibilidade |
| Requests | Requisições HTTP e HTTPS |
| pytest | Testes automatizados |
| Git | Versionamento |
| GitHub Actions | Integração contínua |

---

## 📈 Monitoramento da Infraestrutura

O monitoramento utiliza o template **Proxmox VE by HTTP**, integrado à API do Proxmox.

### Métricas monitoradas

**Infraestrutura:**
- Utilização de CPU
- Consumo de RAM
- Utilização de disco
- Uptime
- Estado das VMs e containers LXC

**Disponibilidade:**
- Estado Running/Stopped
- Detecção de reinicializações
- Triggers de indisponibilidade
- Eventos de recuperação

As consultas à API Proxmox utilizam um token com permissões de leitura e validação TLS habilitada.

---

## 🚨 Alertas e Incidentes

O Zabbix foi configurado para identificar falhas e enviar notificações automáticas por e-mail.

As ações de notificação podem enviar mensagens tanto quando um problema é detectado quanto após sua recuperação.

### Teste de incidente realizado

Foi executada uma simulação controlada de indisponibilidade na VM `ansible-node`.

**Resultado observado:**

| Evento | Horário |
|---|---|
| Indisponibilidade detectada | 19:12:52 |
| Recuperação detectada | 19:14:52 |
| Duração registrada | 2 minutos |

Durante o teste, o Zabbix registrou os eventos e o recebimento da notificação por e-mail foi confirmado.

Esse cenário demonstra um fluxo de monitoramento, detecção e recuperação de incidentes.

---

## 🐍 Health Check em Python

O projeto possui um script que verifica a disponibilidade HTTP de serviços da infraestrutura.

**Arquivo:** `scripts/check_infrastructure.py`

O script realiza requisições HTTP/HTTPS, aplica um timeout e compara os códigos de resposta com os valores esperados.

Exemplos de verificações:

| Serviço | Resposta esperada |
|---|---|
| Proxmox API | HTTP 401 (endpoint protegido) |
| Zabbix | HTTP 200 |
| Grafana Health API | HTTP 200 |

A resposta HTTP 401 no endpoint protegido do Proxmox indica que o serviço respondeu e solicitou autenticação, não que todos os componentes da plataforma estejam saudáveis.

### Executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Crie um arquivo `.env` com os endereços do seu próprio ambiente:

```dotenv
PROXMOX_URL=https://proxmox.example.com:8006/api2/json/version
ZABBIX_URL=https://zabbix.example.com/zabbix/
GRAFANA_URL=https://grafana.example.com/api/health
```

Em instalações com uma CA privada, configure a confiança TLS adequadamente. Nunca desabilite a verificação de certificados para contornar erros de configuração.

Execute:

```bash
python scripts/check_infrastructure.py
```

O comando retorna código `0` quando todas as verificações são aprovadas e `1` quando alguma falha.

---

## 🧪 Testes Automatizados

Os testes utilizam **pytest** e mocks para simular diferentes respostas HTTP, sem depender de acesso à infraestrutura real.

Cenários implementados:

1. Serviço disponível — HTTP 200.
2. Resposta inesperada — HTTP 503.
3. Timeout de conexão.
4. Endpoint protegido do Proxmox — HTTP 401.
5. Configuração ausente.

### Executar os testes

```bash
python -m pytest -v
```

**Resultado da validação local:**

```text
5 passed in 0.12s
```

---

## ⚙️ Integração Contínua

A pipeline está definida no arquivo:

`.github/workflows/ci.yml`

Ela é acionada em pushes para `main`, Pull Requests direcionados à branch `main` e execuções manuais.

O workflow executa as seguintes operações:

1. Checkout do repositório.
2. Preparação do Python 3.13.
3. Instalação das dependências.
4. Execução dos testes com pytest.
5. Validação sintática dos arquivos JSON dos dashboards.

A pipeline utiliza respostas simuladas para os testes Python, permitindo executá-los nos runners do GitHub sem acesso à rede privada do homelab.

### Resultado

A execução #4 do GitHub Actions foi concluída com sucesso, incluindo a validação do dashboard exportado.

---

## 📂 Estrutura do Repositório

```text
Observacao-Homelab/
├── .github/
│   └── workflows/
│       └── ci.yml
├── dashboards/
│   ├── infrastructure-overview-example.json
│   └── README.md
├── scripts/
│   └── check_infrastructure.py
├── tests/
│   └── test_infrastructure.py
├── .gitignore
├── requirements.txt
└── README.md
```

O dashboard disponibilizado no repositório é um exemplo baseado no ambiente original e requer adaptação dos filtros e do datasource antes de ser utilizado em outra instalação.

---

## 🔒 Segurança

Algumas medidas adotadas neste laboratório:

- Token de API Proxmox com permissões de leitura.
- Validação TLS nas conexões HTTPS com o Proxmox.
- Credenciais e configurações locais mantidas fora do repositório.
- Arquivo `.env` ignorado pelo Git.
- Administração do Grafana protegida pelo Cloudflare Access.
- Dashboard público separado da interface administrativa.
- Permissões mínimas de leitura no workflow do GitHub Actions.

O compartilhamento público permite visualizar métricas selecionadas, sem fornecer intencionalmente acesso de administração.

---
