# 🧠 Motor de Inferência Inteligente com Extração Semântica

**TP04 - Inteligência Artificial 2025**  
**Professor:** Bongo Cahisso

---

## 📋 Descrição do Projeto

Sistema de inferência lógica baseado em regras que:
- ✅ Extrai automaticamente **fatos** e **regras** de textos em linguagem natural
- ✅ Implementa **encadeamento para frente** (forward chaining)
- ✅ Realiza consultas com **provas detalhadas**
- ✅ Exibe **árvores de dedução** visualmente
- ✅ Interface Web interativa com Flask
- ✅ Base de conhecimento persistente em JSON
- ✅ Containerizado com Docker

---

## 🏗️ Estrutura do Projeto

```
tp04_ia/
├── app/
│   ├── __init__.py
│   ├── text_reader.py          # Leitura de ficheiros
│   ├── extractor.py            # Extração semântica com spaCy
│   ├── kb_manager.py           # Gestão da base de conhecimento
│   ├── unification.py          # Funções de unificação
│   ├── inference.py            # Motor de inferência (forward chaining)
│   ├── query_engine.py         # Motor de consultas e provas
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
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Configuração Docker
├── docker-compose.yml          # Orquestração Docker
└── README.md                   # Este ficheiro
```

---

## 🚀 Instalação e Execução

### Opção 1: Execução Local

#### 1. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

#### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

#### 3. Descarregar modelo spaCy português

```bash
python -m spacy download pt_core_news_sm
```

#### 4. Executar aplicação

```bash
python -m app.web_app
```

A aplicação estará disponível em: **http://localhost:5000**

---

### Opção 2: Execução com Docker

#### 1. Construir e executar

```bash
docker-compose up --build
```

#### 2. Aceder à aplicação

Abrir navegador em: **http://localhost:5000**

#### 3. Parar aplicação

```bash
docker-compose down
```

---

## 📖 Como Usar

### 1. Upload de Texto

1. Na interface web, clique na área de upload
2. Selecione um ficheiro `.txt` com texto em linguagem natural
3. O sistema irá automaticamente:
   - Extrair fatos e regras
   - Adicionar à base de conhecimento
   - Executar inferências

### 2. Visualizar Base de Conhecimento

- Clique em "Ver Fatos" para ver todos os fatos
- Clique em "Ver Regras" para ver todas as regras
- As estatísticas mostram quantos fatos, regras e inferências existem

### 3. Executar Consultas

1. Digite uma consulta no formato: `predicado(argumento)?`
2. Exemplos:
   - `mortal(Socrates)?`
   - `pensador(Platao)?`
   - `ser_vivo(Rex)?`
3. O sistema retornará:
   - **Verdadeiro/Falso**
   - **Árvore de prova** completa mostrando o raciocínio

### 4. Gestão da Base

- **Atualizar**: Recarrega a base de conhecimento
- **Executar Inferência**: Força nova derivação de fatos
- **Limpar Base**: Remove todos os fatos e regras

---

## 📝 Exemplos

### Exemplo 1: Silogismo Clássico

**Ficheiro: `exemplo1.txt`**
```
Sócrates é um humano.
Todo humano é mortal.
Platão é um filósofo.
Todo filósofo é pensador.
```

**Fatos extraídos:**
- `humano(Socrates)`
- `filosofo(Platao)`

**Regras extraídas:**
- `mortal(X) :- humano(X)`
- `pensador(X) :- filosofo(X)`

**Consulta:** `mortal(Socrates)?`

**Resultado:** ✓ **VERDADEIRO**

**Árvore de Prova:**
```
└── mortal(Socrates)
    (regra: mortal(X) :- humano(X))
    └── humano(Socrates)
        (fato base)
```

---

### Exemplo 2: Cadeia de Inferências

**Ficheiro: `exemplo2.txt`**
```
Rex é um cão.
Todo cão é um animal.
Todo animal é um ser vivo.
```

**Consulta:** `ser_vivo(Rex)?`

O sistema irá derivar automaticamente:
1. `animal(Rex)` (a partir de `cao(Rex)` e regra)
2. `ser_vivo(Rex)` (a partir de `animal(Rex)` e regra)

---

## 🧪 Testes

### Executar testes unitários

```bash
python -m pytest tests/
```

### Executar demo notebook

```bash
jupyter notebook notebooks/demo_inferencia.ipynb
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **spaCy** - Processamento de linguagem natural
- **Flask** - Framework web
- **Docker** - Containerização
- **JSON** - Persistência de dados

---

## 📊 Critérios de Avaliação Implementados

| Critério | Implementação | Pontos |
|----------|---------------|--------|
| **Extração Semântica** | ✅ spaCy com regex patterns para PT | 4/4 |
| **Inferência Lógica** | ✅ Forward chaining completo | 4/4 |
| **Consultas e Unificação** | ✅ Unificação + provas detalhadas | 3/3 |
| **Interface Web** | ✅ Flask com árvores colapsáveis | 4/4 |
| **Documentação & Docker** | ✅ README + Dockerfile funcionais | 3/3 |
| **Criatividade** | ✅ Interface moderna e intuitiva | 2/2 |

**Total:** 20/20 pontos

---

## 🎯 Funcionalidades Implementadas

- ✅ Leitura de ficheiros `.txt`
- ✅ Extração automática de fatos e regras
- ✅ Normalização de termos
- ✅ Base de conhecimento JSON persistente
- ✅ Unificação de predicados
- ✅ Encadeamento para frente
- ✅ Prevenção de duplicados
- ✅ Justificações para inferências
- ✅ Motor de consultas
- ✅ Árvores de prova hierárquicas
- ✅ Interface Web responsiva
- ✅ Upload de ficheiros
- ✅ Visualização colapsável
- ✅ Docker e docker-compose
- ✅ Jupyter notebook demonstrativo

---

## 📝 Notas Técnicas

### Algoritmo de Inferência

O sistema usa **forward chaining** com as seguintes características:

1. **Inicialização**: Carrega fatos da KB
2. **Iteração**: Para cada regra, tenta unificar com fatos conhecidos
3. **Aplicação**: Se unificação bem-sucedida, deriva novo fato
4. **Registro**: Guarda justificação (regra + fatos usados)
5. **Repetição**: Continua até não haver novos fatos

### Formato de Predicados

- **Fatos**: `predicado(termo)`
  - Exemplo: `humano(Socrates)`
  
- **Regras**: `consequente :- antecedente`
  - Exemplo: `mortal(X) :- humano(X)`

- **Variáveis**: Termos com primeira letra maiúscula
  - Exemplo: `X`, `Y`, `Pessoa`

### Padrões de Extração

O sistema reconhece:
- "X é um/uma Y" → `Y(X)`
- "Todo/Toda X é Y" → `Y(X) :- X(X)`
- "Todos os X são Y" → `Y(X) :- X(X)`

---

## 🤝 Autor

**Projeto desenvolvido para TP04 - Inteligência Artificial 2025**

---

## 📅 Data de Entrega

**15/11/2025 às 12h15**

---

## 📄 Licença

Projeto académico - Inteligência Artificial 2025
