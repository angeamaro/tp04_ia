"""
Script para executar todos os testes.
"""
import sys

# Importar todos os módulos de teste
from test_extractor import *
from test_unification import *
from test_inference import *
from test_query import *


def run_all_tests():
    """Executa todos os testes do projeto."""
    print("=" * 60)
    print("🧪 EXECUTANDO TODOS OS TESTES")
    print("=" * 60)
    
    print("\n📝 Testes de Extração...")
    try:
        test_extract_simple_fact()
        test_extract_rule()
        test_normalize_term()
        test_extract_knowledge_complete()
        print("✓ Testes de extração: OK")
    except Exception as e:
        print(f"✗ Testes de extração: FALHOU - {e}")
        return False
    
    print("\n🔗 Testes de Unificação...")
    try:
        test_parse_predicate()
        test_is_variable()
        test_unify_simple()
        test_unify_predicates()
        test_apply_substitution()
        print("✓ Testes de unificação: OK")
    except Exception as e:
        print(f"✗ Testes de unificação: FALHOU - {e}")
        return False
    
    print("\n⚡ Testes de Inferência...")
    try:
        test_forward_chaining_simple()
        test_forward_chaining_chain()
        test_no_duplicate_derivation()
        print("✓ Testes de inferência: OK")
    except Exception as e:
        print(f"✗ Testes de inferência: FALHOU - {e}")
        return False
    
    print("\n🔍 Testes de Consultas...")
    try:
        test_query_base_fact()
        test_query_inferred_fact()
        test_query_unknown()
        test_proof_tree_structure()
        print("✓ Testes de consultas: OK")
    except Exception as e:
        print(f"✗ Testes de consultas: FALHOU - {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
