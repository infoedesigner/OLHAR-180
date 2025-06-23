GENDER_CHOICES = [
    (v, v) for v in [
        'Masculino', 'Feminino', 'Não informado'
    ]
]

STATE_CHOICES = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AM", "Amazonas"),
    ("AP", "Amapá"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MG", "Minas Gerais"),
    ("MS", "Mato Grosso do Sul"),
    ("MT", "Mato Grosso"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("PR", "Paraná"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("RS", "Rio Grande do Sul"),
    ("SC", "Santa Catarina"),
    ("SE", "Sergipe"),
    ("SP", "São Paulo"),
    ("TO", "Tocantins"),
]


DAY_CHOICES = [
    (1, 'Segunda-feira'),
    (2, 'Terça-feira'),
    (3, 'Quarta-feira'),
    (4, 'Quinta-feira'),
    (5, 'Sexta-feira'),
    (6, 'Sábado'),
    (7, 'Domingo'),
]

FREQUENCY_CHOICES = [
    (v, v) for v in (
        'Diário', 'Semanal', 'Quinzenal', 'Mensal', 'Bimestral', 'Trimestral', 'Semestral', 'Anual'
    )
]

MARITAL_STATUS_CHOICES = [
    (v, v) for v in [
        'Solteiro(a)', 'Casado(a)', 'Separado(a) judicialmente',
        'Divorciado(a)', 'Viúvo(a)', 'União Estável', 'Outro'
    ]
]

PIX_KEY_TYPE_CHOICES = [
    (v, v) for v in ['Celular', 'CPF', 'E-mail', 'Aleatória']
]

DEGREE_CHOICES = [
    (v, v) for v in [
        'Analfabeto', 'Fundamental incompleto', 'Fundamental completo', 'Médio incompleto', 'Médio completo',
        'Superior incompleto', 'Superior completo', 'Especialização incompleta', 'Especialização completa',
        'Mestrado incompleto', 'Mestrado completo', 'Doutorado incompleto', 'Doutorado completo',
    ]
]

DOCUMENT_TYPE_CHOICES = [
    (v, v) for v in [
        'Alvará de funcionamento',
        'Balanço',
        'Certidão de Falência e Concordata',
        'Certidão do CNJ',
        'Certidão Estadual',
        'Certidão GDF - Juntos a Orgãos Públicos',
        'Certidão GDF - Juntos ao GDF',
        'Certidão Municipal',
        'Certidão Simplificada - Junta Comercial',
        'Certidão Trabalhista GDF',
        'CND Receita Federal / PREVI - Certidão Negativa de Débitos',
        'CNDT - Certidão Negativa de Débitos Trabalhistas',
        'CNPJ - Cadastro de Pessoa Jurídica',
        'Comprovante de pagamentos dos funcionários',
        'Consulta de Opção do Simples Nacional',
        'Contrato Social',
        'Contratos com fornecedores',
        'CRF - Certificado de Regularidade do FGTS',
        'Documentação dos Sócios',
        'EPP',
        'Imposto de renda PJ',
        'Inscrição Estadual',
        'Jornalista',
        'Marketing',
        'Portal Transparência',
        'SICAF - Declaração de Situação de Cadastro',
        'SIMPLES - Termo de Deferimento da Opção pelo Simples Nacional',
        'TCU',
        'Termo de abertura e encerramento',
    ]
]

DATE_XPATH_CHOICES = [
    ('d/m/Y', 'DD/MM/AAAA'),
    ('d/m/y', 'DD/MM/AA'),
    ('l, d \d\e F \d\e Y, H:i', 'D. Semana, D de M de A, H:m'),
    ('l, d \d\e F \d\e Y', 'D. Semana, D de M de A'),
    ('d/m/Y \à\s H:i', 'DD/MM/AAAA às H:m'),
    ('d/m/Y H:i', 'DD/MM/AAAA H:m'),
]


RATING_CHOICES = [
    (v, v) for v in ['Positiva', 'Negativa', 'Neutra']
]

MENTION_CHOICES = [
    (v, v) for v in ['Direta', 'Indireta']
]

NOTIFICATION_TYPE_CHOICES = [
    (v, v) for v in ('Newsletter', 'Recuperação de Senha', 'Validação de Senha')
]

EVALUATION_CHOICES = [
    (v, v) for v in ('Avaliadas', 'Não Avaliadas', 'Destaques', 'Não Aprovadas')
]

SEGMENTATION_CHOICES = [
    (v, v) for v in [
        'Sem segmentação',
        'Segmentado por veículo',
        'Segmentado por categoria',
        'Segmentado por mídia',
        'Segmentado por categoria/veículo',
        'Segmentado por categoria/mídia/veículo',
        'Segmentado por veículo/categoria',
        'Segmentado por mídia/veículo',
        'Segmentado por mídia/veículo/categoria',
        'Segmentado por mídia/categoria/veículo',
    ]
]

NEWS_LAYOUT_CHOICES = [
    (v, v) for v in [
        'Categoria',
        'Data da notícia',
        'Data da notícia - Decrescente',
        'Data de cadastro',
        'Data de cadastro - Decrescente',
        'Mídia » Veículo » Página » Data de cadastro',
    ]
]

NEWSLETTER_LAYOUT_CHOICES = [
    (v, v) for v in [
        'BÁSICO',
        'CATEGORIA COM CORES PERSONALIZADAS',
        'PERSONALIZADO',
        'REDES SOCIAIS',
    ]
]


EMAIL_STATUS_CHOICES = [
    ('pending', 'Pendente'),
    ('sent', 'Enviado'),
    ('refused', 'Rejeitado'),
]
