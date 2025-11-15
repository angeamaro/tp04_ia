"""
Módulo de extração semântica de fatos e regras usando spaCy.
"""
import spacy
import re
from typing import List, Dict, Tuple


class SemanticExtractor:
    """Extrator de fatos e regras de texto em linguagem natural."""
    
    def __init__(self, model_name: str = "pt_core_news_sm"):
        """
        Inicializa o extrator com modelo spaCy.
        
        Args:
            model_name: Nome do modelo spaCy a usar
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Modelo {model_name} não encontrado. Tentando instalar...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", model_name])
            self.nlp = spacy.load(model_name)
    
    def normalize_term(self, term: str) -> str:
        """
        Normaliza um termo removendo acentos e convertendo para formato adequado.
        
        Args:
            term: Termo a normalizar
            
        Returns:
            Termo normalizado
        """
        # Remove espaços extras
        term = term.strip()
        
        # Primeira letra maiúscula para nomes próprios, resto minúsculo
        if term and term[0].isupper():
            # É um nome próprio (variável ou entidade específica)
            return term.capitalize()
        else:
            # É um predicado ou relação
            return term.lower()
    
    def extract_facts(self, text: str) -> List[str]:
        """
        Extrai fatos simples do texto.
        Exemplo: "Sócrates é um humano" -> humano(Socrates)
        
        Args:
            text: Texto em linguagem natural
            
        Returns:
            Lista de fatos no formato predicado(termo)
        """
        facts = []
        doc = self.nlp(text)
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            
            # Padrão: "X é um/uma Y"
            pattern1 = r"(\w+)\s+é\s+um[a]?\s+(\w+)"
            match = re.search(pattern1, sent_text, re.IGNORECASE)
            if match:
                entity = self.normalize_term(match.group(1))
                attribute = self.normalize_term(match.group(2))
                facts.append(f"{attribute}({entity})")
                continue
            
            # Padrão alternativo: "X é Y"
            pattern2 = r"(\w+)\s+é\s+(\w+)"
            match = re.search(pattern2, sent_text, re.IGNORECASE)
            if match:
                entity = self.normalize_term(match.group(1))
                attribute = self.normalize_term(match.group(2))
                facts.append(f"{attribute}({entity})")
        
        return facts
    
    def extract_rules(self, text: str) -> List[str]:
        """
        Extrai regras universais do texto.
        Exemplo: "Todo humano é mortal" -> mortal(X) :- humano(X)
        
        Args:
            text: Texto em linguagem natural
            
        Returns:
            Lista de regras no formato consequente :- antecedente
        """
        rules = []
        doc = self.nlp(text)
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            
            # Padrão: "Todo/Toda X é Y" ou "Todos os X são Y"
            patterns = [
                r"Tod[oa]s?\s+(?:os?\s+)?(\w+)\s+[ée]\s+(?:um[a]?\s+)?(\w+)",
                r"Qualquer\s+(\w+)\s+é\s+(?:um[a]?\s+)?(\w+)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, sent_text, re.IGNORECASE)
                if match:
                    antecedent = self.normalize_term(match.group(1))
                    consequent = self.normalize_term(match.group(2))
                    rules.append(f"{consequent}(X) :- {antecedent}(X)")
                    break
        
        return rules
    
    def extract_knowledge(self, text: str) -> Dict[str, List[str]]:
        """
        Extrai todos os conhecimentos (fatos e regras) do texto.
        
        Args:
            text: Texto em linguagem natural
            
        Returns:
            Dicionário com 'facts' e 'rules'
        """
        facts = self.extract_facts(text)
        rules = self.extract_rules(text)
        
        return {
            'facts': facts,
            'rules': rules
        }
