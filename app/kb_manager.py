"""
Módulo de gestão da base de conhecimento (Knowledge Base).
Armazena fatos e regras em formato JSON.
"""
import json
import os
from typing import Dict, List, Optional


class KnowledgeBase:
    """Gestor da base de conhecimento."""
    
    def __init__(self, kb_path: str = None):
        """
        Inicializa a base de conhecimento.
        
        Args:
            kb_path: Caminho para o ficheiro JSON da KB (usa KB_PATH env var se não especificado)
        """
        if kb_path is None:
            kb_path = os.environ.get('KB_PATH', 'kb.json')
        
        # Criar diretório se não existir
        kb_dir = os.path.dirname(kb_path)
        if kb_dir and not os.path.exists(kb_dir):
            os.makedirs(kb_dir, exist_ok=True)
        
        self.kb_path = kb_path
        self.facts: List[str] = []
        self.rules: List[str] = []
        self.inferences: List[Dict] = []
        
        self.load()
    
    def load(self):
        """Carrega a base de conhecimento do ficheiro JSON."""
        if os.path.exists(self.kb_path):
            try:
                with open(self.kb_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.facts = data.get('facts', [])
                    self.rules = data.get('rules', [])
                    self.inferences = data.get('inferences', [])
            except Exception as e:
                print(f"Erro ao carregar KB: {e}")
                self._initialize_empty()
        else:
            self._initialize_empty()
    
    def _initialize_empty(self):
        """Inicializa uma base de conhecimento vazia."""
        self.facts = []
        self.rules = []
        self.inferences = []
    
    def save(self):
        """Guarda a base de conhecimento no ficheiro JSON."""
        try:
            data = {
                'facts': self.facts,
                'rules': self.rules,
                'inferences': self.inferences
            }
            with open(self.kb_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao guardar KB: {e}")
    
    def add_fact(self, fact: str):
        """
        Adiciona um fato à base de conhecimento.
        
        Args:
            fact: Fato no formato predicado(termo)
        """
        if fact not in self.facts:
            self.facts.append(fact)
    
    def add_rule(self, rule: str):
        """
        Adiciona uma regra à base de conhecimento.
        
        Args:
            rule: Regra no formato consequente :- antecedente
        """
        if rule not in self.rules:
            self.rules.append(rule)
    
    def add_inference(self, inference: Dict):
        """
        Adiciona uma inferência realizada.
        
        Args:
            inference: Dicionário com informações da inferência
        """
        self.inferences.append(inference)
    
    def get_facts(self) -> List[str]:
        """Retorna todos os fatos."""
        return self.facts.copy()
    
    def get_rules(self) -> List[str]:
        """Retorna todas as regras."""
        return self.rules.copy()
    
    def get_inferences(self) -> List[Dict]:
        """Retorna todas as inferências."""
        return self.inferences.copy()
    
    def clear(self):
        """Limpa toda a base de conhecimento."""
        self.facts = []
        self.rules = []
        self.inferences = []
        self.save()
    
    def import_knowledge(self, facts: List[str], rules: List[str]):
        """
        Importa conhecimento (fatos e regras) para a KB.
        
        Args:
            facts: Lista de fatos
            rules: Lista de regras
        """
        for fact in facts:
            self.add_fact(fact)
        for rule in rules:
            self.add_rule(rule)
        self.save()
    
    def to_dict(self) -> Dict:
        """Retorna a KB como dicionário."""
        return {
            'facts': self.facts,
            'rules': self.rules,
            'inferences': self.inferences
        }
