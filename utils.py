def format_results(r):
    lines = [
        f"Cross-Sectional Area          : {r['A']:.6f} m^2",
        f"Flow Velocity                 : {r['V']:.4f} m/s",
        f"Reynolds Number                : {r['Re']:,.1f}",
        f"Flow Regime                    : {r['regime']}",
        f"Relative Roughness (e/D)       : {r['rel_rough']:.6f}",
        f"Darcy Friction Factor           : {r['f']:.5f}",
        f"Major (Friction) Head Loss      : {r['hf']:.4f} m",
        f"Minor Losses Head Loss          : {r['hm']:.4f} m",
        f"Elevation Head Change           : {r['dz']:+.4f} m",
        f"Total Dynamic Head              : {r['h_total']:.4f} m",
        f"Pressure Drop (friction only)   : {r['dP_friction']:,.1f} Pa  ({r['dP_friction']/1000:.3f} kPa, {r['dP_friction']/6894.76:.3f} psi)",
        f"Mass Flow Rate                  : {r['mdot']:.4f} kg/s",
        f"Hydraulic Pump Power Required   : {r['P_hyd']:,.2f} W  ({r['P_hyd']/1000:.3f} kW)",
        f"Shaft Pump Power (w/ efficiency): {r['P_shaft']:,.2f} W  ({r['P_shaft']/1000:.3f} kW, {r['P_shaft']/745.7:.3f} hp)",
    ]
    return "\n".join(lines)


