"""
Módulo de leitura de ficheiros de texto.
"""
import os
from typing import Optional


def read_text(file_path: str) -> Optional[str]:
    """
    Lê um ficheiro de texto e retorna o seu conteúdo.
    
    Args:
        file_path: Caminho para o ficheiro de texto
        
    Returns:
        Conteúdo do ficheiro ou None se houver erro
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Ficheiro não encontrado: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    except Exception as e:
        print(f"Erro ao ler ficheiro: {e}")
        return None


def read_text_from_upload(file_storage) -> Optional[str]:
    """
    Lê conteúdo de um ficheiro enviado via upload (Flask).
    
    Args:
        file_storage: Objeto FileStorage do Flask
        
    Returns:
        Conteúdo do ficheiro como string
    """
    try:
        content = file_storage.read().decode('utf-8')
        return content
    except Exception as e:
        print(f"Erro ao ler ficheiro do upload: {e}")
        return None
