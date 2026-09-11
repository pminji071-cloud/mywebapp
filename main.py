import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 맞춤 여행지 추천기",
    page_icon="✈️",
    layout="centered"
)

# MBTI별 추천 여행지 데이터베이스
mbti_recommendations = {
    "ISTJ": {
        "destination": "스위스 융프라우 & 인터라켄",
        "tagline": "철저한 계획과 안정이 최고! 질서정연하고 자연이 스며든 명소",
        "features": ["정확한 기차 시간표와 편리한 대중교통", "눈이 즐거운 풍경과 여유로운 산책", "예상치 못한 돌발 상황이 적은 안전한 여행지"]
    },
    "ISFJ": {
        "destination": "일본 교토",
        "tagline": "따뜻함과 아늑함, 그리고 전통의 기품을 느낄 수 있는 곳",
        "features": ["조용하고 고즈넉한 사찰과 거리 walk", "정갈하고 맛있는 음식 문화", "마음의 평화를 찾는 다도 체험 및 온천"]
    },
    "INFJ": {
        "destination": "아이슬란드 레이캬비크",
        "tagline": "깊은 영감과 신비로움, 나만의 사색을 즐길 수 있는 자연",
        "features": ["몽환적인 오로라 관람", "웅장한 빙하와 대자연 속 힐링", "혼자만의 시간을 가지기 좋은 평화로운 분위기"]
    },
    "INTJ": {
        "destination": "영국 런던",
        "tagline": "풍부한 역사, 문화, 지적 호기심을 충족시켜 주는 도시",
        "features": ["세계적인 대형 박물관 및 미술관 탐방", "역사와 현대 기술이 조화된 도시 설계", "계획을 세워 알차게 구경할 수 있는 동선"]
    },
    "ISTP": {
        "destination": "뉴질랜드 퀸스타운",
        "tagline": "액티비티와 자연 그대로를 체감할 수 있는 익스트림 천국",
        "features": ["번지점프, 스카이다이빙 등 다양한 스릴 체험", "복잡하지 않은 여유로운 분위기", "자유로운 로드트립 탐험"]
    },
    "ISFP": {
        "destination": "인도네시아 발리",
        "tagline": "예술적 감성과 여유, 아름다운 석양이 어우러진 휴양지",
        "features": ["아름다운 해변과 여유로운 요가 클래스", "감성적인 카페와 감각적인 인테리어", "틀에 매이지 않는 자유로운 일정"]
    },
    "INFP": {
        "destination": "체코 프라하",
        "tagline": "동화 속 한 장면 같은 낭만과 예술적 감수성이 흘러넘치는 도시",
        "features": ["골목골목 숨겨진 고풍스러운 건축물", "아름다운 야경과 버스킹 음악", "혼자 걸으며 감상에 젖기 좋은 atmosphere"]
    },
    "INTP": {
        "destination": "독일 뮌헨 & 베를린",
        "tagline": "새로운 지식과 철학, 박물관이 공존하는 공간",
        "features": ["세계적인 과학기술 박물관 탐방", "깊이 있는 역사와 맥주 문화 체험", "타인의 시선을 신경 쓰지 않는 자유로움"]
    },
    "ESTP": {
        "destination": "미국 라스베이거스",
        "tagline": "자극과 즐거움, 화려한 밤문화가 가득한 다이내믹 도시",
        "features": ["화려한 쇼와 스트리트 퍼포먼스", "언제든 즐길 수 있는 액티비티", "지루할 틈이 없는 스펙터클한 경험"]
    },
    "ESFP": {
        "destination": "스페인 바르셀로나",
        "tagline": "열정과 축제, 사람들의 에너지로 넘치는 감성 휴양지",
        "features": ["가우디의 창의적인 건축물 감상", "해변에서 즐기는 신나는 파티와 맛있는 타파스", "외국인 친구들과 금방 친해지는 밝은 분위기"]
    },
    "ENFP": {
        "destination": "태국 방콕",
        "tagline": "다채로운 색감, 야시장, 매 순간 새로운 놀거리가 쏟아지는 곳",
        "features": ["화려한 야시장 탐방과 길거리 음식", "에너지 넘치는 밤거리와 문화 체험", "예측 불가능한 흥미진진한 일상 탈출"]
    },
    "ENTP": {
        "destination": "미국 뉴욕",
        "tagline": "트렌드의 중심지, 지루함이라곤 전혀 찾아볼 수 않는 도시",
        "features": ["브로드웨이 뮤지컬과 다양한 문화공연", "끊임없이 변화하는 예술 거리와 팝업 스토어", "다양한 사람들과의 정열적인 소통"]
    },
    "ESTJ": {
        "destination": "싱가포르",
        "tagline": "완벽한 질서와 효율성, 세련된 도시미가 돋보이는 곳",
        "features": ["깔끔하고 안전한 도시 환경", "철저하게 잘 꾸며진 인프라와 쇼핑몰", "계획대로 착착 진행되는 알찬 관광 동선"]
    },
    "ESFJ": {
        "destination": "이탈리아 로마 & 피렌체",
        "tagline": "따뜻한 정과 역사, 함께 나누는 맛있는 음식이 가득한 곳",
        "features": ["일행 모두가 만족할 수 있는 풍부한 먹거리", "역사적인 명소에서 나누는 추억", "현지인들의 정겨운 분위기"]
    },
    "ENFJ": {
        "destination": "프랑스 파리",
        "tagline": "낭만적인 문화와 예술, 타인과의 교감이 활발한 감성 도시",
        "features": ["에펠탑 아래에서의 피크닉", "다양한 미술관 및 박물관 로맨틱 도슨트 투어", "모두를 매료시키는 매력적인 스팟"]
    },
    "ENTJ": {
        "destination": "아랍에미리트 두바이",
        "tagline": "웅장한 규모와 미래지향적 비전, 압도적인 신수도",
        "features": ["세계 최고층 빌딩 버즈 칼리파와 럭셔리 인프라", "혁신적인 미래 박물관 체험", "목표 지향적이고 스케일이 큰 리조트 투어"]
    }
}

# UI 구성
st.title("✈️ MBTI 맞춤 여행지 추천기")
st.write("성격 유형에 딱 맞는 맞춤형 여행지를 찾아드립니다!")

st.divider()

# 사용자 입력
mbti_list = list(mbti_recommendations.keys())
selected_mbti = st.selectbox("당신의 MBTI 유형을 선택해 주세요:", mbti_list)

# 추천 버튼 및 결과 출력
if st.button("추천 여행지 확인하기", type="primary"):
    data = mbti_recommendations[selected_mbti]
    
    st.subheader(f"🌟 {selected_mbti} 유형을 위한 추천 여행지")
    st.header(f"👉 **{data['destination']}**")
    
    st.info(f"**한 줄 요약:** {data['tagline']}")
    
    st.write("### 📌 이 여행지가 딱인 이유:")
    for feature in data["features"]:
        st.write(f"- {feature}")

    st.success("즐겁고 안전한 여행 계획을 세워보세요!")
