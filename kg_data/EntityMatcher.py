import pickle
import multiprocessing
import time
import os

class EntityMatcher:
    def __init__(self, entity_file, sentences_folder, process_num):
        self.process_num = process_num

        with open(entity_file, 'rb') as f:
            entity_dict = pickle.load(f)
        self.entities = list(set(list(entity_dict.keys())))

        # sentence files
        self.sentence_files = []
        for root, dirs, files in os.walk(sentences_folder):
            for file in files:
                self.sentence_files.append(os.path.join(root, file))

    def match(self, file_name):
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
        new_data = []
        for sen in data:
            eset = []
            for entity in self.entities:
                if entity in sen:
                    eset.append(entity)
            if len(eset)>1:
                new_data.append([sen, eset])
        print('%s done!'%(file_name))
        return new_data, file_name

    def write_file(self, data):
        with open(data[1], 'wb') as f:
            pickle.dump(data[0])

    def run(self):
        pool = multiprocessing.Pool(processes=self.process_num)
        for one_file in self.sentence_files:
            pool.apply_async(self.match, args=(str(one_file)), callback=self.write_file)
        pool.close()
        pool.join()

if __name__ == "__main__":
    entity_file = 'processed/entities.pkl'
    sentences_folder = 'processed/sentences'
    process_num = 8
    st = time.localtime()

    em = EntityMatcher(entity_file, sentences_folder, process_num)
    em.run()

    ed = time.localtime()
    print('\n开始时间: ')
    print(time.strftime("%Y-%m-%d %H:%M:%S", st))
    print('结束时间: ')
    print (time.strftime("%Y-%m-%d %H:%M:%S", ed))