# 2021 TOC project

## 主題介紹
### 記錄小幫手
產生一個方便記帳、寫備忘錄的line bot<br>

請先掃QR code來加入好友!<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/QR.PNG)

## 流程
#### help
輸入"help"來得到功能介紹<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/help.jpg)
不同模式下 輸入help得到不同的幫助
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/help2.jpg)

### 模式1 : 記帳
#### 功能1 : 記錄
選擇"記錄"模式<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/記錄.jpg)

根據指令輸入想記錄的內容<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/記錄中.jpg)

記錄完畢記得輸入"返回"<br>

#### 功能2 : 列表
輸入"列表" 查看自己記錄哪些東西<br>
也可以輸入"刪除/id" 將記錄錯的資料刪掉<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/記錄-列表.jpg)

#### 功能3 : 分析
選擇"分析"  產生圓餅圖，自己的財務狀況可以一目瞭然<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/分析.jpg)

輸入"選單"可以返回到一開始的地方<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/返回選單.jpg)

### 模式2 : 備忘錄
選擇"備忘錄"<br>
根據指令來記錄<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/備忘錄.jpg)


輸入"列表"，得知自己有哪些事情須完成<br>
根據指令，輸入"刪除/id"，來把事件刪除<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/備忘錄-列表刪除.jpg)

## FSM 圖片

![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/fsm.png)

---------------------------------------------------------------------------------------------------------
## 其他介紹
1. 對linebot 輸入"FSM" 也可以得到 FSM的圖<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/fsm_linebot.jpg)
2. 連接mySQL，資料皆從mySQL中抓取<br>
3. 輸入"hi"，linebot 會回應圖片<br>
![image](https://github.com/DouCharles/TOC_final_project/blob/master/img/hi.jpg)


## 環境
python 3.7.7 <br>
mysql 5.7.28 <br>
matplotlib 3.4.2<br>
pyMySQL 1.0.2<br>
pyimgur 0.6.0<br>
pipenv<br>

