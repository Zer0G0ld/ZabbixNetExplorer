# ZabbixNetExplorer

Este é um script Python para realizar um **scan de rede** em busca de dispositivos ativos e verificar se eles estão rodando o **Zabbix Agent**. Ele coleta informações como **hostname** e **sistema operacional** dos dispositivos encontrados, e salva essas informações em arquivos separados.

## Descrição

O script foi desenvolvido para facilitar a descoberta de dispositivos em uma rede local e verificar sua compatibilidade com o **Zabbix**, um sistema de monitoramento de rede. A principal funcionalidade é identificar quais dispositivos têm o Zabbix Agent ativo, além de coletar informações sobre cada máquina, como **nome do host** e **sistema operacional**.

Ao final da execução, o script gera dois arquivos de saída com a listagem de dispositivos:

- **ZabbixOnDevices.txt**: Contém os dispositivos com Zabbix Agent ativo.
- **ZabbixOffDevices.txt**: Contém os dispositivos sem Zabbix Agent ativo.

Além disso, ele exibe um resumo no console com a quantidade de dispositivos ativos e inativos, além de uma contagem dos hosts por sistema operacional.

## Requisitos

Para executar o script, você precisa garantir que o ambiente de desenvolvimento possua os seguintes requisitos:

- **Python 3.6 ou superior**.
- Bibliotecas Python necessárias:
  - **nmap**: Para realizar a verificação do sistema operacional dos dispositivos.
  - **scapy**: Para realizar o scan de rede usando pacotes ARP.
  
### Instalação das dependências:

Você pode instalar as bibliotecas necessárias com o seguinte comando:

```bash
pip install python-nmap scapy
```

## Como Usar

### Passo 1: Preparação do Ambiente

Antes de executar o script, é necessário garantir que as dependências estejam instaladas em seu ambiente de desenvolvimento. Para isso, siga as etapas abaixo:

1. **Instalar Python 3.6 ou superior**: O script é compatível com o Python 3.6 ou versões superiores. Caso ainda não tenha o Python instalado, você pode baixá-lo e instalá-lo [aqui](https://www.python.org/downloads/).

2. **Instalar as dependências do script**: O script usa as bibliotecas `nmap` e `scapy`. Para instalá-las, execute os seguintes comandos no terminal:

   ```bash
   pip install python-nmap scapy
   ```

### Passo 2: Modificar o Código (opcional)

O script está configurado para escanear a rede **`192.168.1.0/24`** por padrão. Caso sua rede tenha uma faixa de IP diferente, edite a variável `ip_range` no código para refletir a faixa de IP que você deseja escanear.

No script, altere esta linha para ajustar o intervalo de IPs:

```python
ip_range = "192.168.1.0/24"  # Exemplo de rede padrão
```

Substitua `"192.168.1.0/24"` pela faixa de IP da sua rede.

### Passo 3: Executando o Script

Agora que o ambiente está preparado, você pode executar o script. No terminal, navegue até o diretório onde o arquivo do script está localizado e execute o seguinte comando:

```bash
python network_scanner.py
```

### Passo 4: Interação Inicial

Ao executar o script, ele irá exibir uma mensagem explicativa sobre sua funcionalidade. O usuário será solicitado a confirmar se deseja continuar com o escaneamento da rede:

```
Este script é para vasculhar a rede e buscar dados para automatizar a adição de hosts no Zabbix.
Vamos fazer um scan na sua rede procurando por IPs ativos e verificar se ele tem o Zabbix.
Vamos procurar também o nome de cada máquina com seu respectivo IP e MAC, buscando o nome e o sistema operacional dela.

Concorda com isso? Sim[S] ou Não[N]:
```

Digite **`S`** para continuar ou **`N`** para cancelar o processo.

### Passo 5: Acompanhando o Processo

Se você escolher **`S`** para continuar, o script começará o escaneamento da rede especificada (por padrão, `192.168.1.0/24`) para identificar dispositivos ativos. Durante o processo, o script enviará pacotes ARP para a rede e aguardará as respostas dos dispositivos conectados.

O script também verificará se o **Zabbix Agent** está ativo em cada dispositivo, tentando conectar à porta **`10050`** de cada IP encontrado. Se o agente estiver ativo, o dispositivo será marcado como "Ativo" e será registrado no arquivo **ZabbixOnDevices.txt**. Caso contrário, ele será marcado como "Inativo" e registrado no **ZabbixOffDevices.txt**.

### Passo 6: Resultado Final

Após o escaneamento, o script exibirá um resumo no console com as seguintes informações:

- A faixa de IP escaneada.
- O número total de dispositivos encontrados.
- O número de dispositivos com **Zabbix Agent** ativo.
- O número de dispositivos sem **Zabbix Agent**.
- Uma contagem de dispositivos por **sistema operacional**.

Além disso, ele gerará dois arquivos de saída:

- **ZabbixOnDevices.txt**: Contém os dispositivos com Zabbix Agent ativo.
- **ZabbixOffDevices.txt**: Contém os dispositivos sem Zabbix Agent.

#### Exemplo de Saída no Console:

```
Resumo do Scan:
Range escaneado: 192.168.1.0/24
Dispositivos encontrados: 5
Ativos com Zabbix: 3
Inativos sem Zabbix: 2

Quantidade de hosts por Sistema Operacional:
Linux: 2 hosts
Windows: 1 host
Desconhecido: 2 hosts
```

#### Exemplo de Arquivo de Saída **ZabbixOnDevices.txt**:

```
Dispositivos com Zabbix Agent:
Dispositivo1 - Sistema Operacional: Linux
Dispositivo2 - Sistema Operacional: Windows
```

#### Exemplo de Arquivo de Saída **ZabbixOffDevices.txt**:

```
Dispositivos sem Zabbix Agent:
Dispositivo3 - Sistema Operacional: Linux
Dispositivo4 - Sistema Operacional: Windows
```

### Passo 7: Análise de Resultados

Após a execução do script, você pode abrir os arquivos **ZabbixOnDevices.txt** e **ZabbixOffDevices.txt** para revisar quais dispositivos têm o Zabbix Agent ativo e quais não têm. Esses arquivos podem ser utilizados para automatizar a adição de hosts no Zabbix, ou para outras ações de gerenciamento de rede.

## Estrutura do Código

1. **Função `setup()`**: Inicia o script, solicita a confirmação do usuário e inicia o processo de escaneamento e verificação dos dispositivos.
2. **Função `create_files()`**: Cria os arquivos **ZabbixOnDevices.txt** e **ZabbixOffDevices.txt** para armazenar os dispositivos com e sem Zabbix Agent.
3. **Função `scan_network(ip_range)`**: Realiza o scan da rede usando pacotes ARP para identificar dispositivos ativos.
4. **Função `data_machine_ip(ip)`**: Usa o `nmap` para coletar informações sobre o sistema operacional e hostname do dispositivo.
5. **Função `check_zabbix_agent(ip)`**: Verifica se o Zabbix Agent está ativo no dispositivo, tentando conectar à porta `10050`.
6. **Função `add_to_files(ip, mac, status)`**: Adiciona as informações dos dispositivos encontrados nos arquivos de saída.

## Personalização

Você pode ajustar a faixa de IP que o script irá escanear alterando a variável `ip_range`. No exemplo abaixo, a faixa está configurada para `192.168.1.0/24`, mas você pode modificá-la conforme a sua rede:

```python
ip_range = "192.168.1.0/24"  # Exemplo de rede padrão
```

## Exemplo de Execução

1. Inicie o script:

```bash
python network_scanner.py
```

2. Após a execução, você verá o seguinte no console:

```
Este script é para vasculhar a rede e buscar dados para automatizar a adição de hosts no Zabbix.
Vamos fazer um scan na sua rede procurando por IPs ativos e verificar se ele tem o Zabbix.
Vamos procurar também o nome de cada máquina com seu respectivo IP e MAC, buscando o nome e o sistema operacional dela.

Concorda com isso? Sim[S] ou Não[N]:
```

Digite "S" para continuar ou "N" para cancelar.

Após a execução, os arquivos **ZabbixOnDevices.txt** e **ZabbixOffDevices.txt** serão gerados com as informações dos dispositivos encontrados.

## Logs e Debugging

Durante a execução, o script faz uso do módulo `logging` para capturar detalhes sobre a execução e possíveis erros. Você pode ajustar o nível de log se necessário, alterando a configuração do `logging.basicConfig`.

## Contribuindo

Se você deseja contribuir para este projeto, fique à vontade para abrir pull requests ou relatar problemas através do GitHub.

## Licença

Este projeto é licenciado sob a **GNU General Public License v3.0** - veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
