### 데이터 이해  
1. pandas_profiling 라이브러리 결과 (다운로드 확인 or code) : [Competition data profiling.html](https://github.com/min0355/mx_competition/blob/main/code/Competition%20data%20profiling.html)   

### 데이터 분석  
* INSP 에 따른 불량율 추이 (높을수록 불량율이 높음) : 
<img src="https://github.com/min0355/mx_competition/blob/main/result/newplot.png?raw=true" width="1000" height="350"/>      


### 추가  

* 데이터 셋 이해도 (10 점)  

* 일단 서면 평가 통과를 위해 **제조 현장 문제 이해 + 문제 정의 체계성** (합 20 점) 을 중점적으로  

* 정량적 지표 (30 점) 는 알고리즘 (20 점) 을 고민 후 하이퍼 파라미터 튜닝  

* 결과 해석 및 결과물 작성 (20 점) 

* **raw data 를 감지하는 방법론 등이 기술되면 좋을 것 같음.** 이런 센서로 이런 데이터를 모을 수 있고 그 결과 metric 이 우수해진다. 등  

* 제조 현장 실 적용 가능성을 염두 해 둬야 하므로 머신 러닝으로 부족한 부분에 대해서는 warning 을 띄우는 형태까지 고려 필요  

* 시계열 + real time labeling + 관측 가능한 features 에 통합적으로 쓸 수 있는 모델이 나오면 best  

* 모델 기준으로 자료는 역 작성이 되면 될 듯  

* **접목 할 모델을 빠르게 구현하는 게 가장 시급** 


### TPOTC 일부 구동 결과  
![image](https://user-images.githubusercontent.com/62151520/200161638-131401f5-b5ae-4a49-9dab-ede2e459f3a9.png)
![image](https://user-images.githubusercontent.com/62151520/200161651-403a42a3-8d5a-4f0a-8b69-3579199fb873.png)


참고 : https://www.kaggle.com/code/dimitreoliveira/deep-learning-for-time-series-forecasting     
참고 : https://www.kaggle.com/code/dimitreoliveira/time-series-forecasting-with-lstm-autoencoders/data    


AUC : 47435   
PRECISION : 47943     
RECALL : 48314   
PrecisionATRecall (recall=0.8) : 48321  
false_negatives : 47544
SensitivityAtSpecificity : 47665
