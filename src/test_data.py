"""
Script para popular o banco de dados com dados de teste para demonstração do CRM.
Execute este script após inicializar o banco de dados para ter dados de exemplo.
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

# app já está importado do main.py

# Lista de nomes para dados de teste
NOMES = [
    "Carlos Silva", "Ana Oliveira", "Roberto Santos", "Mariana Costa", 
    "Fernando Almeida", "Juliana Pereira", "Ricardo Ferreira", "Patricia Lima",
    "Marcelo Souza", "Camila Rodrigues", "Eduardo Martins", "Luciana Gomes",
    "Gustavo Ribeiro", "Daniela Carvalho", "Paulo Mendes", "Fernanda Barbosa"
]

# Lista de empresas para dados de teste
EMPRESAS = [
    "Metalúrgica Progresso", "Indústria Automotiva Brasil", "Usinagem Precisão",
    "Motores Elétricos SA", "Linha Branca Tecnologia", "Autopeças Nacional",
    "Manufatura Avançada", "Equipamentos Industriais Ltda", "Plásticos e Componentes",
    "Eletrônicos do Brasil", "Refrigeração Industrial", "Automação e Controle",
    "Máquinas e Ferramentas", "Indústria Química BR", "Têxtil Moderna",
    "Alimentos Processados SA"
]

# Cargos para dados de teste
CARGOS = [
    "CEO", "COO", "CTO", "CFO", "Diretor Industrial", "Diretor de Operações",
    "Diretor de Produção", "Diretor de Qualidade", "Gerente Industrial",
    "Gerente de Operações", "Gerente de Produção", "Gerente de Qualidade",
    "Engenheiro de Produção", "Supervisor de Qualidade"
]

# Setores industriais para dados de teste
SETORES = [
    "Manufatura Geral", "Metalurgia", "Usinagem", "Autopeças", "Linha Branca",
    "Eletrodomésticos", "Motores Elétricos", "Automação Industrial", "Indústria Automotiva",
    "Equipamentos Industriais", "Plásticos e Borrachas", "Eletrônicos"
]

# Regiões para dados de teste
REGIOES = ["Sul", "Sudeste", "Centro-Oeste", "Nordeste", "Norte"]

# Estados por região
ESTADOS = {
    "Sul": ["Paraná", "Santa Catarina", "Rio Grande do Sul"],
    "Sudeste": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Espírito Santo"],
    "Centro-Oeste": ["Goiás", "Mato Grosso", "Mato Grosso do Sul", "Distrito Federal"],
    "Nordeste": ["Bahia", "Ceará", "Pernambuco", "Maranhão", "Paraíba", "Rio Grande do Norte", "Alagoas", "Sergipe", "Piauí"],
    "Norte": ["Pará", "Amazonas", "Rondônia", "Tocantins", "Acre", "Amapá", "Roraima"]
}

# Cidades por estado (simplificado)
CIDADES = {
    "São Paulo": ["São Paulo", "Campinas", "Ribeirão Preto", "São José dos Campos", "Sorocaba"],
    "Minas Gerais": ["Belo Horizonte", "Uberlândia", "Contagem", "Juiz de Fora", "Betim"],
    "Rio de Janeiro": ["Rio de Janeiro", "Niterói", "Duque de Caxias", "Nova Iguaçu", "São Gonçalo"],
    "Paraná": ["Curitiba", "Londrina", "Maringá", "Ponta Grossa", "Cascavel"],
    "Santa Catarina": ["Florianópolis", "Joinville", "Blumenau", "São José", "Criciúma"],
    "Rio Grande do Sul": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Canoas", "Santa Maria"],
    "Bahia": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Camaçari", "Itabuna"],
    "Pernambuco": ["Recife", "Jaboatão dos Guararapes", "Olinda", "Caruaru", "Petrolina"],
    "Goiás": ["Goiânia", "Aparecida de Goiânia", "Anápolis", "Rio Verde", "Luziânia"],
    "Pará": ["Belém", "Ananindeua", "Santarém", "Marabá", "Castanhal"]
}

# Status para dados de teste
STATUS = ["Novo", "Conectado", "Conversando", "Reunião Agendada", "Proposta Enviada", "Negociação", "Cliente", "Perdido"]

# Fontes para dados de teste
FONTES = ["LinkedIn", "Email", "Indicação", "Evento", "Site", "Pesquisa"]

# Prioridades para dados de teste
PRIORIDADES = ["Alta", "Média", "Baixa"]

# Tamanhos de empresa
TAMANHOS_EMPRESA = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5000+"]

# Faturamento anual
FATURAMENTOS = [
    "Até R$ 1 milhão", 
    "R$ 1-10 milhões", 
    "R$ 10-50 milhões", 
    "R$ 50-100 milhões", 
    "R$ 100-500 milhões", 
    "Acima de R$ 500 milhões"
]

# Tecnologias utilizadas
TECNOLOGIAS = [
    "Automação Industrial", 
    "Robótica", 
    "Sensores Ópticos", 
    "Visão Computacional Básica", 
    "Inspeção Manual", 
    "Controle de Qualidade Tradicional", 
    "PLCs", 
    "Sistemas SCADA", 
    "IoT Industrial", 
    "Indústria 4.0 Parcial"
]

# Pontos de dor
PONTOS_DOR = [
    "Alta taxa de retrabalho por falhas não detectadas",
    "Custo elevado com mão de obra para inspeção visual",
    "Falta de padronização no processo de inspeção",
    "Dificuldade em encontrar profissionais qualificados",
    "Perda de material por falhas tardias",
    "Reclamações de clientes por problemas de qualidade",
    "Baixa produtividade na linha de inspeção",
    "Inconsistência nos critérios de aprovação/rejeição",
    "Dificuldade em rastrear origem dos defeitos",
    "Tempo excessivo no processo de inspeção"
]

# Tipos de interação
TIPOS_INTERACAO = ["Conexão LinkedIn", "Mensagem LinkedIn", "Email", "Ligação", "Reunião"]

# Resultados de interação
RESULTADOS_INTERACAO = ["Positivo", "Neutro", "Negativo"]

# Próximos passos
PROXIMOS_PASSOS = [
    "Enviar material técnico",
    "Agendar demonstração",
    "Fazer follow-up em 7 dias",
    "Enviar proposta comercial",
    "Agendar reunião com equipe técnica",
    "Apresentar caso de sucesso similar",
    "Convidar para webinar",
    "Visitar instalações do cliente"
]

# Templates de mensagens
TEMPLATES_MENSAGEM = [
    {
        "categoria": "Conexão LinkedIn",
        "cargo_alvo": "Todos",
        "assunto": "Conexão LinkedIn",
        "conteudo": "Olá {primeiro_nome}, notei seu trabalho como {cargo} na {empresa} e gostaria de conectar para compartilhar insights sobre como a IA na Indústria 4.0 está transformando a inspeção de qualidade no setor de {setor}. Abraços!",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar para primeiro contato no LinkedIn"
    },
    {
        "categoria": "Primeira Mensagem",
        "cargo_alvo": "Diretor Industrial",
        "assunto": "IA para Inspeção de Qualidade Industrial",
        "conteudo": "Olá {primeiro_nome}, obrigado por aceitar minha conexão! Como mencionei, trabalho com sistemas de visão computacional com IA para inspeção de qualidade industrial. Nossa solução já ajudou empresas de {setor} a reduzir custos fixos em 75% e economizar milhões anualmente. O diferencial é a integração completa com o parque industrial existente, identificando trincas, amassados e riscos em tempo real. Seria interessante conversar sobre como isso poderia ser aplicado na {empresa}?",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar após aceite de conexão para Diretores Industriais"
    },
    {
        "categoria": "Primeira Mensagem",
        "cargo_alvo": "CEO",
        "assunto": "Redução de Custos com IA Industrial",
        "conteudo": "Olá {primeiro_nome}, agradeço a conexão! Lidero uma empresa de tecnologia especializada em sistemas de visão computacional com IA para inspeção de qualidade industrial. Um de nossos clientes do setor de {setor} conseguiu economizar R$ 5,3 milhões/ano ao identificar peças com defeitos para retrabalho antes que chegassem ao cliente final. Nossa tecnologia se integra ao parque industrial existente, sem grandes modificações na linha. Podemos conversar sobre como isso poderia impactar positivamente os resultados da {empresa}?",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar após aceite de conexão para CEOs, focando em resultados financeiros"
    },
    {
        "categoria": "Follow-up",
        "cargo_alvo": "Todos",
        "assunto": "Case de Sucesso: Economia de R$ 5,3 milhões com IA",
        "conteudo": "Olá {primeiro_nome}, espero que esteja bem! Gostaria de compartilhar um caso de sucesso recente onde nossa solução de IA para inspeção visual ajudou uma empresa do setor de {setor} a economizar R$ 5,3 milhões por ano ao identificar peças com defeitos para retrabalho. Teria interesse em uma breve demonstração de como funciona?",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Usar como primeiro follow-up após alguns dias sem resposta"
    },
    {
        "categoria": "Email",
        "cargo_alvo": "Gerente de Qualidade",
        "assunto": "Solução para padronização de inspeção de qualidade",
        "conteudo": "Prezado(a) {primeiro_nome},\n\nEspero que esteja bem.\n\nEstou entrando em contato porque nossa empresa desenvolveu uma solução de visão computacional com IA que está ajudando indústrias do setor de {setor} a padronizar seus processos de inspeção de qualidade, eliminando a subjetividade e reduzindo a dependência de mão de obra especializada.\n\nO sistema identifica automaticamente trincas, amassados, riscos e outros defeitos em tempo real, com precisão superior a 99,5%, e se integra facilmente ao parque industrial existente.\n\nGostaria de agendar uma breve demonstração online de 20 minutos para mostrar como funciona?\n\nAtenciosamente,\n[Seu Nome]",
        "variaveis": "{primeiro_nome}, {cargo}, {empresa}, {setor}",
        "notas_uso": "Email inicial para Gerentes de Qualidade, focando na padronização"
    }
]

def gerar_email(nome, empresa):
    """Gera um email fictício baseado no nome e empresa."""
    primeiro_nome = nome.split()[0].lower()
    sobrenome = nome.split()[-1].lower()
    empresa_simplificada = empresa.split()[0].lower()
    
    domínios = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com.br", "uol.com.br"]
    domínio_corporativo = f"{empresa_simplificada}.com.br"
    
    # 70% de chance de ser email corporativo
    if random.random() < 0.7:
        return f"{primeiro_nome}.{sobrenome}@{domínio_corporativo}"
    else:
        return f"{primeiro_nome}.{sobrenome}@{random.choice(domínios)}"

def gerar_linkedin_url(nome):
    """Gera uma URL de LinkedIn fictícia baseada no nome."""
    nome_formatado = nome.lower().replace(" ", "-")
    return f"https://www.linkedin.com/in/{nome_formatado}-{random.randint(100, 999)}"

def gerar_telefone():
    """Gera um número de telefone fictício no formato brasileiro."""
    ddd = random.randint(11, 99)
    numero = random.randint(10000000, 99999999)
    return f"({ddd}) 9{numero}"

def criar_dados_teste():
    """Cria dados de teste no banco de dados."""
    app = create_app() 
    with app.app_context():
        # Criar usuário de teste
        if not User.query.filter_by(username="admin").first():
            user = User(username="admin", email="admin@exemplo.com")
            db.session.add(user)
            db.session.commit()
            print("Usuário de teste criado.")
        
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
            
            # Última interação (se houver)
            ultima_interacao = None
            if status != "Novo" and random.random() < 0.8:
                dias_desde_adicao = random.randint(1, dias_atras)
                ultima_interacao = data_adicao + timedelta(days=dias_desde_adicao)
            
            # Próxima ação (se aplicável)
            proxima_acao = None
            data_proxima_acao = None
            if status in ["Conectado", "Conversando", "Reunião Agendada", "Proposta Enviada", "Negociação"]:
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
        
        # Criar interações de teste
        interacoes_criadas = 0
        for lead in leads_criados:
            # Pular leads novos
            if lead.status == "Novo":
                continue
                
            # Número de interações baseado no status
            num_interacoes = {
                "Conectado": random.randint(1, 2),
                "Conversando": random.randint(2, 4),
                "Reunião Agendada": random.randint(3, 5),
                "Proposta Enviada": random.randint(4, 6),
                "Negociação": random.randint(5, 8),
                "Cliente": random.randint(6, 10),
                "Perdido": random.randint(3, 6)
            }.get(lead.status, 0)
            
            for i in range(num_interacoes):
                tipo = random.choice(TIPOS_INTERACAO)
                
                # Data da interação
                if lead.last_interaction_date:
                    data_base = lead.last_interaction_date
                else:
                    data_base = lead.added_date
                    
                dias_apos_base = random.randint(1, 10)
                data_interacao = data_base + timedelta(days=i * dias_apos_base)
                
                # Conteúdo baseado no tipo
                if tipo == "Conexão LinkedIn":
                    conteudo = "Solicitação de conexão enviada no LinkedIn."
                elif tipo == "Mensagem LinkedIn":
                    conteudo = random.choice([
                        "Enviada mensagem apresentando a solução de IA para inspeção visual.",
                        "Compartilhado case de sucesso sobre economia de R$ 5,3 milhões/ano.",
                        "Enviado artigo sobre IA na Indústria 4.0 aplicada à inspeção de qualidade."
                    ])
                elif tipo == "Email":
                    conteudo = random.choice([
                        "Email com apresentação detalhada da solução.",
                        "Email de follow-up após contato inicial.",
                        "Email com proposta comercial personalizada.",
                        "Email agradecendo pela reunião e enviando materiais adicionais."
                    ])
                elif tipo == "Ligação":
                    conteudo = random.choice([
                        "Ligação para apresentação inicial da solução.",
                        "Ligação de follow-up após envio de materiais.",
                        "Conversa sobre necessidades específicas e pontos de dor.",
                        "Discussão sobre próximos passos e agendamento de demonstração."
                    ])
                else:  # Reunião
                    conteudo = random.choice([
                        "Reunião inicial de apresentação da solução.",
                        "Demonstração técnica da plataforma de IA.",
                        "Reunião com equipe técnica para discutir integração.",
                        "Apresentação de proposta comercial e ROI esperado."
                    ])
                
                # Resposta (mais provável em estágios avançados)
                probabilidade_resposta = {
                    "Conectado": 0.3,
                    "Conversando": 0.6,
                    "Reunião Agendada": 0.8,
                    "Proposta Enviada": 0.9,
                    "Negociação": 0.95,
                    "Cliente": 1.0,
                    "Perdido": 0.4
                }.get(lead.status, 0.2)
                
                resposta = random.random() < probabilidade_resposta
                
                # Resultado (mais positivo em estágios avançados)
                if lead.status in ["Cliente", "Negociação", "Proposta Enviada"]:
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
                
                # Próximo passo
                proximo_passo = random.choice(PROXIMOS_PASSOS)
                dias_futuro = random.randint(1, 14)
                data_proximo_passo = data_interacao + timedelta(days=dias_futuro)
                
                # Notas
                notas = ""
                if resposta:
                    if resultado == "Positivo":
                        notas = random.choice([
                            "Demonstrou interesse na solução. Mencionou problemas com inspeção manual.",
                            "Muito receptivo. Solicitou mais informações sobre casos de sucesso.",
                            "Comentou sobre dificuldades em encontrar mão de obra qualificada para inspeção.",
                            "Interessado na redução de custos e aumento de precisão."
                        ])
                    elif resultado == "Neutro":
                        notas = random.choice([
                            "Pediu para entrar em contato novamente em algumas semanas.",
                            "Está avaliando outras soluções no momento.",
                            "Interessado, mas sem orçamento no momento.",
                            "Solicitou mais informações técnicas para avaliar."
                        ])
                    else:
                        notas = random.choice([
                            "Não vê aplicação imediata na empresa.",
                            "Já utiliza outra solução semelhante.",
                            "Sem interesse no momento devido a restrições orçamentárias.",
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
        print(f"{interacoes_criadas} interações de teste criadas.")
        
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
                        f"Agendar demonstração com {lead.name}",
                        f"Verificar interesse de {lead.name} na solução",
                        f"Compartilhar case de sucesso com {lead.name}"
                    ])
                    
                    descricao = random.choice([
                        "Enviar email de follow-up com materiais adicionais.",
                        "Ligar para verificar recebimento da proposta.",
                        "Enviar mensagem no LinkedIn com novo case de sucesso.",
                        "Agendar reunião para apresentação técnica.",
                        "Verificar feedback sobre materiais enviados anteriormente."
                    ])
                    
                    lembrete = Reminder(
                        lead_id=lead.id,
                        user_id=1,  # ID do usuário admin
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
