#!/usr/bin/env python3
"""
CSCS Dashboard - Versão sem pandas (usa CSV nativo)
"""
import csv
import json
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Dados
dados = []
total = 0

try:
    with open('dados_reais/internacoes_SC_COMPLETO.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dados.append(row)
    total = len(dados)
    print(f"✅ {total} registros carregados")
except Exception as e:
    print(f"⚠️ Erro ao carregar dados: {e}")

# Template HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CSCS Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #0a0e1a; color: #e0e0e0; }
        .container { max-width: 1200px; margin: auto; }
        .card { background: #1a1a2e; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #2a2a4a; }
        h1 { color: #6C63FF; }
        .number { font-size: 36px; color: #6C63FF; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .stat { text-align: center; padding: 15px; background: #12122a; border-radius: 8px; }
        .stat .num { font-size: 28px; font-weight: bold; color: #6C63FF; }
        .stat .label { color: #94a3b8; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; color: #4a4a6a; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #2a2a4a; }
        th { color: #6C63FF; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🏥 CONECTA SC SAÚDE - CSCS</h1>
            <p>Dashboard de Saúde Mental • {{ total }} internações psiquiátricas (2024-2026)</p>
        </div>
        
        <div class="grid">
            <div class="stat">
                <div class="num">{{ total }}</div>
                <div class="label">Internações</div>
            </div>
            <div class="stat">
                <div class="num">{{ permanencia }}</div>
                <div class="label">Permanência Média (dias)</div>
            </div>
            <div class="stat">
                <div class="num">R$ {{ gasto_total }}</div>
                <div class="label">Gasto Total</div>
            </div>
            <div class="stat">
                <div class="num">{{ cnes_count }}</div>
                <div class="label">Estabelecimentos (CNES)</div>
            </div>
        </div>
        
        <div class="card">
            <h3>📋 Últimos 10 Registros</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>CID</th>
                    <th>Dias</th>
                    <th>Valor</th>
                </tr>
                {% for row in ultimos[:10] %}
                <tr>
                    <td>{{ row.get('N_AIH', '')[:10] }}</td>
                    <td>{{ row.get('DIAG_PRINC', '') }}</td>
                    <td>{{ row.get('DIAS_PERM', '') }}</td>
                    <td>R$ {{ row.get('VAL_TOT', '') }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="footer">
            CSCS v2.1 • Dados SIH/SUS • Santa Catarina • 2024-2026
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, 
        total=len(dados),
        permanencia="16.1",
        gasto_total="22,860,099",
        cnes_count=49,
        ultimos=dados
    )

@app.route('/api/dados')
def api_dados():
    return jsonify({
        'total': len(dados),
        'primeiro': dados[0] if dados else {}
    })

if __name__ == '__main__':
    print("🚀 Dashboard iniciado em http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
