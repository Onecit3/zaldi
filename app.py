import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA Y TEMA ---
st.set_page_config(
    page_title="Zaldívar IPSC Monitor",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS AVANZADOS (Soporte Dark/Light) ---
st.markdown("""
<style>
    /* Variables CSS para paleta moderna */
    :root {
        --primary: #3b82f6;
        --success: #10b981;
        --danger: #ef4444;
        --neutral: #64748b;
    }

    /* Tarjetas de Métricas */
    div[data-testid="metric-container"] {
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: var(--primary);
    }

    /* Expanders (Tarjetas) personalizadas */
    .streamlit-expanderHeader {
        background-color: rgba(128, 128, 128, 0.05) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    /* Badges personalizados para Master/Peer */
    .badge-master {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-peer {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    file_path = "Sistema_Radio_Completo.xlsx"  # Asegúrate de tener el archivo
    try:
        df = pd.read_excel(file_path, header=3)
        df = df.dropna(subset=['ID'])
        df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)

        def get_system(id_val):
            if 100 <= id_val < 200:
                return "Prevención - Negrillar"
            elif 200 <= id_val < 300:
                return "Apilado"
            elif 400 <= id_val < 500:
                return "Planta"
            elif 500 <= id_val < 600:
                return "Mina"
            elif 600 <= id_val < 700:
                return "ZALOTRC"
            return "Otros"

        df['Sistema_Logico'] = df['ID'].apply(get_system)
        return df
    except Exception as e:
        return pd.DataFrame()


df = load_data()

if df.empty:
    st.error("No se encontraron datos. Sube el archivo Excel.")
    st.stop()

# --- HEADER ---
st.title("📡 Minera Zaldívar")
st.caption("Monitor de Infraestructura de Radio | IP Site Connect")
st.divider()

# --- KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sistemas", df['Sistema_Logico'].nunique(), delta_color="off")
col2.metric("Sitios Físicos", df['Cerro'].nunique(), delta_color="off")
col3.metric("Total Radios", len(df), delta_color="normal")
col4.metric("Gateway", "10.70.140.1")

st.markdown("###")  # Espaciador

# --- CONTENIDO ---
tabs = st.tabs(["🌐 Vista Lógica", "🏔️ Vista Física", "📊 Matriz"])

# 1. VISTA LÓGICA
with tabs[0]:
    systems = sorted(df['Sistema_Logico'].unique())
    # Grid adaptativo
    cols = st.columns(3)

    for i, sys in enumerate(systems):
        with cols[i % 3]:
            sub_df = df[df['Sistema_Logico'] == sys]
            master = sub_df[sub_df['Tipo Vinculo'].str.contains("Master", na=False)]
            master_loc = master.iloc[0]['Cerro'] if not master.empty else "N/A"

            with st.expander(f"{sys}", expanded=True):
                st.markdown(f"**Master:** `{master_loc}`")

                # Tabla formateada
                display_df = sub_df[['Cerro', 'ID', 'IP Ethernet', 'Tipo Vinculo']].copy()


                # Formateo visual de la tabla (Highlights)
                def color_role(val):
                    color = '#ef4444' if 'Master' in val else '#10b981'  # Red/Green
                    return f'color: {color}; font-weight: bold'


                st.dataframe(
                    display_df.style.applymap(color_role, subset=['Tipo Vinculo']),
                    use_container_width=True,
                    hide_index=True
                )

# 2. VISTA FÍSICA
with tabs[1]:
    for site, sub_df in df.groupby('Cerro'):
        with st.expander(f"📍 {site} ({len(sub_df)} dispositivos)", expanded=False):
            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown("**Sistemas Aloja:**")
                for s in sub_df['Sistema_Logico'].unique():
                    st.markdown(f"- {s}")
            with c2:
                st.dataframe(
                    sub_df[['Sistema_Logico', 'Alias', 'IP Ethernet', 'RX (MHz)']],
                    hide_index=True,
                    use_container_width=True
                )

# 3. MATRIZ SIMPLE
with tabs[2]:
    st.markdown("##### Matriz de Cobertura")
    pivot = pd.pivot_table(
        df,
        values='ID',
        index='Sistema_Logico',
        columns='Cerro',
        aggfunc=lambda x: "✅" if len(x) > 0 else ""
    ).fillna("")
    st.dataframe(pivot, use_container_width=True)