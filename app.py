import streamlit as st
from audio_recorder_streamlit import audio_recorder
from speech_to_text import transcribe_audio
from meeting_agent import generate_summary
from late_join import generate_late_join_catchup
from decision_detector import detect_decisions
from hindsight_memory import save_meeting_memory, recall_meeting_memory
from change_detector import detect_changes


st.set_page_config(
    page_title="MeetingHindsight",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MeetingHindsight")
st.subheader("AI Meeting Intelligence Agent")

st.write(
    "Understand meetings, catch up when you join late, "
    "remember important decisions, and detect what changed."
)

st.divider()

# Meeting transcript
st.header("🎙️ Meeting Transcript")

st.write("🎤 Record the meeting conversation")

audio = audio_recorder(
    text="Click to record",
    recording_color="#ff4b4b",
    neutral_color="#6c757d",
    icon_name="microphone",
    icon_size="2x",
)

transcript = ""

if audio:
    st.audio(audio, format="audio/wav")

    with st.spinner("🎙️ Converting meeting speech to text..."):
        transcript = transcribe_audio(audio)
        if transcript.strip():
           st.session_state.previous_meeting = st.session_state.current_meeting
           st.session_state.current_meeting = transcript

    st.subheader("📝 Meeting Transcript")
    st.write(transcript)

# Five features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎙️ Summary",
    "⚡ Late Join",
    "✅ Decisions",
    "🧠 Hindsight Memory",
    "🔄 What Changed?"
])


# FEATURE 1
with tab1:
    st.header("🎙️ Live Meeting Summary")

    if st.button("Generate Summary"):
        if transcript.strip():
            with st.spinner("Analyzing meeting..."):
                result = generate_summary(transcript)

            st.write(result)
        else:
            st.warning("Please enter a meeting transcript.")


# FEATURE 2
with tab2:
    st.header("⚡ Late-Join Catch-Up")

    st.write(
        "See what happened before a participant joined the meeting."
    )

    if st.button("Generate Catch-Up"):
        if transcript.strip():
            with st.spinner("Preparing catch-up..."):
                result = generate_late_join_catchup(transcript)

            st.write(result)
        else:
            st.warning("Please enter a meeting transcript.")


# FEATURE 3
with tab3:
    st.header("✅ Decision Detection")

    if st.button("Detect Decisions"):
        if transcript.strip():
            with st.spinner("Finding confirmed decisions..."):
                result = detect_decisions(transcript)

            st.write(result)
        else:
            st.warning("Please enter a meeting transcript.")


# FEATURE 4
query = st.text_input(
    "Ask the meeting memory:",
    placeholder="What decisions were made about the demo?"
)

if st.button("Recall Memory"):
    if query.strip():
        with st.spinner("Searching Hindsight memory..."):
            result = recall_meeting_memory(query)

        st.text(str(result))
    else:
        st.warning("Enter a question first.")


# FEATURE 5
with tab5:
    st.header("🔄 What Changed?")

    if "previous_meeting" not in st.session_state:
        st.session_state.previous_meeting = ""

    if "current_meeting" not in st.session_state:
        st.session_state.current_meeting = ""

    st.write("Previous meeting:")
    if st.session_state.previous_meeting:
        st.info(st.session_state.previous_meeting)
    else:
        st.info("No previous meeting recorded yet.")

    st.write("Current meeting:")
    if st.session_state.current_meeting:
        st.info(st.session_state.current_meeting)
    else:
        st.info("No current meeting recorded yet.")

    if st.button("Compare Meetings"):
        if st.session_state.previous_meeting and st.session_state.current_meeting:
            with st.spinner("Detecting changes..."):
                result = detect_changes(
                    st.session_state.previous_meeting,
                    st.session_state.current_meeting
                )
            st.write(result)
        else:
            st.warning("Record at least two meetings first.")