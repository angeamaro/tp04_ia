# Checklist TP04 - Motor de Inferência Inteligente

Use isto como lista de verificação durante o trabalho.

## ✅ Itens Completados

- ✅ Criar virtualenv e requirements.txt.
- ✅ Instalar e configurar spaCy (modelo PT).
- ✅ Implementar read_text(path).
- ✅ Implementar extractor.py:
  - ✅ Extrair fatos simples.
  - ✅ Extrair regras universais.
  - ✅ Normalização dos termos.
  - ✅ Testes básicos de extração.
- ✅ Definir formato JSON para KB (kb.json) e implementar kb_manager.py.
- ✅ Implementar funções básicas de unificação.
- ✅ Implementar motor de inferência (encadeamento para frente):
  - ✅ Aplicação de substituições.
  - ✅ Evitar duplicados.
  - ✅ Registro de justificação/IDs.
- ✅ Implementar módulo de consultas:
  - ✅ Interpretar string de consulta.
  - ✅ Procurar na KB e inferences.
  - ✅ Gerar árvore de prova (estrutura JSON).
- ✅ Desenvolver Interface Web (Flask):
  - ✅ Upload de ficheiros.
  - ✅ Visualização da KB.
  - ✅ Consulta + prova em árvore colapsável.
- ✅ Adicionar Dockerfile e testar containerização.
- ✅ Criar demo_inferencia.ipynb mostrando o fluxo.
- ✅ Escrever README com instruções de execução e exemplos.
- ✅ Criar casos de teste e validar resultados.
- ✅ Revisão final e preparação para entrega.

## 📊 Status do Projeto

**Status:** ✅ **COMPLETO**

**Data de Entrega:** 15/11/2025 às 12:15

### Componentes Implementados:

1. ✅ **Módulo de Processamento de Texto** (`app/text_reader.py`)
2. ✅ **Módulo de Extração Semântica** (`app/extractor.py`)
3. ✅ **Gestor de Base de Conhecimento** (`app/kb_manager.py`)
4. ✅ **Módulo de Unificação** (`app/unification.py`)
5. ✅ **Motor de Inferência** (`app/inference.py`)
6. ✅ **Motor de Consultas** (`app/query_engine.py`)
7. ✅ **Interface Web Flask** (`app/web_app.py` + `templates/index.html`)
8. ✅ **Configuração Docker** (`Dockerfile` + `docker-compose.yml`)
9. ✅ **Jupyter Notebook Demo** (`notebooks/demo_inferencia.ipynb`)
10. ✅ **Testes Unitários** (`tests/`)
11. ✅ **Documentação Completa** (`README.md`)

### Testes:

Todos os testes passam com sucesso:
- ✅ Testes de Extração
- ✅ Testes de Unificação
- ✅ Testes de Inferência
- ✅ Testes de Consultas

### Para Executar:

#### Opção 1: Local
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
python -m app.web_app
```

#### Opção 2: Docker
```bash
docker-compose up --build
```

Aceder: http://localhost:5000
