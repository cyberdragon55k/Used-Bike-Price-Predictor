import streamlit as st
import pandas as pd
import pickle
import os
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Used Bike Price Predictor",
    page_icon="🏍️",
    layout="wide"
)

# --------------------------------------------------
# PATHS
# --------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, "images")

# --------------------------------------------------
# LOAD MODEL & DATA
# --------------------------------------------------
@st.cache_resource
def load_model():
    return pickle.load(open(os.path.join(current_dir, "bike_model.pkl"), "rb"))

@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(current_dir, "Used_Bikes.csv"))

try:
    model = load_model()
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Required files not found.")
    st.stop()

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def get_logo_path(brand_name):
    valid_ext = ["png", "jpg", "jpeg", "svg"]
    if os.path.isdir(images_dir):
        for ext in valid_ext:
            path = os.path.join(images_dir, f"{brand_name}.{ext}")
            if os.path.exists(path):
                return path
    return "https://cdn-icons-png.flaticon.com/512/6750/6750554.png"


def price_counter(value):
    placeholder = st.empty()
    for i in range(0, int(value) + 1, max(1, int(value / 50))):
        placeholder.metric("Estimated Market Value", f"₹ {i:,}")
        time.sleep(0.01)
    placeholder.metric("Estimated Market Value", f"₹ {int(value):,}")

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("Used Bike Price Predictor")
st.caption("Search your bike model to auto-fill specifications and estimate its fair market value.")

h1, h2 = st.columns([4, 1])

with h1:
    all_bikes = sorted(df["bike_name"].unique())
    selected_bike = st.selectbox(
        "Search Bike Model",
        all_bikes,
        index=None,
        placeholder="Type to search..."
    )

if selected_bike:
    bike_row = df[df["bike_name"] == selected_bike].iloc[0]
    auto_power = float(bike_row["power"])
    auto_brand = bike_row["brand"]
    logo = get_logo_path(auto_brand)
else:
    auto_power = 150.0
    auto_brand = None
    logo = get_logo_path("default")

with h2:
    st.image(logo, width=90)
    if auto_brand:
        st.caption(auto_brand)

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Details")
    kms = st.number_input(
        "Kilometers Driven",
        min_value=0,
        step=500,
        value=25000,
        help="Total distance the bike has been ridden"
    )
    year = st.number_input(
        "Manufacturing Year",
        min_value=1990,
        max_value=2026,
        value=2021
    )

with c2:
    st.subheader("Specifications")
    power = st.number_input(
        "Engine Capacity (cc)",
        value=auto_power,
        help="Engine displacement in cubic centimeters"
    )

    if power < 150:
        bike_type = "Commuter / Scooter"
    elif power < 300:
        bike_type = "Sport / Performance"
    else:
        bike_type = "Superbike / Cruiser"

    st.info(f"Category: **{bike_type}**")

st.divider()

# --------------------------------------------------
# PREDICTION CTA
# --------------------------------------------------
predict = st.button(
    "Estimate Price",
    use_container_width=True,
    type="primary"
)

# --------------------------------------------------
# PREDICTION RESULT
# --------------------------------------------------
if predict:
    with st.spinner("Analyzing market trends..."):
        age = 2026 - year
        input_df = pd.DataFrame(
            [[kms, age, power]],
            columns=["kms_driven", "age", "power"]
        )
        prediction = model.predict(input_df)[0]
        time.sleep(0.6)

    st.divider()

    r1, r2 = st.columns([1, 2])

    with r1:
        st.image(logo, width=110)

    with r2:
        price_counter(prediction)

        lower = int(prediction * 0.9)
        upper = int(prediction * 1.1)
        st.caption(f"Expected range: ₹ {lower:,} – ₹ {upper:,}")

        label = selected_bike if selected_bike else "Custom Bike"
        st.info(f"Valuation for **{label} ({year})**")

    # --------------------------------------------------
    # SIMILAR BIKES
    # --------------------------------------------------
    st.subheader("Other bikes available in this price range")

    similar = df[
        (df["price"] >= lower) &
        (df["price"] <= upper)
    ][["bike_name", "kms_driven", "price", "city"]].sort_values("price").head(5)

    if not similar.empty:
        st.dataframe(similar, use_container_width=True, hide_index=True)
    else:
        st.warning("No similar bikes found for this range.")
