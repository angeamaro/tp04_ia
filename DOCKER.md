# 🐳 Guia Docker - TP04

## Uso Rápido com Makefile

```bash
make help          # Ver todos os comandos
make build         # Construir imagem
make run           # Executar container
make logs          # Ver logs
make stop          # Parar container
make clean         # Limpar tudo
```

Aceder: **http://localhost:5000**

---

## Comandos Docker Manuais

### Construir imagem
```bash
docker build -t tp04-inference-engine .
```

### Executar container
```bash
docker run -d \
  --name tp04-app \
  -p 5000:5000 \
  -v $(pwd)/kb.json:/app/kb.json \
  tp04-inference-engine
```

### Ver logs
```bash
docker logs -f tp04-app
```

### Parar container
```bash
docker stop tp04-app
docker rm tp04-app
```

### Entrar no container
```bash
docker exec -it tp04-app /bin/bash
```

---

## Troubleshooting

### Porta 5000 em uso
```bash
# Parar processo na porta
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Ou usar outra porta
docker run -d --name tp04-app -p 8080:5000 tp04-inference-engine
```

### Rebuild após mudanças
```bash
make stop
make build
make run
```

### Limpar tudo
```bash
make clean
# Ou manualmente:
docker stop tp04-app
docker rm tp04-app
docker rmi tp04-inference-engine
```

---

**TP04 - Inteligência Artificial 2025**
