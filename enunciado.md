Aqui está um **arquivo Markdown (MD)** completo e bem organizado com **toda a informação essencial** do projeto **TP04 – Motor de Inferência Inteligente com Extração Semântica e Interface Web**:

---

# 🧠 TP04 – Motor de Inferência Inteligente com Extração Semântica e Interface Web

**Disciplina:** Inteligência Artificial – 2025
**Professor:** Bongo Cahisso
**Entrega:** **15/11/2025 às 12h15 (sem tolerância)**
**Trabalho individual**

---

## 📌 Objetivo Geral

Desenvolver um **motor de inferência lógica baseado em regras e fatos**, capaz de:

* Ler textos naturais (ficheiros .txt)
* Extrair automaticamente **fatos** e **regras** com spaCy
* Realizar **inferência lógica por encadeamento para frente**
* Responder consultas lógicas com prova detalhada
* Exibir **árvores de dedução** visualmente numa interface Web
* Manter uma base de conhecimento persistente em JSON
* Ser executado em ambiente containerizado (Docker)

---

## 🧩 Componentes Obrigatórios

### 1. **Módulo de Processamento de Texto**

* Ler ficheiros `.txt`
* Identificar entidades e relações via NLP
* Extrair predicados no formato:

  * `humano(Socrates)`
  * `mortal(X) :- humano(X)`

---

### 2. **Módulo de Inferência**

* Implementar **encadeamento para frente**
* Aplicar:

  * Unificação
  * Substituições
  * Dedução de novos fatos
* Armazenar justificações para gerar a árvore de prova

---

### 3. **Módulo de Consulta**

* Permitir perguntas como: `mortal(Socrates)?`
* Retornar:

  * Resultado: **verdadeiro / falso / desconhecido**
  * Prova completa em árvore hierárquica e colorida

---

### 4. **Interface Web** (Flask ou Streamlit)

Deve permitir:

* Upload de textos
* Visualizar base de conhecimento (fatos e regras)
* Fazer consultas
* Exibir árvore de dedução colapsável

---

### 5. **Ambiente de Execução**

* `Dockerfile` com a aplicação
* `requirements.txt`
* (Opcional) `demo_inferencia.ipynb` demonstrando todo o pipeline

---

## 📘 Exemplo de Funcionamento

### **Ficheiro de entrada (texto.txt)**

```
Sócrates é um humano.
Todo humano é mortal.
Platão é um filósofo.
Todo filósofo é pensador.
```

### **Base gerada automaticamente**

**Fatos:**

```
humano(Socrates)
filosofo(Platao)
```

**Regras:**

```
mortal(X) :- humano(X)
pensador(X) :- filosofo(X)
```

### **Consulta**

```
mortal(Socrates)?
```

### **Resultado esperado**

✔️ **Verdadeiro**

### **Árvore de prova**

```
└── mortal(Socrates)
    └── humano(Socrates)
        └── fato base
```

---

## 📝 Critérios de Avaliação (20 valores)

| Critério               | Descrição                                          | Pontos |
| ---------------------- | -------------------------------------------------- | ------ |
| Extração Semântica     | Identificação de fatos e relações com spaCy        | **4**  |
| Inferência Lógica      | Encadeamento para frente corretamente implementado | **4**  |
| Consultas e Unificação | Verificação e prova de fatos                       | **3**  |
| Interface Web          | Usabilidade + árvore de dedução                    | **4**  |
| Documentação & Docker  | Execução simples e bem documentada                 | **3**  |
| Criatividade e Clareza | Clareza no raciocínio e visualização               | **2**  |

---

Se quiser, posso gerar um **README.md ainda mais completo**, com instruções de instalação, estrutura de pastas e exemplos reais de código. Quer que eu gere também?
