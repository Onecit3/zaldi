import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="Zaldívar Radio Monitor",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "PREMIUM" (Tipografía y Paleta) ---
st.markdown("""
<style>
    /* 1. IMPORTAR FUENTE 'POPPINS' (Más moderna y bonita) */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        color: #334155; /* Slate 700 */
    }

    /* 2. FONDO SOFISTICADO */
    .stApp {
        background-color: #f8fafc; /* Slate 50 (Gris azulado muy claro) */
    }

    /* 3. TÍTULOS */
    h1 {
        color: #0f172a; /* Slate 900 */
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    h3 {
        color: #475569;
        font-weight: 600;
    }

    /* 4. TARJETAS DE MÉTRICAS (KPIs) */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 16px; /* Bordes más redondeados */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); /* Sombra suave */
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: #6366f1; /* Indigo al pasar el mouse */
    }
    div[data-testid="metric-container"] label {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #1e293b;
        font-weight: 700;
    }

    /* 5. TARJETAS EXPANDIBLES (ACORDEONES) */
    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        color: #1e293b;
        font-weight: 600;
        font-size: 1rem;
    }
    .streamlit-expanderContent {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-top: none;
        border-bottom-left-radius: 12px;
        border-bottom-right-radius: 12px;
        padding: 24px;
    }

    /* 6. PESTAÑAS (TABS) MÁS LIMPIAS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 50px; /* Pestañas tipo pastilla */
        padding: 8px 20px;
        font-weight: 500;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0f172a !important; /* Negro/Azul oscuro */
        color: white !important;
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
        
        def get_system(id_val):
            if 100 <= id_val < 200: return "Prevención - Negrillar"
            elif 200 <= id_val < 300: return "Apilado"
            elif 400 <= id_val < 500: return "Planta"
            elif 500 <= id_val < 600: return "Mina"
            elif 600 <= id_val < 700: return "ZALOTRC"
            return "Otros"
            
        df['Sistema_Logico'] = df['ID'].apply(get_system)
        df['Rol'] = df['Tipo Vinculo'].apply(lambda x: 'Master' if 'Master' in str(x) else 'Peer')
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 4. FUNCIÓN DE ESTILO (PANDAS STYLER) ---
# Aquí definimos los colores bonitos para la tabla
def pretty_style(df_input):
    def highlight_rows(row):
        # Colores Pastel Suaves (Mucho más elegantes que el rojo puro)
        if row['Rol'] == 'Master':
            # Fondo Ambar Suave, Texto Naranja Oscuro
            return ['background-color: #fffbeb; color: #92400e; font-weight: 600'] * len(row)
        else:
            # Fondo Blanco, Texto Gris Oscuro (Limpio)
            return ['background-color: white; color: #475569'] * len(row)
            
    return df_input.style.apply(highlight_rows, axis=1).format(precision=4)

# --- 5. INTERFAZ ---
if df.empty:
    st.error("⚠️ No se encontraron datos. Verifica el archivo Excel.")
    st.stop()

# Header
st.title("Minera Zaldívar")
st.markdown("##### 📡 Monitor de Infraestructura IPSC")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sistemas", df['Sistema_Logico'].nunique())
col2.metric("Sitios Físicos", df['Cerro'].nunique())
col3.metric("Total Radios", len(df))
col4.metric("Gateway", "10.70.140.1")

st.markdown("###")

# Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Sistemas Lógicos", "🏔️ Sitios Físicos", "📊 Matriz"])

# VISTA 1: SISTEMAS
with tab1:
    st.info("💡 **Nota:** Las filas resaltadas en **Dorado/Naranja** indican el equipo **MASTER** que controla el sistema.")
    
    systems = sorted(df['Sistema_Logico'].unique())
    # Grid de 2 columnas
    cols = st.columns(2)
    
    for i, sys in enumerate(systems):
        with cols[i % 2]:
            sub_df = df[df['Sistema_Logico'] == sys].copy()
            master_loc = sub_df[sub_df['Rol'] == 'Master'].iloc[0]['Cerro'] if not sub_df[sub_df['Rol'] == 'Master'].empty else "N/A"
            
            # Icono dinámico
            icon = "🔥" if "Prevención" in sys else "⚙️"
            
            with st.expander(f"{icon} {sys}", expanded=True):
                st.markdown(f"**Ubicación Master:** `{master_loc}`")
                
                display_df = sub_df[['Cerro', 'Alias', 'ID', 'IP Ethernet', 'Rol']]
                
                # APLICAR ESTILO BONITO
                st.dataframe(
                    pretty_style(display_df),
                    use_container_width=True,
                    hide_index=True
                )

# VISTA 2: SITIOS FÍSICOS
with tab2:
    sites = sorted(df['Cerro'].unique())
    
    for site in sites:
        with st.expander(f"📍 {site}", expanded=False):
            sub_df = df[df['Cerro'] == site].copy()
            
            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown("**Resumen:**")
                masters_count = len(sub_df[sub_df['Rol'] == 'Master'])
                st.write(f"Equipos Totales: **{len(sub_df)}**")
                
                if masters_count > 0:
                    st.markdown(f":warning: Aloja **{masters_count} Masters**")
                else:
                    st.markdown(":white_check_mark: Solo Peers")
                    
            with c2:
                display_df = sub_df[['Sistema_Logico', 'Alias', 'ID', 'Rol', 'RX (MHz)']]
                st.dataframe(
                    pretty_style(display_df),
                    use_container_width=True,
                    hide_index=True
                )

# VISTA 3: MATRIZ
with tab3:
    st.markdown("### Mapa de Distribución")
    
    pivot = pd.pivot_table(
        df,
        index='Sistema_Logico',
        columns='Cerro',
        values='Rol',
        aggfunc=lambda x: '👑 MASTER' if 'Master' in str(x) else '🔹 Peer'
    ).fillna("-")
    
    # Estilo específico para la matriz
    def style_matrix(val):
        if 'MASTER' in str(val):
            return 'color: #d97706; font-weight: bold; background-color: #fffbeb' # Amber 600
        elif 'Peer' in str(val):
            return 'color: #3b82f6' # Blue 500
        return 'color: #e2e8f0' # Gris claro para vacíos

    st.dataframe(pivot.style.applymap(style_matrix), use_container_width=True)
