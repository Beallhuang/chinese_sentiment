import os
import codecs

POS = os.path.join(os.getcwd(), 'pos.txt')
NEG = os.path.join(os.getcwd(), 'neg.txt')
FIX_POS = os.path.join(os.getcwd(), 'fix_pos')
FIX_NEG = os.path.join(os.getcwd(), 'fix_neg')
FIX_NEU = os.path.join(os.getcwd(), 'fix_neu')

# with open('pos.txt', 'a', encoding='utf-8') as fl:
#     for file in os.listdir(FIX_POS):
#         with open(os.path.join(FIX_POS, file), 'r', encoding='utf-8') as ff:
#             fl.write(ff.read().replace('\n', '').strip())
#             fl.write('\n')
# with open('neg.txt', 'a', encoding='utf-8') as fl:
#     for file in os.listdir(FIX_NEG):
#         with open(os.path.join(FIX_NEG, file), 'r', encoding='utf-8') as ff:
#             fl.write(ff.read().replace('\n', '').strip())
#             fl.write('\n')


def fix_corpus(dir_s, dir_t):
    for item in os.listdir(dir_s):
        for code in ['gb2312', 'gbk', 'utf-8']:
            try:
                with open(os.path.join(dir_s, item), 'r', encoding=code) as f:
                    fix_s = f.read()
                    # print(fix_s)
                    with codecs.open(os.path.join(dir_t, item), 'w', encoding='utf-8') as ff:
                        ff.write(fix_s)
            except UnicodeDecodeError:
                pass


if __name__ == "__main__":
    if not os.path.isdir(FIX_POS):
        os.mkdir(FIX_POS)
    if not os.path.isdir(FIX_NEG):
        os.mkdir(FIX_NEG)
    # if not os.path.isdir(FIX_NEU):
    #     os.mkdir(FIX_NEU)
    # fix_corpus(POS, FIX_POS)
    # fix_corpus(NEG, FIX_NEG)
    pos_num = max([int(i.split('.')[1]) for i in os.listdir(FIX_POS)]) if os.listdir(FIX_POS) else 0
    neg_num = max([int(i.split('.')[1]) for i in os.listdir(FIX_NEG)]) if os.listdir(FIX_NEG) else 0
    # neu_num = max([int(i.split('.')[1]) for i in os.listdir(FIX_NEU)]) if os.listdir(FIX_NEU) else 0
    for label, num in [['pos', pos_num], ['neg', neg_num]]:
        with open(f"{label}.txt", 'r', encoding='utf-8') as f:
            index_num = num
            for line in f.readlines():
                with open(f'fix_{label}/{label}.{index_num}.txt', 'w', encoding='utf-8') as ff:
                    ff.write(line.strip())
                index_num += 1



