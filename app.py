import streamlit as st  # 'i' சிறிய எழுத்தாக மாற்றப்பட்டது
import pandas as pd
from datetime import datetime

# --- ரகசிய பாஸ்வேர்டு ---
ADMIN_PASSWORD = "admintest@123"

# பக்க அமைப்பு
st.set_page_config(page_title="எங்கள் தெரு நிர்வாகம்", layout="wide")

# 1. டேட்டா மெமரி செட்டப் (Session State)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'announcement' not in st.session_state: st.session_state.announcement = "இன்று எந்த அறிவிப்பும் இல்லை."
if 'income_data' not in st.session_state: st.session_state.income_data = pd.DataFrame(columns=["தேதி", "பெயர்", "தொகை"])
if 'expense_data' not in st.session_state: st.session_state.expense_data = pd.DataFrame(columns=["தேதி", "விபரம்", "தொகை"])

# திருத்தம்: இங்கே tailor_data என்று சரியாக உள்ளது
if 'tailor_data' not in st.session_state: st.session_state.tailor_data = pd.DataFrame(columns=["பெயர்", "உயரம்", "மார்வளவு", "கை_நீளம்"])

if 'bday_members' not in st.session_state: st.session_state.bday_members = pd.DataFrame(columns=["பெயர்", "தொகை", "நிலை"])
if 'fest_members' not in st.session_state: st.session_state.fest_members = pd.DataFrame(columns=["விழா", "பெயர்", "தொகை", "நிலை"])
if 'complaints' not in st.session_state: st.session_state.complaints = pd.DataFrame(columns=["தேதி", "பெயர்", "புகார்", "நிலை"])
if 'contacts' not in st.session_state:
    st.session_state.contacts = pd.DataFrame([{"வேலை": "Electrician", "பெயர்": "குமார்", "எண்": "9876543210"}])

# --- லாகின் பக்கம் ---
if not st.session_state.logged_in:
    # வரி 27 திருத்தப்பட்டது: unsafe_allow_html=True
    st.markdown("<h2 style='text-align: center;'>🏘️ தெரு நண்பர்கள் நிர்வாகம் - லாகின்</h2>", unsafe_allow_html=True)
    with st.container():
        u_name = st.text_input("உங்கள் பெயர்")
        u_phone = st.text_input("தொலைபேசி எண் (10 இலக்கங்கள்)", max_chars=10)
        is_admin_req = st.checkbox("நான் ஒரு நிர்வாகி (Admin)")
        pass_input = st.text_input("நிர்வாகி கடவுச்சொல்", type="password") if is_admin_req else ""

        if st.button("உள்ளே நுழையவும்"):
            if u_name and len(u_phone) == 10:
                if is_admin_req and pass_input == ADMIN_PASSWORD:
                    st.session_state.is_admin, st.session_state.logged_in, st.session_state.user_name = True, True, u_name
                    st.rerun()
                elif is_admin_req and pass_input != ADMIN_PASSWORD:
                    st.error("தவறான நிர்வாகி கடவுச்சொல்!")
                else:
                    st.session_state.logged_in, st.session_state.user_name = True, u_name
                    st.rerun()
            else: st.error("பெயர் மற்றும் சரியான போன் எண் தேவை.")
    st.stop()

# --- மெயின் ஆப் பகுதி ---
st.sidebar.title(f"செல்வம் {st.session_state.user_name}!")
st.sidebar.write(f"அந்தஸ்து: {'👑 தலைவர்' if st.session_state.is_admin else '👤 உறுப்பினர்'}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# 📢 அறிவிப்புப் பலகை
st.info(f"📢 **முக்கிய அறிவிப்பு:** {st.session_state.announcement}")
if st.session_state.is_admin:
    with st.expander("📝 அறிவிப்பை மாற்ற (நிர்வாகி மட்டும்)"):
        new_msg = st.text_area("செய்தியை உள்ளிடவும்:", value=st.session_state.announcement)
        if st.button("Update Notice"):
            st.session_state.announcement = new_msg
            st.rerun()

# --- டேப்கள் (Tabs) ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💰 நிதி", "📐 அளவுகள்", "🎂 பிறந்தநாள்", "🎉 விழாக்கள்", "📩 புகார்", "📞 தொடர்புகள்"])

# 1. நிதி
with tab1:
    st.subheader("வரவு - செலவு கணக்கு")
    c1, c2 = st.columns(2)
    with c1:
        with st.form("inc_f"):
            amt = st.number_input("வசூல் தொகை (₹)", min_value=0)
            if st.form_submit_button("பதிவு செய்"):
                new_in = {"தேதி": str(datetime.now().date()), "பெயர்": st.session_state.user_name, "தொகை": amt}
                st.session_state.income_data = pd.concat([st.session_state.income_data, pd.DataFrame([new_in])], ignore_index=True)
                st.success("வசூல் சேமிக்கப்பட்டது!")
    with c2:
        if st.session_state.is_admin:
            with st.form("exp_f"):
                e_desc = st.text_input("செலவு விபரம்")
                e_amt = st.number_input("செலவு தொகை (₹)", min_value=0)
                if st.form_submit_button("கழித்துவிடு"):
                    new_ex = {"தேதி": str(datetime.now().date()), "விபரம்": e_desc, "தொகை": e_amt}
                    st.session_state.expense_data = pd.concat([st.session_state.expense_data, pd.DataFrame([new_ex])], ignore_index=True)
                    st.warning("செலவு கழிக்கப்பட்டது!")
    
    bal = st.session_state.income_data['தொகை'].sum() - st.session_state.expense_data['தொகை'].sum()
    st.metric("கையிருப்பு (Balance)", f"₹ {bal}")

# 2. தையல் அளவுகள் (திருத்தப்பட்டது)
with tab2:
    st.subheader("தையல் அளவுகள்")
    with st.form("tailor"):
        h, c, hl = st.text_input("உயரம்"), st.text_input("மார்பளவு"), st.text_input("கை நீளம்")
        if st.form_submit_button("அளவைச் சேமி"):
            new_t = {"பெயர்": st.session_state.user_name, "உயரம்": h, "மார்பளவு": c, "கை_நீளம்": hl}
            # பிழை திருத்தம்: tailor_data
            st.session_state.tailor_data = pd.concat([st.session_state.tailor_data, pd.DataFrame([new_t])], ignore_index=True)
            st.success("அளவு சேமிக்கப்பட்டது!")
    st.table(st.session_state.tailor_data)

# 3 & 4. விழாக்கள் நிதி
def money_tracker(df_key, title):
    st.subheader(title)
    with st.form(f"form_{df_key}"):
        amt = st.number_input("தொகை (₹)", min_value=0)
        if st.form_submit_button("சமர்ப்பி"):
            new_r = {"பெயர்": st.session_state.user_name, "தொகை": amt, "நிலை": "Pending"}
            if df_key == 'bday': 
                st.session_state.bday_members = pd.concat([st.session_state.bday_members, pd.DataFrame([new_r])], ignore_index=True)
            else: 
                st.session_state.fest_members = pd.concat([st.session_state.fest_members, pd.DataFrame([new_r])], ignore_index=True)
    
    df = st.session_state.bday_members if df_key == 'bday' else st.session_state.fest_members
    for idx, row in df.iterrows():
        c1, c2, c3 = st.columns([3, 2, 2])
        c1.write(f"👤 {row['பெயர்']} - ₹{row['தொகை']}")
        c2.write(f"நிலை: {row['நிலை']}")
        if st.session_state.is_admin and row['நிலை'] == "Pending":
            if c3.button("Confirm ✅", key=f"{df_key}_{idx}"):
                if df_key == 'bday': st.session_state.bday_members.at[idx, 'நிலை'] = "Paid"
                else: st.session_state.fest_members.at[idx, 'நிலை'] = "Paid"
                st.rerun()

with tab3: money_tracker('bday', "🎂 பிறந்தநாள் நிதி")
with tab4: money_tracker('fest', "🎉 விழாக்கள் நிதி")

# 5. புகார் பெட்டி
with tab5:
    st.subheader("📩 புகார் பெட்டி")
    with st.form("comp"):
        msg = st.text_area("புகாரை எழுதவும்:")
        if st.form_submit_button("அனுப்பு"):
            new_c = {"தேதி": str(datetime.now().date()), "பெயர்": st.session_state.user_name, "புகார்": msg, "நிலை": "New"}
            st.session_state.complaints = pd.concat([st.session_state.complaints, pd.DataFrame([new_c])], ignore_index=True)
            st.success("அனுப்பப்பட்டது!")
    if st.session_state.is_admin:
        st.write("---")
        st.dataframe(st.session_state.complaints)

# 6. தொடர்புகள்
with tab6:
    st.subheader("📞 முக்கியத் தொடர்புகள்")
    if st.session_state.is_admin:
        with st.form("con"):
            j, n, p = st.text_input("பிரிவு"), st.text_input("பெயர்"), st.text_input("எண்")
            if st.form_submit_button("சேமி"):
                st.session_state.contacts = pd.concat([st.session_state.contacts, pd.DataFrame([{"வேலை": j, "பெயர்": n, "எண்": p}])], ignore_index=True)
    st.table(st.session_state.contacts)
