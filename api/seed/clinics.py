from api.database import get_db_connection

def seed_clinics():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM clinics")
        if cur.fetchone()[0] > 0:
            print("✅ Clínicas já existem no banco")
            return

        clinics = [
            # CAPS e Centros Públicos
            {"cnes": "7458169", "name": "CAPS Braço do Norte", "region": "Braço do Norte", 
             "address": "Rua Newton de Andrade Collaço, 2427", "total_beds": 0, "available_beds": 0, 
             "occupancy_rate": 0, "specialties": '["Saúde Mental","Psiquiatria"]', "cnes_verified": 1, "is_example": 0},
             
            {"cnes": "2661365", "name": "CAPS II Tubarão", "region": "Tubarão", 
             "address": "Rua Osvaldo Cruz, 917", "total_beds": 0, "available_beds": 0, 
             "occupancy_rate": 0, "specialties": '["Saúde Mental","Psiquiatria","Transtornos Graves"]', "cnes_verified": 1, "is_example": 0},
             
            {"cnes": "9775390", "name": "Central de Regulação do Acesso", "region": "Balneário Rincão", 
             "address": "Rua das Palmeiras, 150", "total_beds": 0, "available_beds": 0, 
             "occupancy_rate": 0, "specialties": '["Regulação"]', "cnes_verified": 1, "is_example": 0},
             
            {"cnes": "2779129", "name": "UBS Primeiro de Maio", "region": "Içara", 
             "address": "Rua Primeiro de Maio, s/n", "total_beds": 0, "available_beds": 0, 
             "occupancy_rate": 0, "specialties": '["Atenção Primária","Saúde da Família"]', "cnes_verified": 1, "is_example": 0},

            # Hospitais e Clínicas Psiquiátricas
            {"cnes": "IPQ001", "name": "Instituto de Psiquiatria de Santa Catarina (IPq)", "region": "São José", 
             "address": "Av. Engelberto Koerich, 333 - Colônia Santana, São José - SC", "total_beds": 150, "available_beds": 15, 
             "occupancy_rate": 90, "specialties": '["Psiquiatria","Dependência Química","Transtornos Graves","Emergência 24h"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "VIV002", "name": "ViV | Instituto São José", "region": "São José", 
             "address": "R. Antônio Ferreira, 113 - Centro, São José - SC", "total_beds": 30, "available_beds": 5, 
             "occupancy_rate": 83.3, "specialties": '["Psiquiatria","Hospital-Dia","Dependência Química","Pronto Atendimento"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "RIO003", "name": "Casa de Saúde Rio Maina", "region": "Criciúma", 
             "address": "Rodovia Jorge Lacerda, 5000, Criciúma - SC", "total_beds": 80, "available_beds": 12, 
             "occupancy_rate": 85, "specialties": '["Psiquiatria","Internação","Estabilização de Crises","Longo Prazo"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "BEM004", "name": "Bem Viver Centro de Saúde Integrada", "region": "Camboriú", 
             "address": "Av. Santa Catarina, 1112 - Tabuleiro, Camboriú - SC", "total_beds": 20, "available_beds": 3, 
             "occupancy_rate": 85, "specialties": '["Psiquiatria","Plantão 24h","Atenção Integral"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "INJ005", "name": "Instituto de Neurociências Dr. João Quevedo (InJQ)", "region": "Criciúma", 
             "address": "R. Cel. Pedro Benedet, 505 - 104 - Centro, Criciúma - SC", "total_beds": 0, "available_beds": 0, 
             "occupancy_rate": 0, "specialties": '["Neurociências","Psiquiatria","Ambulatorial","Pesquisa"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "GAR006", "name": "Clínica Psiquiátrica Garcia", "region": "Criciúma", 
             "address": "Rua Antônio de Lucca, 165 - Centro, Criciúma - SC", "total_beds": 15, "available_beds": 2, 
             "occupancy_rate": 86.7, "specialties": '["Psiquiatria","Atendimento Clínico"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "HOS007", "name": "Hospital de Custódia Tratamento Psiquiátrico", "region": "Florianópolis", 
             "address": "R. Delminda Silveira, 960 - Agronômica, Florianópolis - SC", "total_beds": 40, "available_beds": 5, 
             "occupancy_rate": 87.5, "specialties": '["Psiquiatria","Custódia Judicial","Tratamento"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "SAN008", "name": "Complexo de Saúde Santo Agostinho", "region": "Criciúma", 
             "address": "R. Luís Pirola de Noé, 150 - Vila Isabel, Criciúma - SC", "total_beds": 25, "available_beds": 4, 
             "occupancy_rate": 84, "specialties": '["Saúde Mental","Terapias","Assistência"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "CON009", "name": "Hospital Nossa Senhora da Conceição", "region": "Urussanga", 
             "address": "Av. Pres. Vargas, 540 - Centro, Urussanga - SC", "total_beds": 40, "available_beds": 7, 
             "occupancy_rate": 82.5, "specialties": '["Clínica Geral","Pronto-Socorro","Saúde"]', "cnes_verified": 0, "is_example": 1},

            # Comunidades Terapêuticas
            {"cnes": "NOV010", "name": "Centro de Reabilitação Psicossocial Novo Amanhecer", "region": "Içara", 
             "address": "SC-443, KM 19 - Linha Anta, Içara - SC", "total_beds": 20, "available_beds": 2, 
             "occupancy_rate": 90, "specialties": '["Dependência Química","Reabilitação","Acompanhamento 24h"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "DES011", "name": "Desafio Jovem de Criciúma SC", "region": "Criciúma", 
             "address": "R. Desafio Jovem, 80 - Recanto Verde, Criciúma - SC", "total_beds": 30, "available_beds": 3, 
             "occupancy_rate": 90, "specialties": '["Reabilitação","Acolhimento","Tratamento"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "CLI012", "name": "Clínica de Reabilitação para Dependentes Químicos", "region": "Balneário Camboriú", 
             "address": "R. 2500, 411 - Centro, Balneário Camboriú - SC", "total_beds": 25, "available_beds": 4, 
             "occupancy_rate": 84, "specialties": '["Dependência Química","Internação","Tratamento"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "REN013", "name": "Comunidade Terapêutica Renascer", "region": "Gravatal", 
             "address": "Estrada Geral do Indaial, s/n° - Indaial, Gravatal - SC", "total_beds": 20, "available_beds": 2, 
             "occupancy_rate": 90, "specialties": '["Comunidade Terapêutica","Ressocialização","Tratamento"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "REC014", "name": "Comunidade Terapêutica Lar Recanto da Esperança", "region": "Florianópolis", 
             "address": "Rod. João Gualberto Soares, 3040 - São João do Rio Vermelho, Florianópolis - SC", "total_beds": 18, "available_beds": 2, 
             "occupancy_rate": 88.9, "specialties": '["Comunidade Terapêutica","Acolhimento","Rotinas Terapêuticas"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "PRA015", "name": "Comunidade Terapêutica Pradda", "region": "Içara", 
             "address": "Rua Santos - R. Augusto C Brunel, 1690 - Liri, Içara - SC", "total_beds": 15, "available_beds": 2, 
             "occupancy_rate": 86.7, "specialties": '["Comunidade Terapêutica","Ressocialização","Tratamento"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "EMA016", "name": "Comunidade Terapêutica Casa Missionária Emanuel", "region": "Içara", 
             "address": "Rodovia ICR 473, s/n - SANTA CRUZ, Içara - SC", "total_beds": 15, "available_beds": 1, 
             "occupancy_rate": 93.3, "specialties": '["Comunidade Terapêutica","Suporte Espiritual","Desintoxicação"]', "cnes_verified": 0, "is_example": 1},
             
            {"cnes": "RES017", "name": "Comunidade Terapêutica Resgatando Esperança", "region": "Içara", 
             "address": "R. Santo Antônio, Casa numero 892 - Esplanada, Içara - SC", "total_beds": 12, "available_beds": 1, 
             "occupancy_rate": 91.7, "specialties": '["Comunidade Terapêutica","Internação","Acompanhamento Comportamental"]', "cnes_verified": 0, "is_example": 1},
        ]

        for c in clinics:
            cur.execute("""
                INSERT INTO clinics (cnes, name, region, address, total_beds, available_beds,
                                     occupancy_rate, specialties, cnes_verified, is_example)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (c["cnes"], c["name"], c["region"], c["address"], c["total_beds"], c["available_beds"],
                  c["occupancy_rate"], c["specialties"], c["cnes_verified"], c["is_example"]))

        conn.commit()
        print(f"✅ {len(clinics)} clínicas carregadas com sucesso!")
