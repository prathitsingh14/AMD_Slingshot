#!/bin/bash
# UrbanAI — AMD ROCm 7 Setup Script
# Run this on a machine with AMD Instinct MI300X / Radeon AI Pro R9700
# Tested on Ubuntu 22.04 LTS

set -e
echo "🔴 UrbanAI AMD ROCm Setup"
echo "========================="

# 1. Install ROCm 7
echo "[1/6] Installing AMD ROCm 7..."
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | sudo apt-key add -
echo "deb [arch=amd64] https://repo.radeon.com/rocm/apt/6.1 jammy main" | \
    sudo tee /etc/apt/sources.list.d/rocm.list
sudo apt-get update -q
sudo apt-get install -y rocm-dev rocm-libs miopen-hip

# 2. Verify ROCm
echo "[2/6] Verifying ROCm installation..."
rocminfo | grep "Agent Type" || echo "ROCm installed but GPU not detected. Check hardware."

# 3. Install PyTorch with ROCm
echo "[3/6] Installing PyTorch (ROCm backend)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1

# 4. Verify PyTorch GPU access
python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'ROCm/CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
"

# 5. Install vLLM (AMD ROCm build)
echo "[4/6] Installing vLLM with ROCm support..."
pip install vllm --extra-index-url https://download.pytorch.org/whl/rocm6.1

# 6. Install AMD Quark (FP8 quantization)
echo "[5/6] Installing AMD Quark quantization toolkit..."
pip install quark --extra-index-url https://pypi.amd.com/simple

# 7. Install remaining requirements
echo "[6/6] Installing UrbanAI requirements..."
pip install -r requirements.txt

echo ""
echo "✅ AMD ROCm setup complete!"
echo ""
echo "Next steps:"
echo "  1. cp config/example.env .env"
echo "  2. Edit .env with your sensor endpoints"
echo "  3. docker-compose up -d  (starts Qdrant + Redis + PostgreSQL)"
echo "  4. uvicorn api.main:app --reload"
echo "  5. cd dashboard && npm install && npm start"
echo ""
echo "Start vLLM server (AMD GPU):"
echo "  python -m vllm.entrypoints.openai.api_server \\"
echo "    --model meta-llama/Llama-3.1-8B-Instruct \\"
echo "    --port 8001 \\"
echo "    --dtype float16"
