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
"DEMOTIC HEALTHCARE PRIVATE LIMITED",
"Fermentis Life Science Pvt Ltd",
"FUELLED NUTRITION PRIVATE LIMITED-MP",
"Functional & Innovative Foods Private Limited",
"GAAEAWELLBEING PRIVATE LIMITED",
"GINNI FILAMENTS LIMITED (CPD-Haridwar)",
"Graphic World",
"GUARDIAN HEALTHCARE SERVICES PRIVATE LIMITED",
"GWELLTH FOODS AND BEVERAGES PRIVATE LIMITED",
"Humpty's",
"KEPRAN HEALTHCARE",
"MEXICO LABORATORIES CO.",
"MUSCLE MANTRA PROJECTS PVT LTD.",
"Musclemantra Ventures Private Limited",
"Nirvasa Healthcare Pvt. Ltd.",
"NUTRIBURST INDIA PRIVATE LIMITED",
"REBALA NUTRI FOODEE PVT LTD",
"RISE OF WINGS PRIVATE LIMITED",
"Roxor Life Long India Private Limited",
"SCYLENE WELLNESS PRIVATE LIMITED",
"Siemens Financial Services Private Limited",
"TEN ABZ SPORT NUTRITION",
"TITAN BIOTECH LIMTED",
"TRUSAN PRINTPACK PRIVATE LIMITED",
"VAIDYADEV AUSHIDHI",
"BUKALO INDIA PVT LTD",
"3S FITNESS TECHNOLOGIES PRIVATE LIMITED (Hr)",
"Acno Health",
"Aggarwal Pharmaceuticals",
"AG Organica Pvt. Ltd.",
"AGUSTO FORMULATIONS PVT LTD",
"AHPVITALS PRIVATE LIMITED",
"AIREN HERBALS",
"All Time Nutrition",
"AMAARA AYURVEDA",
"ANIHAC PHARMA",
"ASEAR HEALTHCARE PVT LTD",
"AUGUST ASSORTMENT PVT LTD",
"AURA GLOBE ENTERPRISES",
"AUREA BIOLABS PRIVATE LIMITED",
"AVEDA AYUR LLP",
"BALAJI CHEMICALS",
"Bhd Sales",
"Bili Life Science LLP",
"Bluebein Nutrix Pvt. Ltd.",
"BODY CORE SCIENCES",
"B.S.Reddy & Co",
"BYBV NUTRA LLP",
"CHABI ENTERPRISES PVT. LTD.",
"Core Nutrition Pvt Ltd",
"COST2COST NUTRACEUTICALS",
"CREAMY FOODS LIMTED",
"Daarvi Pharmaceuticals",
"DESFOC SOLUTION PVT LTD",
"DEV PRIYA INDUSTRIES PRIVATE LIMITED",
"Deyga Organics",
"DS ENTERPRISES",
"Dualshield Pvt.Ltd.",
"Elegant Nutra Private Limited",
"END2END Nutrition Pvt. Ltd.",
"FRISKA NUTRACEUTICALS PVT. LTD.",
"GALLBERRY LIFE SCIENCES PRIVATE LIMITED",
"GAP Sports",
"GHEPAN FOODS PRIVATE LIMITED",
"Gianna Agro Private Limited",
"GRAINBITE FOODS PRIVATE LIMITED",
"GRT NUTRITION",
"HEALTH HAWK NUTRITION",
"HEMBROS FOODS LLP",
"A G HERBAL",
"ALEO WORLD GYM",
"Bio Herbal Remedies Pvt Ltd",
"Bright Lifecare Pvt. Ltd.",
"Enhanced Labs",
"Fitshit Health Solutions Private Limited",
"FOREVER NUTRITION",
"GLOBAL HEALTHFIT RETAIL INDIA PVT LTD",
"Godara Nutrition Hub",
"GOODLUCK CHEMICALS WORKS",
"GURU MANN VENTURES PVT LTD",
"IMAGINE EYE",
"INVENTO BIOHEALTHTECH PRIVATE LIMITED",
"JAIN GARMENTS",
"LEREL HEALTH FOODS LLP",
"MIKIS SPECIALITIES PVT. LTD.",
"Monstabolic Nutrition Private Limited",
"MOTHERSENSE TECHNOLOGIES PRIVATE LIMITED",
"M/s Asap Print Tech",
"M/S HOLOSAFE SECURITY LABELS PVT.LTD.",
"NAMO AYURVEDA PRIVATE LIMITED",
"PS NUTBUTTER",
"SRI GANESH TRADERS",
"Stark Nutrition Pvt Ltd",
"Superchem Nutri Formulation",
"SYNERGIA PAC PRIVATE LIMITED",
"SYNERGIA PAC PVT. LTD. (Sales)",
"TRUE NUTRITION",
"Unbeaten Nutrition",
"HERCULES HEALTH CARES PVT LTD",
"Himanshu International",
"HOLISTIC NUTRITION",
"INSTANT REMEDIES PVT LTD",
"IRON ASTLUM",
"JOVEX INTERNATIONAL",
"Karriers Transport",
"Last 3 Feet Marketing Solutions Pvt Ltd",
"MAXNOVA HEALTHCARE",
"Medpro Biotech",
"MIND BODY",
"Monte Orleans Incorporation",
"MOSAIC WELLNESS PVT LTD",
"MPG BRANDS PRIVATE LIMITED",
"M/s Agnihotri S International",
"M/S DEVPRIYA PAPERS PVT. LTD.",
"M/s G.S. Pharmbutor Private Limited",
"M/S NUTRI WORLD",
"M/s Protein Basket",
"M/S. Siniki Seasoning",
"Mtj Grooming and Wellness Pvt. Ltd. (Bengaluru)",
"MUSCLE DOMINATOR PVT LTD",
"Muscle Store",
"MuscleUp-The Nutrition House",
"M V IMPEX",
"NANGLAMAL SUGAR COMPLEX",
"Natcon Biosciences Private Limited",
"NEORIGINS PVT LTD",
"N.G. Electro Products Pvt. Ltd",
"NIARA HEALTHCARE PVT LTD",
"Numix Industries Private Limited",
"NUTASTE FOOD AND DRINK LABS PVT LTD",
"NUTRIWELL LABORATORIES",
"NUTROSERVE CARE INDIA PRIVATE LIMITED",
"Om Plastic Industries",
"ORIGIN NUTRITION PRIVATE LIMITED",
"PACKRIGHTS TOTAL SOLUTION PVT LTD",
"PHARMAKON HEALTH AND BEAUTY PVT LTD",
"PHINATURALS NUTRITIONS INDIA PRIVATE LIMITED",
"PONTIKA AEROTECH LIMITED",
"PRAVEK KALP PRIVATE LIMITED",
"PURE SOURCE NUTRITION PVT .LTD",
"Quirky Beverages Private Limited",
"RAK FITNESS CONSUMER PRIVATE LIMITED",
"RMS HEALTHCARE",
"SACRED BEAST LLP",
"SAINAV HEALTHCARE",
"SAPIENS LABS",
"SHREEJI GRAPHICS",
"Sirona Hygiene Private Limited Hr",
"Soufflet Malt Alwar Pvt Ltd.",
"Sport Labs Nutrition",
"Sproutlife Foods Private Limited",
"S.S Labels",
"SUMATI PLASTIC PRIVATE LIMITED",
"SWASTHUM WELLNESS PVT LTD",
"Tactus Nutrasciences LLP",
"Tanvi Fitness Pvt Ltd.(Maharastra)",
"UMESH BAN RANA",
"Unived Healthcare Products Pvt. Ltd.",
"V Health Care Nutrition",
"VRS FOODS LIMITED UNIT III",
" Godara Nutrition Hub"
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
            item_name = st.selectbox(f"Item Name {i+1}", ["PP White", "PP Silver", "PP Clear", "Chromo Adhesive", "PE White", "Paper Silver", "Clear PET","PE 85"], key=f"item_{i}")
        with col2:
            finish = st.selectbox(f"Finish {i+1}", ["Gloss Varnish", "Matt Varnish", "Gloss Lamination", "Matt Lamination", "Matt Lamination + Spot UV","Gloss Lamination+SpotUV"], key=f"finish_{i}")
        specs = f"{item_name} - {finish}"

    elif product_type == "Laminates":
        col1, col2, col3 = st.columns(3)
        with col1:
            film_type = st.selectbox(f"Film Type {i+1}", ["12 Pet","18 Matte BOPP","18 BOPP","12 BOPP"], key=f"film_{i}")
        with col2:
            barrier_layer = st.selectbox(f"Barrier {i+1}", ["9 ALU", "12 METPET", "12 PET", "12 METPET/9 ALU","12 PET/9 ALU"], key=f"barrier_{i}")
        with col3:
            inner_layer = st.selectbox(f"Inner Layer {i+1}", ["50 LD","60 LD", "75 LD", "90 LD", "80 LD", "100 LD","110 LD","120 LD","140 LD"], key=f"inner_{i}")
        specs = f"{film_type} + {barrier_layer} + {inner_layer}"

    elif product_type == "3SS Pouch":
        col1,col2,col3,col4=st.columns(4)
        with col1:
            film_type=st.selectbox("Thickness",["12 Pet","18 Matte BOPP","18 BOPP","12 BOPP"], key=f"film_{i}")
        with col2:
            barrier_layer=st.selectbox("Barrier Layer",["9 ALU", "12 METPET", "12 PET", "12 METPET/9 ALU","12 PET/9 ALU"], key=f"barrier_{i}")
        with col3:
            inner_layer=st.selectbox("Inner Layer",["50 LD","90 Poly","60 LD","75 LD","80 LD","100 LD","110 LD","120 LD","140 LD"], key=f"inner_{i}")
        with col4:
            finish_type=st.selectbox("Finish",["Gloss Finish","Matte Finish","Matt Lamination + Spot UV","Gloss Lamination+SpotUV",""], key=f"finish_{i}")
        specs= f"{film_type} + {barrier_layer} + {inner_layer} + {finish_type}"

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
            film_type=st.selectbox("Thickness",["12 Pet","18 Matte BOPP","18 BOPP","12 BOPP"], key=f"film_{i}")
        with col2:
            barrier_layer=st.selectbox("Barrier Layer",["9 ALU", "12 METPET", "12 PET", "12 METPET/9 ALU","12 PET/9 ALU"], key=f"barrier_{i}")
        with col3:
            inner_layer=st.selectbox("Inner Layer",["50 LD","90 Poly","60 LD","75 LD","80 LD","100 LD","110 LD","120 LD","140 LD"], key=f"inner_{i}")
        with col4:
            finish_type=st.selectbox("Finish",["Gloss Finish","Matte Finish","Matt Lamination + Spot UV","Gloss Lamination+SpotUV",""], key=f"finish_{i}")
        specs= f"{film_type} + {barrier_layer} + {inner_layer} + {finish_type}"

    elif product_type=="Standup Pouch":
        col1,col2,col3,col4=st.columns(4)
        with col1:
            film_type=st.selectbox("Thickness",["12 Pet","18 Matte BOPP","18 BOPP","12 BOPP"], key=f"film_{i}")
        with col2:
            barrier_layer=st.selectbox("Barrier Layer", ["9 ALU", "12 METPET", "12 PET", "12 METPET/9 ALU","12 PET/9 ALU"], key=f"barrier_{i}")
        with col3:
            inner_layer=st.selectbox("Inner Layer", ["50 LD","90 Poly","60 LD","75 LD","80 LD","100 LD","110 LD","120 LD","140 LD"], key=f"inner_{i}")
        with col4:
            finish_type=st.selectbox("Finish", ["Gloss Finish","Matte Finish","Matt Lamination + Spot UV","Gloss Lamination+SpotUV",""], key=f"finish_{i}")
        specs=f"{film_type} + {barrier_layer} + {inner_layer} + {finish_type}"
    elif product_type=="Mono Carton":
        col1,col2,col3=st.columns(3)
        with col1:
            first_layer=st.selectbox("First Layer",["SBS 350", "SBS 300","330 FBB"], key=f"outer_{i}")
        with col2:
            second_layer=st.selectbox("Second Layer",["Matte Lamination", "Gloss Lamination","Matt Lamination + Spot UV","Gloss Lamination+SpotUV"],key=f"second_{i}")
        with col3:
            third_layer=st.selectbox("Third Layer",["Emboissing", "Emboissing + SpotUV", "Emboissing + SpotUV + Dripoff","Emboissing + SpotUV + Dripoff + Foiling","" ],key=f"third_{i}")
        spec=f"{first_layer} + {second_layer} + {third_layer}"
    
    elif product_type=="Composite Can":
        col1,col2,col3,col4 =st.columns(4)
        with col1:
            decoration=st.selectbox("Decoration",["Gloss Lamination", "Gloss lamination+ foiling ","Gloss lamination+ foiling+SpotUV ","Matte lamination","Matte lamination+ foiling", "Matte lamination + foiling + spotUV"],key=f"decoration_{i}")
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
import streamlit as st

vendor_list = sorted([
    "Wonderpac",
    "Bdot",
    "Synergia",
    "Spectal", 
    "Holosafe",
    "Hora art",
    "Swiss",
    "Shyam Flexi",
    "Canpack",
    "Start Pack",
    "Zoom Prints"
])

# Step 1: Add a blank option at the top
options = [""] + vendor_list + ["Other"]
selected_vendor = st.selectbox("Select Vendor", options)

# Step 2: Show text input if 'Other' is selected
custom_vendor = ""
if selected_vendor == "Other":
    custom_vendor = st.text_input("Enter Vendor Name")

# Step 3: Final vendor logic (blank by default)
if selected_vendor == "Other":
    vendor = custom_vendor.strip()
else:
    vendor = selected_vendor.strip()

# Just to show the selected or entered vendor
st.write("Final Vendor:", vendor if vendor else "Blank")


#PO NO.
po_number = st.text_area("PO NO.")

# Shared fields
shipping_address = st.text_area("Shipping Address")
billing_address = st.text_area("Billing Address")
delivery_mode = st.text_input("Delivery Mode (e.g., Courier, Transport)")

# ------------------ Submit Order ------------------
# ------------------ Submit Order ------------------
if st.button("📤 Submit Order"):
    try:
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # Load credentials
        if "gcp_service_account" in st.secrets:
            creds_json = st.secrets["gcp_service_account"]
        elif "GCP_CREDENTIALS" in os.environ:
            creds_json = json.loads(os.environ["GCP_CREDENTIALS"])
        else:
            with open("google_service_account.json") as f:
                creds_json = json.load(f)

        creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
        client = gspread.authorize(creds)

        # ✅ Open two different Google Sheets (two files)
        order_sheet = client.open("ORDER FORM").sheet1              # 1st file
        master_sheet = client.open("MASTER LOG SHEET").sheet1       # 2nd file

        # ✅ Save to both
        for product in products:
            row_data = [
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
                delivery_mode,
                po_number,
                vendor
            ]
            order_sheet.append_row(row_data)
            master_sheet.append_row(row_data)

        st.success("✅ All products submitted and saved to BOTH Google Sheet files successfully!")

    except Exception as e:
        st.error(f"❌ Error: {e}")



   
