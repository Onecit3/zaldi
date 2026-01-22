import streamlit as st
import pandas as pd
import altair as alt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Zaldívar Radio Monitor",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="expanded"
)

# --- 2. INYECCIÓN DE CSS (EL MAQUILLAJE PROFESIONAL) ---
# Esto sobreescribe los estilos nativos de Streamlit
st.markdown("""
<style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }

    /* Fondo general */
    .stApp {
        background-color: #f1f5f9; /* Slate 100 */
    }

    /* Estilo del Header */
    h1 {
        color: #0f172a;
        font-weight: 800 !important;
        letter-spacing: -0.05em;
    }
    
    h3 {
        color: #334155;
        font-weight: 600;
    }

    /* Tarjetas de Métricas (KPIs) personalizadas */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 20px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }

    div[data-testid="metric-container"] label {
        color: #64748b; /* Slate 500 */
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 700;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
    }

    /* Estilo para los Expanders (Acordeones) */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        color: #1e293b;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background-color: white;
        border-left: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        padding: 20px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a; /* Dark Slate */
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    
</style>
""", unsafe_allow_html=True)

# --- 3. CARGA DE DATOS ---
@st.cache_data
def load_data():
    file_path = "Sistema_Radio_Completo.xlsx"
    try:
        df = pd.read_excel(file_path, header=3)
        df = df.dropna(subset=['ID'])
        df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
        
        # Mapeo de sistemas
        def get_system(id_val):
            if 100 <= id_val < 200: return "Prevención"
            elif 200 <= id_val < 300: return "Apilado"
            elif 400 <= id_val < 500: return "Planta"
            elif 500 <= id_val < 600: return "Mina"
            elif 600 <= id_val < 700: return "ZALOTRC"
            return "Otros"
            
        df['Sistema'] = df['ID'].apply(get_system)
        
        # Crear columna de Estado para visualización (simulado)
        df['Rol'] = df['Tipo Vinculo'].apply(lambda x: '👑 Master' if 'Master' in str(x) else '🔗 Peer')
        
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR (Navegación y Filtros) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png", width=50) # Placeholder logo
    st.title("IP Site Connect")
    st.caption("Panel de Control de Infraestructura")
    st.markdown("---")
    
    if not df.empty:
        selected_system = st.multiselect(
            "Filtrar por Sistema",
            options=df['Sistema'].unique(),
            default=df['Sistema'].unique()
        )
        
        selected_cerro = st.multiselect(
            "Filtrar por Ubicación",
            options=df['Cerro'].unique(),
            default=df['Cerro'].unique()
        )
        
        # Aplicar filtros
        df_filtered = df[
            (df['Sistema'].isin(selected_system)) & 
            (df['Cerro'].isin(selected_cerro))
        ]
    else:
        df_filtered = df

# --- 5. CUERPO PRINCIPAL ---

if df_filtered.empty:
    st.error("⚠️ No se encontraron datos o no se ha cargado el archivo Excel en el repositorio.")
    st.stop()

# Header Principal
st.title("Minera Zaldívar")
st.markdown(f"**Estado de la Red** • Última actualización: {pd.Timestamp.now().strftime('%d-%m-%Y')}")

st.markdown("###") # Espaciador

# KPI Cards (Fila Superior)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Dispositivos", len(df_filtered), delta="Activos")
col2.metric("Sistemas Operativos", df_filtered['Sistema'].nunique())
col3.metric("Sitios Físicos", df_filtered['Cerro'].nunique())
col4.metric("Gateway Principal", "10.70.140.1")

st.markdown("---")

# Gráficos (Altair) para hacerlo visual
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📡 Distribución de Equipos por Cerro")
    chart_cerro = alt.Chart(df_filtered).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10).encode(
        x=alt.X('Cerro', sort='-y', axis=alt.Axis(labelAngle=0)),
        y='count()',
        color=alt.Color('Cerro', legend=None, scale=alt.Scale(scheme='tableau10')),
        tooltip=['Cerro', 'count()']
    ).properties(height=300)
    st.altair_chart(chart_cerro, use_container_width=True)

with c2:
    st.subheader("🎛️ Por Rol")
    chart_rol = alt.Chart(df_filtered).mark_arc(innerRadius=50).encode(
        theta=alt.Theta("count()", stack=True),
        color=alt.Color("Rol", scale=alt.Scale(range=['#ef4444', '#3b82f6'])), # Rojo Master, Azul Peer
        tooltip=['Rol', 'count()']
    ).properties(height=300)
    st.altair_chart(chart_rol, use_container_width=True)

# Sección de Detalles (Tablas Estilizadas)
st.subheader("Inventario Detallado")

tabs = st.tabs(["Vista de Red", "Parámetros RF"])

with tabs[0]:
    # Usamos column_config para hacer la tabla sexy
    st.dataframe(
        df_filtered[['ID', 'Alias', 'Sistema', 'Cerro', 'IP Ethernet', 'Rol']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rol": st.column_config.TextColumn(
                "Rol de Red",
                help="Master controla el clocking",
                width="small"
            ),
            "IP Ethernet": st.column_config.TextColumn(
                "Dirección IP",
                width="medium"
            ),
            "Sistema": st.column_config.TextColumn(
                "Grupo Lógico",
                width="medium"
            ),
             "Alias": st.column_config.TextColumn(
                "ID Radio",
                width="large"
            ),
        }
    )

with tabs[1]:
    st.dataframe(
        df_filtered[['ID', 'Alias', 'RX (MHz)', 'TX (MHz)', 'Puerto UDP']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "RX (MHz)": st.column_config.NumberColumn(
                "Frecuencia RX",
                format="%.4f MHz"
            ),
            "TX (MHz)": st.column_config.NumberColumn(
                "Frecuencia TX",
                format="%.4f MHz"
            )
        }
    )
