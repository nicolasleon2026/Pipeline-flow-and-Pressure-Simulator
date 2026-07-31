G = 9.81  

FLUIDS = {
    "Water @ 20 C":        (998.2, 1.002e-3),
    "Water @ 60 C":        (983.3, 4.67e-4),
    "Water @ 80 C":        (971.8, 3.55e-4),
    "Air @ 20 C (1 atm)":  (1.204, 1.825e-5),
    "SAE 30 Oil @ 20 C":   (891.0, 0.29),
    "Gasoline @ 20 C":     (720.0, 2.92e-4),
    "Custom":              None,
}

ROUGHNESS_MM = {
    "PVC / Plastic (smooth)": 0.0015,
    "Drawn Copper / Brass":   0.0015,
    "Commercial Steel":       0.045,
    "Galvanized Iron":        0.15,
    "Cast Iron":              0.26,
    "Concrete":                1.0,
    "Riveted Steel":            3.0,
    "Custom":                 None,
}
