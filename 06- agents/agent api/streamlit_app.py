# streamlit run streamlit_app.py
# http://localhost:8501

import streamlit as st
import requests

AGENT_URL = "http://localhost:7777/agents/StockAnalyst/runs"

st.title("📈 Stock Analyst Agent")
st.caption("מופעל דרך AgentOS API")

if st.button("נתח מניות עכשיו", type="primary"):
    with st.spinner("הסוכן מנתח..."):
        try:
            response = requests.post(
                AGENT_URL,
                data={
                    "message": "Analyze stocks now.",
                    "stream": "false",
                },
            )
            response.raise_for_status()
            result = response.json()

            # תשובת הסוכן נמצאת ב- content
            content = result.get("content", "")
            if content:
                st.success("ניתוח הושלם")
                st.write(content)
            else:
                st.json(result)  # fallback — מראה את כל ה-response

        except requests.exceptions.ConnectionError:
            st.error("לא ניתן להתחבר לשרת. האם agent_os_app.py רץ?")
        except Exception as e:
            st.error(f"שגיאה: {e}")
