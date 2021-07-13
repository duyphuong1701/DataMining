# thư viện xử lý văn bản
import gensim
from pyvi import ViTokenizer,ViUtils,ViPosTagger,ViDiac,models
class Text:
    # hàm khởi tạo
    def __init__(self,str):
        # nội dung
        self.str=str
        # xoá thẻ
        self.delTag()
        # tách từ
        self.splitWord()
        # chữ thường
        self.normal()
        # xoá stopword
        self.delStopword()
    # hàm xoá thẻ html,js,...
    def delTag(self):
        # xoa tag
        self.str=gensim.parsing.strip_tags(self.str)
        # xoa khoang trang
        self.str=gensim.parsing.preprocessing.strip_multiple_whitespaces(self.str)
        # xoa ki tu dac biet
        self.str=gensim.parsing.preprocessing.strip_non_alphanum(self.str)
        # xoa dau , .
        self.str=gensim.parsing.preprocessing.strip_punctuation(self.str)
        # xoa so
        self.str=gensim.parsing.preprocessing.strip_numeric(self.str)
    # hàm tách từ tiếng việt
    def splitWord(self):
        self.str=ViTokenizer.tokenize(self.str)
    # hàm chuẩn hoá bộ gõ
    def normal(self):
        self.str=gensim.parsing.preprocessing.stem_text(self.str)
    # hàm xoá từ dừng
    def delStopword(self):
        # mảng lưu từ dừng
        stop_word = []
        # danh sách từ dừng lưu trong file txt
        with open("./stopwords.txt", encoding="utf-8") as f:
            text = f.read()
            # cắt từ theo từ điển đưa vào mảng
            for word in text.split():
                stop_word.append(word)
            f.close()
        # tách các từ ra
        str=self.str.split(" ")
        self.str = ""
        # chạy kiểm tra từng từ có nằm trong từ dừng thì xoá
        for word in str:
            if word not in stop_word:
                self.str+=word+" "
    # hàm dùng để lấy giá trị văn bản sau xử lí
    def getAfterProcess(self):
        return self.str
