"""
Módulo de consultas e geração de árvores de prova.
"""
from typing import Dict, Optional, List
from app.unification import parse_predicate, unify_predicates
from app.kb_manager import KnowledgeBase


class QueryEngine:
    """Motor de consultas com geração de árvores de prova."""
    
    def __init__(self, kb: KnowledgeBase):
        """
        Inicializa o motor de consultas.
        
        Args:
            kb: Instância de KnowledgeBase
        """
        self.kb = kb
    
    def parse_query(self, query: str) -> str:
        """
        Faz parse de uma query, removendo o '?' se existir.
        
        Args:
            query: Query em string (ex: "mortal(Socrates)?")
            
        Returns:
            Query limpa
        """
        return query.strip().rstrip('?')
    
    def query(self, query_str: str) -> Dict:
        """
        Executa uma consulta na base de conhecimento.
        
        Args:
            query_str: Query a executar
            
        Returns:
            Dicionário com resultado e árvore de prova
        """
        query = self.parse_query(query_str)
        
        # Verificar se é um fato direto
        if query in self.kb.get_facts():
            return {
                'result': 'true',
                'query': query,
                'proof_tree': self.build_proof_tree(query, 'base_fact')
            }
        
        # Verificar se foi inferido
        inferences = self.kb.get_inferences()
        for inference in inferences:
            if inference.get('derived_fact') == query:
                return {
                    'result': 'true',
                    'query': query,
                    'proof_tree': self.build_proof_tree(query, 'inference', inference)
                }
        
        # Tentar unificar com fatos existentes (para queries com variáveis)
        all_facts = self.kb.get_facts().copy()
        
        # Adicionar fatos inferidos
        for inference in inferences:
            derived = inference.get('derived_fact')
            if derived:
                all_facts.append(derived)
        
        for fact in all_facts:
            subs = unify_predicates(query, fact)
            if subs is not None:
                # Encontrou match
                inference_info = self.find_inference_for_fact(fact)
                proof_type = 'inference' if inference_info else 'base_fact'
                return {
                    'result': 'true',
                    'query': query,
                    'matched_fact': fact,
                    'substitutions': subs,
                    'proof_tree': self.build_proof_tree(fact, proof_type, inference_info)
                }
        
        # Não encontrado
        return {
            'result': 'false',
            'query': query,
            'proof_tree': None
        }
    
    def find_inference_for_fact(self, fact: str) -> Optional[Dict]:
        """
        Encontra a inferência que gerou um fato.
        
        Args:
            fact: Fato a procurar
            
        Returns:
            Dicionário de inferência ou None
        """
        for inference in self.kb.get_inferences():
            if inference.get('derived_fact') == fact:
                return inference
        return None
    
    def build_proof_tree(self, fact: str, proof_type: str, 
                         inference: Optional[Dict] = None) -> Dict:
        """
        Constrói árvore de prova para um fato.
        
        Args:
            fact: Fato a provar
            proof_type: 'base_fact' ou 'inference'
            inference: Informações de inferência (se aplicável)
            
        Returns:
            Árvore de prova como dicionário
        """
        if proof_type == 'base_fact':
            return {
                'fact': fact,
                'type': 'base_fact',
                'children': [],
                'explanation': 'Fato base da base de conhecimento'
            }
        
        elif proof_type == 'inference' and inference:
            # Construir árvore recursivamente
            children = []
            used_facts = inference.get('using_facts', [])
            
            for used_fact in used_facts:
                # Verificar se este fato também foi inferido
                child_inference = self.find_inference_for_fact(used_fact)
                if child_inference:
                    child_tree = self.build_proof_tree(used_fact, 'inference', child_inference)
                else:
                    child_tree = self.build_proof_tree(used_fact, 'base_fact')
                children.append(child_tree)
            
            return {
                'fact': fact,
                'type': 'inference',
                'rule': inference.get('from_rule', ''),
                'substitutions': inference.get('substitutions', {}),
                'children': children,
                'explanation': f'Derivado pela regra: {inference.get("from_rule", "")}'
            }
        
        return {
            'fact': fact,
            'type': 'unknown',
            'children': [],
            'explanation': 'Origem desconhecida'
        }
    
    def format_proof_tree_text(self, tree: Dict, indent: int = 0) -> str:
        """
        Formata árvore de prova como texto hierárquico.
        
        Args:
            tree: Árvore de prova
            indent: Nível de indentação
            
        Returns:
            String formatada
        """
        if not tree:
            return ""
        
        prefix = "  " * indent + "└── "
        result = f"{prefix}{tree['fact']}\n"
        
        if tree.get('rule'):
            result += f"{'  ' * (indent + 1)}(regra: {tree['rule']})\n"
        
        for child in tree.get('children', []):
            result += self.format_proof_tree_text(child, indent + 1)
        
        return result
