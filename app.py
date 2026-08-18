import streamlit as st
import pydeck as pdk
from model import calculate_production
from data import create_zones

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Rice Territorial Model",
    page_icon="🌾",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🌾 Rice Territorial Model")

st.write(
    "Participatory territorial simulation model"
)

# --------------------------------------------------
# TERRITORY
# --------------------------------------------------

zones = create_zones()

# --------------------------------------------------
# ACTORS
# --------------------------------------------------

st.header("Actors and decisions")

st.subheader("Irrigation authority")

st.write("Irrigation development investment by zone")

irrigation_A = st.slider(
    "Zone A",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)

irrigation_B = st.slider(
    "Zone B",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)

irrigation_C = st.slider(
    "Zone C",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)

irrigation_D = st.slider(
    "Zone D",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)

irrigation = {
    "Zone A": irrigation_A,
    "Zone B": irrigation_B,
    "Zone C": irrigation_C,
    "Zone D": irrigation_D
}

st.subheader("Rice value-chain actors")

value_chain = st.slider(
    "Value-chain development",
    min_value=0,
    max_value=100,
    value=50,
    step=5,
    help="Development of rice markets and value chains."
)


st.subheader("Rural development authority")

rural_development = st.slider(
    "Rural development",
    min_value=0,
    max_value=100,
    value=50,
    step=5,
    help="General rural development support."
)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

st.header("Simulation results")

results = calculate_production(
    zones,
    irrigation,
    value_chain,
    rural_development
)

# --------------------------------------------------
# PRODUCTION COLORS
# --------------------------------------------------

# Fixed production scale
def indicator_color(value, minimum, maximum):

    if maximum == minimum:
        ratio = 0.5
    else:
        ratio = (
            value - minimum
        ) / (
            maximum - minimum
        )

    ratio = max(0, min(1, ratio))

    red = int(255 * (1 - ratio))
    green = int(180 * ratio)

    return [red, green, 60, 180]

# --------------------------------------------------
# MAP
# --------------------------------------------------

st.subheader("Map indicator")

map_indicator = st.selectbox(
    "Choose the indicator displayed on the map:",
    [
        "Annual production",
        "Yield",
        "Irrigation"
    ]
)

if map_indicator == "Annual production":

    values = results["production_t"]

    minimum = 0
    maximum = 15000

elif map_indicator == "Yield":

    values = results["yield_final_t_ha"]

    minimum = 0
    maximum = 6

elif map_indicator == "Irrigation":

    values = results["irrigation"]

    minimum = 0
    maximum = 100


results["color"] = values.apply(
    lambda x: indicator_color(
        x,
        minimum,
        maximum
    )
)

st.subheader("Territory map")

view_state = pdk.ViewState(
    latitude=11.45,
    longitude=104.90,
    zoom=9,
    pitch=0
)

# Create GeoJSON-compatible data

geojson = {
    "type": "FeatureCollection",
    "features": []
}

for _, row in results.iterrows():

    coordinates = [
        [list(point) for point in row["geometry"].exterior.coords]
    ]

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": coordinates
        },
        "properties": {
            "zone": row["zone"],
            "rice_type": row["rice_type"],
            "production_t": row["production_t"],
            "yield_final_t_ha": row["yield_final_t_ha"],
            "irrigation": row["irrigation"],
            "color": row["color"]
        }
    }

    geojson["features"].append(feature)

production_min = results["production_t"].min()
production_max = results["production_t"].max()

def production_color(value):
    """
    Convert production into a color.
    Low production = red
    High production = green
    """

    if production_max == production_min:
        ratio = 0.5
    else:
        ratio = (
            value - production_min
        ) / (
            production_max - production_min
        )

    red = int(255 * (1 - ratio))
    green = int(180 * ratio)

    return [red, green, 60, 180]

results["color"] = results["production_t"].apply(
    production_color
)

layer = pdk.Layer(
    "GeoJsonLayer",
    data=geojson,
    pickable=True,
    filled=True,
    stroked=True,
    get_fill_color="properties.color",
    get_line_color=[50, 50, 50],
    get_line_width=3
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "text": (
            "Zone: {zone}\n"
            "Rice type: {rice_type}\n"
            "Production: {production_t} t\n"
            "Yield: {yield_final_t_ha} t/ha\n"
            "Irrigation: {irrigation}%"
        )
    }
)

st.pydeck_chart(deck)

if map_indicator == "Annual production":

    legend = """
    **Annual rice production**

    🔴 0 t &nbsp;&nbsp;&nbsp;
    🟠 5,000 t &nbsp;&nbsp;&nbsp;
    🟡 10,000 t &nbsp;&nbsp;&nbsp;
    🟢 15,000 t
    """

elif map_indicator == "Yield":

    legend = """
    **Rice yield**

    🔴 0 t/ha &nbsp;&nbsp;&nbsp;
    🟠 2 t/ha &nbsp;&nbsp;&nbsp;
    🟡 4 t/ha &nbsp;&nbsp;&nbsp;
    🟢 6 t/ha
    """

else:

    legend = """
    **Irrigation**

    🔴 0% &nbsp;&nbsp;&nbsp;
    🟠 33% &nbsp;&nbsp;&nbsp;
    🟡 66% &nbsp;&nbsp;&nbsp;
    🟢 100%
    """

st.markdown(legend)

st.subheader("Territorial results")

st.dataframe(
    results[[
        "zone",
        "rice_type",
        "surface_ha",
        "irrigation",
        "irrigation_investment",
        "irrigation_final",
        "yield_final_t_ha",
        "production_t"
    ]],
    use_container_width=True
)

total_production = results["production_t"].sum()

st.metric(
    "Total annual rice production",
    f"{total_production:,.0f} tonnes"
)