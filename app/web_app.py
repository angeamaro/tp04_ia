"""
Interface Web Flask para o Motor de Inferência.
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename

from app.text_reader import read_text, read_text_from_upload
from app.extractor import SemanticExtractor
from app.kb_manager import KnowledgeBase
from app.inference import InferenceEngine
from app.query_engine import QueryEngine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Obter caminho da KB (usar variável de ambiente ou padrão)
kb_path = os.environ.get('KB_PATH', 'kb.json')
os.makedirs(os.path.dirname(kb_path) if os.path.dirname(kb_path) else '.', exist_ok=True)

# Inicializar componentes
kb = KnowledgeBase(kb_path)
extractor = SemanticExtractor()
inference_engine = InferenceEngine(kb)
query_engine = QueryEngine(kb)


@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Processa upload de ficheiro de texto."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum ficheiro enviado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum ficheiro selecionado'}), 400
    
    if file and file.filename.endswith('.txt'):
        # Ler conteúdo
        content = read_text_from_upload(file)
        
        if content:
            # Extrair conhecimento
            knowledge = extractor.extract_knowledge(content)
            
            # Importar para KB
            kb.import_knowledge(knowledge['facts'], knowledge['rules'])
            
            # Executar inferência
            derived = inference_engine.forward_chaining()
            
            # Guardar KB
            kb.save()
            
            return jsonify({
                'success': True,
                'extracted_facts': knowledge['facts'],
                'extracted_rules': knowledge['rules'],
                'derived_facts': derived,
                'message': f'Processado com sucesso! {len(knowledge["facts"])} fatos e {len(knowledge["rules"])} regras extraídos.'
            })
        else:
            return jsonify({'error': 'Erro ao ler ficheiro'}), 400
    else:
        return jsonify({'error': 'Apenas ficheiros .txt são aceites'}), 400


@app.route('/kb', methods=['GET'])
def get_kb():
    """Retorna a base de conhecimento atual."""
    return jsonify(kb.to_dict())


@app.route('/query', methods=['POST'])
def execute_query():
    """Executa uma consulta."""
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query vazia'}), 400
    
    result = query_engine.query(query)
    
    return jsonify(result)


@app.route('/clear', methods=['POST'])
def clear_kb():
    """Limpa a base de conhecimento."""
    kb.clear()
    return jsonify({'success': True, 'message': 'Base de conhecimento limpa'})


@app.route('/infer', methods=['POST'])
def run_inference():
    """Executa inferência manualmente."""
    derived = inference_engine.forward_chaining()
    kb.save()
    
    return jsonify({
        'success': True,
        'derived_facts': derived,
        'message': f'{len(derived)} novos fatos derivados'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
