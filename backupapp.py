import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Used Bike Price Predictor", page_icon="🏍️", layout="wide")


current_dir = os.path.dirname(os.path.abspath(__file__))

images_dir = os.path.join(current_dir, 'images')

@st.cache_resource
def load_model():

    model_path = os.path.join(current_dir, 'bike_model.pkl')
    return pickle.load(open(model_path, 'rb'))

@st.cache_data
def load_data():
    data_path = os.path.join(current_dir, 'Used_Bikes.csv')
    return pd.read_csv(data_path)

try:
    model = load_model()
    df = load_data()
except FileNotFoundError:
    st.error(f"⚠️ Error: Files not found. Looking in: {current_dir}")
    st.stop()


def get_logo_path(brand_name):
    """
    Looks for the brand logo in the 'images' folder using absolute paths.
    """
    brand_clean = brand_name.strip()
    valid_extensions = ['png', 'jpg', 'jpeg', 'svg']
    
    if os.path.isdir(images_dir):
        for ext in valid_extensions:
            filename = f"{brand_clean}.{ext}"
            file_path = os.path.join(images_dir, filename)
            
            if os.path.exists(file_path):
                return file_path
    
    return "https://cdn-icons-png.flaticon.com/512/6750/6750554.png"

st.title("🏍️ Used Bike Price Predictor")
st.markdown("Search for your bike model to automatically fill the details.")

head_col1, head_col2 = st.columns([3, 1])

with head_col1:
    all_bikes = sorted(df['bike_name'].unique())
    selected_bike_name = st.selectbox(
        "🔍 Search Bike Name", 
        all_bikes, 
        index=None, 
        placeholder="Type to search..."
    )

if selected_bike_name:
    bike_info = df[df['bike_name'] == selected_bike_name].iloc[0]
    auto_power = float(bike_info['power'])
    auto_brand = bike_info['brand']
    logo_path = get_logo_path(auto_brand)
else:
    auto_power = 150.0
    auto_brand = "Select a Bike"
    logo_path = "https://cdn-icons-png.flaticon.com/512/6750/6750554.png"

with head_col2:
    st.image(logo_path, width=100)
    if selected_bike_name:
        st.caption(f"**{auto_brand}**")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Details")
    kms = st.number_input("Kilometers Driven", min_value=0, value=25000, step=500)
    year = st.number_input("Manufacturing Year", min_value=1990, max_value=2026, value=2021)

with col2:
    st.subheader("⚙️ Specifications")
    power = st.number_input("Power (CC)", value=auto_power, disabled=False)
    
    if power < 150:
        st.info("🛵 Type: **Commuter / Scooter**")
    elif power < 300:
        st.info("🏍️ Type: **Sport / Performance**")
    else:
        st.info("🚀 Type: **Superbike / Cruiser**")

st.markdown("###")
if st.button("Predict Price 💰", type="primary", use_container_width=True):
    
    age = 2026 - year
    

    input_df = pd.DataFrame([[kms, age, power]], columns=['kms_driven', 'age', 'power'])
    

    pred = model.predict(input_df)[0]
    

    st.balloons()
    st.markdown("---")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(logo_path, width=120)
    with c2:
        st.metric("Fair Market Value", f"₹ {int(pred):,}")
        if selected_bike_name:
            st.info(f"Valuation for **{selected_bike_name}** ({year})")
        else:
            st.info(f"Valuation for **Custom Bike** ({year})")

    st.markdown("---")
    st.subheader(f"👀 Other bikes available for ~ ₹ {int(pred):,}")
    
    min_p = pred * 0.85
    max_p = pred * 1.15
    similar = df[(df['price'] >= min_p) & (df['price'] <= max_p)].head(5)
    
    if not similar.empty:
        st.table(similar[['bike_name', 'kms_driven', 'price', 'city']])
    else:
        st.write("No similar bikes found in this price range.")