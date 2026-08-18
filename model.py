import pandas as pd


def calculate_production(
    zones,
    irrigation,
    value_chain,
    rural_development
):
    """
    Calculate rice production for each territorial zone.
    """

    zones = zones.copy()

    # --------------------------------------------------
    # IRRIGATION
    # --------------------------------------------------

    # Investment decided by the irrigation authority
    zones["irrigation_investment"] = (
        zones["zone"].map(irrigation)
    )

    # Final irrigation level
    zones["irrigation_final"] = (
        zones["irrigation"]
        + zones["irrigation_investment"]
    )

    # Maximum irrigation level = 100%
    zones["irrigation_final"] = (
        zones["irrigation_final"].clip(upper=100)
    )

    # Effect of irrigation on yield
    irrigation_effect = (
        0.20 * (zones["irrigation_final"] / 100)
    )

    # --------------------------------------------------
    # OTHER POLICY EFFECTS
    # --------------------------------------------------

    value_chain_effect = (
        0.05 * (value_chain / 100)
    )

    rural_effect = (
        0.10 * (rural_development / 100)
    )

    # --------------------------------------------------
    # TOTAL EFFECT ON YIELD
    # --------------------------------------------------

    yield_effect = (
        1
        + irrigation_effect
        + value_chain_effect
        + rural_effect
    )

    # --------------------------------------------------
    # FINAL YIELD
    # --------------------------------------------------

    zones["yield_final_t_ha"] = (
        zones["yield_base_t_ha"]
        * yield_effect
    )

    # --------------------------------------------------
    # ANNUAL PRODUCTION
    # --------------------------------------------------

    zones["production_t"] = (
        zones["surface_ha"]
        * zones["yield_final_t_ha"]
    )

    return zones