import requests
import json
import os
import time
from flask import current_app

class LinkedInAPI:
    """
    Classe para integraÃ§Ã£o com LinkedIn.
    
    Nota: O LinkedIn tem restriÃ§Ãµes severas para automaÃ§Ã£o e uso de API.
    Esta implementaÃ§Ã£o fornece mÃ©todos para auxiliar na integraÃ§Ã£o manual
    e preparar mensagens para envio, mas nÃ£o realiza automaÃ§Ã£o direta.
    """
    
    def __init__(self):
        """Inicializa a classe de integraÃ§Ã£o com LinkedIn."""
        pass
        
    def generate_connection_message(self, lead, template=None):
        """
        Gera uma mensagem personalizada para solicitaÃ§Ã£o de conexÃ£o no LinkedIn.
        
        Args:
            lead: Objeto Lead com informaÃ§Ãµes do contato
            template: Template de mensagem (opcional)
            
        Returns:
            str: Mensagem personalizada para conexÃ£o
        """
        if not template:
            template = (
                "OlÃ¡ {nome}, notei seu trabalho como {cargo} na {empresa} e gostaria de "
                "conectar para compartilhar insights sobre como a IA na IndÃºstria 4.0 "
                "estÃ¡ transformando a inspeÃ§Ã£o de qualidade no setor de {setor}. AbraÃ§os!"
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
            lead: Objeto Lead com informaÃ§Ãµes do contato
            interaction_count: NÃºmero de interaÃ§Ãµes anteriores
            template: Template de mensagem (opcional)
            
        Returns:
            str: Mensagem personalizada de follow-up
        """
        if not template:
            if interaction_count == 0:
                template = (
                    "OlÃ¡ {nome}, obrigado por aceitar minha conexÃ£o! Como mencionei, trabalho com "
                    "sistemas de visÃ£o computacional com IA para inspeÃ§Ã£o de qualidade industrial. "
                    "Nossa soluÃ§Ã£o jÃ¡ ajudou empresas de {setor} a reduzir custos fixos em 75% e "
                    "economizar milhÃµes anualmente. O diferencial Ã© a integraÃ§Ã£o completa com o "
                    "parque industrial existente, identificando trincas, amassados e riscos em tempo real. "
                    "Seria interessante conversar sobre como isso poderia ser aplicado na {empresa}?"
                )
            elif interaction_count == 1:
                template = (
                    "OlÃ¡ {nome}, espero que esteja bem! Gostaria de compartilhar um caso de sucesso "
                    "recente onde nossa soluÃ§Ã£o de IA para inspeÃ§Ã£o visual ajudou uma empresa do setor "
                    "de {setor} a economizar R$ 5,3 milhÃµes por ano ao identificar peÃ§as com defeitos "
                    "para retrabalho. Teria interesse em uma breve demonstraÃ§Ã£o de como funciona?"
                )
            else:
                template = (
                    "OlÃ¡ {nome}, notei que sua empresa {empresa} poderia se beneficiar da nossa "
                    "tecnologia de IA para inspeÃ§Ã£o visual, especialmente considerando os desafios "
                    "de mÃ£o de obra qualificada no setor. Posso compartilhar um material especÃ­fico "
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
            
        # Se jÃ¡ comeÃ§a com http, assume que estÃ¡ correta
        if profile_url.startswith("http"):
            return profile_url
            
        # Se comeÃ§a com www, adiciona https
        if profile_url.startswith("www"):
            return f"https://{profile_url}"
            
        # Se Ã© apenas o nome de usuÃ¡rio
        if "/" not in profile_url:
            return f"https://www.linkedin.com/in/{profile_url}"
            
        # Se comeÃ§a com linkedin.com
        if "linkedin.com" in profile_url:
            return f"https://www.{profile_url}"
            
        # Se comeÃ§a com /in/
        if profile_url.startswith("/in/"):
            return f"https://www.linkedin.com{profile_url}"
            
        # Caso padrÃ£o
        return f"https://www.linkedin.com/in/{profile_url}"
        
    def get_profile_instructions(self, lead):
        """
        Gera instruÃ§Ãµes para acessar o perfil do LinkedIn manualmente.
        
        Args:
            lead: Objeto Lead com informaÃ§Ãµes do contato
            
        Returns:
            dict: InstruÃ§Ãµes para acessar o perfil
        """
        profile_url = self.format_profile_url(lead.linkedin_url)
        
        instructions = {
            "profile_url": profile_url,
            "steps": [
                "1. Acesse o LinkedIn e faÃ§a login na sua conta",
                f"2. Abra o perfil usando a URL: {profile_url}",
                "3. Clique em 'Conectar' para enviar uma solicitaÃ§Ã£o de conexÃ£o",
                "4. Selecione 'Adicionar nota' para personalizar a mensagem",
                "5. Cole a mensagem personalizada gerada pelo sistema",
                "6. Envie a solicitaÃ§Ã£o de conexÃ£o"
            ],
            "connection_message": self.generate_connection_message(lead),
            "follow_up_message": self.generate_follow_up_message(lead)
        }
        
        return instructions
        
    def search_similar_profiles(self, lead):
        """
        Gera instruÃ§Ãµes para buscar perfis similares no LinkedIn.
        
        Args:
            lead: Objeto Lead como referÃªncia
            
        Returns:
            dict: InstruÃ§Ãµes e termos de busca
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
                "1. Acesse o LinkedIn e faÃ§a login na sua conta",
                "2. Clique na barra de pesquisa no topo da pÃ¡gina",
                "3. Digite um dos termos de busca sugeridos",
                "4. Filtre os resultados por 'Pessoas'",
                "5. Refine por localizaÃ§Ã£o (Brasil) se necessÃ¡rio",
                "6. Analise os perfis e adicione os relevantes ao CRM"
            ]
        }
        
        return instructions
