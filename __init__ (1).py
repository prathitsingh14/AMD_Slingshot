# UrbanAI Requirements
# Install with: pip install -r requirements.txt
# For ROCm/AMD: ensure ROCm 7+ is installed before pip install torch

# === Core AI / ML ===
torch>=2.3.0          # ROCm-compatible: install via https://pytorch.org with ROCm flag
torchvision>=0.18.0
transformers>=4.41.0
accelerate>=0.30.0
vllm>=0.4.2           # LLM serving (ROCm support in v0.4+)
langchain>=0.2.0
langchain-community>=0.2.0
llama-index>=0.10.0

# === AMD Quark (quantization) ===
# Install from AMD repo: pip install amd-quark
# See: https://quark.docs.amd.com

# === Vector DB / RAG ===
qdrant-client>=1.9.0
sentence-transformers>=3.0.0
faiss-cpu>=1.8.0       # swap for faiss-gpu on ROCm builds

# === Data & ML ===
numpy>=1.26.0
pandas>=2.2.0
scikit-learn>=1.4.0
xgboost>=2.0.0
scipy>=1.13.0
statsmodels>=0.14.0

# === Computer Vision (Footfall) ===
ultralytics>=8.2.0    # YOLOv8
opencv-python>=4.9.0
Pillow>=10.3.0

# === Geospatial ===
geopandas>=0.14.0
shapely>=2.0.0
pyproj>=3.6.0
folium>=0.16.0
rasterio>=1.3.0       # satellite/drone imagery

# === IoT / Sensor Connectors ===
paho-mqtt>=2.0.0      # MQTT for IoT sensors
influxdb-client>=1.43.0
asyncio-mqtt>=0.16.0

# === API ===
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
python-dotenv>=1.0.0
httpx>=0.27.0

# === Monitoring & Eval ===
mlflow>=2.13.0
prometheus-client>=0.20.0
pytest>=8.2.0
pytest-asyncio>=0.23.0

# === Utilities ===
loguru>=0.7.0
rich>=13.7.0
typer>=0.12.0
python-jose>=3.3.0    # JWT auth
passlib>=1.7.4
