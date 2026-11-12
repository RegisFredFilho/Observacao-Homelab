# INC-001 — Indisponibilidade simulada da VM ansible-node

**Projeto:** Observacao-Homelab  
**Ambiente:** Homelab Proxmox VE  
**Tipo:** Incidente simulado  
**Severidade:** Warning  
**Status:** Resolvido  
**Ferramentas:** Proxmox VE, Zabbix e Grafana

---

## 1. Objetivo

Validar a capacidade do ambiente de monitoramento de detectar a indisponibilidade de uma máquina virtual, registrar eventos, executar ações de notificação e identificar a recuperação do serviço.

## 2. Ambiente monitorado

O laboratório utiliza o Proxmox VE como plataforma de virtualização e o Zabbix como ferramenta central de monitoramento.

O template `Proxmox VE by HTTP` realiza consultas à API do Proxmox e permite descobrir automaticamente máquinas virtuais e containers.

O Grafana é utilizado para visualização das métricas coletadas.

**Máquina utilizada no teste:**

- Nome: `ansible-node`
- VMID: `204`
- Plataforma: Proxmox VE
- Monitoramento: Zabbix
- Trigger: `Not running`

## 3. Procedimento de simulação

Foi realizado um desligamento controlado da máquina virtual de laboratório.

O objetivo era provocar um evento real de indisponibilidade e verificar o funcionamento do monitoramento sem interromper serviços críticos.

O ambiente Zabbix já possuía uma trigger para identificar quando a máquina virtual deixasse de apresentar o estado esperado de execução.

Foi configurada uma ação específica para o teste, com envio de mensagens por e-mail.

## 4. Linha do tempo

| Horário | Evento |
|---|---|
| 19:12:52 | Indisponibilidade registrada pelo Zabbix |
| Durante o incidente | Recebimento de notificação por e-mail confirmado |
| 19:14:52 | Recuperação registrada pelo Zabbix |

**Duração registrada:** 2 minutos.

## 5. Detecção

O Zabbix detectou que a VM não estava em execução e registrou um evento de severidade `Warning`.

A trigger utilizada foi:

`Proxmox VE: Node [inferno]: QEMU [ansible-node]: Not running`

O evento pôde ser acompanhado na interface **Monitoring → Problems**.

## 6. Notificações

A ação de monitoramento foi configurada para enviar mensagens aos usuários selecionados por meio de um media type SMTP.

O recebimento de uma notificação por e-mail foi confirmado durante a simulação.

Também foi configurada uma operação para notificar a recuperação do incidente. O recebimento dessa segunda mensagem não foi registrado como evidência neste relatório.

## 7. Recuperação

Após o retorno da VM ao estado de execução, o Zabbix identificou a normalização e registrou a recuperação do problema.

A interface apresentou o horário de recuperação e a duração total do incidente.

## 8. Resultado

A simulação demonstrou o funcionamento das seguintes etapas:

- Descoberta e monitoramento de uma máquina virtual Proxmox.
- Detecção de indisponibilidade pelo Zabbix.
- Registro de evento com severidade.
- Envio de notificação automática por e-mail.
- Identificação da recuperação.
- Registro do período de indisponibilidade.

**Resultado final:** teste de detecção e recuperação concluído com sucesso.

## 9. Lições aprendidas

O monitoramento permite identificar alterações na disponibilidade dos recursos sem depender exclusivamente da observação manual do administrador.

A configuração de ações específicas ajuda a reduzir notificações desnecessárias.

Testes controlados também permitem validar o funcionamento das notificações antes de sua utilização em ambientes críticos.

## 10. Melhorias futuras

- Criar runbooks para incidentes recorrentes.
- Padronizar severidades e critérios de notificação.
- Registrar evidências de envio e recebimento das mensagens de recuperação.
- Expandir os cenários de testes.
- Implementar relatórios periódicos de disponibilidade.

---

**Observação:** incidente executado em ambiente de laboratório, exclusivamente para fins de estudo e validação da solução de monitoramento.
