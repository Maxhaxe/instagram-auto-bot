
import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Instagram Auto-Post Planner", layout="centered")

st.markdown("""
<style>
body {
    background-color: #121212;
    color: #ffffff;
}
.stApp {
    background-color: #121212;
}
.css-1v3fvcr {
    background-color: #121212;
}
</style>
"", unsafe_allow_html=True)

st.title("📸 Instagram Auto-Post Planner")

# Formulier om post toe te voegen
st.header("➕ Plan een nieuwe post")

with st.form("post_form", clear_on_submit=True):
    image = st.file_uploader("Upload een afbeelding", type=["jpg", "jpeg", "png"])
    caption = st.text_area("Bijschrift", max_chars=2200)
    schedule_time = st.datetime_input("Plan tijdstip", value=datetime.now() + timedelta(hours=1))
    submitted = st.form_submit_button("✅ Toevoegen aan planning")

    if submitted and image:
        save_path = os.path.join("assets", image.name)
        os.makedirs("assets", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(image.getbuffer())

        conn = sqlite3.connect("instagram_postplanner.db")
        c = conn.cursor()
        c.execute("INSERT INTO scheduled_posts (image_path, caption, scheduled_time) VALUES (?, ?, ?)",
                  (save_path, caption, schedule_time.strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        st.success("✅ Post succesvol gepland!")

# Overzicht van geplande posts
st.header("🗓️ Geplande posts")

conn = sqlite3.connect("instagram_postplanner.db")
c = conn.cursor()
c.execute("SELECT image_path, caption, scheduled_time, status FROM scheduled_posts ORDER BY scheduled_time ASC")
rows = c.fetchall()
conn.close()

if rows:
    for row in rows:
        img_path, cap, time_str, status = row
        st.image(img_path, width=300)
        st.markdown(f"**Bijschrift:** {cap}")
        st.markdown(f"🕒 Gepland voor: `{time_str}`")
        st.markdown(f"📌 Status: `{status}`")
        st.markdown("---")
else:
    st.info("Nog geen geplande posts.")
