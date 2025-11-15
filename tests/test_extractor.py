"""
Testes unitários para o módulo de extração semântica.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extractor import SemanticExtractor


def test_extract_simple_fact():
    """Testa extração de fato simples."""
    extractor = SemanticExtractor()
    text = "Sócrates é um humano."
    facts = extractor.extract_facts(text)
    
    assert len(facts) > 0
    assert "humano(Sócrates)" in facts


def test_extract_rule():
    """Testa extração de regra universal."""
    extractor = SemanticExtractor()
    text = "Todo humano é mortal."
    rules = extractor.extract_rules(text)
    
    assert len(rules) > 0
    assert "mortal(X) :- humano(X)" in rules


def test_normalize_term():
    """Testa normalização de termos."""
    extractor = SemanticExtractor()
    
    # Nomes próprios devem ter primeira letra maiúscula
    assert extractor.normalize_term("Sócrates") == "Sócrates"
    assert extractor.normalize_term("João") == "João"
    
    # Predicados devem ser minúsculos
    assert extractor.normalize_term("humano") == "humano"


def test_extract_knowledge_complete():
    """Testa extração completa de conhecimento."""
    extractor = SemanticExtractor()
    text = """
    Sócrates é um humano.
    Todo humano é mortal.
    Platão é um filósofo.
    """
    
    knowledge = extractor.extract_knowledge(text)
    
    assert 'facts' in knowledge
    assert 'rules' in knowledge
    assert len(knowledge['facts']) >= 2
    assert len(knowledge['rules']) >= 1


if __name__ == "__main__":
    test_extract_simple_fact()
    test_extract_rule()
    test_normalize_term()
    test_extract_knowledge_complete()
    print("✓ Todos os testes de extração passaram!")
