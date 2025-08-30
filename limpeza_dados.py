#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: limpeza_dados.py
Descrição:
    Este script processa arquivos CSV ou Excel (.xlsx/.xls), realizando limpeza de colunas de texto.

Abordagem de limpeza de dados, conforme o escopo definido:
    - Remove caracteres especiais, mantendo apenas letras, números, underscores (_) e espaços.
    - Corrige textos com mojibake (erros de encoding) e remove acentuação.
    - Normaliza espaços extras.
    - Para bases de produtos, trata especificamente a coluna de preço e padrões de tamanho (ex.: 10x20).
    - Converte colunas numéricas quando aplicável.
    - Exporta o resultado no mesmo formato de entrada (.csv ou .xlsx).
    - Inclui tratamento robusto de erros e segue boas práticas de programação.
"""

from __future__ import annotations
import sys
import os
import re
import unicodedata
import pandas as pd
from typing import Any


def corrigir_mojibake(texto: Any) -> Any:
    """Corrige problemas de encoding (mojibake) em textos importados."""
    if not isinstance(texto, str):
        return texto
    if re.search(r'[ÃÂ ]', texto):
        try:
            return texto.encode('latin1').decode('utf-8')
        except Exception:
            return texto
    return texto


def remover_acentos(texto: Any) -> Any:
    """Remove acentuação e normaliza caracteres especiais em textos."""
    if not isinstance(texto, str):
        return texto
    texto = unicodedata.normalize('NFKD', texto)
    return ''.join(ch for ch in texto if unicodedata.category(ch) != 'Mn')


def limpar_texto(valor: Any, contexto: str = "geral", nome_coluna: str | None = None) -> Any:
    """
    Realiza a limpeza de um valor de texto:
    - Remove caracteres inválidos.
    - Normaliza espaços.
    - Aplica regras específicas para 'produtos' ou 'clientes'.
    """
    if pd.isna(valor): # mantém NaN
        return valor # mantém NaN
    texto = str(valor) # garante que é string
    texto = corrigir_mojibake(texto) # corrige mojibake
    texto = remover_acentos(texto) # remove acentuação
    texto = re.sub(r'(\d),(\d)', r'\1.\2', texto)  # troca vírgula decimal por ponto

    if contexto == "produtos":
        # Regras específicas para produtos
        if nome_coluna and nome_coluna.lower() == "preco":   # coluna de preço
            texto = re.sub(r'[^0-9\.\-]+', '', texto)        # remove inválidos, mantém ponto e hífen
            return texto.strip()                             # remove espaços extras
        if re.fullmatch(r'.*_\d+[xX]\d+', texto):            # padrão tamanho com underscore
            texto = re.sub(r'[^A-Za-z0-9_xX ]+', '', texto)  # remove inválidos, mantém underscore e 'x'
            texto = re.sub(r'\s+', ' ', texto).strip()       # remove espaços extras
            texto = re.sub(r'(\d)\s*[xX]\s*(\d)', r'\1x\2', texto)  # normaliza padrão "x"
            return texto 
        texto = texto.replace("_", " ")                    # trata underscore como espaço
        texto = re.sub(r'[^A-Za-z0-9 ]+', '', texto)       # remove inválidos
        texto = re.sub(r'\s+', ' ', texto).strip()         # remove espaços extras
        texto = re.sub(r'([a-z])([A-Z])', r'\1 \2', texto)  # separa camelCase
        texto = re.sub(r'([A-Za-z])(\d)', r'\1 \2', texto)  # separa letra+número
        texto = re.sub(r'(\d)([A-Za-z])', r'\1 \2', texto)  # separa número+letra
        texto = re.sub(r'(\d)\s*[xX]\s*(\d)', r'\1x\2', texto)  # normaliza padrão "x"
        return texto.strip()
    else:
        # Regras específicas para clientes
        texto = re.sub(r'\s*_\s*', '_', texto)       # mantém underscore limpo
        texto = re.sub(r'[^A-Za-z0-9_ ]+', '', texto)  # remove inválidos
        texto = re.sub(r'\s+', ' ', texto).strip()   # remove espaços extras
        texto = re.sub(r'([A-Za-z])(\d)', r'\1 \2', texto)  # separa letra+número
        texto = re.sub(r'(\d)([A-Za-z])', r'\1 \2', texto)  # separa número+letra
        texto = re.sub(r'\s*_\s*', '_', texto)     # limpa espaços em underscores
        return texto.strip()


def expandir_coluna_csv_embutido(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expande colunas quando um CSV foi salvo incorretamente em uma única coluna.
    Reconstrói o cabeçalho e separa os dados corretamente.
    """
    if df.shape[1] != 1:
        return df
    nome_col = str(df.columns[0])
    if ',' in nome_col:
        cabecalho = [c.strip() for c in nome_col.split(',')]
        serie = df.iloc[:, 0].astype(str)
        dados = serie.str.split(',', n=len(cabecalho)-1, expand=True)
        dados.columns = cabecalho
        dados.reset_index(drop=True, inplace=True)
        return dados
    primeiro = str(df.iloc[0, 0]) if df.shape[0] > 0 else ''
    if ',' in primeiro:
        todas = df.iloc[:, 0].astype(str)
        temp = todas.str.split(',', expand=True)
        header = temp.iloc[0].tolist()
        if len(header) > 1:
            dados = temp.iloc[1:].copy()
            dados.columns = [h.strip() for h in header]
            dados.reset_index(drop=True, inplace=True)
            return dados
    return df


def tentar_converter_numerico(col: pd.Series, contexto: str, nome_coluna: str) -> pd.Series:
    """
    Tenta converter uma coluna textual em valores numéricos.
    Aplica formatação especial para preços em 'produtos'.
    """
    if not pd.api.types.is_object_dtype(col) and not pd.api.types.is_string_dtype(col):
        if contexto == "produtos" and nome_coluna.lower() == "preco":
            col_num = pd.to_numeric(col, errors='coerce').round(2)
            return col_num.map(lambda x: f"{x:.2f}" if pd.notna(x) else "")
        return col
    nao_nulos = col.dropna().astype(str)
    if nao_nulos.empty:
        return col
    nao_nulos = nao_nulos.str.replace(',', '.', regex=False)
    padrao_numerico = nao_nulos.str.match(r'^-?\d+(\.\d+)?$')
    if padrao_numerico.all():
        col_num = pd.to_numeric(nao_nulos, errors='coerce').reindex(col.index)
        if contexto == "produtos" and nome_coluna.lower() == "preco":
            return col_num.round(2).map(lambda x: f"{x:.2f}" if pd.notna(x) else "")
        return col_num
    return col


def processar_arquivo(arquivo_entrada: str, arquivo_saida: str) -> None:
    """
    Processa o arquivo de entrada:
    - Detecta o formato (CSV ou Excel).
    - Aplica a limpeza de dados.
    - Converte colunas numéricas quando aplicável.
    - Salva no formato de saída.
    """
    if not os.path.exists(arquivo_entrada):
        raise FileNotFoundError(f"Arquivo '{arquivo_entrada}' não encontrado.")
    ext_in = arquivo_entrada.lower().split('.')[-1]
    ext_out = arquivo_saida.lower().split('.')[-1]

    # Leitura do arquivo de entrada
    if ext_in == 'csv':
        try:
            df = pd.read_csv(arquivo_entrada, sep=',', encoding='utf-8', dtype=None)
        except Exception:
            df = pd.read_csv(arquivo_entrada, sep=',', encoding='latin1', dtype=None)
    elif ext_in in ('xlsx', 'xls'):
        df = pd.read_excel(arquivo_entrada, dtype=None)
        df = expandir_coluna_csv_embutido(df)
    else:
        raise ValueError("Formato de entrada não suportado. Use .csv ou .xlsx")

    # Define contexto (produtos ou clientes) a partir do nome do arquivo de saída
    contexto = "produtos" if "produtos" in arquivo_saida.lower() else "clientes"

    # Limpeza dos nomes de colunas
    novos_nomes = []
    for col in df.columns:
        nome_limpo = limpar_texto(col, contexto, nome_coluna=col)
        novos_nomes.append(nome_limpo if nome_limpo != '' else col)
    df.columns = novos_nomes

    # Limpeza dos valores textuais
    for coluna in df.columns:
        if pd.api.types.is_string_dtype(df[coluna]) or df[coluna].dtype == object:
            df[coluna] = df[coluna].apply(lambda v: limpar_texto(v, contexto, nome_coluna=coluna))

    # Conversão de colunas numéricas quando possível
    for coluna in df.columns:
        df[coluna] = tentar_converter_numerico(df[coluna], contexto, nome_coluna=coluna)

    # Formatação final da coluna de preço em produtos
    if contexto == "produtos" and "preco" in [c.lower() for c in df.columns]:
        nome_preco = next(c for c in df.columns if c.lower() == "preco")
        df[nome_preco] = pd.to_numeric(df[nome_preco], errors='coerce').round(2).map(
            lambda x: f"{x:.2f}" if pd.notna(x) else ""
        )

    # Exportação do arquivo no formato de saída
    if ext_out == 'csv':
        df.to_csv(arquivo_saida, index=False, sep=',', encoding='utf-8-sig')
    elif ext_out in ('xlsx', 'xls'):
        df.to_excel(arquivo_saida, index=False)
    else:
        raise ValueError("Formato de saída não suportado. Use .csv ou .xlsx")

# Função principal para execução via linha de comando 
def main():
    if len(sys.argv) != 3:
        print("Uso: python limpeza_dados.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)
    entrada = sys.argv[1]
    saida = sys.argv[2]
    try:
        processar_arquivo(entrada, saida)
        print(f"✅ Arquivo processado com sucesso: {saida}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

# Execução direta do script
if __name__ == '__main__':
    main()
