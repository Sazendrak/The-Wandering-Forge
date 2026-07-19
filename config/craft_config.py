class Config:
    DEFAULT_WAGE_RATE = 50.0
    WORKDAY_HOURS = 8.0
    MAX_TEAM_SIZE = 5
    MIN_CRAFTING_DAYS = 1.0
    TAX_THRESHOLD_GP = 400.0

    TIERS = {
        "mundane": {"time_formula": lambda val: val / 50.0, "cost_formula": lambda val: val / 4.0},
        "common": {"time": 5.0, "cost": 50.0},
        "uncommon": {"time": 10.0, "cost": 200.0},
        "rare": {"time": 25.0, "cost": 2000.0},
        "very rare": {"time": 50.0, "cost": 20000.0},
        "legendary": {"time": 100.0, "cost": 100000.0}
    }

    SCROLLS = {
        0: {"time": 1.0, "cost": 15.0},
        1: {"time": 1.0, "cost": 25.0},
        2: {"time": 3.0, "cost": 250.0},
        3: {"time": 5.0, "cost": 500.0},
        4: {"time": 10.0, "cost": 2500.0},
        5: {"time": 12.0, "cost": 5000.0},
        6: {"time": 24.0, "cost": 15000.0},
        7: {"time": 38.0, "cost": 25000.0},
        8: {"time": 96.0, "cost": 50000.0},
        9: {"time": 144.0, "cost": 200000.0}
    }

    BARDING_MODIFIERS = {
        "diminutive": 4.0, "tiny": 2.0, "small": 1.0,
        "medium": 1.0, "large": 2.0, "huge": 4.0, "gargantuan": 8.0
    }

    SACRIFICE_BASE_TIMES = {
        "common": 5.0, "uncommon": 10.0, "rare": 25.0,
        "very rare": 50.0, "legendary": 100.0
    }

    TAX_BRACKETS = [
        (100000.0, 0.20),
        (20000.0, 0.15),
        (2000.0, 0.10),
        (400.0, 0.05)
    ]

    MATERIALS_MAP = {
        "mundane": "Mundane Components (N/A)",
        "common": "Common Essences & Materials (CR 1-4)",
        "uncommon": "Uncommon Monster Reagents (CR 5-8)",
        "rare": "Rare Reagents & Primal Essences (CR 9-12)",
        "very rare": "Very Rare Planar Essences (CR 13-18)",
        "legendary": "Legendary Mythic Essences (CR 19+)"
    }
