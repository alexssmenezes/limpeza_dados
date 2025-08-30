/*
🔍 Exemplo de Case de Lógica da Consulta SQL utilizando LEFT JOIN
- Tabela principal: JUIZO (PJ) — ponto de partida, porque queremos listar todos os juízos.
- LEFT JOIN com COMARCA (PC): garante que, mesmo sem comarca associada, o juízo apareça.
- LEFT JOIN com ESTADO (PE): conecta pelo SIG_ESTADO da comarca, retornando nome e sigla do estado quando existir.
- LEFT JOIN com MUNICIPIO (PM): conecta pelo SIG_MUNICIPIO da comarca, retornando nome do município quando existir.
- Uso de alias (AS) para renomear colunas conforme o formato solicitado.
- Preserva linhas da tabela JUIZO mesmo quando as chaves estrangeiras não encontram correspondência.
*/

-- Consulta de Juízos com informações de Estado, Município e Comarca
SELECT 
    PJ.COD_JUIZO,                  -- Código do Juízo
    PJ.NOM_JUIZO AS NOME,          -- Nome do Juízo
    PE.NOM_ESTADO AS ESTADO,       -- Nome do Estado
    PE.SIG_ESTADO,                 -- Sigla do Estado
    PM.NOM_MUNICIPIO AS MUNICIPIO, -- Nome do Município
    PC.NOM_COMARCA AS COMARCA,     -- Nome da Comarca
    PJ.DES_ENDERECO AS ENDERECO,   -- Endereço
    PJ.DES_COMP_ENDERECO AS COMPLEMENTO, -- Complemento do Endereço
    PJ.NOM_BAIRRO AS BAIRRO,       -- Bairro
    PJ.NUM_CEP AS CEP,             -- CEP
    PJ.DES_EMAIL AS EMAIL          -- E-mail de contato
FROM JUIZO PJ                      -- Tabela de Juízos
LEFT JOIN COMARCA PC               -- Tabela de Comarcas
    ON PJ.COD_COMARCA = PC.COD_COMARCA
LEFT JOIN ESTADO PE                -- Tabela de Estados
    ON PC.SIG_ESTADO = PE.SIG_ESTADO
LEFT JOIN MUNICIPIO PM             -- Tabela de Municípios
    ON PC.SIG_MUNICIPIO = PM.SIG_MUNICIPIO;
