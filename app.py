import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="Zaldívar Repetidores Monitor",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="expanded"
)

# --- 2. CSS MODERNO Y PROFESIONAL ---
def apply_custom_css(dark_mode=False):
    if dark_mode:
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                color: #f1f5f9;
                -webkit-font-smoothing: antialiased;
            }

            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            }

            h1 {
                color: #f1f5f9 !important;
                font-weight: 800 !important;
                font-size: 2.8rem !important;
                letter-spacing: -1.5px !important;
            }

            h3, h5 {
                color: #cbd5e1 !important;
            }

            div[data-testid="metric-container"] {
                background: rgba(30, 41, 59, 0.8);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(71, 85, 105, 0.5);
                padding: 28px 24px;
                border-radius: 20px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }

            div[data-testid="metric-container"]:hover {
                transform: translateY(-8px) scale(1.02);
                border-color: rgba(59, 130, 246, 0.5);
                box-shadow: 0 20px 60px 0 rgba(59, 130, 246, 0.3);
            }

            div[data-testid="metric-container"] label {
                color: #94a3b8 !important;
            }

            div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
                color: #f1f5f9 !important;
            }

            .streamlit-expanderHeader {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(71, 85, 105, 0.5);
                color: #f1f5f9 !important;
            }

            .streamlit-expanderContent {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(71, 85, 105, 0.5);
            }

            .stTabs [data-baseweb="tab-list"] {
                background: rgba(30, 41, 59, 0.6);
            }

            .stTabs [data-baseweb="tab"] {
                color: #94a3b8;
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
                color: white !important;
            }

            .stDataFrame thead tr th {
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                color: #1e293b;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }

            .stApp {
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }

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

            .stDataFrame {
                border-radius: 12px !important;
                overflow: hidden !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
            }

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

            .stDataFrame tbody tr {
                transition: all 0.2s ease;
            }

            .stDataFrame tbody tr:hover {
                background: rgba(59, 130, 246, 0.08) !important;
                transform: scale(1.01);
            }

            .stAlert {
                background: rgba(255, 255, 255, 0.8) !important;
                backdrop-filter: blur(10px) !important;
                border-radius: 12px !important;
                border-left: 4px solid #3b82f6 !important;
                padding: 16px 20px !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
            }

            hr {
                margin: 2rem 0 !important;
                border: none !important;
                height: 1px !important;
                background: linear-gradient(90deg, transparent, #cbd5e1, transparent) !important;
            }

            .stMarkdown code {
                background: rgba(59, 130, 246, 0.1);
                color: #3b82f6;
                padding: 4px 8px;
                border-radius: 6px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.9em;
            }

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

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .element-container {
                animation: fadeIn 0.6s ease-out;
            }
        </style>
        """, unsafe_allow_html=True)

# --- 3. FUNCIONES DE CARGA Y PROCESAMIENTO ---
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
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# --- 4. FUNCIÓN DE ESTILOS PARA TABLAS ---
def premium_style(df_input):
    def highlight_rows(row):
        if row['Rol'] == 'Master':
            return [
                'background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); '
                'color: #1e40af; '
                'font-weight: 700; '
                'border-left: 4px solid #3b82f6;'
            ] * len(row)
        else:
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

# --- 5. FUNCIONES DE ANÁLISIS ---
def check_system_health(dataframe):
    """Detecta anomalías en la configuración"""
    issues = []
    
    for system in dataframe['Sistema_Logico'].unique():
        system_df = dataframe[dataframe['Sistema_Logico'] == system]
        masters = system_df[system_df['Rol'] == 'Master']
        
        if len(masters) == 0:
            issues.append(('error', f"⚠️ **{system}** no tiene Master asignado"))
        elif len(masters) > 1:
            issues.append(('warning', f"⚡ **{system}** tiene múltiples Masters ({len(masters)})"))
    
    duplicate_ips = dataframe[dataframe.duplicated(subset=['IP Ethernet'], keep=False)]
    if not duplicate_ips.empty:
        issues.append(('error', f"🔴 Detectadas {len(duplicate_ips)} IPs duplicadas"))
    
    return issues

# --- 6. FUNCIONES DE EXPORTACIÓN ---
@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Repetidores')
        
        # Agregar hoja de resumen
        summary_data = {
            'Métrica': [
                'Total Repetidores',
                'Total Masters',
                'Total Peers',
                'Sistemas Lógicos',
                'Sitios Físicos',
                'Fecha Reporte'
            ],
            'Valor': [
                len(dataframe),
                len(dataframe[dataframe['Rol'] == 'Master']),
                len(dataframe[dataframe['Rol'] == 'Peer']),
                dataframe['Sistema_Logico'].nunique(),
                dataframe['Cerro'].nunique(),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, index=False, sheet_name='Resumen')
    
    return output.getvalue()

# ============================================
# INICIO DE LA APLICACIÓN
# ============================================

# Cargar datos
df = load_data()

if df.empty:
    st.error("⚠️ No se encontraron datos. Verifica que el archivo 'Sistema_Radio_Completo.xlsx' esté en el directorio.")
    st.stop()

# ============================================
# SIDEBAR - FILTROS Y CONFIGURACIÓN
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    # Modo Oscuro
    dark_mode = st.toggle("🌙 Modo Oscuro", value=False)
    
    st.markdown("---")
    st.markdown("### 🔍 Filtros Avanzados")
    
    # Búsqueda
    search_term = st.text_input("🔎 Buscar (ID/Alias/IP)", "", placeholder="Ejemplo: 101 o CO2")
    
    # Filtros multi-select
    selected_systems = st.multiselect(
        "📊 Sistemas Lógicos",
        options=sorted(df['Sistema_Logico'].unique()),
        default=sorted(df['Sistema_Logico'].unique())
    )
    
    selected_sites = st.multiselect(
        "🏔️ Sitios Físicos",
        options=sorted(df['Cerro'].unique()),
        default=sorted(df['Cerro'].unique())
    )
    
    selected_roles = st.multiselect(
        "👑 Tipo de Repetidor",
        options=['Master', 'Peer'],
        default=['Master', 'Peer']
    )
    
    # Aplicar filtros
    df_filtered = df[
        (df['Sistema_Logico'].isin(selected_systems)) &
        (df['Cerro'].isin(selected_sites)) &
        (df['Rol'].isin(selected_roles))
    ]
    
    if search_term:
        df_filtered = df_filtered[
            df_filtered['ID'].astype(str).str.contains(search_term, case=False) |
            df_filtered['Alias'].str.contains(search_term, case=False, na=False) |
            df_filtered['IP Ethernet'].str.contains(search_term, case=False, na=False)
        ]
    
    st.markdown("---")
    st.metric("🎯 Resultados", len(df_filtered))
    
    # Exportación
    st.markdown("---")
    st.markdown("### 📥 Exportar Datos")
    
    csv = convert_df_to_csv(df_filtered)
    st.download_button(
        label="💾 CSV",
        data=csv,
        file_name=f'repetidores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv',
        use_container_width=True
    )
    
    excel_data = to_excel(df_filtered)
    st.download_button(
        label="📊 Excel",
        data=excel_data,
        file_name=f'reporte_repetidores_{datetime.now().strftime("%Y%m%d")}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True
    )
    
    # Acciones rápidas
    st.markdown("---")
    st.markdown("### ⚡ Acciones")
    
    if st.button("🔄 Refrescar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Aplicar tema
apply_custom_css(dark_mode)

# ============================================
# HEADER
# ============================================
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

# ============================================
# PANEL DE ALERTAS
# ============================================
issues = check_system_health(df_filtered)
if issues:
    with st.expander("🚨 Alertas del Sistema", expanded=True):
        for severity, message in issues:
            if severity == 'error':
                st.error(message)
            elif severity == 'warning':
                st.warning(message)

# ============================================
# KPIs PRINCIPALES
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🎯 SISTEMAS",
        value=df_filtered['Sistema_Logico'].nunique(),
        delta=f"{df['Sistema_Logico'].nunique()} total"
    )

with col2:
    st.metric(
        label="🏔️ SITIOS",
        value=df_filtered['Cerro'].nunique(),
        delta=f"{df['Cerro'].nunique()} total"
    )

with col3:
    st.metric(
        label="📻 REPETIDORES",
        value=len(df_filtered),
        delta=f"{len(df)} total"
    )

with col4:
    masters_count = len(df_filtered[df_filtered['Rol'] == 'Master'])
    st.metric(
        label="👑 MASTERS",
        value=masters_count,
        delta=f"{(masters_count/len(df_filtered)*100):.1f}%"
    )

with col5:
    st.metric(
        label="🌐 GATEWAY",
        value="10.70.140.1"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# DASHBOARD DE ANÁLISIS
# ============================================
st.markdown("### 📊 Análisis de Distribución")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Gráfico de distribución por sistema
    system_counts = df_filtered.groupby('Sistema_Logico').size().reset_index(name='Total')
    fig_bar = px.bar(
        system_counts,
        x='Sistema_Logico',
        y='Total',
        color='Total',
        color_continuous_scale='Blues',
        title="Repetidores por Sistema Lógico",
        labels={'Sistema_Logico': '', 'Total': 'Cantidad'}
    )
    fig_bar.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    # Gráfico Master vs Peer
    role_count = df_filtered.groupby(['Sistema_Logico', 'Rol']).size().reset_index(name='count')
    fig_stack = px.bar(
        role_count,
        x='Sistema_Logico',
        y='count',
        color='Rol',
        title="Distribución Master vs Peer",
        labels={'Sistema_Logico': '', 'count': 'Cantidad'},
        color_discrete_map={'Master': '#3b82f6', 'Peer': '#94a3b8'},
        barmode='stack'
    )
    fig_stack.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12)
    )
    st.plotly_chart(fig_stack, use_container_width=True)

# Gráfico de dona
col_donut, col_stats = st.columns([2, 1])

with col_donut:
    fig_donut = px.pie(
        system_counts,
        values='Total',
        names='Sistema_Logico',
        hole=0.6,
        title="Proporción de Equipos por Sistema",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
    fig_donut.update_layout(
        showlegend=True,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col_stats:
    st.markdown("#### 📈 Estadísticas")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #3b82f6;'>
        <div style='font-size: 0.75rem; color: #64748b; font-weight: 600; text-transform: uppercase; 
                    letter-spacing: 1px; margin-bottom: 8px;'>
            COBERTURA
        </div>
        <div style='font-size: 2rem; font-weight: 800; color: #1e293b;'>
            {df_filtered['Cerro'].nunique()}/{df['Cerro'].nunique()}
        </div>
        <div style='font-size: 0.85rem; color: #475569;'>
            Sitios activos
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    ratio_master_peer = len(df_filtered[df_filtered['Rol'] == 'Master']) / len(df_filtered[df_filtered['Rol'] == 'Peer']) if len(df_filtered[df_filtered['Rol'] == 'Peer']) > 0 else 0
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #f59e0b;'>
        <div style='font-size: 0.75rem; color: #92400e; font-weight: 600; text-transform: uppercase; 
                    letter-spacing: 1px; margin-bottom: 8px;'>
            RATIO M:P
        </div>
        <div style='font-size: 2rem; font-weight: 800; color: #78350f;'>
            1:{ratio_master_peer:.1f}
        </div>
        <div style='font-size: 0.85rem; color: #92400e;'>
            Master por Peer
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    avg_repetidores = len(df_filtered) / df_filtered['Cerro'].nunique() if df_filtered['Cerro'].nunique() > 0 else 0
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                padding: 16px; border-radius: 12px; border-left: 4px solid #3b82f6;'>
        <div style='font-size: 0.75rem; color: #1e40af; font-weight: 600; text-transform: uppercase; 
                    letter-spacing: 1px; margin-bottom: 8px;'>
            PROMEDIO
        </div>
        <div style='font-size: 2rem; font-weight: 800; color: #1e3a8a;'>
            {avg_repetidores:.1f}
        </div>
        <div style='font-size: 0.85rem; color: #1e40af;'>
            Repetidores por sitio
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# TABS PRINCIPALES
# ============================================
tab1, tab2, tab3 = st.tabs([
    "🌐 Sistemas Lógicos", 
    "🏔️ Sitios Físicos", 
    "📊 Matriz de Distribución"
])

# --- TAB 1: SISTEMAS LÓGICOS ---
with tab1:
    st.markdown("""
    <div style='background: rgba(59, 130, 246, 0.1); padding: 16px 20px; border-radius: 12px; 
                border-left: 4px solid #3b82f6; margin-bottom: 24px;'>
        <strong style='color: #1e40af;'>💡 Nota:</strong> 
        <span style='color: #475569;'>Las filas con gradiente <strong>azul</strong> 
        indican el equipo <strong>MASTER</strong> que controla el sistema.</span>
    </div>
    """, unsafe_allow_html=True)
    
    systems = sorted(df_filtered['Sistema_Logico'].unique())
    
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
            sub_df = df_filtered[df_filtered['Sistema_Logico'] == sys].copy()
            master_data = sub_df[sub_df['Rol'] == 'Master']
            master_loc = master_data.iloc[0]['Cerro'] if not master_data.empty else "N/A"
            
            icon = system_icons.get(sys, "⚙️")
            
            with st.expander(f"{icon} **{sys}**", expanded=(i < 2)):
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

# --- TAB 2: SITIOS FÍSICOS ---
with tab2:
    sites = sorted(df_filtered['Cerro'].unique())
    
    for site in sites:
        with st.expander(f"📍 **{site}**", expanded=False):
            sub_df = df_filtered[df_filtered['Cerro'] == site].copy()
            
            c1, c2 = st.columns([1, 3])
            
            with c1:
                masters_count = len(sub_df[sub_df['Rol'] == 'Master'])
                total_count = len(sub_df)
                
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

# --- TAB 3: MATRIZ ---
with tab3:
    st.markdown("### 🗺️ Mapa de Distribución de Equipos")
    st.markdown("<br>", unsafe_allow_html=True)
    
    pivot = pd.pivot_table(
        df_filtered,
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

# ============================================
# FOOTER
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.85rem; 
            padding: 20px; border-top: 1px solid #e2e8f0;'>
    <strong>Minera Zaldívar</strong> • Monitor de Infraestructura IPSC • 2026<br>
    <small>Última actualización: {}</small>
</div>
""".format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')), unsafe_allow_html=True)
