# mx_competition : 검색을 막기 위해 분명한 단어 사용은 지양함.  

# 대회 개시 
1. 과제 : 알죠? 그 데이터 셋  
2. 가이드 북 이해 (코드 필사 외) : 10/28     
3. 공정 이해 : 10/30   

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

### 결과 (가이드의 알고리즘 그대로 사용 기준)  

1. 2 개 Feature 만 사용 시 : 아래 결과 참조  
  - precision: 0.9961  
  - **recall: 0.8063**  
  - **f1-score: 0.8912**  
  - **accuracy: 0.8055**  
  
2. 3 개 (질량) 사용 시 : recall 0.70 (더 나빠짐.)  
3. 3 개 (질량 대신 수분) 사용 시 : recall 0.70, f1 0.8258, accuracy 0.7059  

### 데이터  
1. 교반기 1 개의 데이터로 추정 (모터 스피드 고려 시)  
2. 1 분에 10 개이니 추정컨대 6 초당 1 개의 row 수집  
3. 시계열 처리 필요 (시간에 대한 기여도가 매우 높음. 일반 앙상블로는 89 점 정도가 최고)  
4. RNN 계열 처리 필요, 모터 속도 0 이 되면 비우거나 하는 단계   
5. **과제의 핵심 목표 리마인드 필요 (작업 환경 개선 및 생산성 향상)**    
6. 24 시간 운영되는 데이터로 요일별 특성은 크지 않을 것으로 추정, 다만 NG 가 많이 나오는 시간대가 있는 지 확인 필요 (숙련자 몇 명이 라벨링하는 것으로 추정)  
7. 일반적으로 바로 수집 가능한 데이터로 예측이 우선  
8. 용량은 3,000 ~ 3,600 초 주기로 채워졌다 빠졌다 반복  
9. 대략 10 INDEX 주기  
10. 질량 변수 포함 여부 (물리적으로 의미 있다고는 생각)
  
### 자료   
1. 파악한 공정 설명     
2. **문제의 분명한 정의**  (사전 감지, 재료양 최소화, 품질 불량 원인 찾기 중) 
3. ML 영역   
4. ML 접목 시 이점  
5. ML 이 커버하지 못 하는 부분에 대한 논의 (경고 등)     
6. FULL SYSTEM 에 대한 예시 제안  

### TPOTC 일부 구동 결과  
![image](https://user-images.githubusercontent.com/62151520/200161638-131401f5-b5ae-4a49-9dab-ede2e459f3a9.png)
![image](https://user-images.githubusercontent.com/62151520/200161651-403a42a3-8d5a-4f0a-8b69-3579199fb873.png)

### LSTM 구조   
1. 자연어 처리 :  

```model=Sequential()
model.add(Embedding(max_features,250,mask_zero=True))
model.add(LSTM(128,dropout=0.4, recurrent_dropout=0.4,return_sequences=True))
model.add(LSTM(64,dropout=0.5, recurrent_dropout=0.5,return_sequences=False))
model.add(Dense(num_classes,activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.001),metrics=['accuracy'])
model.summary()```    

판매 예측    
Build a sequential model with drop out for regularization
model = Sequential()
model.add(LSTM(units = 32,return_sequences=True,input_shape = (33,1)))
model.add(Dropout(0.4))
model.add(LSTM(units = 32))
model.add(Dropout(0.3))
model.add(Dense(1))
model.compile(loss = 'mse',optimizer = 'adam', metrics = ['mean_squared_error'])
model.summary()  

수요 예측  
def fit_model(train_X, train_Y, window_size = 1):
    model = Sequential()
    
    model.add(LSTM(4, 
                   input_shape = (1, window_size)))
    model.add(Dense(1))
    model.compile(loss = "mean_squared_error", 
                  optimizer = "adam")
    model.fit(train_X, 
              train_Y, 
              epochs = 100, 
              batch_size = 1, 
              verbose = 2)
    
    return(model)  
    
재고 예측  
# The LSTM architecture
regressor = Sequential()
# First LSTM layer with Dropout regularisation
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1],1)))
regressor.add(Dropout(0.2))
# Second LSTM layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
# Third LSTM layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
# Fourth LSTM layer
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
# The output layer
regressor.add(Dense(units=1))

# Compiling the RNN
regressor.compile(optimizer='rmsprop',loss='mean_squared_error')
# Fitting to the training set
regressor.fit(X_train,y_train,epochs=50,batch_size=32)    
  
같은 데이터 GRU  
# The GRU architecture
regressorGRU = Sequential()
# First GRU layer with Dropout regularisation
regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
regressorGRU.add(Dropout(0.2))
# Second GRU layer
regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
regressorGRU.add(Dropout(0.2))
# Third GRU layer
regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
regressorGRU.add(Dropout(0.2))
# Fourth GRU layer
regressorGRU.add(GRU(units=50, activation='tanh'))
regressorGRU.add(Dropout(0.2))
# The output layer
regressorGRU.add(Dense(units=1))
# Compiling the RNN
regressorGRU.compile(optimizer=SGD(lr=0.01, decay=1e-7, momentum=0.9, nesterov=False),loss='mean_squared_error')
# Fitting to the training set
regressorGRU.fit(X_train,y_train,epochs=50,batch_size=150)```    
  
참고 : https://www.kaggle.com/code/dimitreoliveira/deep-learning-for-time-series-forecasting     
참고 : https://www.kaggle.com/code/dimitreoliveira/time-series-forecasting-with-lstm-autoencoders/data    
