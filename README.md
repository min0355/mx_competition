
### 공정  
1. 교반 속도 : 레미콘의 드럼 or 교반기 회전 속도  
2. 공정 : 입자간 응결 응집이 효율적으로 일어나도록 유체나 입자에 교반을 통한 난류 변동을 가해 입자 floc (뭉치) 상 응집을 일으키는 것  
3. 공정은 전 처리로 이 후 살균 - 분무 건조 순으로 처리  
4. 분무 건조는 페이스트된 재료를 분무 건조기에 넣어 30 ~ 50 미크론 건조 입자로 만드는 작업  

### 데이터 이해  
1. pandas_profiling 라이브러리 결과 (다운로드 확인 or code) : [Competition data profiling.html](https://github.com/min0355/mx_competition/blob/main/code/Competition%20data%20profiling.html)   

### 데이터 분석  
* INSP 에 따른 불량율 추이 (높을수록 불량율이 높음) : 
<img src="https://github.com/min0355/mx_competition/blob/main/result/newplot.png?raw=true" width="1000" height="350"/>      

### 아이디어  
* “통합 모델 개발”   
* 분말을 섞는 통에 가려져 operator 는 정상 비정상 여부를 real time 으로 알지 못하니 관측하기 쉬운 feature 들만 가지고 이상 감지   

* 관측이 쉬운 건 섞는 온도, 교반 속도, 내용량   

* 수분 함유량은 이 후 확인한 사항 (real time 으로 알기 어렵거나 계측이 어려운 것)  과제에선 feature 전체 영향을 분석하므로 다 사용한다고 가이드북에 제시   

* 따라서 관측 쉬운 독립 변수로 수분 함유량부터 먼저 예측가능 한 지 확인  
* 이 후 수분 함유량과 label 의 관계성 예측이 COST 측면에선 유리하나   

* 그러나 수분 함유량은 낮은 cardinality (높은 중복성) 로 인해 단독으로 label 을 설명할 수 없음.   
* 따라서, 알고리즘은 가이드북 제시한 독립 변수에 포함하여 예측 할 수 밖에 없음.   

* 다만, 관측 쉬운 독립 변수로 최종 종속 변수인 양품/불량을 예측하는 2 단계로 가능하다면,  
* 어떤 제조 공정이든 측정이나 관측 가능한 독립 변수로 종속을 (매우 값싼 cost 로) 예측 할 수 있다는 거시적 논리 접근 가능  

* ML 로만 끝낼 수 있도록 독립 변수의 정의가 가장 중요.  
  (수분 함유량을 측정하기 위해선 별도 샘플링 검사 등을 해야 한다면 Man Power 나 추가 비용이 들어감.)  

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
