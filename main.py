import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import pandas as pd

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 커스텀 디자인
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="대한민국 인구 지표 지도",
    page_icon="🗺️",
    layout="wide"
)

st.markdown("""
    <style>
    /* 메인 타이틀 & 설명 스타일 */
    .main-title {
        color: #d63384;
        font-weight: 800;
        font-size: 2rem;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #6c757d;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    
    /* 지표 카드 스타일 */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        border: 1px solid #fecfef;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(214, 51, 132, 0.08);
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #d63384;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #555;
        margin-top: 0.2rem;
    }

    /* 경고 안내 박스 */
    .warning-box {
        background-color: #f8f9fa;
        border-left: 4px solid #adb5bd;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #495057;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🗺️ 대한민국 연도별 인구 지표 지도</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">시군구별 고령화율 및 유소년 비율의 변화를 한눈에 확인해보세요! 🎈</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 예시 데이터 생성 및 행정구역 코드 매핑 보정 함수
# (실제 서비스 환경에서는 외부 CSV/JSON 데이터를 load하도록 대체 가능)
# -----------------------------------------------------------------------------
@st.cache_data
def get_sido_mapping():
    return {
        "전국": "전국",
        "서울특별시": "11",
        "부산광역시": "26",
        "대구광역시": "27",
        "인천광역시": "28",
        "광주광역시": "29",
        "대전광역시": "30",
        "울산광역시": "31",
        "세종특별자치시": "36",
        "경기도": "41",
        "강원특별자치도": "51",
        "충청북도": "43",
        "충청남도": "44",
        "전북특별자치도": "52",
        "전라남도": "46",
        "경상북도": "47",
        "경상남도": "48",
        "제주특별자치도": "50"
    }

@st.cache_data
def load_and_fix_data():
    """
    행정구역 코드 개편 대응:
    - 옛 강원(42) -> 51
    - 옛 전북(45) -> 52
    - 군위군(47720) -> 27720
    """
    years = [2020, 2021, 2022, 2023, 2024]
    
    # 예시 데이터 프레임 생성 (시군구 단위)
    sample_regions = [
        {"code": "11110", "name": "종로구", "sido": "11", "lat": 37.573, "lng": 126.979},
        {"code": "27720", "name": "군위군", "sido": "27", "lat": 36.242, "lng": 128.572}, # 보정된 대구 군위군
        {"code": "51110", "name": "춘천시", "sido": "51", "lat": 37.881, "lng": 127.730}, # 강원 -> 51
        {"code": "52110", "name": "전주시", "sido": "52", "lat": 35.824, "lng": 127.148}, # 전북 -> 52
        {"code": "41110", "name": "수원시", "sido": "41", "lat": 37.263, "lng": 127.028},
        {"code": "48110", "name": "창원시", "sido": "48", "lat": 35.228, "lng": 128.681},
        {"code": "50110", "name": "제주시", "sido": "50", "lat": 33.499, "lng": 126.531},
    ]
    
    rows = []
    import random
    random.seed(42)
    
    for year in years:
        for r in sample_regions:
            # 연도가 올라갈수록 고령화율 상승, 유소년 비율 감소 경향 반영
            base_elder = 15 + (year - 2020) * 1.2
            base_youth = 14 - (year - 2020) * 0.8
            
            # 지역별 변동
            if r["code"] == "27720": # 군위군 (초고령)
                elder_rate = base_elder + 22.0 + random.uniform(-0.5, 0.5)
                youth_rate = max(3.0, base_youth - 6.0 + random.uniform(-0.3, 0.3))
            elif r["code"] == "41110": # 수원시 (젊은 도시)
                elder_rate = base_elder - 4.0 + random.uniform(-0.5, 0.5)
                youth_rate = base_youth + 3.0 + random.uniform(-0.3, 0.3)
            else:
                elder_rate = base_elder + random.uniform(-3, 3)
                youth_rate = base_youth + random.uniform(-2, 2)
                
            rows.append({
                "year": year,
                "code": r["code"],
                "name": r["name"],
                "sido_code": r["sido"],
                "elder_rate": round(elder_rate, 1),
                "youth_rate": round(youth_rate, 1),
                "lat": r["lat"],
                "lng": r["lng"]
            })
            
    df = pd.DataFrame(rows)
    
    # -----------------------------------------------------
    # 행정구역 변경 보정 로직 적용 (요청사항 반영)
    # -----------------------------------------------------
    def fix_code(c):
        c_str = str(c)
        if c_str.startswith("42"): # 옛 강원도 -> 51
            return "51" + c_str[2:]
        elif c_str.startswith("45"): # 옛 전라북도 -> 52
            return "52" + c_str[2:]
        elif c_str == "47720": # 옛 경북 군위군 -> 대구 군위군
            return "27720"
        return c_str

    df["code"] = df["code"].apply(fix_code)
    return df

df_all = load_and_fix_data()
sido_dict = get_sido_mapping()

# -----------------------------------------------------------------------------
# 3. 사용자 제어 옵션 (사이드바 / 컨트롤)
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ 검색 옵션")

# 1) 지표 선택
indicator = st.sidebar.radio(
    "📊 분석 지표 선택",
    options=["고령화율 (65세 이상 %)", "유소년 비율 (0~14세 %)"],
    index=0
)

# 2) 연도 선택 슬라이더
selected_year = st.sidebar.slider(
    "📅 연도 선택",
    min_value=2020,
    max_value=2024,
    value=2024,
    step=1
)

# 3) 시도 선택 드롭다운
selected_sido_name = st.sidebar.selectbox(
    "📍 지역 선택 (확대 보기)",
    options=list(sido_dict.keys()),
    index=0
)
selected_sido_code = sido_dict[selected_sido_name]

# -----------------------------------------------------------------------------
# 4. 필터링 및 지표 구간/색상 설정
# -----------------------------------------------------------------------------
# 연도별 데이터 필터링
df_year = df_all[df_all["year"] == selected_year].copy()

# 지표 설정 분기
if "고령화율" in indicator:
    metric_col = "elder_rate"
    metric_title = "고령화율"
    # 고령화율 固定 고정 구간: 19, 23, 28, 38 (%)
    thresholds = [0, 19, 23, 28, 38, 100]
    colors = ["#fef0d9", "#fdcc8a", "#fc8d59", "#e34a33", "#b30000"] # 연한 주황 -> 진한 빨강
    labels = ["19% 미만", "19% ~ 23%", "23% ~ 28%", "28% ~ 38%", "38% 이상"]
else:
    metric_col = "youth_rate"
    metric_title = "유소년 비율"
    # 유소년 비율 맞춤 고정 구간: 8, 10, 12, 14 (%)
    thresholds = [0, 8, 10, 12, 14, 100]
    colors = ["#edf8fb", "#b2e2e2", "#66c2a4", "#2ca25f", "#006d2c"] # 연한 청록 -> 진한 초록
    labels = ["8% 미만", "8% ~ 10%", "10% ~ 12%", "12% ~ 14%", "14% 이상"]

def get_color(val):
    if pd.isna(val):
        return "#808080" # 데이터 없는 경우 회색 처리
    for i in range(len(thresholds) - 1):
        if thresholds[i] <= val < thresholds[i+1]:
            return colors[i]
    return colors[-1]

# -----------------------------------------------------------------------------
# 5. 지표 카드 3장 상단 배치
# -----------------------------------------------------------------------------
# 전국 평균, 최댓값, 최솟값 계산
nat_avg = df_year[metric_col].mean()
max_row = df_year.loc[df_year[metric_col].idxmax()]
min_row = df_year.loc[df_year[metric_col].idxmin()]

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🇰🇷 {selected_year}년 전국 평균 {metric_title}</div>
            <div class="metric-value">{nat_avg:.1f}%</div>
            <div class="metric-sub">전국 시군구 평균</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🔺 가장 높은 시군구</div>
            <div class="metric-value">{max_row[metric_col]}%</div>
            <div class="metric-sub">{max_row['name']}</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🔹 가장 낮은 시군구</div>
            <div class="metric-value">{min_row[metric_col]}%</div>
            <div class="metric-sub">{min_row['name']}</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. 지도 구성 (시도 확대 & 좌표 설정)
# -----------------------------------------------------------------------------
# 시도별 중심 위치 및 줌 레벨 지정
sido_centers = {
    "전국": ([36.2, 127.8], 7),
    "서울특별시": ([37.5665, 126.9780], 11),
    "부산광역시": ([35.1796, 129.0756], 11),
    "대구광역시": ([35.8714, 128.6014], 10),
    "인천광역시": ([37.4563, 126.7052], 10),
    "광주광역시": ([35.1595, 126.8526], 11),
    "대전광역시": ([36.3504, 127.3845], 11),
    "울산광역시": ([35.5384, 129.3114], 11),
    "세종특별자치시": ([36.4800, 127.2890], 11),
    "경기도": ([37.4138, 127.5183], 9),
    "강원특별자치도": ([37.8228, 128.1555], 9),
    "충청북도": ([36.6357, 127.4913], 9),
    "충청남도": ([36.5184, 126.8000], 9),
    "전북특별자치도": ([35.7175, 127.1530], 9),
    "전라남도": ([34.8161, 126.4629], 9),
    "경상북도": ([36.5760, 128.5056], 8),
    "경상남도": ([35.4606, 128.2132], 9),
    "제주특별자치도": ([33.4996, 126.5312], 10)
}

center_coords, zoom_lvl = sido_centers.get(selected_sido_name, ([36.2, 127.8], 7))

# Folium 지도 객체 생성
m = folium.Map(location=center_coords, zoom_start=zoom_lvl, tiles="cartodbpositron")

# 시도 필터링
if selected_sido_code != "전국":
    display_df = df_year[df_year["sido_code"] == selected_sido_code]
else:
    display_df = df_year

# 서클 마커로 지도상에 표현 (GeoJSON 경계 연결 시 동일하게 맵핑 가능)
for _, row in display_df.iterrows():
    val = row[metric_col]
    color = get_color(val)
    
    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=12,
        fill=True,
        fill_color=color,
        color="#333333",
        weight=1,
        fill_opacity=0.85,
        popup=f"<b>{row['name']}</b> ({selected_year})<br>{metric_title}: {val}%",
        tooltip=f"{row['name']}: {val}%"
    ).add_to(m)

# 지도 출력
st_folium(m, width="100%", height=500)

# -----------------------------------------------------------------------------
# 7. 안내 문구 및 범례 표기
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="warning-box">
        ⚠️ <b>행정구역 코드 매핑 및 데이터 안내</b><br>
        • 연도별 행정구역 개편에 맞춰 <b>강원(42→51)</b>, <b>전북(45→52)</b>, <b>군위군(47720→27720)</b> 코드가 자동 보정되었습니다.<br>
        • 경계 데이터와 일치하지 않거나 통계값이 누락된 지역은 <b>회색(#808080)</b>으로 표시됩니다.
    </div>
""", unsafe_allow_html=True)
