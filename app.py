import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(
    page_title="Zaldívar IPSC Monitor",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Personalizados (Dark/Modern Theme)
st.markdown("""
<style>
    /* Fondo General y Fuente */
    .stApp {
        background-color: #0e1117;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Personalización de los TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1f2937;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #9ca3af;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
        font-weight: bold;
    }

    /* Tarjetas Expandibles (Expander) */
    .streamlit-expanderHeader {
        background-color: #1f2937;
        color: #e5e7eb;
        border: 1px solid #374151;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .streamlit-expanderHeader:hover {
        border-color: #60a5fa;
        color: #60a5fa;
    }
    .streamlit-expanderContent {
        background-color: #111827;
        border: 1px solid #374151;
        border-top: none;
        color: #d1d5db;
        padding: 15px !important;
    }

    /* Métricas (KPIs) */
    div[data-testid="metric-container"] {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    }
    div[data-testid="metric-container"] label {
        color: #9ca3af;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #f3f4f6;
    }

    /* Títulos y textos */
    h1, h2, h3 {
        color: #f3f4f6 !important;
    }
    p, li {
        color: #d1d5db;
    }
    
    /* Badges personalizados para Master/Peer en Dataframes */
    .role-badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.8em;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Asegúrate de que el archivo esté en el repo de GitHub
    file_path = "Sistema_Radio_Completo.xlsx"
    try:
        df = pd.read_excel(file_path, header=3)
        df = df.dropna(subset=['ID'])
        df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
        
        # Lógica de agrupación
        def get_system(id_val):
            if 100 <= id_val < 200: return "Prevención - Negrillar"
            elif 200 <= id_val < 300: return "Apilado"
            elif 400 <= id_val < 500: return "Planta"
            elif 500 <= id_val < 600: return "Mina"
            elif 600 <= id_val < 700: return "ZALOTRC"
            return "Otros"
            
        df['Sistema_Logico'] = df['ID'].apply(get_system)
        
        # Limpieza de columnas clave
        df['Rol'] = df['Tipo Vinculo'].apply(lambda x: 'Master' if 'Master' in str(x) else 'Peer')
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 3. HEADER Y KPIs ---

# Si no hay datos, mostrar aviso amable
if df.empty:
    st.warning("⚠️ No se pudo cargar 'Sistema_Radio_Completo.xlsx'. Por favor verifica que el archivo esté en el repositorio.")
    st.stop()

st.title("📡 Minera Zaldívar")
st.markdown("##### Centro de Control IP Site Connect")
st.markdown("---")

# KPIs Superiores
k1, k2, k3, k4 = st.columns(4)
k1.metric("Sistemas Lógicos", df['Sistema_Logico'].nunique())
k2.metric("Sitios Físicos (Cerros)", df['Cerro'].nunique())
k3.metric("Total Repetidores", len(df))
k4.metric("Gateway", "10.70.140.1")

st.markdown("###") # Espacio

# --- 4. CONTENIDO POR PESTAÑAS (TABS) ---
tab_logico, tab_fisico, tab_matriz = st.tabs(["🌐 Vista Lógica (Sistemas)", "🏔️ Vista Física (Cerros)", "📊 Matriz Resumen"])

# --- PESTAÑA 1: SISTEMAS LÓGICOS ---
with tab_logico:
    st.markdown("### Distribución por Grupos de Servicio")
    
    systems = sorted(df['Sistema_Logico'].unique())
    
    # Creamos un grid de 2 columnas para las tarjetas
    cols = st.columns(2)
    
    for i, sys in enumerate(systems):
        with cols[i % 2]: # Alternar columnas
            sub_df = df[df['Sistema_Logico'] == sys].copy()
            
            # Buscar Master
            master_row = sub_df[sub_df['Rol'] == 'Master']
            master_loc = master_row.iloc[0]['Cerro'] if not master_row.empty else "N/A"
            num_sites = len(sub_df)
            
            # Título de la tarjeta con emoji e info resumen
            card_title = f"{sys}  |  📍 Master: {master_loc}  |  📡 {num_sites} Sitios"
            
            with st.expander(card_title, expanded=True):
                # Preparamos dataframe para mostrar
                display_df = sub_df[['Cerro', 'ID', 'IP Ethernet', 'Rol', 'RX (MHz)']]
                
                # Usamos column_config para iconos y barras
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Rol": st.column_config.TextColumn(
                            "Rol de Red",
                            width="small",
                            help="Master controla la sincronización",
                        ),
                        "IP Ethernet": st.column_config.TextColumn(
                            "IP Address",
                            width="medium",
                        ),
                        "Cerro": st.column_config.TextColumn(
                            "Ubicación",
                            width="medium",
                        ),
                    }
                )
                
                # Pequeña barra visual de progreso o estado
                st.progress(100, text="Estado del Sistema: Operativo")

# --- PESTAÑA 2: UBICACIÓN FÍSICA ---
with tab_fisico:
    st.markdown("### Inventario por Ubicación Geográfica")
    
    sites = sorted(df['Cerro'].unique())
    cols_phys = st.columns(2)
    
    for i, site in enumerate(sites):
        with cols_phys[i % 2]:
            sub_df = df[df['Cerro'] == site]
            sistemas_presentes = sub_df['Sistema_Logico'].unique()
            
            with st.expander(f"🏔️ {site}", expanded=False):
                c1, c2 = st.columns([1, 2])
                
                with c1:
                    st.caption("Sistemas Alojados")
                    for s in sistemas_presentes:
                        st.markdown(f"- **{s}**")
                        
                with c2:
                    st.caption("Detalle Técnico")
                    st.dataframe(
                        sub_df[['Sistema_Logico', 'ID', 'Rol']],
                        hide_index=True,
                        use_container_width=True
                    )

# --- PESTAÑA 3: MATRIZ ---
with tab_matriz:
    st.markdown("### Matriz de Cobertura Cruzada")
    
    # Crear una matriz visual con Pandas
    pivot = pd.pivot_table(
        df, 
        index='Sistema_Logico', 
        columns='Cerro', 
        values='Rol', 
        aggfunc=lambda x: '👑' if 'Master' in str(x) else '🟢' # Emojis para la matriz
    ).fillna("-")
    
    st.dataframe(pivot, use_container_width=True)
    st.caption("Leyenda: 👑 = Master Repeater, 🟢 = Peer Repeater, - = Sin Cobertura")
