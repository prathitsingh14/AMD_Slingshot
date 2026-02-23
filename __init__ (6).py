"""
Greenery Recommender — Soil analysis + plant suitability recommendation engine
"""

import numpy as np
from loguru import logger
from typing import Optional


# Plant database: suitable for Indian campus environments
PLANT_DATABASE = [
    {
        "id": "neem",
        "name": "Neem (Azadirachta indica)",
        "type": "tree",
        "ph_range": (6.0, 8.5),
        "moisture_range": (30, 70),
        "nitrogen_range": (10, 80),
        "benefits": ["Air purification", "Shade", "Natural pesticide", "Medicinal"],
        "co2_absorption_kg_yr": 22,
        "water_requirement": "Low",
        "growth_rate": "Medium",
        "canopy_radius_m": 8,
    },
    {
        "id": "peepal",
        "name": "Peepal (Ficus religiosa)",
        "type": "tree",
        "ph_range": (5.5, 8.0),
        "moisture_range": (40, 80),
        "nitrogen_range": (20, 100),
        "benefits": ["High oxygen output", "Air purification", "Biodiversity support"],
        "co2_absorption_kg_yr": 28,
        "water_requirement": "Medium",
        "growth_rate": "Fast",
        "canopy_radius_m": 10,
    },
    {
        "id": "bamboo",
        "name": "Golden Bamboo (Phyllostachys aurea)",
        "type": "grass/screen",
        "ph_range": (5.5, 7.5),
        "moisture_range": (50, 90),
        "nitrogen_range": (30, 120),
        "benefits": ["Fast carbon sequestration", "Privacy screen", "Erosion control"],
        "co2_absorption_kg_yr": 35,
        "water_requirement": "Medium",
        "growth_rate": "Very Fast",
        "canopy_radius_m": 2,
    },
    {
        "id": "ashoka",
        "name": "Ashoka (Saraca asoca)",
        "type": "tree",
        "ph_range": (6.0, 7.5),
        "moisture_range": (60, 85),
        "nitrogen_range": (40, 100),
        "benefits": ["Ornamental", "Shade", "Biodiversity", "Avenue planting"],
        "co2_absorption_kg_yr": 18,
        "water_requirement": "Medium",
        "growth_rate": "Slow",
        "canopy_radius_m": 5,
    },
    {
        "id": "bougainvillea",
        "name": "Bougainvillea",
        "type": "climber/shrub",
        "ph_range": (5.5, 7.0),
        "moisture_range": (25, 60),
        "nitrogen_range": (10, 60),
        "benefits": ["Low maintenance", "Erosion control", "Ornamental", "Wall cover"],
        "co2_absorption_kg_yr": 5,
        "water_requirement": "Very Low",
        "growth_rate": "Fast",
        "canopy_radius_m": 3,
    },
    {
        "id": "tulsi",
        "name": "Holy Basil / Tulsi (Ocimum tenuiflorum)",
        "type": "herb",
        "ph_range": (6.0, 7.5),
        "moisture_range": (40, 70),
        "nitrogen_range": (20, 80),
        "benefits": ["Air purification", "Medicinal", "Repels insects", "Community value"],
        "co2_absorption_kg_yr": 1,
        "water_requirement": "Low",
        "growth_rate": "Fast",
        "canopy_radius_m": 0.5,
    },
    {
        "id": "areca_palm",
        "name": "Areca Palm (Dypsis lutescens)",
        "type": "palm",
        "ph_range": (6.0, 7.0),
        "moisture_range": (55, 85),
        "nitrogen_range": (30, 90),
        "benefits": ["Air purification (NASA list)", "Humidity regulation", "Indoor/outdoor"],
        "co2_absorption_kg_yr": 6,
        "water_requirement": "Medium",
        "growth_rate": "Medium",
        "canopy_radius_m": 2,
    },
]


class GreeneryRecommender:
    """
    Recommends optimal plant species based on soil data, climate, and spatial constraints.
    """
    
    def __init__(self):
        logger.info("GreeneryRecommender initialized")

    @classmethod
    def load_default(cls) -> "GreeneryRecommender":
        return cls()

    def recommend(self, location: str, soil_data: Optional[dict] = None,
                  area_sqm: Optional[float] = None) -> dict:
        soil = soil_data or self._simulate_soil_analysis(location)
        area = area_sqm or 500.0
        
        scored_plants = []
        for plant in PLANT_DATABASE:
            score = self._score_plant(plant, soil)
            if score > 0.4:
                scored_plants.append({**plant, "suitability_score": round(score, 3)})
        
        scored_plants.sort(key=lambda x: x["suitability_score"], reverse=True)
        top_plants = scored_plants[:5]
        
        layout = self._generate_layout(top_plants, area)
        soil_improvements = self._soil_improvement_plan(soil)
        
        return {
            "location": location,
            "area_sqm": area,
            "soil_analysis": soil,
            "soil_quality": self._soil_quality_label(soil),
            "recommended_plants": top_plants,
            "planting_layout": layout,
            "soil_improvement_plan": soil_improvements,
            "expected_co2_absorption_kg_yr": sum(
                p["co2_absorption_kg_yr"] * layout.get(p["id"], {}).get("count", 1)
                for p in top_plants
            ),
            "maintenance_notes": self._maintenance_notes(top_plants),
        }

    def _score_plant(self, plant: dict, soil: dict) -> float:
        score = 1.0
        
        ph = soil.get("ph", 7.0)
        if not (plant["ph_range"][0] <= ph <= plant["ph_range"][1]):
            score -= 0.4
        
        moisture = soil.get("moisture_pct", 50)
        if not (plant["moisture_range"][0] <= moisture <= plant["moisture_range"][1]):
            score -= 0.3
        
        nitrogen = soil.get("nitrogen_ppm", 50)
        if not (plant["nitrogen_range"][0] <= nitrogen <= plant["nitrogen_range"][1]):
            score -= 0.2
        
        return max(0, score)

    def _simulate_soil_analysis(self, location: str) -> dict:
        """Simulate soil sensor readings — replace with actual soil probe data."""
        return {
            "ph": round(np.random.uniform(5.8, 7.8), 2),
            "moisture_pct": round(np.random.uniform(30, 75), 1),
            "nitrogen_ppm": round(np.random.uniform(15, 110), 1),
            "phosphorus_ppm": round(np.random.uniform(10, 60), 1),
            "potassium_ppm": round(np.random.uniform(80, 300), 1),
            "organic_matter_pct": round(np.random.uniform(0.5, 4.5), 2),
            "texture": np.random.choice(["Sandy loam", "Clay loam", "Loam", "Silty clay"]),
            "salinity_ms_cm": round(np.random.uniform(0.2, 1.8), 2),
        }

    def _soil_quality_label(self, soil: dict) -> str:
        ph = soil.get("ph", 7.0)
        om = soil.get("organic_matter_pct", 2.0)
        if 6.0 <= ph <= 7.5 and om >= 3.0:
            return "Excellent"
        if 5.5 <= ph <= 8.0 and om >= 1.5:
            return "Good"
        if om >= 0.8:
            return "Fair — Amendments recommended"
        return "Poor — Major amendments required"

    def _generate_layout(self, plants: list, area_sqm: float) -> dict:
        layout = {}
        remaining_area = area_sqm
        for plant in plants[:3]:  # top 3 plants for layout
            plant_area = np.pi * (plant["canopy_radius_m"] ** 2)
            count = max(1, int(remaining_area * 0.4 / plant_area))
            layout[plant["id"]] = {
                "count": count,
                "spacing_m": plant["canopy_radius_m"] * 2.2,
                "area_covered_sqm": round(count * plant_area, 1),
                "zone": "Primary" if plant == plants[0] else "Secondary",
            }
            remaining_area -= count * plant_area
        return layout

    def _soil_improvement_plan(self, soil: dict) -> list[str]:
        plan = []
        if soil.get("ph", 7) < 6.0:
            plan.append("🧪 Apply agricultural lime (2-3 ton/ha) to raise pH.")
        if soil.get("ph", 7) > 7.8:
            plan.append("🧪 Apply elemental sulfur or acidifying fertilizers to lower pH.")
        if soil.get("organic_matter_pct", 2) < 1.5:
            plan.append("🌿 Incorporate 10-15 cm layer of compost/vermicompost before planting.")
        if soil.get("nitrogen_ppm", 50) < 20:
            plan.append("💚 Apply nitrogen-fixing cover crop (clover/beans) or NPK fertilizer.")
        if soil.get("moisture_pct", 50) < 30:
            plan.append("💧 Install drip irrigation system before planting.")
        if not plan:
            plan.append("✅ Soil is in good condition. Proceed with planting.")
        return plan

    def _maintenance_notes(self, plants: list) -> list[str]:
        return [
            "📅 Water new plantings daily for first 2 weeks, then reduce to 2-3x/week.",
            "🌿 Apply mulch (5-7 cm) around base of trees to retain moisture.",
            "✂️ Prune ornamental shrubs every 3 months to maintain shape.",
            "🔬 Conduct soil testing every 6 months for ongoing nutrient management.",
            f"🌳 {plants[0]['name']} is the primary recommendation — highest suitability for detected soil conditions.",
        ]
