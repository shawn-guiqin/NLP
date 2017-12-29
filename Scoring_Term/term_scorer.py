# coding: utf-8
# Text Mining and Information Retrieval
import os
import numpy as np
from collections import *


# 获取文件夹下的所有文件
def get_files(file_folder):
    path = os.getcwd() + '/' + file_folder + '/'
    files = {}
    for file_name in os.listdir(path):
        files[file_name] = path + file_name
    return files


# 获取指定文件的内容
def get_file_content(file_name):
    text = open(file_name).read()
    words = text.split('\n')
    return words

#保存成文本
def save_dict_into_txt(data_dict,file_folder,write_model):
    path = os.getcwd() + '/' + file_folder + '/'
    if not os.path.exists(path):
        os.mkdir(path)
    for file_name, file_values in data_dict.items():
        fl = open(path+file_name,write_model)
        for key,values in file_values.items():
            line_str = key+"\t"
            for value in values:
                line_str += str(value)+ "\t"
            line_str+='\n'
            fl.write(line_str)
        fl.close()

# scoring term weighting
def scoring_term_weight():
    file_dict = {}
    # 1 读取文件夹下的所有文件
    files = get_files('temp')
    # 2 读取所有文件的terms
    for file_name, file_value in files.items():
        file_dict[file_name] = get_file_content(file_value)

    total_term_num = 0
    total_term_type = 0
    total_file_num = len(file_dict)
    files_info = {}
    terms_info = {}
    signle_file_terms = {}
    files_terms={}

    for file_name, file_terms in file_dict.items():
        counted_terms = Counter(file_terms)
        total_term_num += len(file_terms)
        total_term_type += len(counted_terms)
        files_info[file_name] = [len(file_terms), len(counted_terms)]  # 多少词  多少种词
        for term_name, term_count in counted_terms.items():
            NTFtd = term_count / len(file_terms)
            WFtd = 0 if term_count <= 0 else (1 + np.log(term_count))
            signle_file_terms[term_name]=[term_count, NTFtd, WFtd,0,0,0]#TF, NTF,WTF,IDF,TFIDF,WFIDF
            if term_name in terms_info.keys():
                terms_info[term_name][0] += term_count
                terms_info[term_name][1]+= 1
            else:
                terms_info[term_name]=[term_count,1] #CF  DF
        files_terms[file_name]= signle_file_terms

    for file_name,file_terms in files_terms.items():
        for term_name,term_info in file_terms.items():
            DFt = terms_info[term_name][1]
            IDFt = np.log(total_file_num/DFt)
            files_terms[file_name][term_name][3]= IDFt
            files_terms[file_name][term_name][4] = files_terms[file_name][term_name][1]*IDFt
            files_terms[file_name][term_name][5] =  files_terms[file_name][term_name][1]*IDFt

    #保存成文本
    #print( files_info)
    save_dict_into_txt(data_dict={'Files_Info.txt':files_info}, file_folder='result/files',write_model='w')
    #print("-------")
    #print(terms_info)
    save_dict_into_txt(data_dict={'Terms_Info.txt': terms_info}, file_folder='result/terms',write_model='w')
    #print("++++++++")
    #print(files_terms)
    save_dict_into_txt(data_dict=files_terms, file_folder='result/files_terms',write_model='w')


    # 2 读取所有文件的terms
def main():
    scoring_term_weight()
