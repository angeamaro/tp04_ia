"""
Módulo de unificação para matching de predicados lógicos.
"""
import re
from typing import Dict, Optional, Tuple


def parse_predicate(predicate: str) -> Tuple[str, list]:
    """
    Faz parse de um predicado no formato predicado(arg1, arg2, ...).
    
    Args:
        predicate: String do predicado
        
    Returns:
        Tupla (nome_predicado, [argumentos])
    """
    match = re.match(r'(\w+)\((.*)\)', predicate.strip())
    if not match:
        return None, []
    
    name = match.group(1)
    args_str = match.group(2)
    
    if args_str:
        args = [arg.strip() for arg in args_str.split(',')]
    else:
        args = []
    
    return name, args


def is_variable(term: str) -> bool:
    """
    Verifica se um termo é uma variável (começa com maiúscula).
    
    Args:
        term: Termo a verificar
        
    Returns:
        True se for variável, False caso contrário
    """
    return term and term[0].isupper()


def unify(term1: str, term2: str, substitutions: Dict[str, str] = None) -> Optional[Dict[str, str]]:
    """
    Unifica dois termos, retornando as substituições necessárias.
    
    Args:
        term1: Primeiro termo
        term2: Segundo termo
        substitutions: Substituições já existentes
        
    Returns:
        Dicionário de substituições ou None se não for possível unificar
    """
    if substitutions is None:
        substitutions = {}
    
    # Aplicar substituições existentes
    term1 = apply_substitution(term1, substitutions)
    term2 = apply_substitution(term2, substitutions)
    
    # Se são iguais, unificação bem-sucedida
    if term1 == term2:
        return substitutions
    
    # Se term1 é variável
    if is_variable(term1):
        if term1 in substitutions:
            return unify(substitutions[term1], term2, substitutions)
        else:
            substitutions[term1] = term2
            return substitutions
    
    # Se term2 é variável
    if is_variable(term2):
        if term2 in substitutions:
            return unify(term1, substitutions[term2], substitutions)
        else:
            substitutions[term2] = term1
            return substitutions
    
    # Não é possível unificar
    return None


def apply_substitution(term: str, substitutions: Dict[str, str]) -> str:
    """
    Aplica substituições a um termo.
    
    Args:
        term: Termo original
        substitutions: Dicionário de substituições
        
    Returns:
        Termo com substituições aplicadas
    """
    for var, value in substitutions.items():
        term = term.replace(var, value)
    return term


def unify_predicates(pred1: str, pred2: str) -> Optional[Dict[str, str]]:
    """
    Unifica dois predicados completos.
    
    Args:
        pred1: Primeiro predicado
        pred2: Segundo predicado
        
    Returns:
        Dicionário de substituições ou None se não unificarem
    """
    name1, args1 = parse_predicate(pred1)
    name2, args2 = parse_predicate(pred2)
    
    # Nomes devem ser iguais
    if name1 != name2:
        return None
    
    # Número de argumentos deve ser igual
    if len(args1) != len(args2):
        return None
    
    substitutions = {}
    
    # Tentar unificar cada par de argumentos
    for arg1, arg2 in zip(args1, args2):
        result = unify(arg1, arg2, substitutions)
        if result is None:
            return None
        substitutions = result
    
    return substitutions


def apply_substitution_to_predicate(predicate: str, substitutions: Dict[str, str]) -> str:
    """
    Aplica substituições a um predicado completo.
    
    Args:
        predicate: Predicado original
        substitutions: Dicionário de substituições
        
    Returns:
        Predicado com substituições aplicadas
    """
    result = predicate
    for var, value in substitutions.items():
        result = result.replace(var, value)
    return result
