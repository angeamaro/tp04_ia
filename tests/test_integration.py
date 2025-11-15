"""
Teste de integração completo - End-to-End
Testa todo o pipeline do sistema.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.text_reader import read_text
from app.extractor import SemanticExtractor
from app.kb_manager import KnowledgeBase
from app.inference import InferenceEngine
from app.query_engine import QueryEngine


def test_complete_pipeline():
    """Testa o pipeline completo do sistema."""
    print("\n" + "="*60)
    print("TESTE DE INTEGRAÇÃO COMPLETO")
    print("="*60)
    
    # 1. Ler texto de exemplo
    print("\n1 - Lendo ficheiro de texto...")
    text = read_text("sample_texts/exemplo1.txt")
    assert text is not None
    print(f"✓ Texto lido: {len(text)} caracteres")
    
    # 2. Extrair conhecimento
    print("\n2 - Extraindo conhecimento com spaCy...")
    extractor = SemanticExtractor()
    knowledge = extractor.extract_knowledge(text)
    print(f"✓ Fatos extraídos: {len(knowledge['facts'])}")
    print(f"✓ Regras extraídas: {len(knowledge['rules'])}")
    for fact in knowledge['facts']:
        print(f"  - {fact}")
    for rule in knowledge['rules']:
        print(f"  - {rule}")
    
    # 3. Criar e popular base de conhecimento
    print("\n3 - Criando base de conhecimento...")
    kb = KnowledgeBase("test_integration.json")
    kb.clear()
    kb.import_knowledge(knowledge['facts'], knowledge['rules'])
    print(f"✓ KB criada com {len(kb.get_facts())} fatos e {len(kb.get_rules())} regras")
    
    # 4. Executar inferência
    print("\n4️⃣ Executando inferência (forward chaining)...")
    engine = InferenceEngine(kb)
    derived = engine.forward_chaining()
    print(f"✓ {len(derived)} novos fatos derivados:")
    for fact in derived:
        print(f"  - {fact}")
    
    # 5. Realizar consultas
    print("\n5️⃣ Executando consultas...")
    query_engine = QueryEngine(kb)
    
    # Consulta 1: Fato base
    print("\n  📋 Consulta 1: Fato base")
    result1 = query_engine.query("humano(Sócrates)?")
    print(f"  Resultado: {result1['result']}")
    assert result1['result'] == 'true'
    
    # Consulta 2: Fato inferido
    print("\n  📋 Consulta 2: Fato inferido")
    result2 = query_engine.query("mortal(Sócrates)?")
    print(f"  Resultado: {result2['result']}")
    if result2['result'] == 'true':
        print("\n  🌲 Árvore de Prova:")
        print(query_engine.format_proof_tree_text(result2['proof_tree']))
    
    # Consulta 3: Outro fato inferido
    print("\n  📋 Consulta 3: Outro fato inferido")
    result3 = query_engine.query("pensador(Platão)?")
    print(f"  Resultado: {result3['result']}")
    
    # Consulta 4: Fato desconhecido
    print("\n  📋 Consulta 4: Fato desconhecido")
    result4 = query_engine.query("imortal(Zeus)?")
    print(f"  Resultado: {result4['result']}")
    assert result4['result'] == 'false'
    
    # 6. Verificar persistência
    print("\n6️⃣ Verificando persistência...")
    kb.save()
    kb2 = KnowledgeBase("test_integration.json")
    print(f"✓ KB recarregada: {len(kb2.get_facts())} fatos, {len(kb2.get_rules())} regras")
    
    # Limpar
    os.remove("test_integration.json")
    
    print("\n" + "="*60)
    print("✅ TESTE DE INTEGRAÇÃO COMPLETO: SUCESSO!")
    print("="*60)
    print("\n✨ Todos os componentes funcionam perfeitamente juntos!")
    print()


if __name__ == "__main__":
    try:
        test_complete_pipeline()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
