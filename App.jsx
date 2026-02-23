# UrbanAI Environment Configuration
# Copy to .env and fill in your values

# === LLM Backend ===
LLM_MODEL=meta-llama/Llama-3.1-8B-Instruct
LLM_BASE_URL=http://localhost:8001/v1   # vLLM server endpoint
LLM_API_KEY=your_vllm_api_key_here
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.1

# === AMD / ROCm ===
HIP_VISIBLE_DEVICES=0,1               # GPU device IDs
ROCM_HOME=/opt/rocm
AMD_QUARK_QUANTIZE=true               # enable FP8 quantization
AMD_QUARK_DTYPE=fp8                   # fp4 | fp8 | int8

# === Vector Database (Qdrant) ===
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=urbanai_knowledge

# === IoT / MQTT ===
MQTT_BROKER=mqtt.campus.local
MQTT_PORT=1883
MQTT_USERNAME=urbanai
MQTT_PASSWORD=your_mqtt_password

# === InfluxDB (time-series sensor data) ===
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=your_influx_token
INFLUX_ORG=urbanai
INFLUX_BUCKET=sensors

# === GIS / Mapping ===
ARCGIS_API_KEY=your_arcgis_key
MAPBOX_TOKEN=your_mapbox_token
CAMPUS_BOUNDS_LAT=28.6139            # center lat of campus/city
CAMPUS_BOUNDS_LNG=77.2090            # center lng

# === Camera / CCTV Streams (Footfall) ===
RTSP_STREAMS=rtsp://cam1.local/stream,rtsp://cam2.local/stream
FOOTFALL_MODEL_PATH=models/footfall/weights/yolov8_footfall.pt

# === Database ===
DATABASE_URL=postgresql://urbanai:password@localhost:5432/urbanai
REDIS_URL=redis://localhost:6379

# === API ===
API_SECRET_KEY=your_super_secret_key_here
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,https://your-dashboard.com

# === MLflow ===
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=urbanai_training

# === Logging ===
LOG_LEVEL=INFO
LOG_FILE=logs/urbanai.log
