import streamlit as st

st.title("Bike Sharing 시계열 예측")
st.write("월별 자전거 대여량 확인하고 미래 값을 예측합니다.")

import pandas as pd 
uploaded_file = st.file_uploader("Bike Sharing Demand CSV 파일을 업로드하세요." , type = "csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("업로드한 원본 데이터")
    st.dataframe(data)

    if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data['datetime']=pd.to_datetime(data['datetime'])
    data=data.sort_values("datetime")
    data['month']=(data['datetime'].dt.to_period("M").dt.to_timestamp())
    monthly = (data.groupby("month", as_index=False)['count'].sum())
    monthly = monthly.set_index('month')

    st.write("월별 자전거 대여량")
    st.dataframe(monthly)
    st.write("시간에 따른 월별 대여량 변화")
    st.line_chart(monthly["count"])

forecast_period = st.selectbox("예측 기간을 선택세요 : ", [1,3,6])   

from statsmodels.tsa.arima.model import ARIMA 

model = ARIMA(monthly['count'],order=(2,2,1))
model_fit = model.fit()
forecast = model_fit.forecast(steps=forecast_period)
