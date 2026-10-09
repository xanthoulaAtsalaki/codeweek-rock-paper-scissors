
import streamlit as st
import random

st.set_page_config(page_title="Can You Beat the AI?", page_icon="🎮")

moves = ["πέτρα", "ψαλίδι", "χαρτί"]
emojis = {"πέτρα": "🪨", "ψαλίδι": "✂️", "χαρτί": "📄"}
beats = {"πέτρα": "ψαλίδι", "ψαλίδι": "χαρτί", "χαρτί": "πέτρα"}
counter = {"πέτρα": "χαρτί", "ψαλίδι": "πέτρα", "χαρτί": "ψαλίδι"}

def new_game():
    st.session_state.history = []
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.ties = 0
    st.session_state.finished = False
    st.session_state.result = ""

if "history" not in st.session_state:
    new_game()

st.title("🎮 Can You Beat the AI?")
st.write("Πέτρα – Ψαλίδι – Χαρτί")
st.write("🏆 Κερδίζει όποιος φτάσει πρώτος στις 7 νίκες!")

mode = st.radio("Διάλεξε αντίπαλο:", ["Random Bot", "AI Bot"])

player = st.radio(
    "Διάλεξε την κίνησή σου:",
    moves,
    format_func=lambda x: emojis[x] + " " + x
)

st.subheader("🏆 Βαθμολογία")
c1, c2, c3 = st.columns(3)
c1.metric("Εσύ", st.session_state.player_score)
c2.metric("Υπολογιστής", st.session_state.computer_score)
c3.metric("Ισοπαλίες", st.session_state.ties)

if not st.session_state.finished:
    if st.button("▶️ ΠΑΙΞΕ!", use_container_width=True):
        history = st.session_state.history

        if mode == "Random Bot" or len(history) < 3:
            computer = random.choice(moves)
            prediction = None
        else:
            prediction = max(moves, key=history.count)
            computer = counter[prediction]

        if player == computer:
            message = "🤝 Ισοπαλία!"
            st.session_state.ties += 1
        elif beats[player] == computer:
            message = "🎉 Κέρδισες τον γύρο!"
            st.session_state.player_score += 1
        else:
            message = "🤖 Κέρδισε ο υπολογιστής!"
            st.session_state.computer_score += 1

        history.append(player)

        st.session_state.result = (
            f"Εσύ: {emojis[player]} {player}\n\n"
            f"Υπολογιστής: {emojis[computer]} {computer}\n\n"
            f"{message}"
        )

        if prediction is not None:
            st.session_state.result += (
                f"\n\nΤο AI προέβλεψε: {prediction}"
            )

        if (st.session_state.player_score == 7 or
                st.session_state.computer_score == 7):
            st.session_state.finished = True

    if st.button("⏹️ STOP – Τέλος παιχνιδιού"):
        st.session_state.finished = True

if st.session_state.result:
    st.info(st.session_state.result)

if st.session_state.finished:
    st.header("🏁 ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ")
    st.write("Νίκες παίκτη:", st.session_state.player_score)
    st.write("Νίκες υπολογιστή:", st.session_state.computer_score)

    if st.session_state.player_score == 7:
        st.success("🏆 Συγχαρητήρια! Νίκησες!")
    elif st.session_state.computer_score == 7:
        st.error("🤖 Νικητής είναι ο υπολογιστής!")
    else:
        st.write("Το παιχνίδι διακόπηκε.")

st.subheader("📊 Ιστορικό κινήσεων")
for move in moves:
    st.write(emojis[move], move, ":", st.session_state.history.count(move))

if st.button("🔄 Νέο παιχνίδι"):
    new_game()
    st.rerun()

st.caption("EU Code Week 2026 – 5ο Γυμνάσιο Ηρακλείου")
