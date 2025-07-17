import streamlit as st
import pandas as pd
from datetime import datetime
import os
import gspread
import json
# <<< CHANGE START: These imports are new or updated. The old oauth2client is removed.
from google.oauth2.service_account import Credentials
# <<< CHANGE END


# ------------------ UI ------------------
st.set_page_config(page_title="Sales Order Form", layout="centered")
st.title("📝 Order Entry Form")
st.markdown("---")

# Salesperson dropdown
salespeople = {"Amit": 1, "Arpit": 2, "Rahul": 3}
salesperson_name = st.selectbox("Select Salesperson", list(salespeople.keys()))
salesperson_id = salespeople[salesperson_name]

# Company with "Other"
company_list = sorted([
    "3S Fitness", "AG organica", "Animal booster", "Angrish", "Anutrition", "Arscore", "Asthetic Pharma",
    "BBI", "BIO Herbal", "Body Armore", "Body Armour", "Bluebin", "Bukalo", "Dabur", "Davisco", "Demotic",
    "Denzour", "Dr. Morapen", "Duhi", "Easy Eat", "Enhance", "Enhanced Dubai", "Fabley Costamics",
    "Fermentis", "Fit Red", "Fit treat", "GoodLuck", "GXN", "Hercules", "HFN", "Imagine Eyes", "Influx",
    "Jovex", "Little Joy", "Mind & Body", "Monsterbolic", "Muscle Dominator", "Muscle venture", "My Fitness",
    "N.g Electro", "Nectarine Pharmacy", "Nestor Pharma", "Nirvasa Healthcare Pvt. Ltd.", "Nutricore Bioscience",
    "Nutriburst", "One Punch Nutrition", "OZN", "Owleaf", "Packrights", "PB", "Percos", "Pontika", "Pressage",
    "PSN", "RME", "RMS", "Rebela", "Roxor", "Sacred beast", "Sapiens lab", "Sirona", "Snikki",
    "Sprivil Healthcare", "STARK NUTRITION", "Super Muscle", "Tforma", "The Natural Wash", "Thrive on",
    "Titon Biotech", "Trusan", "Trojan", "Trojan Pharma", "TrueNutrition", "TVC", "UP&RUN", "Vivoiz",
    "WellBeing Nutrition", "White Wolf", "Wings Nutrition", "Zucchero"
])
selected_company = st.selectbox("Select Company", company_list + ["Other"])
company = st.text_input("Enter Company Name") if selected_company == "Other" else selected_company

# ------------------ Multiple Product Entries ------------------
st.subheader(" Add Products")
products = []
num_products = st.number_input("How many products do you want to add?", min_value=1, max_value=20, value=1, step=1)

for i in range(num_products):
    st.markdown(f"**Product {i+1}**")

    product_type = st.selectbox(f"Select Product Type {i+1}", [
        "Labels", "Laminates", "3SS Pouch", "Neck Shrink",
        "Body Shrink",  "Standup Pouch", "3D Pouch", "Mono Carton", "Composite Can"
    ], key=f"product_type_{i}")

    # Dynamic specs
    specs = ""
    if product_type == "Labels":
        col1, col2 = st.columns(2)
        with col1:
            item_name = st.selectbox(f"Item Name {i+1}", ["PP White", "PP Silver", "PP Clear", "Chromo Adhesive", "PE White", "Paper Silver", "Clear PET"], key=f"item_{i}")
        with col2:
            finish = st.selectbox(f"Finish {i+1}", ["Gloss Varnish", "Matt Varnish", "Gloss Lamination", "Matt Lamination", "Matt Lamination + Spot UV"], key=f"finish_{i}")
        specs = f"{item_name} - {finish}"

    elif product_type == "Laminates":
        col1, col2, col3 = st.columns(3)
        with col1:
            film_type = st.selectbox(f"Film Type {i+1}", ["12 BOPP", "18 Matte BOPP"], key=f"film_{i}")
        with col2:
            barrier_layer = st.selectbox(f"Barrier {i+1}", ["9 ALU", "12 METPET", "12 PET"], key=f"barrier_{i}")
        with col3:
            inner_layer = st.selectbox(f"Inner Layer {i+1}", ["60 LD", "75 LD", "90 LD", "80 LD", "100 LD"], key=f"inner_{i}")
        specs = f"{film_type} + {barrier_layer} + {inner_layer}"

    elif product_type == "3SS Pouch":
         col1,col2 = st.columns(2)
         with col1:
             filmtype = st.selectbox("Thickness", ["12metpet", "18 Matte BOPP"], key=f"film_{i}")
         with col2:
             barrier_layer = st.selectbox("Barrier Layer",["60LD Matte Lamination", "12Metpet 90Poly"], key=f"barrier_{i}")
         specs = f"{filmtype}+{barrier_layer}"
    
    elif product_type == "Neck Shrink":
        col1, = st.columns(1)
        with col1:
            thickness=st.selectbox("Thickness",["40 Micron","50 Micron"], key=f"thickness_{i}")
        specs= f"{thickness}"

    elif product_type == "Body Shrink":
        col1, = st.columns(1)
        with col1:
            thickness=st.selectbox("Thickness",["40 Micron","50 Micron"], key=f"thickness_{i}")
        specs= f"{thickness}"
    
    elif product_type == "3D Pouch":
        col1,col2,col3,col4=st.columns(4)
        with col1:
            film_type=st.selectbox("Thickness",["12 Pet","18 BOPP"], key=f"film_{i}")
        with col2:
            barrier_layer=st.selectbox("Barrier Layer",["12 Metpet","9 ALU"], key=f"barrier_{i}")
        with col3:
            inner_layer=st.selectbox("Inner Layer",["90 Poly","60 LD","80 LD","100 LD"], key=f"inner_{i}")
        with col4:
            finish_type=st.selectbox("Finish",["Gloss Finish","Matte Finish",""], key=f"finish_{i}")
        specs= f"{film_type} + {barrier_layer} + {inner_layer} + {finish_type}"

    elif product_type=="Standup Pouch":
        col1,col2,col3,col4=st.columns(4)
        with col1:
            film_type=st.selectbox("Thickness",["12 Pet", "18 Matt BOPP"], key=f"film_{i}")
        with col2:
            barrier_layer=st.selectbox("Barrier Layer", ["12 Metpet"], key=f"barrier_{i}")
        with col3:
            inner_layer=st.selectbox("Inner Layer", ["100 LD"], key=f"inner_{i}")
        with col4:
            finish_type=st.selectbox("Finish", ["Gloss Finish","Matte Finish",""], key=f"finish_{i}")
        specs=f"{film_type} + {barrier_layer} + {inner_layer} + {finish_type}"
    elif product_type=="Mono Carton":
        col1,col2,col3=st.columns(3)
        with col1:
            first_layer=st.selectbox("First Layer",["SBS 350", "SBS 300","330 FBB"], key=f"outer_{i}")
        with col2:
            second_layer=st.selectbox("Second Layer",["Matte Lamination", "Gloss Lamination"],key=f"second_{i}")
        with col3:
            third_layer=st.selectbox("Third Layer",["Emboissing", "Emboissing + SpotUV", "Emboissing + SpotUV + Dripoff","Emboissing + SpotUV + Dripoff + Foiling","" ],key=f"third_{i}")
        spec=f"{first_layer} + {second_layer} + {third_layer}"
    
    elif product_type=="Composite Can":
        col1,col2,col3,col4 =st.columns(4)
        with col1:
            decoration=st.selectbox("Decoration",["Gloss Lamination", "Gloss lamination+ foiling ","Matte lamination","Matte lamination+ foiling", "Matte lamination + foiling + spotUV"],key=f"decoration_{i}")
        with col2:
            cap_type=st.selectbox("Cap Type",["Long Cap", "Short Cap"],key=f"cap_{i}")
        with col3:
            cushion_require=st.selectbox("Cushion Required",["Yes","No"],key=f"cushion_{i}")
        cushioning_type=""
        with col4:
            if cushion_require=="Yes":
                cushioning_type=st.text_input("Enter cushioning type",key=f"cushioning_{i}")
        specs=f"{decoration} / {cap_type} / {cushioning_type}"

    else:
        specs = st.text_input("Enter Specifications")
    product_description = st.text_input(f"Product Description {i+1}", key=f"prod_desc_{i}")
    quantity = st.number_input(f"Quantity {i+1}", min_value=1, key=f"qty_{i}")
    rate = st.number_input(f"Rate {i+1}", min_value=0.0, format="%.2f", key=f"rate_{i}")

    products.append({
        "Product Type": product_type,
        "Specs": specs,
        "Product Description": product_description,
        "Quantity": quantity,
        "Rate": rate
    })

# Shared fields
shipping_address = st.text_area("Shipping Address")
billing_address = st.text_area("Billing Address")
delivery_mode = st.text_input("Delivery Mode (e.g., Courier, Transport)")

# ------------------ Submit Order ------------------
if st.button("📤 Submit Order"):
    try:
        # <<< CHANGE START: This entire block is new. It replaces your old connection code.
        # This code connects to Google Sheets using the secrets you configured.
        scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

        # Check for secrets in Streamlit Cloud deployment
        if "gcp_service_account" in st.secrets:
            creds_json = st.secrets["gcp_service_account"]
        # Check for secrets in GitHub Actions deployment
        elif "GCP_CREDENTIALS" in os.environ:
            creds_json_str = os.environ["GCP_CREDENTIALS"]
            creds_json = json.loads(creds_json_str)
        # Fallback for local development
        else:
            try:
                # Use a specific filename for clarity
                creds_json = "google_service_account.json"
            except FileNotFoundError:
                st.error("Credentials file not found and secrets are not available.")
                st.stop()

        creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
        client = gspread.authorize(creds)
        # <<< CHANGE END

        

        # ✅ Save to Google Sheets
        # The OLD connection code that was here has been REMOVED and REPLACED above.
        sheet = client.open("ORDER FORM").sheet1  # Change to your Google Sheet name
        for product in products:
            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                salesperson_name,
                company,
                product["Product Type"],
                product["Specs"],
                product["Product Description"],
                product["Quantity"],
                product["Rate"],
                shipping_address,
                billing_address,
                delivery_mode
            ])

        st.success("✅ All products submitted and saved to Google Sheets successfully!")



    except Exception as e:
        st.error(f"❌ Error: {e}")


   
