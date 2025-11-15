"""
Motor de inferência com encadeamento para frente (forward chaining).
"""
from typing import Dict, List, Set, Optional
from app.unification import parse_predicate, unify_predicates, apply_substitution_to_predicate
import uuid


class InferenceEngine:
    """Motor de inferência lógica por encadeamento para frente."""
    
    def __init__(self, kb):
        """
        Inicializa o motor de inferência.
        
        Args:
            kb: Instância de KnowledgeBase
        """
        self.kb = kb
        self.derived_facts: Set[str] = set()
        self.justifications: Dict[str, Dict] = {}
    
    def parse_rule(self, rule: str) -> tuple:
        """
        Faz parse de uma regra no formato: consequente :- antecedente.
        
        Args:
            rule: Regra em string
            
        Returns:
            Tupla (consequente, [antecedentes])
        """
        if ':-' not in rule:
            return None, []
        
        parts = rule.split(':-')
        consequent = parts[0].strip()
        
        # Pode haver múltiplos antecedentes separados por vírgula
        antecedents_str = parts[1].strip()
        antecedents = [a.strip() for a in antecedents_str.split(',')]
        
        return consequent, antecedents
    
    def forward_chaining(self) -> List[str]:
        """
        Executa inferência por encadeamento para frente.
        Deriva novos fatos a partir dos fatos e regras existentes.
        
        Returns:
            Lista de novos fatos derivados
        """
        # Inicializa com fatos da base de conhecimento
        known_facts = set(self.kb.get_facts())
        self.derived_facts = set()
        self.justifications = {}
        
        # Loop até não haver mais fatos novos
        changed = True
        iteration = 0
        max_iterations = 100  # Limite de segurança
        
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            
            # Para cada regra
            for rule in self.kb.get_rules():
                consequent, antecedents = self.parse_rule(rule)
                
                if not consequent or not antecedents:
                    continue
                
                # Tentar aplicar a regra
                new_facts = self.apply_rule(consequent, antecedents, known_facts, rule)
                
                for new_fact in new_facts:
                    if new_fact not in known_facts:
                        known_facts.add(new_fact)
                        self.derived_facts.add(new_fact)
                        changed = True
        
        return list(self.derived_facts)
    
    def apply_rule(self, consequent: str, antecedents: List[str], 
                   known_facts: Set[str], original_rule: str) -> List[str]:
        """
        Tenta aplicar uma regra aos fatos conhecidos.
        
        Args:
            consequent: Consequente da regra
            antecedents: Lista de antecedentes
            known_facts: Conjunto de fatos conhecidos
            original_rule: Regra original (para justificação)
            
        Returns:
            Lista de novos fatos derivados
        """
        new_facts = []
        
        # Para cada fato conhecido
        for fact in known_facts:
            # Tentar unificar com cada antecedente
            for antecedent in antecedents:
                substitutions = unify_predicates(antecedent, fact)
                
                if substitutions is not None:
                    # Aplicar substituições ao consequente
                    new_fact = apply_substitution_to_predicate(consequent, substitutions)
                    
                    # Verificar se o novo fato ainda tem variáveis
                    if not self.has_variables(new_fact):
                        # Guardar justificação
                        fact_id = str(uuid.uuid4())
                        self.justifications[new_fact] = {
                            'id': fact_id,
                            'fact': new_fact,
                            'rule': original_rule,
                            'used_facts': [fact],
                            'substitutions': substitutions
                        }
                        
                        # Adicionar à KB
                        self.kb.add_inference({
                            'id': fact_id,
                            'derived_fact': new_fact,
                            'from_rule': original_rule,
                            'using_facts': [fact],
                            'substitutions': substitutions
                        })
                        
                        new_facts.append(new_fact)
        
        return new_facts
    
    def has_variables(self, predicate: str) -> bool:
        """
        Verifica se um predicado contém variáveis (termos com maiúscula).
        Variáveis são tipicamente letras únicas maiúsculas (X, Y, Z, etc.)
        
        Args:
            predicate: Predicado a verificar
            
        Returns:
            True se contém variáveis
        """
        _, args = parse_predicate(predicate)
        for arg in args:
            # Variável é uma letra única maiúscula ou segue padrão Var1, Var2, etc.
            if arg and arg[0].isupper() and (len(arg) == 1 or arg.isalnum() and any(c.isdigit() for c in arg)):
                return True
        return False
    
    def get_justification(self, fact: str) -> Optional[Dict]:
        """
        Obtém a justificação de um fato derivado.
        
        Args:
            fact: Fato a consultar
            
        Returns:
            Dicionário com informações de justificação ou None
        """
        return self.justifications.get(fact)
