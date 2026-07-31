from io_helpers import collect_pipeline_inputs
from calculations import compute_pipeline, system_curve
from utils import format_results


def run_pipeline(params):
    return compute_pipeline(params["D"], params["L"], params["Q"], params["rho"], params["mu"],
                             params["epsilon_mm"], params["minor_k"], params["dz"], params["pump_eff"])

def run_single_analysis():
    params = collect_pipeline_inputs()
    try:
        r = run_pipeline(params)
    except ValueError as e:
        print(f"\n[Error] {e}")
        return

    print("\n=== RESULTS ===")
    print(format_results(r))

    ans = input("\nGenerate & save a system-curve graph? (y/n) [y]: ").strip().lower()
    if ans in ("", "y", "yes"):
        Q_arr, h_arr = system_curve(params["D"], params["L"], params["rho"], params["mu"],
                                     params["epsilon_mm"], params["minor_k"], params["dz"],
                                     params["Q"] * 2.0)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(Q_arr * 1000, h_arr, color="#0e7490", linewidth=2, label="System curve")
        ax.scatter([params["Q"] * 1000], [r["h_total"]], color="#dc2626", zorder=5,
                   label="Operating point")
        ax.set_title("Pipeline System Curve (Head Loss vs Flow Rate)")
        ax.set_xlabel("Flow Rate (L/s)")
        ax.set_ylabel("Total Dynamic Head (m)")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        fig.tight_layout()

        fname = "pipeline_system_curve.png"
        fig.savefig(fname, dpi=150)
        print(f"Saved graph to {fname}")
        plt.show()
        plt.close(fig)
        names = [s["name"] for s in scenarios]

    head_losses = [s["results"]["h_total"] for s in scenarios]
    powers_kw = [s["results"]["P_shaft"] / 1000 for s in scenarios]
    cmap = plt.get_cmap("tab10")
    colors = [cmap(i % 10) for i in range(len(names))]

    fig = plt.figure(figsize=(12, 7))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.3], hspace=0.55, wspace=0.3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    ax1.bar(names, head_losses, color=colors)
    ax1.set_title("Total Dynamic Head by Scenario")
    ax1.set_ylabel("Head Loss (m)")
    ax1.grid(True, axis="y", linestyle="--", alpha=0.5)
    ax1.tick_params(axis="x", labelrotation=30, labelsize=8)
    for lbl in ax1.get_xticklabels():
        lbl.set_ha("right")

    ax2.bar(names, powers_kw, color=colors)
    ax2.set_title("Pump Shaft Power by Scenario")
    ax2.set_ylabel("Power (kW)")
    ax2.grid(True, axis="y", linestyle="--", alpha=0.5)
    ax2.tick_params(axis="x", labelrotation=30, labelsize=8)
    for lbl in ax2.get_xticklabels():
        lbl.set_ha("right")

    Q_max_global = max(s["params"]["Q"] for s in scenarios) * 1.6
    for i, s in enumerate(scenarios):
        p, r = s["params"], s["results"]
        Q_arr, h_arr = system_curve(p["D"], p["L"], p["rho"], p["mu"], p["epsilon_mm"],
                                     p["minor_k"], p["dz"], Q_max_global)
        ax3.plot(Q_arr * 1000, h_arr, color=colors[i], linewidth=2, label=s["name"])
        ax3.scatter([p["Q"] * 1000], [r["h_total"]], color=colors[i], zorder=5, edgecolor="black")

    ax3.set_title("System Curves - Head Loss vs Flow Rate (dots = design operating point)")
    ax3.set_xlabel("Flow Rate (L/s)")
    ax3.set_ylabel("Total Dynamic Head (m)")
    ax3.grid(True, linestyle="--", alpha=0.5)
    ax3.legend(fontsize=8, loc="upper left")

    fname = "pipeline_scenario_comparison.png"
    fig.savefig(fname, dpi=150, bbox_inches="tight")
    print(f"Saved comparison graph to {fname}")
    plt.show()
    plt.close(fig)
