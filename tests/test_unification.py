"""
Testes unitários para o módulo de unificação.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.unification import (
    parse_predicate, 
    is_variable, 
    unify, 
    unify_predicates,
    apply_substitution_to_predicate
)


def test_parse_predicate():
    """Testa parsing de predicados."""
    name, args = parse_predicate("humano(Socrates)")
    assert name == "humano"
    assert args == ["Socrates"]
    
    name, args = parse_predicate("pai(Joao, Maria)")
    assert name == "pai"
    assert args == ["Joao", "Maria"]


def test_is_variable():
    """Testa detecção de variáveis."""
    assert is_variable("X") == True
    assert is_variable("Socrates") == True
    assert is_variable("humano") == False
    assert is_variable("x") == False


def test_unify_simple():
    """Testa unificação simples."""
    result = unify("X", "Socrates")
    assert result == {"X": "Socrates"}
    
    result = unify("Socrates", "Socrates")
    assert result == {}


def test_unify_predicates():
    """Testa unificação de predicados completos."""
    result = unify_predicates("humano(X)", "humano(Socrates)")
    assert result == {"X": "Socrates"}
    
    result = unify_predicates("humano(Socrates)", "humano(Socrates)")
    assert result == {}
    
    result = unify_predicates("humano(X)", "mortal(Socrates)")
    assert result is None


def test_apply_substitution():
    """Testa aplicação de substituições."""
    result = apply_substitution_to_predicate("mortal(X)", {"X": "Socrates"})
    assert result == "mortal(Socrates)"


if __name__ == "__main__":
    test_parse_predicate()
    test_is_variable()
    test_unify_simple()
    test_unify_predicates()
    test_apply_substitution()
    print("✓ Todos os testes de unificação passaram!")
