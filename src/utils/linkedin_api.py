import requests
import json
import os
import time
from flask import current_app

class LinkedInAPI:
    """
    Classe para integração com LinkedIn.
    
    Nota: O LinkedIn tem restrições severas para automação e uso de API.
    Esta implementação fornece métodos para auxiliar na integração manual
    e preparar mensagens para envio, mas não realiza automação direta.
    """
    
    def __init__(self):
        """Inicializa a classe de integração com LinkedIn."""
        pass
        
    def generate_connection_message(self, lead, template=None):
        """
        Gera uma mensagem personalizada para solicitação de conexão no LinkedIn.
        
        Args:
            lead: Objeto Lead com informações do contato
            template: Template de mensagem (opcional)
            
        Returns:
            str: Mensagem personalizada para conexão
        """
        if not template:
            template = (
                "Olá {nome}, notei seu trabalho como {cargo} na {empresa} e gostaria de "
                "conectar para compartilhar insights sobre como a IA na Indústria 4.0 "
                "está transformando a inspeção de qualidade no setor de {setor}. Abraços!"
            )
            
        # Personalizar o template
        message = template
        message = message.replace("{nome}", lead.name.split()[0] if lead.name else "")
        message = message.replace("{cargo}", lead.position or "")
        message = message.replace("{empresa}", lead.company or "")
        message = message.replace("{setor}", lead.industry or "")
        
        return message
        
    def generate_follow_up_message(self, lead, interaction_count=0, template=None):
        """
        Gera uma mensagem de follow-up personalizada para LinkedIn.
        
        Args:
            lead: Objeto Lead com informações do contato
            interaction_count: Número de interações anteriores
            template: Template de mensagem (opcional)
            
        Returns:
            str: Mensagem personalizada de follow-up
        """
        if not template:
            if interaction_count == 0:
                template = (
                    "Olá {nome}, obrigado por aceitar minha conexão! Como mencionei, trabalho com "
                    "sistemas de visão computacional com IA para inspeção de qualidade industrial. "
                    "Nossa solução já ajudou empresas de {setor} a reduzir custos fixos em 75% e "
                    "economizar milhões anualmente. O diferencial é a integração completa com o "
                    "parque industrial existente, identificando trincas, amassados e riscos em tempo real. "
                    "Seria interessante conversar sobre como isso poderia ser aplicado na {empresa}?"
                )
            elif interaction_count == 1:
                template = (
                    "Olá {nome}, espero que esteja bem! Gostaria de compartilhar um caso de sucesso "
                    "recente onde nossa solução de IA para inspeção visual ajudou uma empresa do setor "
                    "de {setor} a economizar R$ 5,3 milhões por ano ao identificar peças com defeitos "
                    "para retrabalho. Teria interesse em uma breve demonstração de como funciona?"
                )
            else:
                template = (
                    "Olá {nome}, notei que sua empresa {empresa} poderia se beneficiar da nossa "
                    "tecnologia de IA para inspeção visual, especialmente considerando os desafios "
                    "de mão de obra qualificada no setor. Posso compartilhar um material específico "
                    "sobre como estamos ajudando empresas similares a identificar falhas como trincas, "
                    "amassados e riscos em tempo real?"
                )
                
        # Personalizar o template
        message = template
        message = message.replace("{nome}", lead.name.split()[0] if lead.name else "")
        message = message.replace("{cargo}", lead.position or "")
        message = message.replace("{empresa}", lead.company or "")
        message = message.replace("{setor}", lead.industry or "")
        
        return message
        
    def format_profile_url(self, profile_url):
        """
        Formata corretamente uma URL de perfil do LinkedIn.
        
        Args:
            profile_url: URL do perfil (pode estar incompleta)
            
        Returns:
            str: URL formatada corretamente
        """
        if not profile_url:
            return ""
            
        # Se já começa com http, assume que está correta
        if profile_url.startswith("http"):
            return profile_url
            
        # Se começa com www, adiciona https
        if profile_url.startswith("www"):
            return f"https://{profile_url}"
            
        # Se é apenas o nome de usuário
        if "/" not in profile_url:
            return f"https://www.linkedin.com/in/{profile_url}"
            
        # Se começa com linkedin.com
        if "linkedin.com" in profile_url:
            return f"https://www.{profile_url}"
            
        # Se começa com /in/
        if profile_url.startswith("/in/"):
            return f"https://www.linkedin.com{profile_url}"
            
        # Caso padrão
        return f"https://www.linkedin.com/in/{profile_url}"
        
    def get_profile_instructions(self, lead):
        """
        Gera instruções para acessar o perfil do LinkedIn manualmente.
        
        Args:
            lead: Objeto Lead com informações do contato
            
        Returns:
            dict: Instruções para acessar o perfil
        """
        profile_url = self.format_profile_url(lead.linkedin_url)
        
        instructions = {
            "profile_url": profile_url,
            "steps": [
                "1. Acesse o LinkedIn e faça login na sua conta",
                f"2. Abra o perfil usando a URL: {profile_url}",
                "3. Clique em 'Conectar' para enviar uma solicitação de conexão",
                "4. Selecione 'Adicionar nota' para personalizar a mensagem",
                "5. Cole a mensagem personalizada gerada pelo sistema",
                "6. Envie a solicitação de conexão"
            ],
            "connection_message": self.generate_connection_message(lead),
            "follow_up_message": self.generate_follow_up_message(lead)
        }
        
        return instructions
        
    def search_similar_profiles(self, lead):
        """
        Gera instruções para buscar perfis similares no LinkedIn.
        
        Args:
            lead: Objeto Lead como referência
            
        Returns:
            dict: Instruções e termos de busca
        """
        search_terms = []
        
        if lead.position and lead.industry:
            search_terms.append(f'"{lead.position}" "{lead.industry}"')
            
        if lead.company:
            search_terms.append(f'"{lead.company}"')
            
        if lead.industry:
            search_terms.append(f'"{lead.industry}" "Diretor"')
            search_terms.append(f'"{lead.industry}" "Gerente"')
            
        instructions = {
            "search_terms": search_terms,
            "steps": [
                "1. Acesse o LinkedIn e faça login na sua conta",
                "2. Clique na barra de pesquisa no topo da página",
                "3. Digite um dos termos de busca sugeridos",
                "4. Filtre os resultados por 'Pessoas'",
                "5. Refine por localização (Brasil) se necessário",
                "6. Analise os perfis e adicione os relevantes ao CRM"
            ]
        }
        
        return instructions
