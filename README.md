# Motor de Inferência Inteligente com Extração Semântica

**TP04 - Inteligência Artificial 2025**  
**Professor:** Bongo Cahisso  
---

## Descrição

Sistema de inferência lógica baseado em regras que:
- ✅ Extrai automaticamente **fatos** e **regras** de textos em linguagem natural
- ✅ Implementa **encadeamento para frente** (forward chaining)
- ✅ Realiza consultas com **provas detalhadas**
- ✅ Exibe **árvores de dedução** visualmente
- ✅ Interface Web interativa com Flask
- ✅ Base de conhecimento persistente em JSON
- ✅ Containerizado com Docker

---

## Instalação e Execução

### Opção 1: Makefile (Recomendado)

```bash
make build    # Construir imagem Docker
make run      # Executar container
```

Aceder: **http://localhost:5000**

Ver todos os comandos: `make help`

### Opção 2: Docker Manual

```bash
docker build -t tp04-inference-engine .
docker run -d --name tp04-app -p 5000:5000 tp04-inference-engine
```

Consultar **[DOCKER.md](DOCKER.md)** para guia completo.

### Opção 3: Execução Local

```bash
make install  # Instalar dependências
make local    # Executar aplicação
```

Ou manualmente:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
python -m app.web_app
```

---

##  Estrutura do Projeto

```
tp04_ia/
├── app/
│   ├── text_reader.py          # Leitura de ficheiros
│   ├── extractor.py            # Extração semântica (spaCy)
│   ├── kb_manager.py           # Gestão da base de conhecimento
│   ├── unification.py          # Unificação de predicados
│   ├── inference.py            # Motor de inferência (forward chaining)
│   ├── query_engine.py         # Motor de consultas com provas
│   ├── web_app.py              # Aplicação Flask
│   └── templates/
│       └── index.html          # Interface Web
├── sample_texts/               # Textos de exemplo
│   ├── exemplo1.txt
│   ├── exemplo2.txt
│   └── exemplo3.txt
├── notebooks/
│   └── demo_inferencia.ipynb   # Demonstração completa
├── tests/                      # Testes unitários
│   ├── test_extractor.py
│   ├── test_unification.py
│   ├── test_inference.py
│   ├── test_query.py
│   ├── test_integration.py
│   └── run_all_tests.py
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Configuração Docker
├── Makefile                    # Comandos simplificados
├── DOCKER.md                   # Guia completo Docker
├── start.sh                    # Script de início rápido
└── README.md                   # Este ficheiro
```

---

## Como Usar

### 1. Upload de Texto

1. Aceder à interface web em http://localhost:5000
2. Clicar na área de upload
3. Selecionar um ficheiro `.txt` (ex: `sample_texts/exemplo1.txt`)
4. O sistema extrai automaticamente fatos e regras

### 2. Visualizar Base de Conhecimento

- Clicar em **"Ver Fatos"** para expandir os fatos extraídos
- Clicar em **"Ver Regras"** para expandir as regras
- Visualizar estatísticas (fatos, regras, inferências)

### 3. Executar Consultas

Digite consultas no formato: `predicado(argumento)?`

**Exemplos:**
- `mortal(Sócrates)?`
- `pensador(Platão)?`
- `ser_vivo(Rex)?`

O sistema retorna:
- ✅ **Verdadeiro** / ❌ **Falso**
- **Árvore de prova** completa

---

##  Exemplo Prático

### Ficheiro de entrada (`exemplo1.txt`)

```
Sócrates é um humano.
Todo humano é mortal.
Platão é um filósofo.
Todo filósofo é pensador.
```

### Fatos Extraídos

```
humano(Sócrates)
filósofo(Platão)
```

### Regras Extraídas

```
mortal(X) :- humano(X)
pensador(X) :- filósofo(X)
```

### Consulta: `mortal(Sócrates)?`

**Resultado:** ✅ **VERDADEIRO**

**Árvore de Prova:**
```
└── mortal(Sócrates)
    (regra: mortal(X) :- humano(X))
    └── humano(Sócrates)
        (fato base)
```

---

## 🧪 Executar Testes

### Todos os testes

```bash
source venv/bin/activate
python tests/run_all_tests.py
```

### Teste de integração

```bash
python tests/test_integration.py
```

### Resultado Esperado

```
============================================================
🧪 EXECUTANDO TODOS OS TESTES
============================================================

 Testes de Extração...
✓ Testes de extração: OK

 Testes de Unificação...
✓ Testes de unificação: OK

⚡ Testes de Inferência...
✓ Testes de inferência: OK

 Testes de Consultas...
✓ Testes de consultas: OK

============================================================
✅ TODOS OS TESTES PASSARAM COM SUCESSO!
============================================================
```

---

## 🐳 Docker

### Construir e Executar

```bash
docker-compose up --build
```

### Parar

```bash
docker-compose down
```

### Características do Container

- **Imagem Base:** Python 3.11-slim
- **Modelo spaCy:** pt_core_news_sm-3.7.0
- **Porta:** 5000
- **Volumes:** Persistência de dados
- **Auto-restart:** Configurado

---

## Tecnologias Utilizadas

- **Python 3.11**
- **spaCy 3.7.2** - Processamento de linguagem natural
- **Flask 3.0.0** - Framework web
- **Docker** - Containerização
- **JSON** - Persistência de dados

---

##  Funcionalidades Implementadas

- ✅ Identificação de entidades com spaCy
- ✅ Extração de fatos: "X é um Y"
- ✅ Extração de regras: "Todo X é Y"
- ✅ Normalização de termos
- ✅ Suporte a Unicode (português)
- ✅ Encadeamento para frente (forward chaining)
- ✅ Unificação de predicados
- ✅ Aplicação de substituições
- ✅ Derivação de novos fatos
- ✅ Prevenção de duplicados
- ✅ Justificações com IDs únicos
- ✅ Parse de consultas
- ✅ Busca em base de conhecimento
- ✅ Geração de árvores de prova
- ✅ Formato hierárquico
- ✅ Tracking de derivações
- ✅ Upload de ficheiros
- ✅ Visualização da KB
- ✅ Consultas interativas
- ✅ Árvores de prova colapsáveis
- ✅ Design moderno e responsivo
- ✅ README completo
- ✅ Dockerfile funcional
- ✅ Interface moderna com gradientes
- ✅ Jupyter Notebook demonstrativo
- ✅ Script de início rápido
- ✅ Suite completa de testes

---

## 📚 Recursos Adicionais

- **Jupyter Notebook:** `notebooks/demo_inferencia.ipynb` - Demo interativa completa
- **Textos de Exemplo:** `sample_texts/*.txt` - Exemplos prontos a usar
- **Instruções de Avaliação:** `INSTRUCOES_AVALIACAO.md` - Guia para o professor
- **Checklist:** `checklist.md` - Lista de tarefas completa

---

## 🎓 Autor
**Ângela Amaro - 20220145**
**Projeto desenvolvido para TP04 - Inteligência Artificial 2025, ISPTEC**

---

## 📄 Licença

Projeto académico - ISPTEC - cadeira de Inteligência Artificial 2025
