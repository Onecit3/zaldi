import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Zaldívar IPSC Monitor",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS PARA MODO CLARO (Light Mode) ---
st.markdown("""
<style>
    /* Fuente Global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: #1f2937; /* Gris Oscuro para texto */
    }

    /* Fondo de la Aplicación */
    .stApp {
        background-color: #f8f9fa; /* Gris muy claro (Casi blanco) */
    }

    /* TABS (Pestañas) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        color: #6b7280;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important; /* Azul Corporativo */
        color: white !important;
        border: none;
    }

    /* TARJETAS DE MÉTRICAS (KPIs) */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #2563eb; /* Acento Azul */
    }
    div[data-testid="metric-container"] label {
        color: #64748b; /* Slate 500 */
        font-size: 0.9rem;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #111827; /* Casi negro */
        font-size: 1.8rem;
    }

    /* EXPANDERS (Acordeones/Tarjetas) */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        color: #1f2937;
        font-weight: 700;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .streamlit-expanderContent {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-top: none;
        padding: 20px;
    }

    /* Títulos */
    h1 { color: #111827 !important; letter-spacing: -0.5px; }
    h2, h3 { color: #374151 !important; }
    
</style>
""", unsafe_allow_html=True)

# --- 3. CARGA Y PROCESAMIENTO DE DATOS ---
@st.cache_data
def load_data():
    file_path = "Sistema_Radio_Completo.xlsx"
    try:
        df = pd.read_excel(file_path, header=3)
        df = df.dropna(subset=['ID'])
        df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
        
        # Mapeo de Sistemas
        def get_system(id_val):
            if 100 <= id_val < 200: return "Prevención - Negrillar"
            elif 200 <= id_val < 300: return "Apilado"
            elif 400 <= id_val < 500: return "Planta"
            elif 500 <= id_val < 600: return "Mina"
            elif 600 <= id_val < 700: return "ZALOTRC"
            return "Otros"
            
        df['Sistema_Logico'] = df['ID'].apply(get_system)
        
        # Simplificar Rol
        df['Rol'] = df['Tipo Vinculo'].apply(lambda x: 'Master' if 'Master' in str(x) else 'Peer')
        
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- FUNCIÓN DE ESTILO (HIGHLIGHT) ---
def style_dataframe(df_input):
    """
    Colorea de rojo suave la fila completa si es Master.
    Colorea de verde suave si es Peer.
    """
    def highlight_rows(row):
        if row['Rol'] == 'Master':
            return ['background-color: #fef2f2; color: #991b1b; font-weight: bold'] * len(row) # Rojo suave
        else:
            return ['background-color: #f0fdf4; color: #166534'] * len(row) # Verde suave
            
    return df_input.style.apply(highlight_rows, axis=1)

# --- 4. INTERFAZ DE USUARIO ---

if df.empty:
    st.error("⚠️ No se encontraron datos. Sube el archivo 'Sistema_Radio_Completo.xlsx' al repositorio.")
    st.stop()

# Header
st.title("Minera Zaldívar")
st.markdown("##### 📡 Monitor de Infraestructura IPSC")
st.divider()

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Sistemas", df['Sistema_Logico'].nunique())
c2.metric("Sitios Físicos", df['Cerro'].nunique())
c3.metric("Repetidores", len(df))
c4.metric("Gateway", "10.70.140.1")

st.markdown("###")

# TABS
tab_logic, tab_phys, tab_matrix = st.tabs(["🌐 Vista Lógica", "🏔️ Vista Física", "📊 Matriz"])

# VISTA LÓGICA
with tab_logic:
    st.info("💡 Las filas rojas indican el equipo **MASTER** del sistema.")
    
    systems = sorted(df['Sistema_Logico'].unique())
    cols = st.columns(2)
    
    for i, sys in enumerate(systems):
        with cols[i % 2]:
            sub_df = df[df['Sistema_Logico'] == sys].copy()
            master_loc = sub_df[sub_df['Rol'] == 'Master'].iloc[0]['Cerro'] if not sub_df[sub_df['Rol'] == 'Master'].empty else "N/A"
            
            with st.expander(f"{sys}  (Master en {master_loc})", expanded=True):
                # Preparamos columnas
                display_df = sub_df[['Cerro', 'Alias', 'ID', 'IP Ethernet', 'Rol']]
                # APLICAMOS EL ESTILO
                st.dataframe(style_dataframe(display_df), use_container_width=True, hide_index=True)

# VISTA FÍSICA
with tab_phys:
    sites = sorted(df['Cerro'].unique())
    
    for site in sites:
        with st.expander(f"📍 {site}", expanded=False):
            sub_df = df[df['Cerro'] == site].copy()
            
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.markdown("**Resumen:**")
                n_masters = len(sub_df[sub_df['Rol'] == 'Master'])
                st.write(f"- Equipos: {len(sub_df)}")
                st.write(f"- Masters: {n_masters}")
                if n_masters > 0:
                    st.warning("⚠️ Sitio Crítico (Aloja Master)")
                
            with col_b:
                display_df = sub_df[['Sistema_Logico', 'Alias', 'ID', 'Rol', 'RX (MHz)']]
                # APLICAMOS EL ESTILO
                st.dataframe(style_dataframe(display_df), use_container_width=True, hide_index=True)

# MATRIZ
with tab_matrix:
    st.markdown("### Mapa de Calor de Roles")
    pivot = pd.pivot_table(
        df, 
        index='Sistema_Logico', 
        columns='Cerro', 
        values='Rol', 
        aggfunc=lambda x: '👑 MASTER' if 'Master' in str(x) else '🟢 Peer'
    ).fillna("-")
    
    # Estilo condicional específico para la matriz
    def color_matrix(val):
        if 'MASTER' in str(val):
            return 'background-color: #fee2e2; color: #b91c1c; font-weight: bold'
        elif 'Peer' in str(val):
            return 'color: #15803d'
        return 'color: #e5e7eb'

    st.dataframe(pivot.style.applymap(color_matrix), use_container_width=True)
