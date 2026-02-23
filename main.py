"""
Waste Predictor — Biodegradable waste generation forecasting + biogas yield estimation
"""

import numpy as np
from datetime import datetime, timedelta
from loguru import logger


class WastePredictor:
    """Predicts waste generation and recommends biodegradable processing strategies."""
    
    AREA_PROFILES = {
        "cafeteria": {"daily_kg_baseline": 250, "biodegradable_pct": 0.78},
        "hostels": {"daily_kg_baseline": 180, "biodegradable_pct": 0.65},
        "academic_block": {"daily_kg_baseline": 40, "biodegradable_pct": 0.45},
        "sports_complex": {"daily_kg_baseline": 30, "biodegradable_pct": 0.55},
        "campus_wide": {"daily_kg_baseline": 600, "biodegradable_pct": 0.68},
    }
    
    # Biogas conversion: ~0.4 m³ methane per kg biodegradable waste
    BIOGAS_YIELD_M3_PER_KG = 0.4

    def __init__(self):
        logger.info("WastePredictor initialized")

    @classmethod
    def load_default(cls) -> "WastePredictor":
        return cls()

    def predict(self, area: str, waste_type: str = "biodegradable", days: int = 7) -> dict:
        profile = self.AREA_PROFILES.get(area.lower().replace(" ", "_"), 
                                          self.AREA_PROFILES["campus_wide"])
        now = datetime.now()
        
        daily_forecasts = []
        total_waste = 0
        total_biodegradable = 0
        
        for d in range(days):
            date = now + timedelta(days=d)
            is_weekend = date.weekday() >= 5
            
            # Weekend adjustment: 60% of weekday waste
            multiplier = 0.6 if is_weekend else 1.0
            # Small random variation
            daily_total = profile["daily_kg_baseline"] * multiplier * (1 + np.random.normal(0, 0.08))
            daily_bio = daily_total * profile["biodegradable_pct"]
            biogas = daily_bio * self.BIOGAS_YIELD_M3_PER_KG
            
            total_waste += daily_total
            total_biodegradable += daily_bio
            
            daily_forecasts.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%A"),
                "total_waste_kg": round(daily_total, 1),
                "biodegradable_kg": round(daily_bio, 1),
                "recyclable_kg": round(daily_total * 0.20, 1),
                "residual_kg": round(daily_total * 0.12, 1),
                "biogas_yield_m3": round(biogas, 2),
                "biogas_energy_kwh": round(biogas * 5.5, 2),  # ~5.5 kWh per m³ biogas
            })
        
        total_biogas = total_biodegradable * self.BIOGAS_YIELD_M3_PER_KG
        
        return {
            "area": area,
            "waste_type": waste_type,
            "forecast_days": days,
            "summary": {
                "total_waste_kg": round(total_waste, 1),
                "total_biodegradable_kg": round(total_biodegradable, 1),
                "biodegradable_percentage": round(profile["biodegradable_pct"] * 100, 1),
                "total_biogas_m3": round(total_biogas, 1),
                "total_energy_kwh": round(total_biogas * 5.5, 1),
                "co2_offset_kg": round(total_biogas * 1.9, 1),
            },
            "daily_forecasts": daily_forecasts,
            "recommendations": self._recommendations(total_biodegradable, area),
            "collection_schedule": self._optimize_collection_schedule(daily_forecasts),
        }

    def _recommendations(self, total_bio_kg: float, area: str) -> list[str]:
        recs = [
            f"♻️ Install biodigester rated for {total_bio_kg/7:.0f} kg/day minimum capacity.",
            f"⚡ Estimated energy recovery: {total_bio_kg * self.BIOGAS_YIELD_M3_PER_KG * 5.5 / 7:.0f} kWh/day — can power campus street lighting.",
            "🌱 Composting secondary stream can generate ~2 tons of fertilizer monthly for campus gardens.",
            f"📉 Segregation at source (cafeteria, hostels) can increase biodegradable recovery by 20-25%.",
            "🔬 Deploy IoT-enabled smart bins with fill-level sensors for dynamic collection scheduling.",
        ]
        return recs

    def _optimize_collection_schedule(self, forecasts: list) -> list[dict]:
        schedule = []
        for f in forecasts:
            # Collect on high-waste days more frequently
            if f["total_waste_kg"] > 400:
                frequency = "2x daily"
            elif f["total_waste_kg"] > 200:
                frequency = "Daily"
            else:
                frequency = "Every 2 days"
            schedule.append({"date": f["date"], "collection_frequency": frequency,
                             "priority": "HIGH" if f["total_waste_kg"] > 400 else "NORMAL"})
        return schedule
