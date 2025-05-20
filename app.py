# app.py
import streamlit as st
import pandas as pd
import sqlite3
import json

st.set_page_config(page_title="실시간 입찰공고 대시보드", layout="wide")
st.title("📢 나라장터 실시간 입찰공고")

# SQLite 연결 및 데이터 로딩
def load_data():
    conn = sqlite3.connect("bids_raw.db")
    df = pd.read_sql_query("SELECT * FROM bids", conn)
    conn.close()
    
    # JSON 컬럼을 펼치기
    expanded = pd.json_normalize([json.loads(row) for row in df["raw_json"]])
    return expanded

# 데이터 불러오기
try:
    df_bids = load_data()
    st.success(f"총 {len(df_bids)}건의 공고를 불러왔습니다.")

    # 주요 컬럼 표시 (필요에 따라 조정)
    display_cols = [
        "bidNtceNo", "bidNtceNm", "dminsttNm", "bidNtceDt", "bidNtceBgnDt", "bidNtceEndDt"
    ]
    df_display = df_bids[display_cols].copy()
    df_display.columns = ["공고번호", "공고명", "발주기관", "공고일자", "게시일시", "마감일시"]

    # 필터 UI
    keyword = st.text_input("🔍 공고명 또는 발주기관 검색")
    if keyword:
        df_display = df_display[
            df_display["공고명"].str.contains(keyword, case=False, na=False) |
            df_display["발주기관"].str.contains(keyword, case=False, na=False)
        ]

    st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류 발생: {e}")
