"""Reload and serve a saved model"""
import jieba
import re
from pathlib import Path
from tensorflow.contrib import predictor
from functools import partial
from thread_api import Thread_Api


class LSTM():
    def __init__(self):
        export_dir = 'saved_model'
        subdirs = [x for x in Path(export_dir).iterdir()
                   if x.is_dir() and 'temp' not in str(x)]
        latest = str(sorted(subdirs)[-1])
        self.predict_fn = partial(self.predict, predictor.from_saved_model(latest))

    def predict(self, pred_fn, raw_line, length=300):
        raw_line = str(raw_line)
        line = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])', '', raw_line)
        if re.search('.*[用户].*[未|没有].*[评论|评价].*|.*[系统默认].*[评论|评价].*', line.strip()):
            self.result_dict['data'].append({'text': line, 'label': 'Other'})
        elif line.strip().isdigit():
            self.result_dict['data'].append({'text': line, 'label': 'Other'})
        elif '好评模板' in line.strip() or '模板' in line.strip() or '仙女很懒' in line.strip():
            self.result_dict['data'].append({'text': line, 'label': 'POS'})
        elif line.strip() in ['好用', '好', '备着', '超赞', 'GOOD', 'Ok', 'okk', '超棒', 'yyds', '靠谱']:
            self.result_dict['data'].append({'text': line, 'label': 'POS'})
        elif raw_line.strip() in ['👌', '👍', '🉑']:
            self.result_dict['data'].append({'text': line, 'label': 'POS'})
        else:
            sentence = ' '.join(jieba.cut(line.strip(), cut_all=False, HMM=True))
            words = [w.encode() for w in sentence.strip().split()]
            nwords = len(words)
            predictions = pred_fn({'words': [words], 'nwords': [nwords]})
            self.result_dict['data'].append({'text': raw_line, 'label': predictions['labels'][0].decode()})

    def main(self, sentence_list, threadNum=6):
        self.result_dict = {'total_sentence': len(sentence_list), 'data': []}
        Thread_Api(sentence_list, self.predict_fn, threadNum=threadNum).main()
        return self.result_dict


if __name__ == '__main__':
    pass



