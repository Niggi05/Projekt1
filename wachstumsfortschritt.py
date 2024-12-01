import streamlit as st
from PIL import Image, ImageDraw
import datetime

def get_growth_data(week):
    growth_per_week = [0, 1, 3, 5, 8, 12, 15, 20, 25, 30, 35, 40]  # Wachstum in cm
    if week < len(growth_per_week):
        return growth_per_week[week - 1]
    else:
        return growth_per_week[-1]  # Maximale Höhe nach Woche 12 (30-40 cm)

def create_growth_image(plant_height_cm):
    img_size = (150, 300)
    img = Image.new('RGB', img_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    plant_height_pixels = int(plant_height_cm * 7)  # Skalierung von cm zu Pixeln
    plant_position = (50, img_size[1] - plant_height_pixels)
    draw.rectangle([plant_position, (100, img_size[1])], fill="green")
    return img

def create_finished_image():
    plant_height_cm = 40
    return create_growth_image(plant_height_cm)

def categorize_level(level):
    """Funktion zur Kategorisierung der Level"""
    if level <= 2:
        return "Anfänger Gärtner 🌱"
    elif level <= 4:
        return "Fortgeschrittener Gärtner 🌿"
    elif level <= 6:
        return "Profi Gärtner 🌳"
    else:
        return "Meister Gärtner 🌟"

def app():
    if "component_status" not in st.session_state:
        st.session_state.component_status = {}

    if "level" not in st.session_state:
        st.session_state.level = 0

    st.sidebar.header(f"Level: {st.session_state.level} ({categorize_level(st.session_state.level)})")

    if "history" not in st.session_state:
        st.session_state.history = []

    if "plant_date" not in st.session_state:
        st.session_state.plant_date = datetime.date.today()
        st.session_state.weeks_passed = 0

    plant_date = st.date_input("Wann hast du die Lauchzwiebeln gepflanzt?", st.session_state.plant_date)

    today = datetime.date.today()
    weeks_passed = (today - plant_date).days // 7

    if weeks_passed < 1:
        weeks_passed = 1

    if plant_date != st.session_state.plant_date:
        st.session_state.plant_date = plant_date
        st.session_state.weeks_passed = 0

    st.session_state.weeks_passed = weeks_passed

    plant_height_cm = get_growth_data(weeks_passed)

    growth_image = create_growth_image(plant_height_cm)
    finished_image = create_finished_image()

    col1, col2 = st.columns(2)

    with col1:
        st.image(growth_image, caption=f"Wachstumsfortschritt der Lauchzwiebel: Woche {weeks_passed}", width=150)
        st.write(f"Die Pflanze ist aktuell {plant_height_cm} cm hoch.")
    
    with col2:
        st.image(finished_image, caption="Fertige Lauchzwiebel (maximale Größe: 40 cm)", width=150)
        st.write("Die Lauchzwiebel ist in Woche 12 vollständig gewachsen.")

    st.subheader(f"Aktuelle Woche: {weeks_passed}")
    st.write(f"Die Lauchzwiebel wächst in Woche {weeks_passed} und ist derzeit {plant_height_cm} cm groß.")

    if weeks_passed >= 12:
        st.warning("⚠️ Die Lauchzwiebel ist jetzt bereit zur Ernte! 🌾")

    if st.button("Ernten! 🌾"):
        st.success("🎉 Herzlichen Glückwunsch! Du hast erfolgreich geerntet! 🎉")
        st.balloons()
        st.write("Du erhältst 10 Punkte für deine erfolgreiche Ernte! Weiter so! 🚀")
        
        # Historische Daten aktualisieren
        harvest_info = {
            "plant_date": st.session_state.plant_date,
            "harvest_date": today,
            "plant_height_cm": plant_height_cm,
            "status": "Geerntet"
        }
        st.session_state.history.append(harvest_info)

        # Level erhöhen
        previous_level = st.session_state.level
        st.session_state.level += 1
        new_category = categorize_level(st.session_state.level)

        # Überprüfen, ob eine neue Kategorie erreicht wurde
        if categorize_level(previous_level) != new_category:
            st.write(f"🚀 Glückwunsch! Du bist jetzt {new_category}!")

    if st.session_state.history:
        st.subheader("📜 Historische Anbaudaten")
        for record in st.session_state.history:
            st.write(f"🌱 Pflanzdatum: {record['plant_date']} | Erntedatum: {record['harvest_date']} | Höhe: {record['plant_height_cm']} cm | Status: {record['status']}")

if __name__ == "__main__":
    app()
