"""Reload and serve a saved model"""
import re
import jieba
from pathlib import Path
from tensorflow.contrib import predictor
from functools import partial


def predict(pred_fn, line, length=300):
    line = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])', '', line)
    sentence = ' '.join(jieba.cut(line.strip(), cut_all=False, HMM=True))
    words = [w.encode() for w in sentence.strip().split()]
    if len(words) >= length:
        words = words[:length]
    else:
        words.extend(['<pad>'] * (length - len(words)))
    predictions = pred_fn({'words': [words]})
    return predictions


if __name__ == '__main__':
    export_dir = 'saved_model'
    subdirs = [x for x in Path(export_dir).iterdir()
               if x.is_dir() and 'temp' not in str(x)]
    latest = str(sorted(subdirs)[-1])
    predict_fn = partial(predict, predictor.from_saved_model(latest))
    # print(LINE)
    # print(predict_fn(LINE, params['nwords']))
    # line = input('\n\n输入一句中文： ')
    # while line.strip().lower() != 'q':
    #     print('\n\n', predict_fn(line))
    #     line = input('\n\n输入一句中文： ')
    with open(r"C:\Users\2331\Desktop\新建文本文档.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if predict_fn(line)['labels'][0] == b'NEG' and line.strip() != '此用户没有填写评价。':
                print(line.strip())

