def print_scenario_table(scenarios):
    if not scenarios:
        print("(no scenarios yet)")
        return
    headers = ["#", "Name", "D(mm)", "L(m)", "Q(L/s)", "V(m/s)", "Re", "Regime", "f", "H(m)", "dP(kPa)", "Pump(kW)"]
    widths = [3, 18, 7, 7, 7, 7, 10, 12, 8, 8, 9, 9]
    line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-" * len(line))
    for i, s in enumerate(scenarios, 1):
        p, r = s["params"], s["results"]
        row = [
            str(i), s["name"][:18],
            f"{p['D']*1000:.1f}", f"{p['L']:.1f}", f"{p['Q']*1000:.2f}",
            f"{r['V']:.3f}", f"{r['Re']:,.0f}", r["regime"], f"{r['f']:.4f}",
            f"{r['h_total']:.3f}", f"{r['dP_friction']/1000:.2f}", f"{r['P_shaft']/1000:.3f}",
        ]
        print(" | ".join(val.ljust(w) for val, w in zip(row, widths)))


def load_example_scenarios(scenarios):
    examples = [
        dict(name="4-inch Steel Pipe", Q_Lps=15.0, D_mm=100.0, L_m=300.0, dz_m=5.0,
             fluid="Water @ 20 C", material="Commercial Steel", minor_k=3.0, pump_eff=72.0),
        dict(name="6-inch Steel Pipe", Q_Lps=15.0, D_mm=150.0, L_m=300.0, dz_m=5.0,
             fluid="Water @ 20 C", material="Commercial Steel", minor_k=3.0, pump_eff=72.0),
        dict(name="6-inch PVC Pipe", Q_Lps=15.0, D_mm=150.0, L_m=300.0, dz_m=5.0,
             fluid="Water @ 20 C", material="PVC / Plastic (smooth)", minor_k=3.0, pump_eff=72.0),
    ]
    for ex in examples:
        rho, mu = FLUIDS[ex["fluid"]]
        epsilon_mm = ROUGHNESS_MM[ex["material"]]
        params = dict(D=ex["D_mm"] / 1000.0, L=ex["L_m"], Q=ex["Q_Lps"] / 1000.0, rho=rho, mu=mu,
                      epsilon_mm=epsilon_mm, minor_k=ex["minor_k"], dz=ex["dz_m"], pump_eff=ex["pump_eff"])
        r = run_pipeline(params)
        scenarios.append({"name": ex["name"], "params": params, "results": r})
    print(f"Loaded {len(examples)} example scenarios (4-inch vs 6-inch steel vs 6-inch PVC).")


def remove_scenario(scenarios):
    if not scenarios:
        print("No scenarios to remove.")
        return
    print_scenario_table(scenarios)
    raw = input("Enter the # of the scenario to remove (blank to cancel): ").strip()
    if raw == "":
        return
    if raw.isdigit() and 1 <= int(raw) <= len(scenarios):
        removed = scenarios.pop(int(raw) - 1)
        print(f"Removed '{removed['name']}'.")
    else:
        print("Invalid selection.")

def run_comparison():
    scenarios = []
    while True:
        print(f"\n=== SCENARIO COMPARISON ({len(scenarios)} scenario(s) loaded) ===")
        print("1) Add a new scenario")
        print("2) Load 3 example scenarios (diameter/material comparison)")
        print("3) View scenario table")
        print("4) Remove a scenario")
        print("5) Generate comparison graphs")
        print("6) Return to main menu")
        choice = input("Select an option [1-6]: ").strip()

        if choice == "1":
            name, params = collect_pipeline_inputs(ask_name=True, default_name=f"Scenario {len(scenarios) + 1}")
            try:
                r = run_pipeline(params)
            except ValueError as e:
                print(f"\n[Error] {e}")
                continue
            scenarios.append({"name": name, "params": params, "results": r})
            print(f"Added '{name}'.")
        elif choice == "2":
            load_example_scenarios(scenarios)
        elif choice == "3":
            print()
            print_scenario_table(scenarios)
        elif choice == "4":
            remove_scenario(scenarios)
        elif choice == "5":
            plot_comparison(scenarios)
        elif choice == "6":
            break
        else:
            print("Invalid option, please choose 1-6.")

