# Makefile para TP04 - Motor de Inferência Inteligente

.PHONY: help build run stop logs shell clean test local install

IMAGE_NAME = tp04-inference-engine
CONTAINER_NAME = tp04-app
PORT = 5000

help:
	@echo "======================================"
	@echo "  TP04 - Motor de Inferência"
	@echo "======================================"
	@echo ""
	@echo "Comandos Docker:"
	@echo "  make build       - Construir imagem Docker"
	@echo "  make run         - Executar container"
	@echo "  make stop        - Parar container"
	@echo "  make logs        - Ver logs do container"
	@echo "  make shell       - Entrar no container"
	@echo "  make clean       - Remover container e imagem"
	@echo ""
	@echo "Comandos Locais:"
	@echo "  make install     - Instalar dependências"
	@echo "  make local       - Executar localmente"
	@echo "  make test        - Executar testes"
	@echo ""
	@echo "Uso rápido:"
	@echo "  make build && make run"
	@echo ""

build:
	@echo "🔨 Construindo imagem Docker..."
	docker build -t $(IMAGE_NAME) .
	@echo "✅ Imagem construída: $(IMAGE_NAME)"

run:
	@echo "🚀 Executando container..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		-v $(PWD)/kb.json:/app/kb.json \
		$(IMAGE_NAME)
	@echo "✅ Container executando: http://localhost:$(PORT)"
	@echo "   Para ver logs: make logs"

stop:
	@echo "🛑 Parando container..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@echo "✅ Container parado"

logs:
	@docker logs -f $(CONTAINER_NAME)

shell:
	@docker exec -it $(CONTAINER_NAME) /bin/bash

clean:
	@echo "🧹 Limpando..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@docker rmi $(IMAGE_NAME) 2>/dev/null || true
	@rm -rf app/__pycache__ tests/__pycache__
	@rm -f kb.json
	@echo "✅ Limpeza completa"

install:
	@echo "📦 Instalando dependências..."
	@[ -d ".venv" ] || python3 -m venv .venv
	@. .venv/bin/activate && pip install --upgrade pip
	@. .venv/bin/activate && pip install -r requirements.txt
	@. .venv/bin/activate && python -m spacy download pt_core_news_sm
	@echo "✅ Dependências instaladas"

local:
	@echo "🚀 Executando localmente..."
	@. .venv/bin/activate && python -m app.web_app

test:
	@echo "🧪 Executando testes..."
	@. .venv/bin/activate && python tests/run_all_tests.py
