
# Gerador de Verbetes DHBB 0.1

Este software é produzido e mantido dentro do âmbito do projeto "Programação aplicada ao DHBB" pelo CPDOC/FGV, com o objetivo de fornecer uma solução automatizada de geração dos verbetes biográficos do Dicionário Histórico Biográfico Brasileiro (DHBB),  gestão e manutenção de seus metadados.

## ⚙️ Requisitos
- Windows 10 ou superior;
- Python 3.6 ou superior;

## 🖥️ Rodando localmente

Clone o projeto
# EDITAR

```bash
git clone https://github.com/danielbonattoseco/DHBB
```

Entre no diretório do projeto


```bash
cd **seu diretório de clone do projeto**
```

Para executar a aplicação localmente em sua máquina, siga uma das seguintes abordagens:

### 🔴 Opção 1 -  Arquivo Executável

Esta é uma opção mais simples, porém com um arquivo mais pesado e com maior tempo de processamento por trazer consigo todas as dependências necessárias para a execução *standalone* (gerado por [PyInstaller](https://pyinstaller.org/en/stable/)).

**1 -** Execute o arquivo main.exe:

```bash
start dist\main.exe
```

### 🔴 Opção 2 - Arquivo .py (base)

Esta opção rodará o software diretamente no seu ambiente Python, e instalará possíveis dependências no seu sistema.

**1 -** Instale as dependências

```bash
pip install -r requirements.txt
```

**2 -** Execute o arquivo `main.py`:
```bash
python main.py
```

### 🔴 Opção 3 - Arquivo .py (em ambiente virtual)

Esta é uma opção de instalação mais limpa, que instala as dependências diretamente no ambiente virtual e que podem ser eliminadas juntamente com o mesmo, sem interferir no sistema.

**1 -** Crie um novo ambiente virtual em seu diretório de trabalho:

```bash
python -m venv virtual_env
```

**2. -** Ative o ambiente virtual criado:

```bash
virtual_env\Scripts\activate
```
**3 -** Instale as dependências

```bash
pip install -r requirements.txt
```

**4 -** Execute o arquivo `main.py`:
```bash
python main.py
```
## Autores
Orientador: - [Profa. Dra. Jaqueline Porto Zulini](http://lattes.cnpq.br/4672784311890510)
Orientando/Desenvolvedor: - [Daniel Bonatto Seco](http://lattes.cnpq.br/8325397475123191)

## Licença

[MIT](https://choosealicense.com/licenses/mit/)




![Logo](https://cpdoc.fgv.br/sites/default/files/inline-images/logo-pt-br.png)
