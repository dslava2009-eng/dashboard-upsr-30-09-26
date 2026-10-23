import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- 1. НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="Аналитика портфеля", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #F8F9FA;
        background-image: repeating-linear-gradient(
            45deg, transparent, transparent 10px, rgba(0, 0, 0, 0.02) 10px, rgba(0, 0, 0, 0.02) 11px
        );
    }
    section[data-testid="stSidebar"] { background-color: #F0F2F6; }
    div[data-testid="stPlotlyChart"] {
        background-color: #FFFFFF; border-radius: 8px; padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF; padding: 15px; border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF; border-radius: 8px; padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Дашборд страхового портфеля")
st.markdown("Интерактивный анализ (2025 vs 2026)")

# --- 2. ЗАГРУЗКА ДАННЫХ ---
@st.cache_data
def load_data():
    # 1. УБЫТОЧНОСТЬ (Продукты)
    data_products_2025 = {
        'Название': ['506 ОСЦПВ', '500 КАСКО', '511 Майно', '515 Медичне', '510 КАСКО Застава'],
        '31.03.2025': [54.44, 50.81, 29.78, 41.15, 7.94],
        '31.05.2025': [56.73, 75.44, 43.94, 40.25, 14.79],
        '30.06.2025': [57.79, 75.86, 24.05, 39.13, 14.52],
        '31.07.2025': [58.13, 65.90, 22.93, 38.52, 15.72],
        '31.08.2025': [58.80, 62.78, 19.44, 38.20, 15.15],
        '30.09.2025': [59.22, 64.69, 8.76, 38.56, 15.19]
    }
    data_products_2026 = {
        'Название': ['506 ОСЦПВ', '500 КАСКО', '511 Майно', '515 Медичне', '510 КАСКО Застава'],
        '31.03.2026': [58.27, 30.05, 1.79, 25.95, 6.29],
        '31.05.2026': [64.29, 71.93, 23.85, 30.30, 6.04],
        '30.06.2026': [59.77, 52.48, 843.31, 29.47, 7.80],
        '31.07.2026': [59.90, 40.71, 599.51, 28.56, 8.26],
        '31.08.2026': [64.52, 38.25, 656.63, 27.62, 8.81],
        '30.09.2026': [65.81, 33.69, 196.92, 26.56, 7.10]
    }

    # 2. ЗОНЫ (506)
    zones_2025 = {
        'Название': ['Меньше 100 тис.', 'Від 100 до 500 тис.', 'м. Київ', 'Більше 1 млн.', 
                     'Бориспіль, Боярка', 'Від 500 тис. до 1 млн.', 'Інші країни'],
        '31.03.2025': [36.53, 48.09, 34.84, 34.52, 41.79, 40.90, 5.75],
        '31.05.2025': [37.38, 50.35, 37.20, 37.09, 40.65, 38.20, 5.42],
        '30.06.2025': [38.07, 50.80, 38.24, 37.35, 48.15, 36.19, 5.30],
        '31.07.2025': [37.60, 50.21, 40.73, 38.76, 42.33, 37.04, 5.21],
        '31.08.2025': [37.77, 50.40, 39.85, 43.82, 40.68, 35.25, 5.14],
        '30.09.2025': [38.69, 50.39, 40.92, 40.45, 40.02, 35.22, 16.66]
    }
    zones_2026 = {
        'Название': ['Меньше 100 тис.', 'Від 100 до 500 тис.', 'м. Київ', 'Більше 1 млн.', 
                     'Бориспіль, Боярка', 'Від 500 тис. до 1 млн.', 'Інші країни'],
        '31.03.2026': [42.66, 36.69, 34.62, 34.16, 84.21, 109.27, 0.00],
        '31.05.2026': [43.07, 57.25, 24.42, 28.79, 44.22, 58.94, 34.57],
        '30.06.2026': [41.38, 47.71, 31.29, 32.96, 31.42, 40.77, 65.15],
        '31.07.2026': [36.37, 49.40, 30.84, 43.53, 26.33, 41.84, 60.93],
        '31.08.2026': [41.19, 57.66, 35.37, 46.01, 23.55, 50.41, 50.34],
        '30.09.2026': [39.90, 59.06, 44.15, 43.63, 22.02, 52.21, 47.75]
    }

    # 3. НЕТТО-СТАВКИ (506)
    netto_2025 = {
        'Название': ['Меньше 100 тис.', 'Від 100 до 500 тис.', 'м. Київ', 'Більше 1 млн.', 
                     'Бориспіль, Боярка', 'Від 500 тис. до 1 млн.', 'Інші країни'],
        '31.03.2025': [848, 1641, 1795, 1511, 1948, 1497, 164],
        '31.05.2025': [875, 1734, 1939, 1644, 1918, 1406, 160],
        '30.06.2025': [893, 1755, 2002, 1663, 2281, 1335, 159],
        '31.07.2025': [883, 1738, 2140, 1732, 2012, 1370, 158],
        '31.08.2025': [888, 1748, 2098, 1963, 1936, 1306, 157],
        '30.09.2025': [911, 1751, 2160, 1817, 1909, 1307, 513]
    }
    netto_2026 = {
        'Название': ['Меньше 100 тис.', 'Від 100 до 500 тис.', 'м. Київ', 'Більше 1 млн.', 
                     'Бориспіль, Боярка', 'Від 500 тис. до 1 млн.', 'Інші країни'],
        '31.03.2026': [986, 1258, 1868, 1596, 4206, 4086, 0],
        '31.05.2026': [1013, 2011, 1321, 1341, 2237, 2227, 832],
        '30.06.2026': [987, 1694, 1703, 1538, 1603, 1555, 1598],
        '31.07.2026': [879, 1774, 1685, 2033, 1354, 1613, 1520],
        '31.08.2026': [1008, 2088, 1939, 2155, 1225, 1954, 1262],
        '30.09.2026': [987, 2152, 2427, 2046, 1156, 2037, 1230]
    }

    # 4. НАГРУЗКИ И СРЕДНЯЯ ПРЕМИЯ (506) - 2025
    loads_data_2025 = {
        'Название': ['Меньше 100 тис.', 'Від 100 до 500 тис.', 'м. Київ', 'Більше 1 млн.', 
                     'Бориспіль, Боярка', 'Від 500 тис. до 1 млн.', 'Інші країни'],
        'Фин': [0.34, 0.34, 0.28, 0.27, 0.28, 0.33, 0.31],
        'Налог': [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
        'МТСБУ': [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06],
        'ОР': [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
        'ВП': [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
        'Тариф': [1.02, 1.13, 0.98, 0.96, 0.97, 0.97, 0.77],
        'Уб факт': [0.39, 0.50, 0.41, 0.40, 0.40, 0.35, 0.17],
        'Уб план': [0.37, 0.37, 0.43, 0.44, 0.43, 0.38, 0.40],
        'СП ср факт': [2361, 3501, 5317, 4533, 4787, 3733, 3158],
        'СП ср план': [2451, 4684, 5037, 4113, 4486, 3452, 1295]
    }
    df_loads_2025 = pd.DataFrame(loads_data_2025)
    df_loads_2025['Год'] = '2025'

    # 5. НАГРУЗКИ И СРЕДНЯЯ ПРЕМИЯ (506) - 2026
    loads_data_2026 = {
        'Название': ['Меньше 100 тис.', 'Від 100 до 500 тис.', 'м. Київ', 'Більше 1 млн.', 
                     'Бориспіль, Боярка', 'Від 500 тис. до 1 млн.', 'Інші країни'],
        'Фин': [0.33, 0.33, 0.26, 0.26, 0.28, 0.32, 0.31],
        'Налог': [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
        'МТСБУ': [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06],
        'ОР': [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
        'ВП': [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
        'Тариф': [1.02, 1.21, 0.99, 0.98, 0.79, 1.13, 1.08],
        'Уб факт': [0.40, 0.59, 0.44, 0.44, 0.22, 0.52, 0.48],
        'Уб план': [0.38, 0.38, 0.45, 0.45, 0.43, 0.39, 0.40],
        'СП ср факт': [2608, 3790, 5676, 4864, 5473, 4072, 3157],
        'СП ср план': [2590, 5623, 5397, 4502, 2689, 5256, 3111]
    }
    df_loads_2026 = pd.DataFrame(loads_data_2026)
    df_loads_2026['Год'] = '2026'

    # Объединяем нагрузки
    df_loads = pd.concat([df_loads_2025, df_loads_2026], ignore_index=True)
   
    # 6. ОРГАНИЗАЦИИ (Убыточность)
    orgs_2025 = {
        'Название': [
            'УПСК', 'Рівненська філія', 'Київська філія', 'Рівненська дирекція', 
            'Полтавське ОУ', 'Київська дирекція', 'Черкаська філія', 
            'Західна дирекція', 'Івано-Франківське ОУ', 'Хмельницьке ОУ'
        ],
        '31.03.2025': [20.48, 44.64, 56.14, 55.40, 39.08, 48.36, 43.30, 54.28, 79.37, 56.16],
        '31.05.2025': [27.58, 47.13, 27.57, 58.49, 38.49, 74.73, 43.15, 52.05, 78.22, 56.31],
        '30.06.2025': [27.90, 48.34, 27.94, 59.28, 37.84, 75.22, 43.31, 53.67, 46.44, 57.94],
        '31.07.2025': [27.66, 46.69, 27.70, 58.10, 39.10, 62.35, 42.19, 52.28, 45.25, 55.57],
        '31.08.2025': [26.17, 50.92, 28.37, 58.88, 39.88, 61.22, 42.98, 51.33, 43.96, 55.99],
        '30.09.2025': [24.46, 50.05, 28.82, 59.03, 40.62, 61.68, 44.33, 51.31, 48.62, 56.38]
    }
    orgs_2026 = {
        'Название': [
            'УПСК', 'Рівненська філія', 'Київська філія', 'Рівненська дирекція', 
            'Полтавське ОУ', 'Київська дирекція', 'Черкаська філія', 
            'Західна дирекція', 'Івано-Франківське ОУ', 'Хмельницьке ОУ'
        ],
        '31.03.2026': [15.78, 71.78, 18.67, 44.81, 15.76, 38.05, 59.71, 75.35, 26.93, 47.01],
        '31.05.2026': [29.91, 55.46, 22.42, 44.91, 24.03, 86.59, 67.13, 53.17, 73.11, 77.17],
        '30.06.2026': [159.39, 50.89, 24.06, 62.25, 26.57, 43.36, 70.98, 38.21, 55.84, 86.70],
        '31.07.2026': [118.30, 53.57, 23.27, 52.55, 22.75, 38.14, 69.52, 40.41, 42.65, 61.67],
        '31.08.2026': [93.02, 327.27, 34.83, 50.98, 37.77, 37.51, 69.62, 42.43, 61.36, 64.36],
        '30.09.2026': [23.55, 273.14, 33.06, 53.35, 34.94, 47.78, 61.82, 56.22, 52.39, 56.96]
    }

    def melt_data(data_dict, year_label):
        df = pd.DataFrame(data_dict)
        df_long = df.melt(id_vars=['Название'], var_name='Дата', value_name='Значение')
        df_long['Дата'] = pd.to_datetime(df_long['Дата'], format='%d.%m.%Y')
        df_long['Рік'] = year_label
        df_long['Месяц'] = df_long['Дата'].dt.strftime('%b')
        return df_long

    df_products = pd.concat([melt_data(data_products_2025, '2025'), melt_data(data_products_2026, '2026')], ignore_index=True)
    df_products['Показатель'] = 'Убыточность'
    
    df_zones = pd.concat([melt_data(zones_2025, '2025'), melt_data(zones_2026, '2026')], ignore_index=True)
    df_zones['Показатель'] = 'Убыточность'
    
    df_netto = pd.concat([melt_data(netto_2025, '2025'), melt_data(netto_2026, '2026')], ignore_index=True)
    df_netto['Показатель'] = 'Нетто-ставка'
    
    df_orgs = pd.concat([melt_data(orgs_2025, '2025'), melt_data(orgs_2026, '2026')], ignore_index=True)
    df_orgs['Показатель'] = 'Убыточность'

    df_top10_2025 = pd.DataFrame({
        'Клиент': ["ПрАТ «Тернопільський молокозавод»", "Кадіум груп 2025", "ПрАТ «Костопільський завод скловиробів»", "ТОВ «ФУТБОЛЬНИЙ КЛУБ «ЛНЗ»"],
        'Договоры': [1, 349, 1, 2],
        'Премия (грн)': [4550400, 3035020, 1425600, 972435],
        'Убыточность (%)': [78.72, 37.36, 15.25, 14.07]
    })
    
    df_top10_2026 = pd.DataFrame({
        'Клиент': ["Плейтекс", "ПАТ «ЮРІЯ»", "ППО КП Вінницької міської ради", "ПрАТ «НАК «НАДРА УКРАЇНИ»", "Київ-Атлантік Україна АТ", "ТОВ «Кременчуцький завод технічного вуглецю»", "ПРИВАТНЕ ПІДПРИЄМСТВО «УКРГОСПТОВАРИ»", "Сільськогосподарське товариство «АГРОКО»", "ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ «СІД КОРП»", "ТОВ «Першотравневий молочноконсервний комбінат»"],
        'Договоры': [447, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'Премия (грн)': [10441428, 3270900, 3100680, 2241545, 1926432, 2640000, 1944600, 1144080, 1219680, 840240],
        'Убыточность (%)': [19.31, 28.34, 19.69, 64.34, 0.00, 32.19, 25.80, 13.15, 12.64, 10.68]
    })

    df_leleka = pd.DataFrame({
        'Год': ['2025', '2026'],
        'Договоры': [1128, 649],
        'Премия (грн)': [2412365, 2799206],
        'Выплаты (грн)': [472700, 589500],
        'Убыточность (%)': [19.82, 30.58],
        'Валовая маржа (грн)': [606773, 1486932],
        'Валовая маржа (%)': [25.15, 53.12]
    })

    return df_products, df_zones, df_netto, df_orgs, df_top10_2025, df_top10_2026, df_leleka, df_loads

# --- 3. ВЫЗОВ ФУНКЦИИ ЗАГРУЗКИ ---
df_products, df_zones, df_netto, df_orgs, df_top10_2025, df_top10_2026, df_leleka, df_loads = load_data()

# --- 4. БОКОВАЯ ПАНЕЛЬ И ВКЛАДКИ ---
st.sidebar.header("Фильтры")

tab1, tab2, tab3, tab4 = st.tabs(["📈 Динамика", "🏆 ТОП-10 Клиентов", "🏥 Проект «Лелека»", "⚖️ Нагрузки (506)"])

# --- ВКЛАДКА 1: ДИНАМИКА ---
with tab1:
    selected_metric = st.sidebar.radio("Показатель:", options=['Убыточность', 'Нетто-ставка'])
    compare_mode = st.sidebar.checkbox("📈 Сравнить 2025 и 2026")

    if not compare_mode:
        selected_year = st.sidebar.radio("Выберите год:", options=['2025', '2026'], key="year_dynamics")
    else:
        selected_year = None

    if selected_metric == 'Нетто-ставка':
        st.sidebar.info("💡 Нетто-ставка доступна только в разрезе Зон (продукт 506)")
        view_mode = 'Зоны (только 506)'
        df_to_filter = df_netto
    else:
        view_mode = st.sidebar.radio("Разрез данных:", options=['Продукты', 'Организации', 'Зоны (только 506)'])
        if view_mode == 'Продукты':
            df_to_filter = df_products
        elif view_mode == 'Организации':
            df_to_filter = df_orgs
        else:
            df_to_filter = df_zones

    selected_item = None
    if view_mode == 'Продукты':
        selected_item = st.sidebar.selectbox("Выберите продукт:", options=df_products['Название'].unique())
    elif view_mode == 'Организации':
        selected_item = st.sidebar.selectbox("Выберите организацию:", options=df_orgs['Название'].unique())
    else:
        selected_item = st.sidebar.selectbox("Выберите зону:", options=df_zones['Название'].unique())

    if not compare_mode:
        filtered_df = df_to_filter[(df_to_filter['Название'] == selected_item) & (df_to_filter['Рік'] == selected_year)]
        if not filtered_df.empty:
            last_value = filtered_df['Значение'].iloc[-1]
            first_value = filtered_df['Значение'].iloc[0]
            
            if selected_metric == 'Нетто-ставка':
                value_str = f"{last_value:.0f} грн"
                delta_str = f"{last_value - first_value:.0f} грн (с начала года)"
            else:
                value_str = f"{last_value:.2f}%"
                delta_str = f"{last_value - first_value:.2f}% (с начала года)"
                
            st.metric(label=f"{selected_metric} ({selected_item}, {selected_year})", value=value_str, delta=delta_str)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=filtered_df['Месяц'], y=filtered_df['Значение'], mode='lines+markers+text',
                text=[f"{v:.0f}" if selected_metric == 'Нетто-ставка' else f"{v:.1f}%" for v in filtered_df['Значение']],
                textposition="top center", line=dict(width=3, color='#1f3a5f'), marker=dict(size=8)
            ))
            fig.update_xaxes(title_text="Месяц")
            fig.update_yaxes(title_text=f"{selected_metric}")
            fig.update_layout(title=f"Динамика: {selected_item} ({selected_year})")
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("Показать все данные"):
                st.dataframe(filtered_df[['Название', 'Дата', 'Значение']], use_container_width=True)
    else:
        filtered_df = df_to_filter[df_to_filter['Название'] == selected_item]
        df_25 = filtered_df[filtered_df['Рік'] == '2025']
        df_26 = filtered_df[filtered_df['Рік'] == '2026']

        if not df_25.empty and not df_26.empty:
            last_25 = df_25['Значение'].iloc[-1]
            last_26 = df_26['Значение'].iloc[-1]
            
            if selected_metric == 'Нетто-ставка':
                value_str = f"{last_26:.0f} грн"
                delta_str = f"{last_26 - last_25:.0f} грн (к 2025)"
            else:
                value_str = f"{last_26:.2f}%"
                delta_str = f"{last_26 - last_25:.2f}% (к 2025)"
                
            st.metric(label=f"Сравнение (сентябрь): 2026 vs 2025 ({selected_item})", value=value_str, delta=delta_str)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_25['Месяц'], y=df_25['Значение'], mode='lines+markers+text', name='2025',
                text=[f"{v:.0f}" if selected_metric == 'Нетто-ставка' else f"{v:.1f}%" for v in df_25['Значение']],
                textposition="bottom center", line=dict(width=2, color='#8fb3d9', dash='dash'), marker=dict(size=6)
            ))
            fig.add_trace(go.Scatter(
                x=df_26['Месяц'], y=df_26['Значение'], mode='lines+markers+text', name='2026',
                text=[f"{v:.0f}" if selected_metric == 'Нетто-ставка' else f"{v:.1f}%" for v in df_26['Значение']],
                textposition="top center", line=dict(width=3, color='#f18a21'), marker=dict(size=8)
            ))
            fig.update_xaxes(title_text="Месяц")
            fig.update_yaxes(title_text=f"{selected_metric}")
            fig.update_layout(title=f"Сравнение: {selected_item} ({selected_metric})", hovermode="x unified", legend=dict(orientation="h"))
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("Показать все данные"):
                st.dataframe(filtered_df[['Название', 'Дата', 'Значение']], use_container_width=True)

# --- ВКЛАДКА 2: ТОП-10 КЛИЕНТОВ ---
with tab2:
    st.header("ТОП-10 корпоративных клиентов")
    client_year = st.radio("Выберите год:", options=['2025', '2026'], horizontal=True)
    
    df_clients = df_top10_2025 if client_year == '2025' else df_top10_2026
    df_clients = df_clients.sort_values(by="Убыточность (%)", ascending=False)
    
    total_premium = df_clients['Премия (грн)'].sum()
    total_contracts = df_clients['Договоры'].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("Суммарная премия ТОП-10", f"{total_premium/1e6:.1f} млн грн")
    col2.metric("Всего договоров", f"{total_contracts}")
    
    st.dataframe(df_clients, use_container_width=True, hide_index=True)

    fig_clients = px.bar(
        df_clients, x='Убыточность (%)', y='Клиент', orientation='h',
        title=f'Убыточность ТОП-10 клиентов ({client_year})',
        color='Убыточность (%)', color_continuous_scale='Reds'
    )
    fig_clients.update_yaxes(showticklabels=False)
    fig_clients.update_layout(height=500)
    st.plotly_chart(fig_clients, use_container_width=True)

# --- ВКЛАДКА 3: ПРОЕКТ ЛЕЛЕКА ---
with tab3:
    st.header("Проект «Лелека» (коды 514, 515)")
    st.markdown("Сравнение показателей за 2025 и 2026 годы")
    
    st.dataframe(df_leleka, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)

    with col1:
        fig_ub = go.Figure()
        fig_ub.add_trace(go.Bar(
            x=df_leleka['Год'], y=df_leleka['Убыточность (%)'],
            name='Убыточность, %', marker_color=['#8fb3d9', '#f18a21'],
            text=[f"{v:.2f}%" for v in df_leleka['Убыточность (%)']], textposition='auto'
        ))
        fig_ub.update_layout(title='Убыточность проекта «Лелека»', yaxis_title='Убыточность, %', yaxis=dict(range=[0, 40]))
        st.plotly_chart(fig_ub, use_container_width=True)

    with col2:
        fig_margin = go.Figure()
        fig_margin.add_trace(go.Bar(
            x=df_leleka['Год'], y=df_leleka['Валовая маржа (грн)'],
            name='Маржа, грн', marker_color=['#8fb3d9', '#f18a21'],
            text=[f"{v:,.0f} грн".replace(',', ' ') for v in df_leleka['Валовая маржа (грн)']], 
            textposition='auto'
        ))
        fig_margin.update_layout(title='Валовая маржа проекта «Лелека» (грн)', yaxis_title='Сумма, грн')
        st.plotly_chart(fig_margin, use_container_width=True)

    st.info("""
    **Висновок:** У 2026 році проект «Лелека» показав значне зростання валової маржі (як у гривнях, так і у відсотках), 
    незважаючи на зростання убыточности з 19.82% до 30.58%. Це свідчить про оптимізацію витрат (зниження ФІН/КВ) 
    та значне збільшення премій при меншій кількості договорів.
    """)

# # --- ВКЛАДКА 4: НАГРУЗКИ (506) ---
with tab4:
    st.header("Нетто-ставка и нагрузка: 506 (по зонам)")
    st.markdown("Сравнение фактической и плановой средней премии (СП) по зонам")

    # Переключатель года
    load_year = st.radio("Выберите год:", options=['2025', '2026'], horizontal=True, key="year_loads")
    df_current = df_loads[df_loads['Год'] == load_year].copy()

    # Считаем коэффициент
    df_current['Коэф. план/факт'] = df_current.apply(
        lambda row: row['СП ср план'] / row['СП ср факт'] if row['СП ср факт'] > 0 else 0, 
        axis=1
    ).round(2)

    # --- ДОБАВЛЯЕМ ИТОГОВУЮ СТРОКУ (ИСПРАВЛЕНО ПО ВАШИМ СКРИНШОТАМ) ---
    if load_year == '2025':
        total_row = pd.DataFrame([{
            'Название': 'Всего',
            'Фин': 0.33, 'Налог': 0.03, 'МТСБУ': 0.06, 'ОР': 0.10, 'ВП': 0.10,
            'Тариф': 1.03, 'Уб факт': 0.42, 'Уб план': 0.38,
            'СП ср факт': 2923, 'СП ср план': 3159,
            'Год': '2025',
            'Коэф. план/факт': 1.08
        }])
    else: # 2026
        total_row = pd.DataFrame([{
            'Название': 'Всего',
            'Фин': 0.32, 'Налог': 0.03, 'МТСБУ': 0.06, 'ОР': 0.10, 'ВП': 0.10,
            'Тариф': 1.06, 'Уб факт': 0.45, 'Уб план': 0.39,
            'СП ср факт': 3132, 'СП ср план': 3428,
            'Год': '2026',
            'Коэф. план/факт': 1.09
        }])
    
    # Объединяем данные с итоговой строкой
    df_display = pd.concat([df_current, total_row], ignore_index=True)

    # Форматируем проценты для красивого вывода в таблице
    df_show = df_display.copy()
    for col in ['Фин', 'Налог', 'МТСБУ', 'ОР', 'ВП', 'Уб факт', 'Уб план', 'Тариф']:
        df_show[col] = df_show[col].apply(lambda x: f"{x*100:.0f}%")
    for col in ['СП ср факт', 'СП ср план']:
        df_show[col] = df_show[col].apply(lambda x: f"{x:,.0f}".replace(',', ' '))

    # Выбираем только нужные колонки
    columns_to_show = ['Название', 'Фин', 'Налог', 'МТСБУ', 'ОР', 'ВП', 'Тариф', 
                       'Уб факт', 'Уб план', 'СП ср факт', 'СП ср план', 'Коэф. план/факт']
    
    st.dataframe(df_show[columns_to_show], use_container_width=True, hide_index=True)

    # --- ГРАФИК СРАВНЕНИЯ СП ---
    df_chart = df_current.copy()

    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        x=df_chart['Название'], y=df_chart['СП ср факт'],
        name='СП ср факт', marker_color='#1f3a5f',
        text=[f"{v:,.0f}" for v in df_chart['СП ср факт']], textposition='auto'
    ))
    fig_compare.add_trace(go.Bar(
        x=df_chart['Название'], y=df_chart['СП ср план'],
        name='СП ср план', marker_color='#f18a21',
        text=[f"{v:,.0f}" for v in df_chart['СП ср план']], textposition='auto'
    ))
    fig_compare.update_layout(
        title=f'Сравнение фактической и плановой средней премии ({load_year})',
        barmode='group',
        yaxis_title='Средняя премия, грн',
        xaxis_title='Зона',
        hovermode='x unified'
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    # --- ТЕКСТОВЫЙ ВЫВОД (ДИНАМИЧЕСКИЙ) ---
    st.subheader("Вывод по коэффициенту «план/факт»")

    # Разделяем зоны по значению коэффициента
    bad_zones = df_current[df_current['Коэф. план/факт'] > 1]['Название'].tolist()
    good_zones = df_current[df_current['Коэф. план/факт'] < 1]['Название'].tolist()
    ok_zones = df_current[df_current['Коэф. план/факт'] == 1]['Название'].tolist()

    # Формируем строки для вывода
    bad_str = ', '.join(bad_zones) if bad_zones else 'нет'
    good_str = ', '.join(good_zones) if good_zones else 'нет'
    ok_str = ', '.join(ok_zones) if ok_zones else 'нет'

    st.markdown(f"""
**Коэффициент «план/факт» = СП ср план / СП ср факт**

* 🔴 **Коэффициент > 1 — плохой показатель.** Фактическая средняя премия ниже плановой, 
  то есть текущей премии **не хватает**, чтобы покрыть убытки и нагрузки 
  (финансирование, налог, отчисления МТСБУ, валовую прибыль и операционные расходы).  
  **Зоны с коэффициентом > 1 ({load_year}):** {bad_str}.

* 🟢 **Коэффициент < 1 — хороший показатель.** Фактическая средняя премия выше плановой, 
  то есть собранной премии **хватает** на покрытие убытков и нагрузок с запасом.  
  **Зоны с коэффициентом < 1 ({load_year}):** {good_str}.

* 🟡 **Коэффициент = 1 — всего хватает.** Фактическая премия ровно совпала с плановой: 
  покрытие убытков и нагрузок идёт ровно «в ноль», без запаса.  
  **Зоны с коэффициентом = 1 ({load_year}):** {ok_str}.
""")

    # --- АНАЛИЗ ОТКЛОНЕНИЙ ---
    st.subheader("Анализ отклонений")
    df_current['Отклонение СП, грн'] = df_current['СП ср факт'] - df_current['СП ср план']
    df_current['Отклонение СП, %'] = (df_current['СП ср факт'] / df_current['СП ср план'] - 1) * 100
    
    worst_zone = df_current.loc[df_current['Отклонение СП, %'].idxmin()]
    best_zone = df_current.loc[df_current['Отклонение СП, %'].idxmax()]
    
    st.info(f"""
    **Ключевые наблюдения ({load_year}):**
    *   **Наибольшее недовыполнение плана по СП:** {worst_zone['Название']} (факт {worst_zone['СП ср факт']:,.0f} грн против плана {worst_zone['СП ср план']:,.0f} грн, отклонение {worst_zone['Отклонение СП, %']:.1f}%).
    *   **Наибольшее перевыполнение плана по СП:** {best_zone['Название']} (факт {best_zone['СП ср факт']:,.0f} грн против плана {best_zone['СП ср план']:,.0f} грн, отклонение +{best_zone['Отклонение СП, %']:.1f}%).
    *   **Среднее отклонение по зонам:** {df_current['Отклонение СП, %'].mean():+.1f}% (простое среднее по 7 зонам, сильно зависит от выбросов).
    """)

    # --- ГРАФИК ОТКЛОНЕНИЙ ---
    fig_diff = go.Figure()
    colors = ['#C62828' if x < 0 else '#4CAF50' for x in df_current['Отклонение СП, %']]
    fig_diff.add_trace(go.Bar(
        x=df_current['Название'], y=df_current['Отклонение СП, %'],
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in df_current['Отклонение СП, %']], textposition='auto'
    ))
    fig_diff.update_layout(
        title=f'Отклонение фактической СП от плановой ({load_year})',
        yaxis_title='Отклонение, %',
        xaxis_title='Зона',
        yaxis=dict(zeroline=True, zerolinewidth=1, zerolinecolor='black')
    )
    st.plotly_chart(fig_diff, use_container_width=True)