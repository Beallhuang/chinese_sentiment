from pathlib import Path
import os
import jieba
import re


def build_data_file(directory, samples_path, label, mode_str):
    for sample_path in samples_path:
        with Path('{}/{}'.format(directory, sample_path)).open(encoding='utf-8') as f:
            words = [' '.join(jieba.cut(re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])', '', line)
                                        .strip(), cut_all=False, HMM=True)) for line in f if line.strip() != '']
            with Path('{}.words.txt'.format(mode_str)).open('a', encoding='utf-8') as g:
                g.write('{}\n'.format(' '.join(words)))
            with Path('{}.labels.txt'.format(mode_str)).open('a', encoding='utf-8') as h:
                h.write('{}\n'.format(label))


if __name__ == '__main__':
    pos_dir = Path('raw_data/fix_pos')
    neg_dir = Path('raw_data/fix_neg')
    # neu_dir = Path('raw_data/fix_neu')
    pos_samples = os.listdir(pos_dir)
    neg_samples = os.listdir(neg_dir)
    # neu_samples = os.listdir(neu_dir)
    num_pos = len(pos_samples)
    num_neg = len(neg_samples)
    # num_neu = len(neu_samples)
    build_data_file(pos_dir, pos_samples[0:(num_pos - num_pos // 5)], 'POS', 'train')
    build_data_file(pos_dir, pos_samples[(num_pos - num_pos // 5):], 'POS', 'eval')
    build_data_file(neg_dir, neg_samples[0:(num_neg - num_neg // 5)], 'NEG', 'train')
    build_data_file(neg_dir, neg_samples[(num_neg - num_neg // 5):], 'NEG', 'eval')
    # build_data_file(neu_dir, neu_samples[0:(num_neu - num_neu // 5)], 'NEU', 'train')
    # build_data_file(neu_dir, neu_samples[(num_neu - num_neu // 5):], 'NEU', 'eval')