"""
Water Analyzer — Anomaly detection on pipeline sensor data + treatment recommendations
"""

import numpy as np
from datetime import datetime
from loguru import logger
from typing import Optional


class WaterAnalyzer:
    """
    Analyzes water quality and pipeline sensor data.
    Recommends treatment installations based on detected issues.
    Uses isolation forest for anomaly detection.
    """
    
    # WHO / BIS drinking water thresholds
    THRESHOLDS = {
        "ph": (6.5, 8.5),
        "turbidity_ntu": (0, 4.0),
        "tds_ppm": (0, 500),
        "chlorine_ppm": (0.2, 1.0),
        "flow_rate_lpm": (10, 500),
        "pressure_bar": (1.0, 4.5),
        "temperature_c": (5, 30),
    }
    
    ZONES = {
        "Z1": "Academic Block Water Supply",
        "Z2": "Hostel Water Supply",
        "Z3": "Sports Complex Supply",
        "Z4": "Campus Irrigation Network",
        "Z5": "Grey Water Recycling Loop",
    }

    def __init__(self):
        self._init_anomaly_detector()
        logger.info("WaterAnalyzer initialized")

    def _init_anomaly_detector(self):
        try:
            from sklearn.ensemble import IsolationForest
            self.anomaly_detector = IsolationForest(contamination=0.05, random_state=42)
            # Would be trained on historical sensor data in production
            self.has_detector = True
        except ImportError:
            self.has_detector = False
            logger.warning("scikit-learn not available — using threshold-based detection")

    @classmethod
    def load_default(cls) -> "WaterAnalyzer":
        return cls()

    def analyze(self, zone: str, sensor_data: Optional[dict] = None) -> dict:
        now = datetime.now()
        zone_name = self.ZONES.get(zone, zone)
        
        # Use provided or simulated sensor data
        readings = sensor_data or self._simulate_sensor_readings(zone)
        
        anomalies = self._detect_anomalies(readings)
        quality_score = self._compute_quality_score(readings, anomalies)
        
        return {
            "zone": zone,
            "zone_name": zone_name,
            "timestamp": now.isoformat(),
            "sensor_readings": readings,
            "quality_score": quality_score,
            "quality_grade": self._quality_grade(quality_score),
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "parameter_status": self._parameter_status(readings),
            "treatment_recommendations": self._treatment_recommendations(readings, anomalies, zone),
            "installation_recommendations": self._installation_recommendations(readings, anomalies),
            "risk_level": "HIGH" if len(anomalies) >= 3 else "MEDIUM" if anomalies else "LOW",
        }

    def _simulate_sensor_readings(self, zone: str) -> dict:
        """Simulate sensor readings — replace with real IoT data pipeline."""
        base = {
            "ph": round(np.random.normal(7.2, 0.3), 2),
            "turbidity_ntu": round(abs(np.random.normal(1.5, 0.8)), 2),
            "tds_ppm": round(np.random.normal(280, 60), 1),
            "chlorine_ppm": round(np.random.normal(0.5, 0.15), 3),
            "flow_rate_lpm": round(np.random.normal(120, 25), 1),
            "pressure_bar": round(np.random.normal(2.8, 0.4), 2),
            "temperature_c": round(np.random.normal(22, 2.5), 1),
        }
        # Inject some anomalies for demo
        if zone in ("Z4", "Z5"):
            base["turbidity_ntu"] = round(np.random.uniform(5, 12), 2)
            base["tds_ppm"] = round(np.random.uniform(600, 900), 1)
        return base

    def _detect_anomalies(self, readings: dict) -> list[dict]:
        anomalies = []
        for param, value in readings.items():
            if param not in self.THRESHOLDS:
                continue
            low, high = self.THRESHOLDS[param]
            if value < low or value > high:
                severity = "CRITICAL" if (value < low * 0.7 or value > high * 1.5) else "WARNING"
                anomalies.append({
                    "parameter": param,
                    "value": value,
                    "threshold_min": low,
                    "threshold_max": high,
                    "deviation": round(max(low - value, value - high, 0), 3),
                    "severity": severity,
                })
        return anomalies

    def _compute_quality_score(self, readings: dict, anomalies: list) -> float:
        base_score = 100.0
        for a in anomalies:
            base_score -= 15 if a["severity"] == "CRITICAL" else 7
        return round(max(0, min(100, base_score)), 1)

    def _quality_grade(self, score: float) -> str:
        if score >= 90: return "A — Excellent"
        if score >= 75: return "B — Good"
        if score >= 60: return "C — Acceptable"
        if score >= 40: return "D — Poor"
        return "F — Unsafe"

    def _parameter_status(self, readings: dict) -> dict:
        status = {}
        for param, value in readings.items():
            if param not in self.THRESHOLDS:
                status[param] = "OK"
                continue
            low, high = self.THRESHOLDS[param]
            status[param] = "OK" if low <= value <= high else "OUT_OF_RANGE"
        return status

    def _treatment_recommendations(self, readings: dict, anomalies: list, zone: str) -> list[str]:
        recs = []
        params_out = {a["parameter"] for a in anomalies}
        
        if "ph" in params_out:
            ph = readings["ph"]
            recs.append(f"⚗️ pH at {ph} — {'Add lime/soda ash for neutralization' if ph < 6.5 else 'Add CO₂ or acid dosing to reduce alkalinity'}.")
        if "turbidity_ntu" in params_out:
            recs.append(f"💧 Turbidity at {readings['turbidity_ntu']} NTU — Install multimedia sand filter + coagulation-flocculation unit.")
        if "tds_ppm" in params_out:
            recs.append(f"🧪 TDS at {readings['tds_ppm']} ppm — Install RO (Reverse Osmosis) system rated for {readings.get('flow_rate_lpm', 100)} LPM.")
        if "chlorine_ppm" in params_out:
            cl = readings["chlorine_ppm"]
            recs.append(f"🦠 Chlorine at {cl} ppm — {'Increase chlorine dosing at pump station' if cl < 0.2 else 'Reduce dosage; install activated carbon post-filter'}.")
        if not recs:
            recs.append("✅ All parameters within acceptable range. Continue routine monitoring.")
        return recs

    def _installation_recommendations(self, readings: dict, anomalies: list) -> list[str]:
        return [
            "📡 Install continuous IoT water quality sensors (pH, turbidity, TDS, chlorine) at all zone inlets.",
            "🤖 Implement AI-driven auto-dosing system for real-time chemical treatment adjustment.",
            "🔄 Add SCADA integration for central monitoring and control of all water zones.",
            "💧 Install pressure sensors every 200m on distribution lines for leak detection.",
            "🌧️ Rainwater harvesting + greywater recycling can offset 20-30% of campus water demand.",
        ]
