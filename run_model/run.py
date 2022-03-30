import time
from serve import LSTM
import pandas as pd

df = pd.read_excel(r"C:\Users\2331\Desktop\商品评论2.xlsx", encodings='utf-8')
s_list = df['评价内容'].to_list()

start_time = time.time()
lstm = LSTM()

sentence_list_ = s_list
res_dict = lstm.main(sentence_list_, threadNum=10)
print(f'打标后评论数: {len(s_list)}')
print(f"打标后评论数: {len(res_dict['data'])}")

print(f'\n耗时 {round(time.time() - start_time, 2)} s')