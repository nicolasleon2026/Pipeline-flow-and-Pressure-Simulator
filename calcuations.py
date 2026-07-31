import math
from constants import G
import numpy as np


def friction_factor(Re, rel_roughness):
    """Darcy friction factor. Laminar -> 64/Re. Turbulent -> Swamee-Jain
    explicit approximation of Colebrook-White. Transitional zone is
    linearly blended between the two so the curve stays continuous."""
    if Re <= 0:
        raise ValueError("Reynolds number must be positive.")

    def swamee_jain(re):
        return 0.25 / (math.log10(rel_roughness / 3.7 + 5.74 / re ** 0.9)) ** 2

    if Re < 2300:
        return 64.0 / Re, "Laminar"
    elif Re <= 4000:
        f_lam = 64.0 / 2300.0
        f_turb = swamee_jain(4000.0)
        f = np.interp(Re, [2300.0, 4000.0], [f_lam, f_turb])
        return float(f), "Transitional"
    else:
        return swamee_jain(Re), "Turbulent"


def compute_pipeline(D, L, Q, rho, mu, epsilon_mm, minor_k, dz, pump_eff_pct):
    """All core calculations for one pipeline design.

    D   : pipe internal diameter (m)
    L   : pipe length (m)
    Q   : volumetric flow rate (m^3/s)
    rho : fluid density (kg/m^3)
    mu  : fluid dynamic viscosity (Pa-s)
    epsilon_mm : absolute pipe roughness (mm)
    minor_k    : sum of minor-loss K coefficients (fittings, valves, etc.)
    dz  : net elevation rise of the pipeline (m); negative = downhill
    pump_eff_pct : pump efficiency (%), used for shaft power
    """
    if D <= 0 or L <= 0 or Q <= 0 or rho <= 0 or mu <= 0:
        raise ValueError("Diameter, length, flow rate, density and viscosity must all be positive.")

    A = math.pi / 4.0 * D ** 2
    V = Q / A
    Re = rho * V * D / mu
    epsilon = epsilon_mm / 1000.0
    rel_rough = epsilon / D
    f, regime = friction_factor(Re, rel_rough)

    hf = f * (L / D) * (V ** 2 / (2 * G))          # major (friction) head loss, m
    hm = minor_k * (V ** 2 / (2 * G))              # minor losses, m
    h_total = hf + hm + dz                         # total dynamic head, m

    dP_friction = (hf + hm) * rho * G              # Pa
    mdot = rho * Q                                  # kg/s

    P_hyd = rho * G * Q * h_total                   # W (hydraulic power the pump must deliver)
    eff = max(pump_eff_pct, 1e-6) / 100.0
    P_shaft = P_hyd / eff                            # W

    return {
        "A": A, "V": V, "Re": Re, "regime": regime, "rel_rough": rel_rough,
        "f": f, "hf": hf, "hm": hm, "dz": dz, "h_total": h_total,
        "dP_friction": dP_friction, "mdot": mdot,
        "P_hyd": P_hyd, "P_shaft": P_shaft,
    }


def system_curve(D, L, rho, mu, epsilon_mm, minor_k, dz, Q_max, n=120):
    """Head loss (m) vs flow rate (m^3/s) for a fixed pipe, used to draw the
    classic 'system curve' engineers use to size pumps."""
    Q_arr = np.linspace(max(Q_max * 0.02, 1e-6), Q_max, n)
    h_arr = np.empty_like(Q_arr)
    for i, Q in enumerate(Q_arr):
        r = compute_pipeline(D, L, Q, rho, mu, epsilon_mm, minor_k, dz, 100.0)
        h_arr[i] = r["h_total"]
    return Q_arr, h_arr
  
def run_pipeline(params):
    return compute_pipeline(params["D"], params["L"], params["Q"], params["rho"], params["mu"],
                             params["epsilon_mm"], params["minor_k"], params["dz"], params["pump_eff"])
