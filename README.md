# 실증 사업 대비 예제

## AI 허브 데이터로 예제 작성 (2024-07-10)

1. 웹페이지의 샘플데이터 다운로드
2. url : https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=157

## 추후 퓨전 레이어 적용 예정 (ndvi, 날씨, 토양 등)

- ResNet-50, ndvi 데이터 처리 레이어 , 날씨 및 토양 데이터 레이어.
- 스마트컴퓨팅 연구실 조언에 따라 Explainable AI (XAI) 등도 적용 가능하도록...

## 고려해볼 내용

1. 앙상블

- ImageModel, NDVIModel , WeatherSoilModel 만들어서 진행
- 퓨전레이어보다 효과가 있을지?

2. XGBoost

- XGBoostWrapper 적용
- 비용대비 효과가 있는지?

3. 궁금한 내용

- 퓨전레이어로 된 모델에 병해충 모델을 개발하여 앙상블로 붙였을 때의 효과?

## 추후 개발 환경 관련

docker , env 설정 진행 할것.

