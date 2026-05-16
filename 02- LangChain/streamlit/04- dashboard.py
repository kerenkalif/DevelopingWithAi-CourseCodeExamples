import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    # ── Sidebar ───────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.title("⚙️ הגדרות")
        st.divider()

        selected_year = st.selectbox("שנה", [2022, 2023, 2024], index=2)
        selected_region = st.multiselect(
            "אזורים",
            ["צפון", "דרום", "מרכז", "חיפה"],
            default=["צפון", "מרכז"]
        )
        show_forecast = st.toggle("הצג תחזית", value=True)
        st.divider()
        st.metric("סה״כ לקוחות", "1,248", "+12%")
        st.metric("עסקאות פתוחות", "34", "-5")

    # ── Generate fake data ────────────────────────────────────────────────────────
    np.random.seed(42)
    dates = [datetime(selected_year, 1, 1) + timedelta(days=i) for i in range(365)]
    df = pd.DataFrame({
        "date":   dates,
        "sales":  np.random.normal(50000, 8000, 365).cumsum(),
        "leads":  np.random.randint(10, 80, 365),
        "region": np.random.choice(["צפון", "דרום", "מרכז", "חיפה"], 365),
    })
    df_filtered = df[df["region"].isin(selected_region)] if selected_region else df

    # ── Title ─────────────────────────────────────────────────────────────────────
    st.title("📊 דשבורד מכירות")
    st.caption(f"נתוני {selected_year} | עודכן: {datetime.now().strftime('%H:%M')}")

    # ── KPI row ───────────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 הכנסות", "₪2.4M", "+18%")
    col2.metric("🛒 עסקאות", "847",   "+7%")
    col3.metric("👥 לקוחות חדשים", "213", "-3%")
    col4.metric("⭐ שביעות רצון", "4.7/5", "+0.2")

    st.divider()

    # ── Tabs ──────────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📈 מגמות", "🗺️ אזורים", "🔍 פירוט"])

    with tab1:
        left, right = st.columns([2, 1])

        with left:
            # Line chart with Plotly
            monthly = df_filtered.groupby(df_filtered["date"].dt.month)["sales"].sum().reset_index()
            monthly.columns = ["month", "sales"]

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=monthly["month"], y=monthly["sales"],
                mode="lines+markers",
                name="מכירות בפועל",
                line=dict(color="#009688", width=3),
                fill="tozeroy", fillcolor="rgba(0,150,136,0.1)"
            ))
            if show_forecast:
                forecast = monthly["sales"] * np.random.uniform(1.05, 1.15, len(monthly))
                fig_line.add_trace(go.Scatter(
                    x=monthly["month"], y=forecast,
                    mode="lines", name="תחזית",
                    line=dict(color="#FFD54F", width=2, dash="dash")
                ))
            fig_line.update_layout(
                title="מכירות לפי חודש",
                xaxis_title="חודש", yaxis_title="₪",
                plot_bgcolor="white", height=350
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with right:
            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=78,
                delta={"reference": 70},
                title={"text": "יעד שנתי (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar":  {"color": "#009688"},
                    "steps": [
                        {"range": [0, 50],  "color": "#FFEBEE"},
                        {"range": [50, 75], "color": "#FFF9C4"},
                        {"range": [75, 100],"color": "#E8F5E9"},
                    ],
                    "threshold": {
                        "line": {"color": "#E53935", "width": 4},
                        "thickness": 0.75, "value": 90
                    }
                }
            ))
            fig_gauge.update_layout(height=350)
            st.plotly_chart(fig_gauge, use_container_width=True)

        # Bar chart
        weekly = df_filtered.groupby(df_filtered["date"].dt.isocalendar().week)["leads"].mean().reset_index()
        weekly.columns = ["week", "leads"]
        fig_bar = px.bar(weekly.head(20), x="week", y="leads",
                        title="ממוצע לידים שבועי",
                        color="leads", color_continuous_scale="Teal")
        fig_bar.update_layout(height=280)
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        left2, right2 = st.columns(2)

        with left2:
            region_sales = df.groupby("region")["sales"].sum().reset_index()
            fig_pie = px.pie(region_sales, values="sales", names="region",
                            title="חלוקת מכירות לפי אזור",
                            color_discrete_sequence=px.colors.sequential.Teal)
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

        with right2:
            fig_box = px.box(df, x="region", y="leads",
                            title="פיזור לידים לפי אזור",
                            color="region",
                            color_discrete_sequence=px.colors.sequential.Teal)
            fig_box.update_layout(height=400)
            st.plotly_chart(fig_box, use_container_width=True)

    with tab3:
        search = st.text_input("🔍 חפש לפי אזור")
        df_show = df[df["region"].str.contains(search)] if search else df

        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.dataframe(
                df_show[["date", "region", "sales", "leads"]].head(50),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "date":   st.column_config.DateColumn("תאריך"),
                    "sales":  st.column_config.NumberColumn("מכירות", format="₪%d"),
                    "leads":  st.column_config.ProgressColumn("לידים", max_value=80),
                    "region": "אזור",
                }
            )
        with col_b:
            st.subheader("סטטיסטיקות")
            st.write(df_show["sales"].describe().rename({
                "mean": "ממוצע", "std": "סטיית תקן",
                "min": "מינימום", "max": "מקסימום"
            }))

    # ── Expander ──────────────────────────────────────────────────────────────────
    with st.expander("📋 הצג נתונים גולמיים"):
        st.dataframe(df_filtered.head(20), use_container_width=True)
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ הורד CSV", csv, "sales_data.csv", "text/csv")
except Exception as e:
    st.exception(e)