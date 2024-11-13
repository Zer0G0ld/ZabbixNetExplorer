# ZabbixNetExplorer

Este script Python realiza um **scan de rede** para detectar dispositivos ativos e verificar se estão executando o **Zabbix Agent**. O script coleta informações como **hostname** e **sistema operacional** dos dispositivos encontrados e salva essas informações em arquivos separados.

## Descrição

O **ZabbixNetExplorer** facilita a descoberta de dispositivos em uma rede local e verifica sua compatibilidade com o **Zabbix** (um sistema de monitoramento de rede). A principal funcionalidade do script é identificar dispositivos que possuem o Zabbix Agent ativo e coletar dados sobre cada máquina, como **nome do host** e **sistema operacional**.

Após a execução, o script gera dois arquivos de saída com a listagem de dispositivos:

- **ZabbixOnDevices.txt**: Contém os dispositivos com Zabbix Agent ativo.
- **ZabbixOffDevices.txt**: Contém os dispositivos sem Zabbix Agent ativo.

Além disso, um resumo é exibido no console, indicando a quantidade de dispositivos ativos e inativos, bem como a contagem de hosts por sistema operacional.

## Requisitos

Para executar o script, você precisa garantir que o ambiente de desenvolvimento possua os seguintes requisitos:

- **Python 3.6 ou superior**.
- Bibliotecas Python necessárias:
  - **nmap**: Para verificar o sistema operacional dos dispositivos.
  - **scapy**: Para realizar o scan de rede usando pacotes ARP.

### Instalação das dependências

Para instalar as bibliotecas necessárias, execute:

```bash
pip install python-nmap scapy
```

## Criando um Ambiente Virtual

### Passo 1: Instalar o Python

O script foi desenvolvido para **Python 3.6 ou superior**. Verifique sua versão com:

```bash
python --version
```

Se necessário, baixe e instale o Python [aqui](https://www.python.org/downloads/).

### Passo 2: Criar um Ambiente Virtual

1. **Abra o terminal** (ou prompt de comando no Windows).
2. **Navegue até o diretório do seu projeto**:

   ```bash
   cd /caminho/para/seu/projeto
   ```

3. **Crie o ambiente virtual**:

   - No Linux/macOS:

     ```bash
     python3 -m venv venv
     ```

   - No Windows:

     ```bash
     python -m venv venv
     ```

   Isso cria a pasta `venv` com o ambiente virtual.

### Passo 3: Ativar o Ambiente Virtual

- No Linux/macOS:

  ```bash
  source venv/bin/activate
  ```

- No Windows:

  ```bash
  .\venv\Scripts\activate
  ```

Após ativar, seu prompt de comando mudará para indicar que o ambiente virtual está ativo.

### Passo 4: Instalar as Dependências

Se você tiver um arquivo `requirements.txt`, instale as dependências com:

```bash
pip install -r requirements.txt
```

Caso contrário, use os comandos para instalar as bibliotecas necessárias diretamente:

```bash
pip install python-nmap scapy
```

### Passo 5: Desativar o Ambiente Virtual

Para desativar o ambiente virtual:

```bash
deactivate
```

### Passo 6: Recriar o Ambiente Virtual

Se necessário, recrie o ambiente virtual:

1. Crie o ambiente virtual (Passo 2).
2. Instale as dependências com `pip install -r requirements.txt` (Passo 4).

## Como Usar

### Passo 1: Preparação do Ambiente

Antes de executar o script, instale as dependências e verifique se o Python 3.6+ está corretamente instalado.

### Passo 2: Modificar a Faixa de IP (opcional)

O script escaneia a rede **`192.168.1.0/24`** por padrão. Para modificar a faixa de IP, altere a variável `ip_range` no código:

```python
ip_range = "192.168.1.0/24"  # Substitua pela faixa de IP da sua rede
```

### Passo 3: Executando o Script

No terminal, navegue até o diretório do script e execute:

```bash
python network_scanner.py
```

### Passo 4: Interação Inicial

O script solicitará confirmação antes de iniciar o escaneamento:

```
Este script realiza o scan da rede e verifica quais dispositivos têm o Zabbix Agent ativo. Concorda com isso? (S/N)
```

Digite **`S`** para continuar ou **`N`** para cancelar.

### Passo 5: Acompanhando o Processo

Após a confirmação, o script inicia o scan da rede, utilizando pacotes ARP para identificar dispositivos ativos e verificando a presença do Zabbix Agent na porta **`10050`**. Dispositivos com o Zabbix Agent ativo são salvos no arquivo **ZabbixOnDevices.txt** e os inativos em **ZabbixOffDevices.txt**.

### Passo 6: Resultado Final

Após o scan, o script exibe no console:

- A faixa de IP escaneada.
- O número total de dispositivos encontrados.
- O número de dispositivos com Zabbix Agent ativo.
- O número de dispositivos sem Zabbix Agent.
- A contagem de dispositivos por **sistema operacional**.

Arquivos gerados:

- **ZabbixOnDevices.txt**: Dispositivos com Zabbix Agent ativo.
- **ZabbixOffDevices.txt**: Dispositivos sem Zabbix Agent.

#### Exemplo de Saída no Console:

```
Resumo do Scan:
Faixa escaneada: 192.168.1.0/24
Dispositivos encontrados: 5
Ativos com Zabbix: 3
Inativos sem Zabbix: 2

Hosts por Sistema Operacional:
Linux: 2
Windows: 1
Desconhecido: 2
```

#### Exemplo de Arquivo **ZabbixOnDevices.txt**:

```
Dispositivos com Zabbix Agent:
Dispositivo1 - Sistema Operacional: Linux
Dispositivo2 - Sistema Operacional: Windows
```

#### Exemplo de Arquivo **ZabbixOffDevices.txt**:

```
Dispositivos sem Zabbix Agent:
Dispositivo3 - Sistema Operacional: Linux
Dispositivo4 - Sistema Operacional: Windows
```

### Passo 7: Análise de Resultados

Revise os arquivos gerados para identificar dispositivos com o Zabbix Agent ativo e para automatizar a adição de hosts no Zabbix.

## Estrutura do Código

1. **`setup()`**: Inicia o script, solicita confirmação do usuário e inicia o processo de escaneamento.
2. **`create_files()`**: Cria os arquivos de saída **ZabbixOnDevices.txt** e **ZabbixOffDevices.txt**.
3. **`scan_network(ip_range)`**: Realiza o scan de rede usando pacotes ARP.
4. **`data_machine_ip(ip)`**: Usa `nmap` para obter informações sobre o sistema operacional e hostname.
5. **`check_zabbix_agent(ip)`**: Verifica a presença do Zabbix Agent na porta **10050**.
6. **`add_to_files(ip, mac, status)`**: Registra informações sobre os dispositivos nos arquivos de saída.

## Personalização

Você pode ajustar a faixa de IP no código:

```python
ip_range = "192.168.1.0/24"  # Alterar para a faixa de IP da sua rede
```

## Exemplo de Execução

1. Execute o script:

```bash
python network_scanner.py
```

2. Confirme a execução com **`S`** ou **`N`**.

Após a execução, os arquivos **ZabbixOnDevices.txt** e **ZabbixOffDevices.txt** serão gerados com as informações dos dispositivos.

## Logs e Debugging

O script utiliza o módulo `logging` para capturar erros e detalhes da execução. Você pode ajustar o nível de log, se necessário.

## Contribuindo

Se quiser contribuir, envie pull requests ou abra issues no GitHub.

## Licença

Este projeto está licenciado sob a **GNU General Public License v3.0**. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.
