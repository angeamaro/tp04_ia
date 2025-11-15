#!/bin/bash
# Script de início rápido para o projeto TP04

echo "Motor de Inferência Inteligente - TP04"
echo "=========================================="
echo ""

# Verificar se venv existe
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo " Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo " Instalando dependências..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo " Baixando modelo spaCy português..."
    python -m spacy download pt_core_news_sm
else
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        source .venv/bin/activate
    fi
fi

echo ""
echo " Ambiente configurado!"
echo ""
echo "Escolha uma opção:"
echo "1) Executar aplicação web"
echo "2) Executar testes"
echo "3) Abrir Jupyter Notebook demo"
echo "4) Sair"
echo ""
read -p "Opção: " option

case $option in
    1)
        echo ""
        echo " Iniciando aplicação web..."
        echo " Acesse: http://localhost:5000"
        echo ""
        python -m app.web_app
        ;;
    2)
        echo ""
        echo " Executando testes..."
        python tests/run_all_tests.py
        ;;
    3)
        echo ""
        echo " Abrindo Jupyter Notebook..."
        pip install jupyter > /dev/null 2>&1
        jupyter notebook notebooks/demo_inferencia.ipynb
        ;;
    4)
        echo " Até logo!"
        exit 0
        ;;
    *)
        echo " Opção inválida!"
        exit 1
        ;;
esac
