import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="Zaldívar Radio Monitor",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS MODERNO Y PROFESIONAL (2026 TRENDS) ---
st.markdown("""
<style>
    /* ============================================
       TIPOGRAFÍA MODERNA - INTER FONT
       ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1e293b;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* ============================================
       FONDO CON GRADIENTE SUTIL
       ============================================ */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* ============================================
       HEADER - TÍTULO PRINCIPAL
       ============================================ */
    h1 {
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        letter-spacing: -1.5px !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h5 {
        color: #64748b !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-top: 0 !important;
    }

    h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        letter-spacing: -0.5px !important;
    }

    /* ============================================
       MÉTRICAS KPI - GLASSMORPHISM EFFECT
       ============================================ */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        padding: 28px 24px;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px 0 rgba(31, 38, 135, 0.08),
            0 2px 8px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    /* Efecto gradiente sutil en el fondo */
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(147, 51, 234, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: 0;
    }

    div[data-testid="metric-container"]:hover::before {
        opacity: 1;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px 0 rgba(59, 130, 246, 0.15),
            0 4px 16px 0 rgba(0, 0, 0, 0.1);
        border-color: rgba(59, 130, 246, 0.3);
    }

    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        position: relative;
        z-index: 1;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        letter-spacing: -1px !important;
        position: relative;
        z-index: 1;
    }

    /* ============================================
       EXPANDERS - TARJETAS ELEGANTES
       ============================================ */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 18px 24px !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.95);
        border-color: #3b82f6;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.12);
        transform: translateX(4px);
    }

    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-top: none;
        border-bottom-left-radius: 16px;
        border-bottom-right-radius: 16px;
        padding: 28px !important;
        margin-top: -1px;
    }

    /* ============================================
       PESTAÑAS - DISEÑO MODERNO TIPO PÍLDORA
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.6);
        padding: 8px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #64748b;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.3px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        box-shadow: 
            0 4px 12px rgba(59, 130, 246, 0.3),
            0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    /* ============================================
       DATAFRAMES - TABLAS MODERNAS
       ============================================ */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }

    /* Encabezados de tabla */
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 16px 12px !important;
        border: none !important;
    }

    /* Filas de tabla */
    .stDataFrame tbody tr {
        transition: all 0.2s ease;
    }

    .stDataFrame tbody tr:hover {
        background: rgba(59, 130, 246, 0.08) !important;
        transform: scale(1.01);
    }

    /* ============================================
       INFO/WARNING BOXES
       ============================================ */
    .stAlert {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border-left: 4px solid #3b82f6 !important;
        padding: 16px 20px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }

    /* ============================================
       DIVISORES (SEPARADORES)
       ============================================ */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent) !important;
    }

    /* ============================================
       MARKDOWN PERSONALIZADO
       ============================================ */
    .stMarkdown strong {
        color: #1e293b;
        font-weight: 700;
    }

    .stMarkdown code {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
        padding: 4px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9em;
    }

    /* ============================================
       ANIMACIONES GLOBALES
       ============================================ */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .element-container {
        animation: fadeIn 0.6s ease-out;
    }

    /* ============================================
       SCROLLBAR PERSONALIZADO
       ============================================ */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #94a3b8, #64748b);
        border-radius: 10px;
        transition: background 0.3s;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #64748b, #475569);
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

# --- 4. FUNCIÓN DE ESTILO MEJORADA ---
def premium_style(df_input):
    def highlight_rows(row):
        if row['Rol'] == 'Master':
            # Gradiente azul para Master
            return [
                'background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); '
                'color: #1e40af; '
                'font-weight: 700; '
                'border-left: 4px solid #3b82f6;'
            ] * len(row)
        else:
            # Blanco limpio para Peer
            return [
                'background: white; '
                'color: #475569; '
                'font-weight: 500;'
            ] * len(row)
            
    return df_input.style.apply(highlight_rows, axis=1)\
                        .format(precision=4)\
                        .set_properties(**{
                            'text-align': 'left',
                            'padding': '14px 12px',
                            'border-bottom': '1px solid #f1f5f9'
                        })

# --- 5. INTERFAZ MEJORADA ---
if df.empty:
    st.error("⚠️ No se encontraron datos. Verifica el archivo Excel.")
    st.stop()

# Header con icono personalizado
st.markdown("""
<div style='text-align: left; margin-bottom: 1rem;'>
    <span style='font-size: 3.5rem; background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        📡
    </span>
</div>
""", unsafe_allow_html=True)

st.title("Minera Zaldívar")
st.markdown("##### 📊 Monitor de Infraestructura IPSC")
st.markdown("<br>", unsafe_allow_html=True)

# KPIs con iconos mejorados
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 SISTEMAS",
        value=df['Sistema_Logico'].nunique()
    )

with col2:
    st.metric(
        label="🏔️ SITIOS FÍSICOS",
        value=df['Cerro'].nunique()
    )

with col3:
    st.metric(
        label="📻 TOTAL RADIOS",
        value=len(df)
    )

with col4:
    st.metric(
        label="🌐 GATEWAY",
        value="10.70.140.1"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Sistemas Lógicos", "🏔️ Sitios Físicos", "📊 Matriz de Distribución"])

# ========================================
# TAB 1: SISTEMAS LÓGICOS
# ========================================
with tab1:
    st.markdown("""
    <div style='background: rgba(59, 130, 246, 0.1); padding: 16px 20px; border-radius: 12px; 
                border-left: 4px solid #3b82f6; margin-bottom: 24px;'>
        <strong style='color: #1e40af;'>💡 Nota:</strong> 
        <span style='color: #475569;'>Las filas con gradiente <strong>azul</strong> 
        indican el equipo <strong>MASTER</strong> que controla el sistema.</span>
    </div>
    """, unsafe_allow_html=True)
    
    systems = sorted(df['Sistema_Logico'].unique())
    
    # Mapeo de iconos por sistema
    system_icons = {
        "Prevención - Negrillar": "🚨",
        "Apilado": "📦",
        "Planta": "🏭",
        "Mina": "⛏️",
        "ZALOTRC": "🔧",
        "Otros": "⚙️"
    }
    
    cols = st.columns(2)
    
    for i, sys in enumerate(systems):
        with cols[i % 2]:
            sub_df = df[df['Sistema_Logico'] == sys].copy()
            master_data = sub_df[sub_df['Rol'] == 'Master']
            master_loc = master_data.iloc[0]['Cerro'] if not master_data.empty else "N/A"
            
            icon = system_icons.get(sys, "⚙️")
            
            with st.expander(f"{icon} **{sys}**", expanded=(i < 2)):
                # Info del master
                st.markdown(f"""
                <div style='background: rgba(255, 255, 255, 0.6); padding: 12px 16px; 
                            border-radius: 10px; margin-bottom: 16px; 
                            border-left: 3px solid #3b82f6;'>
                    <strong style='color: #1e293b;'>📍 Ubicación Master:</strong> 
                    <code style='background: rgba(59, 130, 246, 0.1); color: #3b82f6; 
                                 padding: 4px 12px; border-radius: 6px; font-size: 0.95em;'>
                        {master_loc}
                    </code>
                </div>
                """, unsafe_allow_html=True)
                
                display_df = sub_df[['Cerro', 'Alias', 'ID', 'IP Ethernet', 'Rol']]
                
                st.dataframe(
                    premium_style(display_df),
                    use_container_width=True,
                    hide_index=True,
                    height=min(400, len(display_df) * 50 + 50)
                )

# ========================================
# TAB 2: SITIOS FÍSICOS
# ========================================
with tab2:
    sites = sorted(df['Cerro'].unique())
    
    for site in sites:
        with st.expander(f"📍 **{site}**", expanded=False):
            sub_df = df[df['Cerro'] == site].copy()
            
            c1, c2 = st.columns([1, 3])
            
            with c1:
                masters_count = len(sub_df[sub_df['Rol'] == 'Master'])
                total_count = len(sub_df)
                
                # Card de resumen
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                            padding: 20px; border-radius: 12px; text-align: center; 
                            border: 2px solid #cbd5e1;'>
                    <div style='font-size: 2.5rem; font-weight: 800; color: #1e293b; 
                                margin-bottom: 8px;'>
                        {total_count}
                    </div>
                    <div style='font-size: 0.85rem; color: #64748b; font-weight: 600; 
                                text-transform: uppercase; letter-spacing: 1px;'>
                        Equipos Totales
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if masters_count > 0:
                    st.markdown(f"""
                    <div style='background: rgba(59, 130, 246, 0.1); padding: 12px; 
                                border-radius: 10px; border-left: 4px solid #3b82f6;'>
                        <strong style='color: #1e40af;'>👑 {masters_count} Master(s)</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background: rgba(34, 197, 94, 0.1); padding: 12px; 
                                border-radius: 10px; border-left: 4px solid #22c55e;'>
                        <strong style='color: #15803d;'>✓ Solo Peers</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with c2:
                display_df = sub_df[['Sistema_Logico', 'Alias', 'ID', 'Rol', 'RX (MHz)']]
                st.dataframe(
                    premium_style(display_df),
                    use_container_width=True,
                    hide_index=True,
                    height=min(400, len(display_df) * 50 + 50)
                )

# ========================================
# TAB 3: MATRIZ
# ========================================
with tab3:
    st.markdown("### 🗺️ Mapa de Distribución de Equipos")
    st.markdown("<br>", unsafe_allow_html=True)
    
    pivot = pd.pivot_table(
        df,
        index='Sistema_Logico',
        columns='Cerro',
        values='Rol',
        aggfunc=lambda x: '👑 MASTER' if 'Master' in list(x) else '🔹 Peer'
    ).fillna("—")
    
    def style_matrix(val):
        if 'MASTER' in str(val):
            return 'color: #1e40af; font-weight: 700; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);'
        elif 'Peer' in str(val):
            return 'color: #3b82f6; font-weight: 600; background: white;'
        return 'color: #cbd5e1; background: #f8fafc;'

    st.dataframe(
        pivot.style.applymap(style_matrix).set_properties(**{
            'text-align': 'center',
            'padding': '14px 10px',
            'border': '1px solid #f1f5f9'
        }),
        use_container_width=True,
        height=400
    )
    
    # Leyenda
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 12px; border-radius: 10px; text-align: center;'>
            <strong style='color: #1e40af;'>👑 MASTER</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div style='background: white; padding: 12px; border-radius: 10px; 
                    text-align: center; border: 2px solid #e2e8f0;'>
            <strong style='color: #3b82f6;'>🔹 PEER</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col_c:
        st.markdown("""
        <div style='background: #f8fafc; padding: 12px; border-radius: 10px; 
                    text-align: center; border: 2px solid #e2e8f0;'>
            <strong style='color: #cbd5e1;'>— Sin Equipo</strong>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.85rem; 
            padding: 20px; border-top: 1px solid #e2e8f0;'>
    <strong>Minera Zaldívar</strong> • Monitor IPSC • 2026
</div>
""", unsafe_allow_html=True)
