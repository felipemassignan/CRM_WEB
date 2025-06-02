"""
Script para popular o banco de dados com dados de teste para demonstraÃ§Ã£o do CRM.
Execute este script apÃ³s inicializar o banco de dados para ter dados de exemplo.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import create_app, db
from src.models.lead import Lead
from src.models.interaction import Interaction
from src.models.template import Template
from src.models.reminder import Reminder
from src.models.user import User
from datetime import datetime, timedelta
import random

# app jÃ¡ estÃ¡ importado do main.py

# Lista de nomes para dados de teste
NOMES = [
    "Carlos Silva", "Ana Oliveira", "Roberto Santos", "Mariana Costa", 
    "Fernando Almeida", "Juliana Pereira", "Ricardo Ferreira", "Patricia Lima",
    "Marcelo Souza", "Camila Rodrigues", "Eduardo Martins", "Luciana Gomes",
    "Gustavo Ribeiro", "Daniela Carvalho", "Paulo Mendes", "Fernanda Barbosa"
]

# Lista de empresas para dados de teste
EMPRESAS = [
    "MetalÃºrgica Progresso", "IndÃºstria Automotiva Brasil", "Usinagem PrecisÃ£o",
    "Motores ElÃ©tricos SA", "Linha Branca Tecnologia", "AutopeÃ§as Nacional",
    "Manufatura AvanÃ§ada", "Equipamentos Industriais Ltda", "PlÃ¡sticos e Componentes",
    "EletrÃ´nicos do Brasil", "RefrigeraÃ§Ã£o Industrial", "AutomaÃ§Ã£o e Controle",
    "MÃ¡quinas e Ferramentas", "IndÃºstria QuÃ­mica BR", "TÃªxtil Moderna",
    "Alimentos Processados SA"
]

# Cargos para dados de teste
CARGOS = [
    "CEO", "COO", "CTO", "CFO", "Diretor Industrial", "Diretor de OperaÃ§Ãµes",
    "Diretor de ProduÃ§Ã£o", "Diretor de Qualidade", "Gerente Industrial",
    "Gerente de OperaÃ§Ãµes", "Gerente de ProduÃ§Ã£o", "Gerente de Qualidade",
    "Engenheiro de ProduÃ§Ã£o", "Supervisor de Qualidade"
]

# Setores industriais para dados de teste
SETORES = [
    "Manufatura Geral", "Metalurgia", "Usinagem", "AutopeÃ§as", "Linha Branca",
    "EletrodomÃ©sticos", "Motores ElÃ©tricos", "AutomaÃ§Ã£o Industrial", "IndÃºstria Automotiva",
    "Equipamentos Industriais", "PlÃ¡sticos e Borrachas", "EletrÃ´nicos"
]

# RegiÃµes para dados de teste
REGIOES = ["Sul", "Sudeste", "Centro-Oeste", "Nordeste", "Norte"]

# Estados por regiÃ£o
ESTADOS = {
    "Sul": ["ParanÃ¡", "Santa Catarina", "Rio Grande do Sul"],
    "Sudeste": ["SÃ£o Paulo", "Rio de Janeiro", "Minas Gerais", "EspÃ­rito Santo"],
    "Centro-Oeste": ["GoiÃ¡s", "Mato Grosso", "Mato Grosso do Sul", "Distrito Federal"],
    "Nordeste": ["Bahia", "CearÃ¡", "Pernambuco", "MaranhÃ£o", "ParaÃ­ba", "Rio Grande do Norte", "Alagoas", "Sergipe", "PiauÃ­"],
    "Norte": ["ParÃ¡", "Amazonas", "RondÃ´nia", "Tocantins", "Acre", "AmapÃ¡", "Roraima"]
}

# Cidades por estado (simplificado)
CIDADES = {
    "SÃ£o Paulo": ["SÃ£o Paulo", "Campinas", "RibeirÃ£o Preto", "SÃ£o JosÃ© dos Campos", "Sorocaba"],
    "Minas Gerais": ["Belo Horizonte", "UberlÃ¢ndia", "Contagem", "Juiz de Fora", "Betim"],
    "Rio de Janeiro": ["Rio de Janeiro", "NiterÃ³i", "Duque de Caxias", "Nova IguaÃ§u", "SÃ£o GonÃ§alo"],
    "ParanÃ¡": ["Curitiba", "Londrina", "MaringÃ¡", "Ponta Grossa", "Cascavel"],
    "Santa Catarina": ["FlorianÃ³polis", "Joinville", "Blumenau", "SÃ£o JosÃ©", "CriciÃºma"],
    "Rio Grande do Sul": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Canoas", "Santa Maria"],
    "Bahia": ["Salvador", "Feira de Santana", "VitÃ³ria da Conquista", "CamaÃ§ari", "Itabuna"],
    "Pernambuco": ["Recife", "JaboatÃ£o dos Guararapes", "Olinda", "Caruaru", "Petrolina"],
    "GoiÃ¡s": ["GoiÃ¢nia", "Aparecida de GoiÃ¢nia", "AnÃ¡polis", "Rio Verde", "LuziÃ¢nia"],
    "ParÃ¡": ["BelÃ©m", "Ananindeua", "SantarÃ©m", "MarabÃ¡", "Castanhal"]
}

# Status para dados de teste
STATUS = ["Novo", "Conectado", "Conversando", "ReuniÃ£o Agendada", "Proposta Enviada", "NegociaÃ§Ã£o", "Cliente", "Perdido"]

# Fontes para dados de teste
FONTES = ["LinkedIn", "Email", "IndicaÃ§Ã£o", "Evento", "Site", "Pesquisa"]

# Prioridades para dados de teste
PRIORIDADES = ["Alta", "MÃ©dia", "Baixa"]

# Tamanhos de empresa
TAMANHOS_EMPRESA = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5000+"]

# Faturamento anual
FATURAMENTOS = [
    "AtÃ© R$ 1 milhÃ£o", 
    "R$ 1-10 milhÃµes", 
    "R$ 10-50 milhÃµes", 
    "R$ 50-100 milhÃµes", 
    "R$ 100-500 milhÃµes", 
    "Acima de R$ 500 milhÃµes"
]

# Tecnologias utilizadas
TECNOLOGIAS = [
    "AutomaÃ§Ã£o Industrial", 
    "RobÃ³tica", 
    "Sensores Ãpticos", 
    "VisÃ£o Computacional BÃ¡sica", 
    "InspeÃ§Ã£o Manual", 
    "Controle de Qualidade Tradicional", 
    "PLCs", 
    "Sistemas SCADA", 
    "IoT Industrial", 
    "IndÃºstria 4.0 Parcial"
]

# Pontos de dor
PONTOS_DOR = [
    "Alta taxa de retrabalho por falhas nÃ£o detectadas",
    "Custo elevado com mÃ£o de obra para inspeÃ§Ã£o visual",
    "Falta de padronizaÃ§Ã£o no processo de inspeÃ§Ã£o",
    "Dificuldade em encontrar profissionais qualificados",
    "Perda de material por falhas tardias",
    "ReclamaÃ§Ãµes de clientes por problemas de qualidade",
    "Baixa produtividade na linha de inspeÃ§Ã£o",
    "InconsistÃªncia nos critÃ©rios de aprovaÃ§Ã£o/rejeiÃ§Ã£o",
    "Dificuldade em rastrear origem dos defeitos",
    "Tempo excessivo no processo de inspeÃ§Ã£o"
]

# Tipos de interaÃ§Ã£o
TIPOS_INTERACAO = ["ConexÃ£o LinkedIn", "Mensagem LinkedIn", "Email", "LigaÃ§Ã£o", "ReuniÃ£o"]

# Resultados de interaÃ§Ã£o
RESULTADOS_INTERACAO = ["Positivo", "Neutro", "Negativo"]

# PrÃ³ximos passos
PROXIMOS_PASSOS = [
    "Enviar material tÃ©cnico",
    "Agendar demonstraÃ§Ã£o",
    "Fazer follow-up em 7 dias",
    "Enviar proposta comercial",
    "Agendar reuniÃ£o com equipe tÃ©cnica",
    "Apresentar caso de sucesso similar",
    "Convidar para webinar",
    "Visitar instalaÃ§Ãµes do cliente"
]

# Templates de mensagens
TEMPLATES_MENSAGEM = [
    {
        "categoria": "ConexÃ£o LinkedIn",
        "cargo_alvo": "Todos",
        "assunto": "ConexÃ£o LinkedIn",
        "conteudo": "OlÃ¡ {primeiro_nome}, notei seu trabalho como {cargo} na {empresa} e gostaria de conectar para compartilhar insights sobre como a IA na IndÃºstria 4.0 estÃ¡ transformando a inspeÃ§Ã£o de qualidade no setor de {setor}. AbraÃ§os!",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar para primeiro contato no LinkedIn"
    },
    {
        "categoria": "Primeira Mensagem",
        "cargo_alvo": "Diretor Industrial",
        "assunto": "IA para InspeÃ§Ã£o de Qualidade Industrial",
        "conteudo": "OlÃ¡ {primeiro_nome}, obrigado por aceitar minha conexÃ£o! Como mencionei, trabalho com sistemas de visÃ£o computacional com IA para inspeÃ§Ã£o de qualidade industrial. Nossa soluÃ§Ã£o jÃ¡ ajudou empresas de {setor} a reduzir custos fixos em 75% e economizar milhÃµes anualmente. O diferencial Ã© a integraÃ§Ã£o completa com o parque industrial existente, identificando trincas, amassados e riscos em tempo real. Seria interessante conversar sobre como isso poderia ser aplicado na {empresa}?",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar apÃ³s aceite de conexÃ£o para Diretores Industriais"
    },
    {
        "categoria": "Primeira Mensagem",
        "cargo_alvo": "CEO",
        "assunto": "ReduÃ§Ã£o de Custos com IA Industrial",
        "conteudo": "OlÃ¡ {primeiro_nome}, agradeÃ§o a conexÃ£o! Lidero uma empresa de tecnologia especializada em sistemas de visÃ£o computacional com IA para inspeÃ§Ã£o de qualidade industrial. Um de nossos clientes do setor de {setor} conseguiu economizar R$ 5,3 milhÃµes/ano ao identificar peÃ§as com defeitos para retrabalho antes que chegassem ao cliente final. Nossa tecnologia se integra ao parque industrial existente, sem grandes modificaÃ§Ãµes na linha. Podemos conversar sobre como isso poderia impactar positivamente os resultados da {empresa}?",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar apÃ³s aceite de conexÃ£o para CEOs, focando em resultados financeiros"
    },
    {
        "categoria": "Follow-up",
        "cargo_alvo": "Todos",
        "assunto": "Case de Sucesso: Economia de R$ 5,3 milhÃµes com IA",
        "conteudo": "OlÃ¡ {primeiro_nome}, espero que esteja bem! Gostaria de compartilhar um caso de sucesso recente onde nossa soluÃ§Ã£o de IA para inspeÃ§Ã£o visual ajudou uma empresa do setor de {setor} a economizar R$ 5,3 milhÃµes por ano ao identificar peÃ§as com defeitos para retrabalho. Teria interesse em uma breve demonstraÃ§Ã£o de como funciona?",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar como primeiro follow-up apÃ³s alguns dias sem resposta"
    },
    {
        "categoria": "Email",
        "cargo_alvo": "Gerente de Qualidade",
        "assunto": "SoluÃ§Ã£o para padronizaÃ§Ã£o de inspeÃ§Ã£o de qualidade",
        "conteudo": "Prezado(a) {primeiro_nome},\n\nEspero que esteja bem.\n\nEstou entrando em contato porque nossa empresa desenvolveu uma soluÃ§Ã£o de visÃ£o computacional com IA que estÃ¡ ajudando indÃºstrias do setor de {setor} a padronizar seus processos de inspeÃ§Ã£o de qualidade, eliminando a subjetividade e reduzindo a dependÃªncia de mÃ£o de obra especializada.\n\nO sistema identifica automaticamente trincas, amassados, riscos e outros defeitos em tempo real, com precisÃ£o superior a 99,5%, e se integra facilmente ao parque industrial existente.\n\nGostaria de agendar uma breve demonstraÃ§Ã£o online de 20 minutos para mostrar como funciona?\n\nAtenciosamente,\n[Seu Nome]",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Email inicial para Gerentes de Qualidade, focando na padronizaÃ§Ã£o"
    }
]

def gerar_email(nome, empresa):
    """Gera um email fictÃ­cio baseado no nome e empresa."""
    primeiro_nome = nome.split()[0].lower()
    sobrenome = nome.split()[-1].lower()
    empresa_simplificada = empresa.split()[0].lower()
    
    domÃ­nios = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com.br", "uol.com.br"]
    domÃ­nio_corporativo = f"{empresa_simplificada}.com.br"
    
    # 70% de chance de ser email corporativo
    if random.random() < 0.7:
        return f"{primeiro_nome}.{sobrenome}@{domÃ­nio_corporativo}"
    else:
        return f"{primeiro_nome}.{sobrenome}@{random.choice(domÃ­nios)}"

def gerar_linkedin_url(nome):
    """Gera uma URL de LinkedIn fictÃ­cia baseada no nome."""
    nome_formatado = nome.lower().replace(" ", "-")
    return f"https://www.linkedin.com/in/{nome_formatado}-{random.randint(100, 999)}"

def gerar_telefone():
    """Gera um nÃºmero de telefone fictÃ­cio no formato brasileiro."""
    ddd = random.randint(11, 99)
    numero = random.randint(10000000, 99999999)
    return f"({ddd}) 9{numero}"

def criar_dados_teste():
    """Cria dados de teste no banco de dados."""
    app = create_app() 
    with app.app_context():
        # Criar usuÃ¡rio de teste
        if not User.query.filter_by(username="admin").first():
            user = User(username="admin", email="admin@exemplo.com")
            db.session.add(user)
            db.session.commit()
            print("UsuÃ¡rio de teste criado.")
        
        # Criar leads de teste
        leads_criados = []
        for i in range(30):  # Criar 30 leads de teste
            nome = random.choice(NOMES)
            empresa = random.choice(EMPRESAS)
            cargo = random.choice(CARGOS)
            setor = random.choice(SETORES)
            regiao = random.choice(REGIOES)
            estado = random.choice(ESTADOS[regiao])
            cidade = random.choice(CIDADES.get(estado, ["Cidade Principal"]))
            status = random.choice(STATUS)
            fonte = random.choice(FONTES)
            prioridade = random.choice(PRIORIDADES)
            
            # Datas
            dias_atras = random.randint(1, 90)
            data_adicao = datetime.now() - timedelta(days=dias_atras)
            
            # Ãltima interaÃ§Ã£o (se houver)
            ultima_interacao = None
            if status != "Novo" and random.random() < 0.8:
                dias_desde_adicao = random.randint(1, dias_atras)
                ultima_interacao = data_adicao + timedelta(days=dias_desde_adicao)
            
            # PrÃ³xima aÃ§Ã£o (se aplicÃ¡vel)
            proxima_acao = None
            data_proxima_acao = None
            if status in ["Conectado", "Conversando", "ReuniÃ£o Agendada", "Proposta Enviada", "NegociaÃ§Ã£o"]:
                proxima_acao = random.choice(PROXIMOS_PASSOS)
                dias_futuro = random.randint(1, 14)
                data_proxima_acao = datetime.now() + timedelta(days=dias_futuro)
            
            # Campos adicionais
            tamanho_empresa = random.choice(TAMANHOS_EMPRESA)
            faturamento = random.choice(FATURAMENTOS)
            tecnologias = ", ".join(random.sample(TECNOLOGIAS, random.randint(1, 3)))
            pontos_dor = random.choice(PONTOS_DOR)
            
            lead = Lead(
                name=nome,
                position=cargo,
                company=empresa,
                industry=setor,
                linkedin_url=gerar_linkedin_url(nome),
                email=gerar_email(nome, empresa),
                phone=gerar_telefone(),
                region=regiao,
                state=estado,
                city=cidade,
                status=status,
                source=fonte,
                added_date=data_adicao,
                last_interaction_date=ultima_interacao,
                next_action=proxima_acao,
                next_action_date=data_proxima_acao,
                owner="admin",
                priority=prioridade,
                company_size=tamanho_empresa,
                annual_revenue=faturamento,
                technologies_used=tecnologias,
                pain_points=pontos_dor,
                notes=f"Lead de teste gerado automaticamente. {random.choice(PONTOS_DOR)}"
            )
            
            db.session.add(lead)
            db.session.flush()  # Para obter o ID do lead
            leads_criados.append(lead)
        
        db.session.commit()
        print(f"{len(leads_criados)} leads de teste criados.")
        
        # Criar interaÃ§Ãµes de teste
        interacoes_criadas = 0
        for lead in leads_criados:
            # Pular leads novos
            if lead.status == "Novo":
                continue
                
            # NÃºmero de interaÃ§Ãµes baseado no status
            num_interacoes = {
                "Conectado": random.randint(1, 2),
                "Conversando": random.randint(2, 4),
                "ReuniÃ£o Agendada": random.randint(3, 5),
                "Proposta Enviada": random.randint(4, 6),
                "NegociaÃ§Ã£o": random.randint(5, 8),
                "Cliente": random.randint(6, 10),
                "Perdido": random.randint(3, 6)
            }.get(lead.status, 0)
            
            for i in range(num_interacoes):
                tipo = random.choice(TIPOS_INTERACAO)
                
                # Data da interaÃ§Ã£o
                if lead.last_interaction_date:
                    data_base = lead.last_interaction_date
                else:
                    data_base = lead.added_date
                    
                dias_apos_base = random.randint(1, 10)
                data_interacao = data_base + timedelta(days=i * dias_apos_base)
                
                # ConteÃºdo baseado no tipo
                if tipo == "ConexÃ£o LinkedIn":
                    conteudo = "SolicitaÃ§Ã£o de conexÃ£o enviada no LinkedIn."
                elif tipo == "Mensagem LinkedIn":
                    conteudo = random.choice([
                        "Enviada mensagem apresentando a soluÃ§Ã£o de IA para inspeÃ§Ã£o visual.",
                        "Compartilhado case de sucesso sobre economia de R$ 5,3 milhÃµes/ano.",
                        "Enviado artigo sobre IA na IndÃºstria 4.0 aplicada Ã  inspeÃ§Ã£o de qualidade."
                    ])
                elif tipo == "Email":
                    conteudo = random.choice([
                        "Email com apresentaÃ§Ã£o detalhada da soluÃ§Ã£o.",
                        "Email de follow-up apÃ³s contato inicial.",
                        "Email com proposta comercial personalizada.",
                        "Email agradecendo pela reuniÃ£o e enviando materiais adicionais."
                    ])
                elif tipo == "LigaÃ§Ã£o":
                    conteudo = random.choice([
                        "LigaÃ§Ã£o para apresentaÃ§Ã£o inicial da soluÃ§Ã£o.",
                        "LigaÃ§Ã£o de follow-up apÃ³s envio de materiais.",
                        "Conversa sobre necessidades especÃ­ficas e pontos de dor.",
                        "DiscussÃ£o sobre prÃ³ximos passos e agendamento de demonstraÃ§Ã£o."
                    ])
                else:  # ReuniÃ£o
                    conteudo = random.choice([
                        "ReuniÃ£o inicial de apresentaÃ§Ã£o da soluÃ§Ã£o.",
                        "DemonstraÃ§Ã£o tÃ©cnica da plataforma de IA.",
                        "ReuniÃ£o com equipe tÃ©cnica para discutir integraÃ§Ã£o.",
                        "ApresentaÃ§Ã£o de proposta comercial e ROI esperado."
                    ])
                
                # Resposta (mais provÃ¡vel em estÃ¡gios avanÃ§ados)
                probabilidade_resposta = {
                    "Conectado": 0.3,
                    "Conversando": 0.6,
                    "ReuniÃ£o Agendada": 0.8,
                    "Proposta Enviada": 0.9,
                    "NegociaÃ§Ã£o": 0.95,
                    "Cliente": 1.0,
                    "Perdido": 0.4
                }.get(lead.status, 0.2)
                
                resposta = random.random() < probabilidade_resposta
                
                # Resultado (mais positivo em estÃ¡gios avanÃ§ados)
                if lead.status in ["Cliente", "NegociaÃ§Ã£o", "Proposta Enviada"]:
                    resultado = random.choices(
                        RESULTADOS_INTERACAO, 
                        weights=[0.7, 0.2, 0.1]
                    )[0]
                elif lead.status == "Perdido":
                    resultado = random.choices(
                        RESULTADOS_INTERACAO, 
                        weights=[0.1, 0.3, 0.6]
                    )[0]
                else:
                    resultado = random.choice(RESULTADOS_INTERACAO)
                
                # PrÃ³ximo passo
                proximo_passo = random.choice(PROXIMOS_PASSOS)
                dias_futuro = random.randint(1, 14)
                data_proximo_passo = data_interacao + timedelta(days=dias_futuro)
                
                # Notas
                notas = ""
                if resposta:
                    if resultado == "Positivo":
                        notas = random.choice([
                            "Demonstrou interesse na soluÃ§Ã£o. Mencionou problemas com inspeÃ§Ã£o manual.",
                            "Muito receptivo. Solicitou mais informaÃ§Ãµes sobre casos de sucesso.",
                            "Comentou sobre dificuldades em encontrar mÃ£o de obra qualificada para inspeÃ§Ã£o.",
                            "Interessado na reduÃ§Ã£o de custos e aumento de precisÃ£o."
                        ])
                    elif resultado == "Neutro":
                        notas = random.choice([
                            "Pediu para entrar em contato novamente em algumas semanas.",
                            "EstÃ¡ avaliando outras soluÃ§Ãµes no momento.",
                            "Interessado, mas sem orÃ§amento no momento.",
                            "Solicitou mais informaÃ§Ãµes tÃ©cnicas para avaliar."
                        ])
                    else:
                        notas = random.choice([
                            "NÃ£o vÃª aplicaÃ§Ã£o imediata na empresa.",
                            "JÃ¡ utiliza outra soluÃ§Ã£o semelhante.",
                            "Sem interesse no momento devido a restriÃ§Ãµes orÃ§amentÃ¡rias.",
                            "Prefere manter o processo manual atual."
                        ])
                
                interacao = Interaction(
                    lead_id=lead.id,
                    date=data_interacao,
                    type=tipo,
                    content=conteudo,
                    response=resposta,
                    next_step=proximo_passo if i == num_interacoes - 1 else None,
                    next_step_date=data_proximo_passo if i == num_interacoes - 1 else None,
                    result=resultado,
                    notes=notas
                )
                
                db.session.add(interacao)
                interacoes_criadas += 1
        
        db.session.commit()
        print(f"{interacoes_criadas} interaÃ§Ãµes de teste criadas.")
        
        # Criar templates de mensagem
        templates_criados = 0
        for template in TEMPLATES_MENSAGEM:
            t = Template(
                category=template["categoria"],
                target_position=template["cargo_alvo"],
                subject=template["assunto"],
                content=template["conteudo"],
                variables=template["variaveis"],
                usage_notes=template["notas_uso"],
                usage_count=random.randint(0, 15),
                last_used=datetime.now() - timedelta(days=random.randint(1, 30)) if random.random() < 0.7 else None
            )
            db.session.add(t)
            templates_criados += 1
        
        db.session.commit()
        print(f"{templates_criados} templates de mensagem criados.")
        
        # Criar lembretes
        lembretes_criados = 0
        for lead in leads_criados:
            # Apenas criar lembretes para leads ativos
            if lead.status not in ["Novo", "Perdido", "Cliente"]:
                # 70% de chance de ter um lembrete
                if random.random() < 0.7:
                    dias_futuro = random.randint(1, 14)
                    data_vencimento = datetime.now() + timedelta(days=dias_futuro)
                    
                    titulo = random.choice([
                        f"Follow-up com {lead.name}",
                        f"Enviar proposta para {lead.company}",
                        f"Agendar demonstraÃ§Ã£o com {lead.name}",
                        f"Verificar interesse de {lead.name} na soluÃ§Ã£o",
                        f"Compartilhar case de sucesso com {lead.name}"
                    ])
                    
                    descricao = random.choice([
                        "Enviar email de follow-up com materiais adicionais.",
                        "Ligar para verificar recebimento da proposta.",
                        "Enviar mensagem no LinkedIn com novo case de sucesso.",
                        "Agendar reuniÃ£o para apresentaÃ§Ã£o tÃ©cnica.",
                        "Verificar feedback sobre materiais enviados anteriormente."
                    ])
                    
                    lembrete = Reminder(
                        lead_id=lead.id,
                        user_id=1,  # ID do usuÃ¡rio admin
                        title=titulo,
                        description=descricao,
                        due_date=data_vencimento,
                        is_completed=False
                    )
                    
                    db.session.add(lembrete)
                    lembretes_criados += 1
        
        db.session.commit()
        print(f"{lembretes_criados} lembretes de teste criados.")
        
        print("Dados de teste criados com sucesso!")

if __name__ == "__main__":
    criar_dados_teste()
