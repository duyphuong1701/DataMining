import pickle
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.model_selection import train_test_split

from textProcess import Text


class classification:
    # hàm khởi tạo OOP
    def __init__(self,number):
        # load dữ liệu đã lưu
        data = pickle.load(open('dulieu.pkl', 'rb'))
        # nghi thức holdout test 30%
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(data.noidung,data.nhan,shuffle=True,test_size=0.3)
        # chọn model
        self.model = self.select_model(number)
        # training
        self.model.fit(self.x_train, self.y_train)
    # hàm chọn model
    def select_model(self,number):
      # 1 là Bayes, 2 là cây quyết định, 3 là máy học hỗ trợ
      # pipeline để đưa 2 thuật toán vào cùng lúc
      # tfidfVectorizer là thuật toán số hoá dữ liệu trên tần suất
      if number==1:
        temp = make_pipeline(TfidfVectorizer(), MultinomialNB())
      if number==2:
        temp = make_pipeline(TfidfVectorizer(), DecisionTreeClassifier())
      if number==3:
        temp = make_pipeline(TfidfVectorizer(),svm.SVC(kernel="rbf"))
      return temp
    # hàm dự đoán nhiều giá trị
    def predictions(self, my_sentence):
      for i in range(0,len(my_sentence)):
        my_sentence[i] = Text(my_sentence[i]).getAfterProcess()
        prediction = self.model.predict(my_sentence)
        return prediction
    # hàm dự đoán đơn biến
    def prediction(self, my_sentence):
        my_sentence = Text(my_sentence).getAfterProcess()
        prediction = self.model.predict([my_sentence])
        return prediction
    # điểm chính xác mô hình
    def getScore(self):
        return self.model.score(self.x_test,self.y_test)



# so sánh độ chính xác với các mô hình Decision Tree, SVM
aver_bayes = 0
aver_decisiontree = 0
aver_svm = 0
# phần đánh giá mô hình bằng accuracy
print('Độ chính xác mô hình')
for i in range(10):
    # chia holdout testsize 30% dữ liệu trộn lại sau mỗi lần build model
    print("Lan: "+str(i+1))
    # 1 là mô hình Bayes
    model1 = classification(1)
    # 2 là mô hình Decision Tree
    model2 = classification(2)
    # 3 là mô hình SVM
    model3 = classification(3)
    # biến lưu tổng điểm để chia trung bình
    aver_bayes= aver_bayes+model1.getScore()
    aver_decisiontree =aver_decisiontree+model2.getScore()
    aver_svm = aver_svm+model3.getScore()
    # in kết quả theo mỗi lần train đã mix lại dữ liệu
    print("Naive Bayes: ",model1.getScore())
    print("Decision Tree: ",model2.getScore())
    print("SVM: " ,model3.getScore())
# độ chính xác trung bình
print("Do chinh xac trung binh")
print("Naive Bayes: ",aver_bayes/10)
print("Decision Tree: ",aver_decisiontree/10)
print("SVM: " ,aver_svm/10)
# phần đánh giá mô hình bằng confusion matrix
print("Confusion matrix mô hình Bayes")
model=model1.model
y_pred = model.predict(model1.x_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(model1.y_test, y_pred)
print(cm)
# lưu mô hình bayes đã train lại
Pkl_Filename = "Bayes.pkl"
with open(Pkl_Filename, 'wb') as file:
    pickle.dump(model1.model, file)