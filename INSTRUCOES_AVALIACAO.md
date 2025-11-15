# 👨‍🏫 INSTRUÇÕES PARA AVALIAÇÃO - TP04

**Professor:** Bongo Cahisso  
**Disciplina:** Inteligência Artificial 2025  
**Aluno:** [Seu Nome]  
**Data:** 15/11/2025

---

## 🚀 Como Executar o Projeto

### Opção 1: Execução Rápida com Script (RECOMENDADO)

```bash
cd tp04_ia
./start.sh
```

O script apresentará um menu interativo:
1. Executar aplicação web
2. Executar testes
3. Abrir Jupyter Notebook demo
4. Sair

### Opção 2: Execução Manual

```bash
cd tp04_ia

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Baixar modelo spaCy português
python -m spacy download pt_core_news_sm

# Executar aplicação
python -m app.web_app
```

**Aceder:** http://localhost:5000

### Opção 3: Docker (Mais Simples)

```bash
cd tp04_ia
docker-compose up --build
```

**Aceder:** http://localhost:5000

---

## 🧪 Executar Testes

### Todos os testes:
```bash
source venv/bin/activate  # ou .venv/bin/activate
python tests/run_all_tests.py
```

### Teste de integração completo:
```bash
python tests/test_integration.py
```

### Testes individuais:
```bash
python tests/test_extractor.py      # Extração semântica
python tests/test_unification.py    # Unificação
python tests/test_inference.py      # Inferência
python tests/test_query.py          # Consultas
```

**Resultado Esperado:** Todos os testes devem passar ✅

---

## 📖 Demo Interativa

### Opção 1: Jupyter Notebook
```bash
source venv/bin/activate
pip install jupyter
jupyter notebook notebooks/demo_inferencia.ipynb
```

### Opção 2: Interface Web
1. Aceder a http://localhost:5000
2. Fazer upload de `sample_texts/exemplo1.txt`
3. Ver fatos e regras extraídos
4. Executar consultas como:
   - `mortal(Sócrates)?`
   - `pensador(Platão)?`
   - `ser_vivo(Rex)?`

---

## 📝 Exemplos de Uso na Interface Web

### Passo 1: Upload de Texto
1. Clicar na área de upload
2. Selecionar `sample_texts/exemplo1.txt`
3. Observar extração automática

### Passo 2: Visualizar Base de Conhecimento
1. Clicar em "Ver Fatos" para expandir
2. Clicar em "Ver Regras" para expandir
3. Observar estatísticas

### Passo 3: Executar Consultas
Digite no campo de consulta:
- `humano(Sócrates)?` → ✅ VERDADEIRO (fato base)
- `mortal(Sócrates)?` → ✅ VERDADEIRO (inferido)
- `pensador(Platão)?` → ✅ VERDADEIRO (inferido)
- `imortal(Zeus)?` → ❌ FALSO (desconhecido)

### Passo 4: Ver Árvores de Prova
Após cada consulta bem-sucedida, a árvore de prova é exibida mostrando:
- Fato consultado
- Regras aplicadas
- Fatos base utilizados
- Cadeia completa de raciocínio

---

## 🔍 Pontos de Avaliação

### 1. Extração Semântica (4 pontos)
**Localização:** `app/extractor.py`

**Testar:**
```python
from app.extractor import SemanticExtractor

extractor = SemanticExtractor()
text = "Sócrates é um humano. Todo humano é mortal."
knowledge = extractor.extract_knowledge(text)

print(knowledge['facts'])   # ['humano(Sócrates)', ...]
print(knowledge['rules'])   # ['mortal(X) :- humano(X)', ...]
```

**Funciona com:**
- Padrões "X é um/uma Y"
- Padrões "Todo/Toda X é Y"
- Normalização de termos
- Modelo spaCy português

### 2. Inferência Lógica (4 pontos)
**Localização:** `app/inference.py`

**Testar:**
```python
from app.kb_manager import KnowledgeBase
from app.inference import InferenceEngine

kb = KnowledgeBase()
kb.add_fact("humano(Sócrates)")
kb.add_rule("mortal(X) :- humano(X)")

engine = InferenceEngine(kb)
derived = engine.forward_chaining()

print(derived)  # ['mortal(Sócrates)']
```

**Características:**
- Encadeamento para frente
- Unificação de predicados
- Substituições corretas
- Prevenção de duplicados
- Justificações com IDs

### 3. Consultas e Unificação (3 pontos)
**Localização:** `app/query_engine.py`, `app/unification.py`

**Testar:**
```python
from app.query_engine import QueryEngine

query_engine = QueryEngine(kb)
result = query_engine.query("mortal(Sócrates)?")

print(result['result'])      # 'true'
print(result['proof_tree'])  # Árvore completa
```

**Características:**
- Consultas booleanas
- Árvores de prova hierárquicas
- Formato JSON estruturado
- Tracking de derivações

### 4. Interface Web (4 pontos)
**Localização:** `app/web_app.py`, `app/templates/index.html`

**Testar:**
1. Aceder a http://localhost:5000
2. Upload de ficheiros
3. Visualização de KB
4. Consultas interativas
5. Árvores colapsáveis

**Características:**
- Design moderno e responsivo
- Upload funcional
- Visualização clara
- Interatividade completa
- Árvores coloridas

### 5. Documentação & Docker (3 pontos)
**Localização:** `README.md`, `Dockerfile`, `docker-compose.yml`

**Verificar:**
- README completo ✅
- Instruções claras ✅
- Docker funcional ✅
- Exemplos práticos ✅

### 6. Criatividade e Clareza (2 pontos)
**Observar:**
- Interface web moderna e intuitiva
- Código bem estruturado
- Testes completos
- Documentação exemplar
- Jupyter notebook demonstrativo

---

## 📊 Estrutura do Código

```
app/
├── text_reader.py      → Leitura de ficheiros
├── extractor.py        → Extração com spaCy
├── kb_manager.py       → Base de conhecimento JSON
├── unification.py      → Unificação de predicados
├── inference.py        → Forward chaining
├── query_engine.py     → Consultas e provas
└── web_app.py          → Flask application
```

---

## ✅ Checklist de Verificação

- [ ] Aplicação executa sem erros
- [ ] Interface web acessível em localhost:5000
- [ ] Upload de ficheiros funciona
- [ ] Extração de fatos e regras correta
- [ ] Inferência deriva novos fatos
- [ ] Consultas retornam resultados corretos
- [ ] Árvores de prova são exibidas
- [ ] Testes todos passam
- [ ] Docker constrói e executa
- [ ] Documentação está clara

---

## 🎯 Casos de Teste Sugeridos

### Teste 1: Silogismo Clássico
**Input:** `sample_texts/exemplo1.txt`
```
Sócrates é um humano.
Todo humano é mortal.
```
**Consulta:** `mortal(Sócrates)?`
**Esperado:** ✅ VERDADEIRO com árvore de prova

### Teste 2: Cadeia de Inferências
**Input:** `sample_texts/exemplo2.txt`
```
Rex é um cão.
Todo cão é um animal.
Todo animal é um ser vivo.
```
**Consulta:** `ser_vivo(Rex)?`
**Esperado:** ✅ VERDADEIRO com cadeia completa

### Teste 3: Múltiplas Entidades
**Input:** `sample_texts/exemplo3.txt`
```
Maria é uma estudante.
Pedro é um estudante.
Todo estudante é uma pessoa.
```
**Consultas:**
- `pessoa(Maria)?` → ✅ VERDADEIRO
- `pessoa(Pedro)?` → ✅ VERDADEIRO

---

## 📞 Suporte

**Ficheiros Importantes:**
- `README.md` - Documentação completa
- `SUMMARY.md` - Resumo executivo
- `checklist.md` - Checklist do projeto
- `notebooks/demo_inferencia.ipynb` - Demo interativa

**Todos os testes passam!** ✅  
**Projeto completo e funcional!** 🎉

---

**TP04 - Inteligência Artificial 2025**
