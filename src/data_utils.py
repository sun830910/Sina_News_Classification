# -*- coding: utf-8 -*-

"""
Created on 3/18/21 4:42 PM
@Author  : Justin Jiang
@Email   : jw_jiang@pku.edu.com
"""

import os
from config import GlobalConfig
import jieba


def read_data_from_file(file_path):
    if not os.path.exists(file_path):
        print("初始化失败，该文件不存在：{}".format(file_path))
    with open(file_path) as file:
        result = []
        line = file.readline()
        result.append(line)
        while line:
            line = file.readline()
            result.append(line)
    return result


class TextPreprocesser(object):
    def __init__(self):
        self.vocab_idx_dict = {}
        self.label_idx_dict = {}

    def cut_sequence(self, sequence):
        temp = jieba.cut(sequence)
        result = []
        for vocab in temp:
            result.append(vocab)
            if vocab not in self.vocab_idx_dict:
                self.vocab_idx_dict.setdefault(vocab, len(self.vocab_idx_dict))
        return result

    def label2idx(self, label):
        if label not in self.label_idx_dict:
            self.label_idx_dict.setdefault(label, len(self.label_idx_dict))
        return self.label_idx_dict.get(label)

    def get_vocab_dict(self):
        return self.vocab_idx_dict

    def get_label_dict(self):
        return self.label_idx_dict


class DataUtiler(object):
    def __init__(self):
        self.config = GlobalConfig
        self.data_preprocesser = TextPreprocesser()
        self.data_dir_path = self.config.get("data_dir_path")
        self.train_data_path = self.data_dir_path + self.config.get("train_data_name")
        self.test_data_path = self.data_dir_path + self.config.get("test_data_name")
        self.val_data_path = self.data_dir_path + self.config.get("val_data_name")
        self.train_texts = None
        self.train_labels = None
        self.test_texts = None
        self.test_labels = None
        self.val_text = None
        self.val_labels = None
        self.data_format()

    def train_data_format(self):
        self.train_texts = []
        self.train_labels = []
        lines = read_data_from_file(self.train_data_path)
        for line in lines:
            temp = line.strip('\n').split('\t')
            if len(temp) == 2:
                self.train_labels.append(self.data_preprocesser.label2idx(temp[0]))
                self.train_texts.append(self.data_preprocesser.cut_sequence(temp[1]))

    def test_data_format(self):
        self.test_texts = []
        self.test_labels = []
        lines = read_data_from_file(self.test_data_path)
        for line in lines:
            temp = line.strip('\n').split('\t')
            if len(temp) == 2:
                self.test_labels.append(temp[0])
                self.test_texts.append(temp[1])

    def val_data_format(self):
        self.val_texts = []
        self.val_labels = []
        lines = read_data_from_file(self.val_data_path)
        for line in lines:
            temp = line.strip('\n').split('\t')
            if len(temp) == 2:
                self.val_labels.append(temp[0])
                self.val_texts.append(temp[1])

    def data_format(self):
        self.train_data_format()
        self.test_data_format()
        self.val_data_format()


if __name__ == '__main__':
    test = DataUtiler()
    print(test.data_preprocesser.get_vocab_dict())
    print(test.data_preprocesser.get_label_dict())
