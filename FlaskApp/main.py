import pickle

from flask import Flask, render_template, request
import textProcess

app = Flask(__name__,template_folder='./templates',static_folder='./static')
# load mô hình bayes đã train
with open('Bayes.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route("/", methods=['GET', 'POST'])
def index():
    # thao tác dữ liệu với ajax
    if request.method == "POST":
        # lấy trường dữ liệu
        name = request.form["name"]
        # tiền xử lý dữ liệu lấy về
        txt = textProcess.Text(name).getAfterProcess()
        # gọi mô hình phân loại
        pre = model.predict([txt])
        # biến đổi nhãn
        if pre[0] == 0:
            res = 'Không tiêu cực'
        if pre[0] == 1:
            res = 'Tiêu cực'
        # trả lại kết quả
        return str(res)
    return render_template("index2.html")
def main():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)