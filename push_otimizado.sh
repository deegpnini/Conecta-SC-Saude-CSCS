#!/bin/bash

echo "============================================================"
echo "📤 PUSH OTIMIZADO - REDE INSTÁVEL"
echo "============================================================"

# Configurações otimizadas
git config --global http.postBuffer 524288000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999

# Tentar múltiplas vezes
MAX_TENTATIVAS=5
TENTATIVA=1

while [ $TENTATIVA -le $MAX_TENTATIVAS ]; do
    echo ""
    echo "📤 Tentativa $TENTATIVA de $MAX_TENTATIVAS..."
    
    # Tentar HTTPS primeiro
    git push origin --force main 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Branch main enviado com sucesso!"
        break
    else
        echo "⚠️ Falha na tentativa $TENTATIVA"
        if [ $TENTATIVA -lt $MAX_TENTATIVAS ]; then
            echo "⏳ Aguardando $(($TENTATIVA * 5)) segundos antes de tentar novamente..."
            sleep $(($TENTATIVA * 5))
        fi
    fi
    
    TENTATIVA=$((TENTATIVA + 1))
done

# Enviar tags
echo ""
echo "📤 Enviando tags..."
TENTATIVA=1
while [ $TENTATIVA -le $MAX_TENTATIVAS ]; do
    echo "📤 Tentativa $TENTATIVA de $MAX_TENTATIVAS para tags..."
    
    git push origin --force --tags 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Tags enviadas com sucesso!"
        break
    else
        echo "⚠️ Falha na tentativa $TENTATIVA"
        if [ $TENTATIVA -lt $MAX_TENTATIVAS ]; then
            echo "⏳ Aguardando $(($TENTATIVA * 5)) segundos..."
            sleep $(($TENTATIVA * 5))
        fi
    fi
    
    TENTATIVA=$((TENTATIVA + 1))
done

echo ""
echo "============================================================"
echo "✅ PUSH FINALIZADO"
echo "============================================================"
echo ""
echo "🔗 Verifique: https://github.com/deegpnini/Conecta-SC-Saude-CSCS"
