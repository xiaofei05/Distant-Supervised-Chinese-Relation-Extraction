import pickle
import jieba
import os
import multiprocessing
import time

def read_txt(file_name):
    txt_data = []
    with open(file_name, 'r', encoding='utf8') as f:
        d = f.readline()
        while d:
            txt_data.append(d.strip())
            d = f.readline()
    return txt_data

class SentenceSegment:
    def __init__(self, dict_file, stop_word_file, sentences_folder, process_num):
        self.process_num = process_num
        self.stop_word = read_txt(stop_word_file)
        jieba.load_userdict(dict_file)
        # sentence files
        self.sentence_files = []
        for root, dirs, files in os.walk(sentences_folder):
            for file in files:
                self.sentence_files.append(os.path.join(root, file))


    def segment(self, file_name):
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
        new_data = []
        for d in data:
            # sentence segment
            sen_seg = []
            for word in jieba.cut(d[0]):
                if word not in self.stop_word:
                    sen_seg.append(word)
            d.append(sen_seg)
            # filter entities again
            new_eset = []
            for entity in d[1]:
                if entity in sen_seg:
                    new_eset.append(entity)
            # remove data the number of whose entity less than 2
            # and rebuilt data
            if len(new_eset)>1:
                for i in new_eset:
                    for j in new_eset:
                        if j!=i:
                            new_data.append([d[0], i, j, sen_seg])
        print('%s done!'%(file_name))
        return new_data, file_name

    def write_file(self, data):
        with open(data[1], 'wb') as f:
            pickle.dump(data[0])

    def run(self):
        pool = multiprocessing.Pool(processes=self.process_num)
        for one_file in self.sentence_files:
            pool.apply_async(self.segment, args=(str(one_file)), callback=self.write_file)
        pool.close()
        pool.join()

if __name__ == "__main__":
    dict_file = 'dict.txt'
    stop_word = 'stop_word.txt'
    sentences_folder = 'processed/sentences'
    process_num = 8
    st = time.localtime()

    ss = SentenceSegment(dict_file, stop_word, sentences_folder, process_num)
    ss.run()

    ed = time.localtime()
    print('\n开始时间: ')
    print(time.strftime("%Y-%m-%d %H:%M:%S", st))
    print('结束时间: ')
    print (time.strftime("%Y-%m-%d %H:%M:%S", ed))