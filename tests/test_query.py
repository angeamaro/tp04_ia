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


def test_query_false_different_entity():
    """Testa que consulta retorna falso para entidade diferente."""
    kb = KnowledgeBase("test_query_false1.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    kb.add_rule("mortal(X) :- humano(X)")
    
    engine = InferenceEngine(kb)
    engine.forward_chaining()
    
    query_engine = QueryEngine(kb)
    
    # Maria não está na KB
    result = query_engine.query("mortal(Maria)?")
    assert result['result'] == 'false', "Deve retornar falso para entidade não presente"
    
    # Pedro também não está
    result = query_engine.query("humano(Pedro)?")
    assert result['result'] == 'false', "Deve retornar falso para fato inexistente"
    
    os.remove("test_query_false1.json")


def test_query_false_no_applicable_rule():
    """Testa que consulta retorna falso quando não há regra aplicável."""
    kb = KnowledgeBase("test_query_false2.json")
    kb.clear()
    
    kb.add_fact("cão(Rex)")
    kb.add_rule("mortal(X) :- humano(X)")  # Regra só para humanos
    
    engine = InferenceEngine(kb)
    engine.forward_chaining()
    
    query_engine = QueryEngine(kb)
    
    # Rex é cão, não humano, logo não é mortal pela regra
    result = query_engine.query("mortal(Rex)?")
    assert result['result'] == 'false', "Deve retornar falso quando regra não se aplica"
    
    # Humano também não foi definido para Rex
    result = query_engine.query("humano(Rex)?")
    assert result['result'] == 'false', "Deve retornar falso para predicado diferente"
    
    os.remove("test_query_false2.json")


def test_query_false_predicate_not_exists():
    """Testa que consulta retorna falso para predicado inexistente."""
    kb = KnowledgeBase("test_query_false3.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    kb.add_fact("filósofo(Platão)")
    
    query_engine = QueryEngine(kb)
    
    # Predicados que não existem na KB
    result = query_engine.query("imortal(João)?")
    assert result['result'] == 'false', "Deve retornar falso para predicado inexistente"
    
    result = query_engine.query("divino(Platão)?")
    assert result['result'] == 'false', "Deve retornar falso para predicado não definido"
    
    result = query_engine.query("voador(João)?")
    assert result['result'] == 'false', "Deve retornar falso para predicado desconhecido"
    
    os.remove("test_query_false3.json")


def test_query_false_wrong_type():
    """Testa que consulta retorna falso para tipo errado."""
    kb = KnowledgeBase("test_query_false4.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    kb.add_fact("animal(Rex)")
    kb.add_rule("pensador(X) :- humano(X)")
    kb.add_rule("ser_vivo(X) :- animal(X)")
    
    engine = InferenceEngine(kb)
    engine.forward_chaining()
    
    query_engine = QueryEngine(kb)
    
    # Rex é animal, não pensador
    result = query_engine.query("pensador(Rex)?")
    assert result['result'] == 'false', "Animal não deve ser pensador"
    
    # João é humano, não classificado como animal diretamente
    result = query_engine.query("animal(João)?")
    assert result['result'] == 'false', "Humano não deve ser animal sem regra"
    
    os.remove("test_query_false4.json")


def test_query_false_mixed_cases():
    """Testa casos mistos de verdadeiro e falso."""
    kb = KnowledgeBase("test_query_false5.json")
    kb.clear()
    
    kb.add_fact("estudante(João)")
    kb.add_fact("professor(Maria)")
    kb.add_rule("pessoa(X) :- estudante(X)")
    kb.add_rule("pessoa(X) :- professor(X)")
    kb.add_rule("trabalhador(X) :- professor(X)")
    
    engine = InferenceEngine(kb)
    engine.forward_chaining()
    
    query_engine = QueryEngine(kb)
    
    # Verdadeiros
    assert query_engine.query("estudante(João)?")['result'] == 'true'
    assert query_engine.query("pessoa(João)?")['result'] == 'true'
    assert query_engine.query("professor(Maria)?")['result'] == 'true'
    assert query_engine.query("pessoa(Maria)?")['result'] == 'true'
    assert query_engine.query("trabalhador(Maria)?")['result'] == 'true'
    
    # Falsos - João não é professor
    assert query_engine.query("professor(João)?")['result'] == 'false'
    assert query_engine.query("trabalhador(João)?")['result'] == 'false'
    
    # Falsos - Maria não é estudante
    assert query_engine.query("estudante(Maria)?")['result'] == 'false'
    
    # Falsos - Pedro não existe
    assert query_engine.query("estudante(Pedro)?")['result'] == 'false'
    assert query_engine.query("pessoa(Pedro)?")['result'] == 'false'
    
    os.remove("test_query_false5.json")


def test_query_false_chain_broken():
    """Testa que cadeia de inferência quebrada retorna falso."""
    kb = KnowledgeBase("test_query_false6.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    kb.add_rule("mortal(X) :- humano(X)")
    kb.add_rule("finito(X) :- mortal(X)")
    # Falta regra para 'eterno'
    
    engine = InferenceEngine(kb)
    engine.forward_chaining()
    
    query_engine = QueryEngine(kb)
    
    # Verdadeiros - cadeia funciona
    assert query_engine.query("humano(João)?")['result'] == 'true'
    assert query_engine.query("mortal(João)?")['result'] == 'true'
    assert query_engine.query("finito(João)?")['result'] == 'true'
    
    # Falso - não há regra para eterno
    assert query_engine.query("eterno(João)?")['result'] == 'false'
    
    os.remove("test_query_false6.json")


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
    print("🧪 Testando consultas básicas...")
    test_query_base_fact()
    test_query_inferred_fact()
    test_query_unknown()
    
    print("🧪 Testando consultas que devem retornar FALSO...")
    test_query_false_different_entity()
    test_query_false_no_applicable_rule()
    test_query_false_predicate_not_exists()
    test_query_false_wrong_type()
    test_query_false_mixed_cases()
    test_query_false_chain_broken()
    
    print("🧪 Testando estrutura de prova...")
    test_proof_tree_structure()
    
    print("✓ Todos os testes de consultas passaram!")
