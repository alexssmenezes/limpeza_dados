# 📢 ATENÇÃO

- Para que o script funcione corretamente, deve estar no mesmo nível das bases (.csv e .xlsx), ou seja tem que ser relativo à execução. Por exemplo, no mesmo caminho do projeto cd ~/Downloads/limpeza_dados ou se baixar em desktop cd ~/Desktop/limpeza_dados
- Obs.: o arquivo case_left_join.sql não tem relação com o projeto em sí, foi criado para outra finalidade e se preferir pode excluí-lo do seu projeto.

---

## 🧹 limpeza_dados.py

Script Python para **limpeza de bases de dados em CSV e Excel (.xlsx/.xls)**, desenvolvido para remover caracteres especiais e padronizar colunas de texto, atendendo aos critérios de boas práticas e robustez.

---

## 📌 Funcionalidades

- Remove caracteres especiais, mantendo apenas:
  - Letras (a-z, A-Z)
  - Números (0-9)
  - Underscores (`_`)
  - Espaços
- Corrige textos com **mojibake** (erros de encoding).
- Remove **acentuação** e normaliza caracteres.
- Elimina **espaços extras**.
- Trata regras específicas para:
  - **Produtos**: limpeza de preços e padrões de medidas (`10x20`).
  - **Clientes**: preservação de underscores e normalização de nomes.
- Conversão automática de colunas numéricas quando aplicável.
- Exporta no mesmo formato de entrada (`.csv` ou `.xlsx`).
- Tratamento de erros robusto (arquivos inexistentes, formatos inválidos, encoding).

---

## ⚙️ Requisitos

- Python **3.9+**
- Bibliotecas:
  - [pandas](https://pandas.pydata.org/)
  - [openpyxl](https://openpyxl.readthedocs.io/) (para arquivos Excel)

Instalação das dependências:

```bash
pip install pandas openpyxl
```

---

## ▶️ Uso

- O script é executado via linha de comando:

```bash
python limpeza_dados.py <arquivo_entrada> <arquivo_saida>

```

---

## ▶️ Exemplos

- Processar base de clientes:

```bash
python limpeza_dados.py clientes.csv clientes_limpos.csv

```

- Processar base de produtos:

```bash
python limpeza_dados.py produtos.xlsx produtos_limpos.xlsx

```

---

## 📂 Estrutura esperada

- Entrada

- Arquivos CSV ou Excel contendo colunas de texto com caracteres especiais e inconsistências.

- Exemplo:

- clientes.csv → colunas nome, idade, endereco, observacao

- produtos.xlsx → colunas produto, preco, descricao, categoria

- Saída

- Arquivos no mesmo formato de entrada, com colunas e dados limpos e padronizados.

- Exemplo:

- clientes_limpos.csv

- produtos_limpos.xlsx

---

## 🛠️ Estrutura do Código

- O script é modular e segue boas práticas de programação:

- corrigir_mojibake → corrige problemas de encoding.

- remover_acentos → remove acentos e caracteres especiais.

- limpar_texto → aplica regras de limpeza em valores de texto.

- expandir_coluna_csv_embutido → corrige CSVs salvos em coluna única.

- tentar_converter_numerico → converte colunas textuais para numéricas.

- processar_arquivo → organiza o fluxo de leitura, limpeza e gravação.

- main → executa o script via linha de comando.

---

## ⚖️ Critérios Atendidos

- ✔ Funcionalidade → Limpeza correta de caracteres especiais e espaços extras.
- ✔ Robustez → Tratamento de erros e compatibilidade CSV/Excel.
- ✔ Boas práticas → Código modular, legível, nomes de variáveis significativos.
- ✔ Eficiência → Uso otimizado do pandas, pronto para bases reais.

---

## 📜 Licença

- Este projeto pode ser utilizado e adaptado livremente para fins educacionais e corporativos.
- Copyright (c) 2025 Alex Menezes - limpeza_dados.py
