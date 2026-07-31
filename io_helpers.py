from constants import FLUIDS, ROUGHNESS_MM, G


def prompt_float(msg, default):
    while True:
        raw = input(f"{msg} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a valid number.")


def prompt_choice(msg, options, default_index=0):
    print(msg)
    for i, opt in enumerate(options, 1):
        marker = "  <- default" if i - 1 == default_index else ""
        print(f"  {i}) {opt}{marker}")
    while True:
        raw = input(f"Select [1-{len(options)}] (Enter for default): ").strip()
        if raw == "":
            return options[default_index]
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("  Invalid selection, try again.")


def collect_pipeline_inputs(ask_name=False, default_name="Scenario"):
    """Interactively collects all parameters for one pipeline design.
    Returns (name, params) if ask_name else params. params uses SI units."""
    print("\n--- Pipeline Parameters ---")
    name = None
    if ask_name:
        name = input(f"Scenario name [{default_name}]: ").strip() or default_name

    Q_Lps = prompt_float("Flow rate Q (L/s)", 10.0)
    D_mm = prompt_float("Pipe diameter D (mm)", 100.0)
    L_m = prompt_float("Pipe length L (m)", 250.0)
    dz_m = prompt_float("Elevation rise dz (m, negative = downhill)", 0.0)

    fluid_name = prompt_choice("\nFluid:", list(FLUIDS.keys()), default_index=0)
    if FLUIDS[fluid_name] is None:
        rho = prompt_float("  Density (kg/m^3)", 998.2)
        mu = prompt_float("  Viscosity (Pa-s)", 1.002e-3)
    else:
        rho, mu = FLUIDS[fluid_name]
        print(f"  -> rho = {rho} kg/m^3, mu = {mu} Pa-s")

    materials = list(ROUGHNESS_MM.keys())
    material_name = prompt_choice("\nPipe material:", materials, default_index=materials.index("Commercial Steel"))
    if ROUGHNESS_MM[material_name] is None:
        epsilon_mm = prompt_float("  Roughness (mm)", 0.045)
    else:
        epsilon_mm = ROUGHNESS_MM[material_name]
        print(f"  -> roughness = {epsilon_mm} mm")

    minor_k = prompt_float("\nTotal minor-loss K (sum of fittings/valves)", 2.0)
    pump_eff = prompt_float("Pump efficiency (%)", 70.0)

    params = dict(D=D_mm / 1000.0, L=L_m, Q=Q_Lps / 1000.0, rho=rho, mu=mu,
                  epsilon_mm=epsilon_mm, minor_k=minor_k, dz=dz_m, pump_eff=pump_eff)
    if ask_name:
        return name, params
    return params
