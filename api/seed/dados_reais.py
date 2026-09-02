from api.database import get_db_connection
import random

def seed_pacientes():
    with get_db_connection() as conn:
        cur = conn.cursor()

        # Verificar se já existem pacientes
        cur.execute("SELECT COUNT(*) FROM requests")
        if cur.fetchone()[0] > 0:
            print("✅ Pacientes já existem no banco")
            return

        # Pacientes fictícios com dados realistas
        pacientes = [
            {"nome": "Maria Aparecida da Silva", "cpf": "123.456.789-00", "telefone": "(48) 99999-0001", "cidade": "São Ludgero"},
            {"nome": "João Batista dos Santos", "cpf": "987.654.321-00", "telefone": "(48) 99999-0002", "cidade": "Criciúma"},
            {"nome": "Ana Paula Oliveira", "cpf": "456.789.123-00", "telefone": "(48) 99999-0003", "cidade": "Içara"},
            {"nome": "Carlos Alberto Pereira", "cpf": "789.123.456-00", "telefone": "(48) 99999-0004", "cidade": "Florianópolis"},
            {"nome": "Mariana Ferreira", "cpf": "321.654.987-00", "telefone": "(48) 99999-0005", "cidade": "Braço do Norte"},
            {"nome": "Mateus Silva Santos", "cpf": "111.222.333-44", "telefone": "(48) 99999-0006", "cidade": "Balneário Rincão"},
            {"nome": "Carla Mendes", "cpf": "555.666.777-88", "telefone": "(48) 99999-0007", "cidade": "Tubarão"},
            {"nome": "Roberto Nunes", "cpf": "999.888.777-66", "telefone": "(48) 99999-0008", "cidade": "Içara"},
            {"nome": "Patrícia Lopes", "cpf": "111.222.333-55", "telefone": "(48) 99999-0009", "cidade": "Balneário Rincão"},
            {"nome": "Fernando Rocha", "cpf": "444.555.666-77", "telefone": "(48) 99999-0010", "cidade": "Criciúma"},
        ]

        especialidades = ["Psiquiatria", "Cardiologia", "Neurologia", "Ortopedia", "Oncologia", "Clínica Geral"]
        urgencias = ["alta", "media", "baixa"]

        observacoes = [
            "Paciente em crise psicótica aguda, necessita de avaliação psiquiátrica urgente",
            "Paciente com dor torácica intensa, suspeita de infarto",
            "Paciente com cefaleia intensa há 3 dias, necessidade de avaliação neurológica",
            "Paciente com fratura de fêmur, necessita de internação para cirurgia",
            "Paciente com diagnóstico de neoplasia, necessita de quimioterapia",
            "Adolescente com crise de ansiedade grave, necessita acompanhamento",
            "Paciente com ideação suicida, emergência psiquiátrica",
            "Criança com comportamento agressivo, necessita avaliação neuropsiquiátrica",
            "Paciente com hipertensão descontrolada, risco de AVC",
            "Paciente com arritmia cardíaca, necessita avaliação urgente"
        ]

        for p in pacientes:
            especialidade = random.choice(especialidades)
            urgencia = random.choice(urgencias)
            observacao = random.choice(observacoes)

            cur.execute("""
                INSERT INTO requests (patient_name, patient_cpf, patient_phone, specialty, urgency, region, doctor_name, observations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (p["nome"], p["cpf"], p["telefone"], especialidade, urgencia, p["cidade"], "Dr. Carlos Silva", observacao))

        conn.commit()
        print("✅ Pacientes simulados carregados com sucesso!")
