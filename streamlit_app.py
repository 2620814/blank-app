import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(page_title="대학 위치 정보 가이드", layout="wide")
st.title("🏫 전국 주요 대학 위치 정보")
st.write("원하는 대학을 선택하면 지도에서 위치를 확인할 수 있습니다.")

# 2. 대학 데이터 생성 (예시 데이터)
# 실제 서비스 시에는 CSV 파일이나 공공데이터 API를 연동하면 좋습니다.
college_data = {
    "대학명": ["서울대학교", "연세대학교", "고려대학교", "카이스트 (본원)", "포항공과대학교"],
    "지역": ["서울", "서울", "서울", "대전", "경북"],
    "위도": [37.459882, 37.565784, 37.589385, 36.372140, 36.014213],
    "경도": [126.951905, 126.938572, 127.031778, 127.360362, 129.324810],
    "웹사이트": [
        "https://www.snu.ac.kr",
        "https://www.yonsei.ac.kr",
        "https://www.korea.ac.kr",
        "https://www.kaist.ac.kr",
        "https://www.postech.ac.kr"
    ]
}
df = pd.DataFrame(college_data)

# 3. 사이드바 - 대학 선택 필터
st.sidebar.header("🔍 대학 검색")
selected_region = st.sidebar.selectbox("지역 선택", ["전체"] + list(df["지역"].unique()))

# 지역 필터링
if selected_region != "전체":
    filtered_df = df[df["지역"] == selected_region]
else:
    filtered_df = df

selected_college = st.sidebar.selectbox("대학 선택", filtered_df["대학명"])

# 4. 선택된 대학 정보 매칭
college_info = df[df["대학명"] == selected_college].iloc[0]

# 5. 화면 레이아웃 분할 (좌측: 정보, 우측: 지도)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"📍 {college_info['대학명']}")
    st.write(f"**지역:** {college_info['지역']}")
    st.write(f"**위도:** {college_info['위도']}")
    st.write(f"**경도:** {college_info['경도']}")
    st.markdown(f"[🌐 공식 웹사이트 방문하기]({college_info['웹사이트']})")
    
    st.markdown("---")
    st.dataframe(filtered_df[["대학명", "지역"]], use_container_width=True)

with col2:
    st.subheader("🗺️ 지도 확인")
    
    # folium을 이용한 인터랙티브 지도 생성
    # 선택된 대학의 위/경도를 중심으로 지도 시작
    m = folium.Map(location=[college_info["위도"], college_info["경도"]], zoom_start=15)
    
    # 지도에 마커 추가
    folium.Marker(
        [college_info["위도"], college_info["경도"]],
        popup=college_info["대학명"],
        tooltip=college_info["대학명"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    
    # 스트림릿에 지도 렌더링
    st_folium(m, width=700, height=500, key="college_map")