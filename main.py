import streamlit as st

# 1. 페이지 기본 설정 (사랑스러운 아이콘과 제목)
st.set_page_config(
    page_title="설렘 가득 MBTI 여행 추천",
    page_icon="🌸",
    layout="centered"
)

# 2. 커스텀 CSS (사랑스러운 핑크 & 파스텔 톤 테마 적용)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 색상 느낌 맞추기 */
    .stApp {
        background-color: #fffafb;
    }
    /* 선택 박스 및 버튼 스타일 다듬기 */
    .stSelectbox label {
        color: #d63384 !important;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.7rem 1rem;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(255, 154, 158, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #fecfef 0%, #ff9a9e 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 사랑스러운 문구의 MBTI 여행지 데이터
mbti_recommendations = {
    "ISTJ": {
        "destination": "스위스 융프라우 🏔️✨",
        "tagline": "#완벽한_일정 #마음이_편안해지는 #청정자연",
        "desc": "정확하고 깨끗한 스위스는 마음의 평화를 줘요. 풍경을 바라보며 계획대로 즐기는 완벽한 힐링!"
    },
    "ISFJ": {
        "destination": "일본 교토 🍵🌸",
        "tagline": "#아기자기한_골목 #온천_힐링 #따스한_감성",
        "desc": "정갈한 거리와 따뜻한 온천이 기다리는 곳이에요. 소중한 사람과 온기를 나누기 딱 좋은 여행지랍니다."
    },
    "INFJ": {
        "destination": "아이슬란드 레이캬비크 🌌❄️",
        "tagline": "#신비로운_오로라 #나만의_사색 #몽환적인_풍경",
        "desc": "한 편의 동화 같은 오로라 아래에서 깊은 생각과 감성을 채울 수 있는 낭만적인 공간이에요."
    },
    "INTJ": {
        "destination": "영국 런던 🏰📚",
        "tagline": "#지적_호기심 #알찬_박물관 #고풍스러운_동선",
        "desc": "역사와 지성이 숨 쉬는 도시! 마음속 지도를 그리며 구석구석 알차게 탐험해 보세요."
    },
    "ISTP": {
        "destination": "뉴질랜드 퀸스타운 🪂🌿",
        "tagline": "#자유로운_모험 #스릴_만점 #자연그대로",
        "desc": "바람을 가르며 즐기는 자유! 액티비티를 즐기며 자유로운 에너지를 가득 채워보세요."
    },
    "ISFP": {
        "destination": "인도네시아 발리 🌴🍹",
        "tagline": "#포근한_휴식 #아름다운_노을 #예술적_감성",
        "desc": "느긋하게 일어나 바다를 바라보고, 노을빛 카페에서 여유를 만끽하는 포근한 휴양지예요."
    },
    "INFP": {
        "destination": "체코 프라하 🏰🎻",
        "tagline": "#동화_속_한장면 #낭만적인_야경 #감성_충전",
        "desc": "골목마다 버스킹 음악이 흐르는 감성의 성지! 내 안의 로맨틱한 꿈을 펼쳐보세요."
    },
    "INTP": {
        "destination": "독일 베를린 🎨🍺",
        "tagline": "#자유로운_영혼 #힙한_예술 #창의적_영감",
        "desc": "틀에 매이지 않는 독특한 문화와 지적인 박물관들이 당신의 호기심을 반갑게 맞아줄 거예요."
    },
    "ESTP": {
        "destination": "미국 라스베이거스 🎰✨",
        "tagline": "#화려한_밤 #심장_쿵쿵 #자극과_즐거움",
        "desc": "눈이 부시게 화려한 조명과 신나는 퍼포먼스! 지루할 틈 없이 매 순간이 에너제틱해요."
    },
    "ESFP": {
        "destination": "스페인 바르셀로나 💃🇪🇸",
        "tagline": "#열정의_축제 #신나는_해변 #모두가_친구",
        "desc": "밝은 햇살 아래 맛있는 타파스를 나누고, 어딜 가나 웃음꽃이 피어나는 파티 같은 도시!"
    },
    "ENFP": {
        "destination": "태국 방콕 🛺🌺",
        "tagline": "#알록달록_야시장 #매일이_통발탈출 #흥미진진",
        "desc": "통통 튀는 색감과 예측할 수 없는 즐거움! 당신의 호기심을 무한히 자극해 줄 모험지랍니다."
    },
    "ENTP": {
        "destination": "미국 뉴욕 🗽🍕",
        "tagline": "#트렌드의_중심 #반짝이는_아이디어 #지루함_제로",
        "desc": "세상의 모든 신선함이 모인 곳! 브로드웨이 뮤지컬부터 힙한 팝업스토어까지 에너지가 솟구쳐요."
    },
    "ESTJ": {
        "destination": "싱가포르 🏙️🌺",
        "tagline": "#쾌적함_100점 #완벽한_인프라 #알찬_일정",
        "desc": "깨끗함과 편리함이 조화로운 완벽한 도시! 계획한 대로 차곡차곡 추억을 쌓을 수 있어요."
    },
    "ESFJ": {
        "destination": "이탈리아 피렌체 🍕🍷",
        "tagline": "#따스한_사람들 #맛있는_음식 #사랑스러운_추억",
        "desc": "소중한 사람들과 맛있는 음식을 함께 나누며 따뜻한 사랑과 정을 느낄 수 있는 로맨틱한 도시예요."
    },
    "ENFJ": {
        "destination": "프랑스 파리 🥐🗼",
        "tagline": "#에펠탑_피크닉 #감성_교감 #로맨틱_끝판왕",
        "desc": "에펠탑 아래 잔디밭에서 소풍을 즐기고, 예술과 낭만을 마음껏 주고받는 사랑스러운 공간!"
    },
    "ENTJ": {
        "destination": "아랍에미리트 두바이 🇦🇪✨",
        "tagline": "#압도적_스케일 #럭셔리_원탑 #멋진_비전",
        "desc": "세계 최고를 자랑하는 웅장한 도시! 원대한 꿈과 멋진 도전을 자극하는 최고급 여행지예요."
    }
}

# 4. 화면 헤더 구성
st.markdown("<p style='text-align: center; color: #ff85a2; font-weight: bold;'>💗 마음을 설레게 하는 MBTI 여행 가이드 💗</p>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #d63384;'>✨ 나에게 딱 맞는 러블리 여행지는? ✨</h2>", unsafe_allow_html=True)
st.write("")

# 5. MBTI 선택
mbti_list = list(mbti_recommendations.keys())
selected_mbti = st.selectbox("당신의 MBTI 유형을 선택해 주세요 🎀", mbti_list)

st.write("")

# 6. 결과 확인 및 효과
if st.button("💖 나만의 추천 여행지 확인하기 💖", type="primary"):
    # 사랑스러운 눈꽃/풍선 효과
    st.snow()
    
    data = mbti_recommendations[selected_mbti]
    
    st.write("")
    st.markdown(f"#### 💌 **{selected_mbti}** 님만을 위한 추천")
    st.header(data["destination"])
    
    # 핑크빛 안채 상자
    st.write(f"**{data['tagline']}**")
    st.info(f"🌸 **사랑스러운 포인트:** {data['desc']}")
    
    st.success("💕 소중한 사람들과 함께 행복한 여행을 꿈꿔보세요!")
