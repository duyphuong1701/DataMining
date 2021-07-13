import pickle
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

# hàm lấy mã sản phẩm theo giá
def get_url_product(product_list):
  arr=[]
  for url in product_list:
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    c1 = soup.findAll("li",{"class":"item"})
    for link in c1:
      temp_link = link.a.get('href')
      temp_link=temp_link.split('?')
      arr.append(temp_link[0])
    # print(len(arr))
  return arr

# hàm lấy tất cả bình luận của một sản phẩm
def getCmt(url_name):
  print("Đang cào bình luận sản phẩm : " + url_name)
  dt = pd.DataFrame(data=None)
  # list lưu số sao và lưu comment
  list_star=[]
  list_cmt=[]
  # 1 -> 20 là số trang tối đa của danh sách bình luận
  for i in (range(1,20)):
    # url +mã sản phẩm +số trang
    url = "https://www.thegioididong.com"+url_name+"/danh-gia?p="
    url += str(i)
    # phần header dùng để cào cho trang TGDĐ
    headers = {
      "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # mỗi một người bình luận sẽ nằm trong div.comment__item
    check_none =soup.findAll("div", {"class": "comment__item"})
    # kiem tra san pham co binh luan khong
    for div in check_none:
      # div1 là số sao, div2 là bình luận
      div1 =div.find_all("div",class_="item-rate")
      div2 =div.find_all("div",class_="comment-content")
      iTags=0
      for tag in div1:
        # đếm số sao
        iTags = len(tag.find_all("i", {"class": "icon-star"}))
      # lưu vào DataFrame
      list_star.append(iTags)
      list_cmt.append(div2[0].p.text)
      # print(len(list_star))
      # print(len(list_cmt))
  dt['noidung'] = list_cmt
  dt['nhan'] = list_star
  # print(dt)
  return dt
# hàm lấy tất cả bình luận
def getAllCmt(arr):
  # DataFrame lưu kết quả
  res = pd.DataFrame()
  for id in tqdm(arr) :
    a = getCmt(id)
    res=res.append(a,ignore_index = True)
  return res
# hàm xoá các bình luận là phản hồi
def removeNotCmt(dt):
  # mảng lưu vị trí
  list_del=[]
  for i in range(len(dt)):
    # các phản hồi thì giá trị đánh giá là 0
    if dt.nhan.iloc[i]==0:
      list_del.append(i)
  # xoá theo vị trí
  dt=dt.drop(list_del)
  # xoá các bình luận trùng
  dt=dt.drop_duplicates()
  return dt
# hàm này dùng để chuyển các đánh giá 1,2,3 sao thành tiêu cực và 4,5 sao thành tích cực
def binary_variable(data):
  # mảng lưu vị trí bình luận tiêu cực và tích cực
  list_123 = []
  list_45= []
  for i in range(len(data)):
    # các phản hồi thì giá trị đánh giá là 1,2,3 đưa vào mảng tiêu cực
    if data.nhan.iloc[i] == 1 or data.nhan.iloc[i] == 2 or data.nhan.iloc[i] == 3:
      list_123.append(i)
    # trường hợp ngược lại đưa vào mảng tích cực
    else:
      list_45.append(i)
  data2 =data
  # cập nhật vị trí tiêu cực
  for i in range(len(list_123)):
    data2.nhan.iloc[list_123[i]]=1
  # cập nhật vị trí tích cực
  for i in range(len(list_45)):
    data2.nhan.iloc[list_45[i]]=0
  # trả kết quả
  return data2
# Hàm vẽ biểu đồ
def char(data):
  import matplotlib.pyplot as plt
  char=data.nhan.value_counts().sort_values()
  print(char)
  char.plot.bar()
  plt.xlabel('Số sao')
  plt.ylabel('Số lượt đánh giá')
  plt.title('Biểu đồ đánh giá bình luận')
  plt.show()

# ____________________

# mảng lưu link sản phẩm theo giá
product_list=["https://www.thegioididong.com/dtdd?p=tren-20-trieu","https://www.thegioididong.com/dtdd?p=tu-13-20-trieu","https://www.thegioididong.com/dtdd?p=tu-7-13-trieu","https://www.thegioididong.com/dtdd?p=tu-4-7-trieu","https://www.thegioididong.com/dtdd?p=tu-2-4-trieu","https://www.thegioididong.com/dtdd?p=duoi-2-trieu"]
# lấy danh sách sản phẩm
arr = get_url_product(product_list)
# lấy tất cả bình luận theo danh sách sản phẩm
# data =getCmt(arr)
data = getAllCmt(arr)
# xoá các bình luận là phản hồi
data = removeNotCmt(data)
# vẽ đồ thị dữ liệu
char(data)
# chuyển về tiêu cực tích cực
data = binary_variable(data)
print(data)
# lưu dữ liệu
Pkl_Filename = "dulieu.pkl"
with open(Pkl_Filename, 'wb') as file:
    pickle.dump(data, file)

# dữ liệu đã lưu trên máy
# data = pickle.load(open('dulieu.pkl', 'rb'))
