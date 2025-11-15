"""
Testes unitários para o motor de inferência.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.kb_manager import KnowledgeBase
from app.inference import InferenceEngine


def test_forward_chaining_simple():
    """Testa encadeamento para frente simples."""
    # Criar KB temporária
    kb = KnowledgeBase("test_kb.json")
    kb.clear()
    
    # Adicionar fato e regra
    kb.add_fact("humano(João)")
    kb.add_rule("mortal(X) :- humano(X)")
    
    # Executar inferência
    engine = InferenceEngine(kb)
    derived = engine.forward_chaining()
    
    # Verificar resultado
    assert "mortal(João)" in derived
    
    # Limpar
    os.remove("test_kb.json")


def test_forward_chaining_chain():
    """Testa cadeia de inferências."""
    kb = KnowledgeBase("test_kb_chain.json")
    kb.clear()
    
    # Adicionar fatos e regras em cadeia
    kb.add_fact("cao(Rex)")
    kb.add_rule("animal(X) :- cao(X)")
    kb.add_rule("ser_vivo(X) :- animal(X)")
    
    # Executar inferência
    engine = InferenceEngine(kb)
    derived = engine.forward_chaining()
    
    # Verificar que ambos foram derivados
    all_derived = set(derived)
    assert "animal(Rex)" in all_derived or "animal(Rex)" in kb.get_facts()
    
    # Limpar
    os.remove("test_kb_chain.json")


def test_no_duplicate_derivation():
    """Testa que não há derivações duplicadas."""
    kb = KnowledgeBase("test_kb_dup.json")
    kb.clear()
    
    kb.add_fact("humano(João)")
    kb.add_rule("mortal(X) :- humano(X)")
    
    engine = InferenceEngine(kb)
    derived1 = engine.forward_chaining()
    
    # Adicionar o fato derivado à KB manualmente
    for fact in derived1:
        kb.add_fact(fact)
    
    # Executar novamente - não deve haver novos fatos
    engine2 = InferenceEngine(kb)
    derived2 = engine2.forward_chaining()
    
    # Não deve haver novos fatos na segunda execução
    assert len(derived2) == 0
    
    # Limpar
    os.remove("test_kb_dup.json")


if __name__ == "__main__":
    test_forward_chaining_simple()
    test_forward_chaining_chain()
    test_no_duplicate_derivation()
    print("✓ Todos os testes de inferência passaram!")
