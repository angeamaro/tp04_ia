"""
Testes unitários para o motor de consultas.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.kb_manager import KnowledgeBase
from app.inference import InferenceEngine
from app.query_engine import QueryEngine


def test_query_base_fact():
    """Testa consulta de fato base."""
    kb = KnowledgeBase("test_query_kb.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    
    query_engine = QueryEngine(kb)
    result = query_engine.query("humano(João)?")
    
    assert result['result'] == 'true'
    assert result['query'] == 'humano(João)'
    assert result['proof_tree'] is not None
    
    os.remove("test_query_kb.json")


def test_query_inferred_fact():
    """Testa consulta de fato inferido."""
    kb = KnowledgeBase("test_query_inf.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    kb.add_rule("mortal(X) :- humano(X)")
    
    # Executar inferência
    engine = InferenceEngine(kb)
    engine.forward_chaining()
    
    # Consultar fato derivado
    query_engine = QueryEngine(kb)
    result = query_engine.query("mortal(João)?")
    
    assert result['result'] == 'true'
    assert result['proof_tree'] is not None
    assert result['proof_tree']['type'] == 'inference'
    
    os.remove("test_query_inf.json")


def test_query_unknown():
    """Testa consulta de fato desconhecido."""
    kb = KnowledgeBase("test_query_unk.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    
    query_engine = QueryEngine(kb)
    result = query_engine.query("mortal(João)?")
    
    assert result['result'] == 'false'
    
    os.remove("test_query_unk.json")


def test_proof_tree_structure():
    """Testa estrutura da árvore de prova."""
    kb = KnowledgeBase("test_proof_tree.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    kb.add_rule("mortal(X) :- humano(X)")
    
    engine = InferenceEngine(kb)
    engine.forward_chaining()
    
    query_engine = QueryEngine(kb)
    result = query_engine.query("mortal(João)?")
    
    tree = result['proof_tree']
    assert 'fact' in tree
    assert 'type' in tree
    assert 'children' in tree
    assert tree['fact'] == 'mortal(João)'
    
    os.remove("test_proof_tree.json")


if __name__ == "__main__":
    test_query_base_fact()
    test_query_inferred_fact()
    test_query_unknown()
    test_proof_tree_structure()
    print("✓ Todos os testes de consultas passaram!")
