import streamlit as st
from groq import Groq

st.set_page_config(page_title="Spotify Discovery Companion", page_icon="🎶")
st.title("🎶 Spotify Discovery Companion")
st.markdown("*Tell me where you are musically — I'll show you where to go next.*")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Right now")
    mood = st.text_area("How are you feeling?", height=90,
        placeholder="Tired but need energy, nostalgic, anxious and need to focus...")
    recent = st.text_area("What have you been listening to?", height=90,
        placeholder="Stuck on Arctic Monkeys and sad indie for weeks...")
with col2:
    st.subheader("Where you want to go")
    goal = st.selectbox("Discovery goal:", [
        "Something new but still familiar",
        "Take me somewhere completely different",
        "Same vibe, different artists — I'm bored",
        "Match my mood more precisely",
        "Explore a genre I know nothing about"
    ])
    desired = st.text_area("What do you want to feel?", height=90,
        placeholder="Motivated but calm, euphoric, like I'm in a film...")

extra = st.text_input("Anything else? (optional)",
    placeholder="No heavy bass / need no lyrics for work / only 90s music...")

if st.button("🎯 Find My Discovery Path", type="primary", use_container_width=True):
    if not mood or not recent or not desired:
        st.warning("Please fill in your mood, recent listening, and desired feeling.")
    else:
        with st.spinner("Building your personal discovery path..."):
            prompt = (
                "You are a music discovery guide helping a Spotify user break out of their listening bubble.\n\n"
                f"Current mood: {mood}\n"
                f"Recent listening: {recent}\n"
                f"Discovery goal: {goal}\n"
                f"Desired feeling: {desired}\n"
                f"Extra context: {extra if extra else 'None'}\n\n"
                "Give them:\n"
                "1. A brief empathetic acknowledgment of where they are musically (1-2 sentences)\n"
                "2. A Discovery Path - 5 specific real songs with artist names bridging from their current listening to their desired feeling. For each: title + artist, why it bridges the gap (1 sentence), what to listen for (1 sentence)\n"
                "3. A creative name for this discovery path\n"
                "4. 3 questions to ask themselves while listening\n"
                "5. One Spotify search term to keep exploring\n\n"
                "Be specific with real songs. Explain the emotional and sonic bridge."
            )

            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                st.markdown("---")
                st.subheader("🗺️ Your Personal Discovery Path")
                st.markdown(chat.choices[0].message.content)
                st.markdown("---")
                st.info("💡 **Why this works differently than Spotify's algorithm:** This understands your emotional context and desired state — not just your listening history.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Built to solve Spotify's discovery problem: the algorithm knows your past. This knows your now.")
