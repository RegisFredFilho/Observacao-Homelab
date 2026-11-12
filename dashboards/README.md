
# Grafana Dashboard — Infrastructure Overview

Dashboard de observabilidade criado para monitorar
um servidor Proxmox VE utilizando Zabbix e Grafana.

## Tecnologias

- Grafana 13
- Zabbix 7.4
- Proxmox VE
- Plugin Grafana Zabbix

## Painéis

1. Monitoramento de containers LXC
2. Monitoramento de máquinas virtuais
3. Utilização de CPU
4. Utilização de memória RAM
5. Utilização de disco
6. CPU atual
7. Uptime do servidor

## Configuração

O arquivo `infrastructure-overview-example.json`
é um exemplo baseado no ambiente original.

Antes de importá-lo, adapte:

- `REPLACE_WITH_ZABBIX_DATASOURCE_UID`:
  identificador do datasource Zabbix no Grafana.
- `ExampleHost`:
  nome do host cadastrado no Zabbix.
- `example-node`:
  nome do nó Proxmox monitorado.
- Grupo `Proxmox`:
  ajuste caso utilize outro grupo no Zabbix.

## Observações

O dashboard depende dos itens coletados pelo template
Proxmox VE by HTTP do Zabbix.

A validação JSON realizada pela CI verifica apenas
a sintaxe do arquivo, não a compatibilidade de
importação nem a disponibilidade das métricas.

Nenhuma credencial deve ser incluída no repositório.
