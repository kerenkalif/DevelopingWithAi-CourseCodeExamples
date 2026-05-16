import streamlit as st
import requests
from langchain_core.tools import tool
from langchain.agents import create_agent

# ─── Tools (זהים לקובץ המקורי) ───────────────────────────────────────────────
@tool
def get_current_location():
    """Returns user current geographic location according to its ip."""
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            return {"city": data["city"], "country": data["country"],
                    "lat": data["lat"], "lon": data["lon"]}
    except Exception as e:
        return f"Error detecting location: {e}"

@tool
def get_coordinates(city_name: str, country_name: str = ""):
    """Gets city name and country, returns its coordinates."""
    try:
        query = f"{city_name}, {country_name}" if country_name else city_name
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&language=en&format=json"
        data = requests.get(url).json()
        if "results" in data and data["results"]:
            r = data["results"][0]
            return {"lat": r["latitude"], "lon": r["longitude"],
                    "full_name": f"{r.get('name')}, {r.get('country')}"}
        return "Location not found."
    except Exception as e:
        return f"Error: {e}"

@tool
def get_weather_in_location(lat: float, lon: float) -> float:
    """Returns current temperature according to coordinate."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        data = requests.get(url).json()
        return data["current_weather"]["temperature"]
    except Exception as e:
        return f"Error: {e}"

# ─── Agent (נטען פעם אחת, נשמר ב-cache) ─────────────────────────────────────
@st.cache_resource
def get_agent():
    return create_agent(
        model="claude-sonnet-4-6",
        tools=[get_current_location, get_coordinates, get_weather_in_location],
        system_prompt="You are a helpful weather assistant. Use the tools to answer.",
    )

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Weather Assistant", page_icon="🌤️", layout="wide")

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🌤️ Weather Assistant")
    st.divider()

    st.subheader("🔧 כלים זמינים")
    st.info("📍 **get_current_location**\nזיהוי מיקום לפי IP")
    st.info("🗺️ **get_coordinates**\nמציאת קואורדינטות לפי עיר")
    st.info("🌡️ **get_weather_in_location**\nטמפרטורה לפי קואורדינטות")

    st.divider()
    st.subheader("💡 שאלות לדוגמה")
    examples = [
        "What is the temperature at my place?",
        "How warm is it in London right now?",
        "Compare the temperature in Tel Aviv and Paris",
        "Is it warmer in Tokyo or New York?",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_prompt = example

    st.divider()
    if st.button("🗑️ נקה שיחה", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ─── Main ─────────────────────────────────────────────────────────────────────
st.title("🌤️ Weather Assistant")
st.caption("סוכן AI שמשתמש ב-3 כלים כדי לענות על שאלות מזג אוויר")

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "tools_used" in msg and msg["tools_used"]:
            with st.expander(f"🔧 כלים שהופעלו ({len(msg['tools_used'])})"):
                for tool_call in msg["tools_used"]:
                    st.code(tool_call, language="text")

# Handle input — either from chat_input or sidebar button
prompt = st.chat_input("שאל שאלה על מזג האוויר...")
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("מפעיל כלים..."):
            agent  = get_agent()
            result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

        # Extract final answer
        final_answer = result["messages"][-1].content
        st.write(final_answer)

        # Extract tool calls from intermediate messages
        tools_used = []
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tools_used.append(f"🔧 {tc['name']}({tc['args']})")
            if hasattr(msg, "type") and msg.type == "tool":
                tools_used.append(f"   ↳ תוצאה: {msg.content}")

        if tools_used:
            with st.expander(f"🔧 כלים שהופעלו ({len([t for t in tools_used if t.startswith('🔧')])})", expanded=False):
                for line in tools_used:
                    st.text(line)

    st.session_state.messages.append({
        "role": "assistant",
        "content": final_answer,
        "tools_used": tools_used
    })
    st.rerun()