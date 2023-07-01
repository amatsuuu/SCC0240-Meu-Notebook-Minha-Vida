# Meu Notebook, Minha Vida

## Descrição

Projeto de um sistema de banco de dados para auxiliar no empréstimo de dispositivos e armazenamento de informações do projeto *Codifique* - um projeto que promove o ensino de programação a alunos de escolas públicas do ensino médio de São Carlos desde 2013. 

O desenvolvimento desse projeto foi feito pelo grupo 6 da disciplina de *Bases de Dados* (SSC0240) realizada no 1° Semestre de 2023.

### Desenvolvedores:
- [André Kenji Hidaka Matsumoto](https://github.com/amatsuuu)
- [Rebeca Vieira Carvalho](https://github.com/rebeca-vc)
- [Reynaldo Coronatto Neto](https://github.com/reynaldocoronatto)
- [Theo da Mota dos Santos](https://github.com/theosant)

## Instalação

Instale Python caso não tenha feito e, em seguida, utilize o gerenciador de pacote [pip](https://pypi.org/project/pip/) para instalar o [oracledb](https://pypi.org/project/oracledb/) e o [dotenv](https://pypi.org/project/python-dotenv/)
```
pip install oracledb

pip install python-dotenv
```

## Utilização

Antes de executar o código, é preciso criar um arquivo *.env* no diretório [App/*](https://github.com/reynaldocoronatto/SCC0240-Meu-Notebook-Minha-Vida/tree/master/App), com as credenciais de acesso ao banco de dados do Oracle. Ele tem que estar no formato:
```
USER_NAME={seu usuário}
USER_PASSWORD={sua senha}
```

Depois disso, para executar o código, certifique-se que você está no diretório [App/](https://github.com/reynaldocoronatto/SCC0240-Meu-Notebook-Minha-Vida/tree/master/App) e execute o seguinte código no terminal:

```
python main.py
```

Caso isso não funcione, tente:

```
python3 main.py
```

## Modelagem
- [Modelo Entidade Relacionamento](https://github.com/reynaldocoronatto/SCC0240-Meu-Notebook-Minha-Vida/blob/master/Modelagem/modelo_entidade_relacionamento.jpg)
- [Modelo Relacional](https://github.com/reynaldocoronatto/SCC0240-Meu-Notebook-Minha-Vida/blob/master/Modelagem/modelo_relacional.jpg)