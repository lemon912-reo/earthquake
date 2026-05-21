import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 데이터 불러오기
df_new = pd.read_csv("earthquake.csv")

# 위험도 사전
risk_dict = {0: '높음',1: '낮음',2: '중간'}

# 군집 색상
colors = {0: 'red', 1: 'blue', 2: 'green'}

# 제목
st.title("세계 지진 위험도 분석 시스템")

st.write("위도와 경도를 입력하면 주변 지진 데이터를 기반으로 위험도를 분석합니다.")

# 사용자 입력
lat = st.number_input("위도 입력", value=37.5)
lon = st.number_input("경도 입력", value=127.0)

# 버튼 클릭 시
if st.button("위험도 분석"):

    # 주변 지진 찾기
    near_df = df_new[
        (df_new['위도'] >= lat - 5) &
        (df_new['위도'] <= lat + 5) &
        (df_new['경도'] >= lon - 5) &
        (df_new['경도'] <= lon + 5)
    ]

    # 주변 데이터가 없는 경우
    if len(near_df) == 0:
        st.warning("주변 지진 데이터가 없습니다.")

    else:
        # 군집 비율 계산
        cluster_ratio = near_df['cluster'].value_counts(normalize=True)

        # 가장 많은 군집
        main_cluster = cluster_ratio.idxmax()

        # 위험도 출력
        st.subheader(f"예상 위험도: {risk_dict[main_cluster]}")

        # 지도 생성
        m = folium.Map(location=[lat, lon], zoom_start=4, tiles="CartoDB positron")

        # 데이터 샘플링
        df_sample = df_new.sample(500, random_state=42)

        # 지도에 점 표시
        for i in range(len(df_sample)):

            cluster = df_sample.iloc[i]['cluster']

            folium.CircleMarker(
                location=[
                    df_sample.iloc[i]['위도'],
                    df_sample.iloc[i]['경도']
                ],
                radius=df_sample.iloc[i]['규모'],
                color=colors[cluster],
                fill=True,
                fill_color=colors[cluster],
                fill_opacity=0.7
            ).add_to(m)

        # 사용자 위치 표시
        folium.Marker(
            location=[lat, lon],
            popup="입력 위치",
            icon=folium.Icon(color='black', icon='star')
        ).add_to(m)

        # 스트림릿에 지도 출력
        st_folium(m, width=1000, height=600, returned_objects=[])
