# coding: utf-8
# Natural Language Process
import os
from porter_stemmer import PorterStemmer
import fool
import jieba

def get_basic_tools():
     return { 'stop_words':{'en':"stop_words_eng.txt",'zh-gbk':"stop_words_zh_GBK.txt",'zh-utf8':"stop_words_zh_UTF-8.txt"}}

#0 get stop words list 获取 stop_words 无意义词汇
def get_en_stop_words(lang_code = 'en'):
    stop_words = []
    file_name = get_basic_tools()['stop_words'][lang_code]
    path = os.getcwd() + '/tool/stop_words/'
    fd = open( path + file_name,'r')
    for line in fd.readlines():
        stop_words.append(line.strip())
    return stop_words

def get_cn_stop_words(lang_code = 'en'):
    stop_words = []
    file_name = get_basic_tools()['stop_words'][lang_code]
    path = os.getcwd() + '/tool/stop_words/'
    text = open( path + file_name).read()
    stop_words = text.split('\n')
    return stop_words

# 1 get documents name from the specific folder 获取指定文件夹下的文件名
def get_file_names(file_folder='data'):
    path = os.getcwd() + '/'+ file_folder + '/'
    files = {}
    for file_name in os.listdir(path):
        files[file_name] = path + file_name
    return files

# 2 get documents text 获取指定文件的内容
def get_file_content(file_path):
    content=''
    fd = open(file_path, 'r')
    for line in fd.readlines():
         content += line.replace('\n',' ')
    return content

def get_cn_file_content(file_path):
    content=''
    content = open(file_path).read()
    return content

#3 Text Normalization
def en_text_normalization(text):
    punctuations = ["{","}","【","】","[","]","`","·","~","!","！","@","#","$","￥","%","^","……","&","*","(",")","（","）","-","-","_","——","+","=","|","\\","、","\"","\'","“","”","‘","’",";","；","?","?",".","。",",","，","<",">","《","》"]
    for punctuation in punctuations:
        text = text.replace(punctuation," ")
    return text

#3 Text Normalization
def cn_text_normalization(text_list):
    punctuations = ["{","}","【","】","[","]","`","·","~","!","！","@","#","$","￥","%","^","……","&","*","(",")","（","）","-","-","_","——","+","=","|","\\","、","\"","\'","“","”","‘","’",";","；","?","?",".","。",",","，","<",">","《","》"]
    for punctuation in punctuations:
        for i in range(0,len(text_list)):
            if i<len(text_list):
                if text_list[i] == punctuation:
                    text_list.pop(i)
            else:
                break
    return text_list

# 4 Text Lowercasing
def text_lowercasing(text):
    return text.lower()

#5 Text Tokenization Text -> terms
def text_tokenization(text):
    return text.split()

#6 Stop word dropping
def text_stopword_dropping(text_list,stop_words):
    for stop_word in stop_words:
        for i in range(0,len(text_list)):
            if i >= len(text_list):
                break
            if text_list[i] == stop_word:
                text_list.pop(i)

    return text_list

#7 Stemming and lemmatization
#Porter’s algorithm
# 第一步，处理复数，以及ed和ing结束的单词。
# 第二步，如果单词中包含元音，并且以y结尾，将y改为i。
# 第三步，将双后缀的单词映射为单后缀。
# 第四步，处理-ic-，-full，-ness等等后缀。
# 第五步，在<c>vcvc<v>情形下，去除-ant，-ence等后缀。
# 第六步，也就是最后一步，在m()>1的情况下，移除末尾的“e”。
def text_stemming_lemmatization(text_list):
    ps = PorterStemmer()
    for i in range(0,len(text_list)):
        text_list[i] =  ps.stem(text_list[i],0,len(text_list[i])-1)
    return text_list

#保存成文本
def save_document_terms(file_name,document_terms,file_folder='temp'):
    path = os.getcwd() + '/' + file_folder + '/'
    sep='\n'
    fl = open(path+file_name, 'w')
    fl.write(sep.join(document_terms))
    fl.close()

#获取英文文件的关键词
def get_en_documents_terms():
    #documents_terms ={}
    #0 get stop words list
    stop_words = get_en_stop_words()

    # 1 get documents name from the specific folder
    file_names = get_file_names()
    # 2 get documents text
    for file_key, file_value in file_names.items():
        raw_text = get_file_content(file_value)
        #确认效果
        #print(raw_text)

        #3 Text Normalization
        normalized_text = en_text_normalization(raw_text)
        # 确认效果
        #print(normalized_text)

        # 4 Text Lowercasing
        lowercasing_text = text_lowercasing(normalized_text)
        # 确认效果
        #print(lowercasing_text)

        #5 Text Tokenization Text -> terms
        tokenized_list = text_tokenization(lowercasing_text)
        # 确认效果
        #print(tokenized_list)

        #6 Stop word dropping
        highlights_list = text_stopword_dropping(tokenized_list, stop_words)
        #print(highlights_text)

        #7 Stemming and lemmatization linguistic preprocessing of tokens（词干提取和词性还原）
        stm_len_list = text_stemming_lemmatization(highlights_list)
        #print(stm_len_list)

        #8 Stop word dropping
        final_list = text_stopword_dropping(stm_len_list, stop_words)
        #print(final_list)

        #9 保存成文本
        save_document_terms(file_name=file_key, document_terms=final_list, file_folder='temp')

        #Index the documents that each term occurs in
        #documents_terms[ file_key]= final_list

    #return documents_terms

#获取中文文件的关键词
def get_cn_documents_terms(cut_type='jieba'):
    #documents_terms ={}
    #0 get stop words list
    stop_words = get_cn_stop_words(lang_code = 'zh-utf8')

    # 1 get documents name from the specific folder
    file_names = get_file_names()
    # 2 get documents text
    for file_key, file_value in file_names.items():
        raw_text = get_cn_file_content(file_value)
        #确认效果
        #print(raw_text)

        # 3Text Tokenization Text -> terms
        # 导入自定义词典
        #jieba.load_userdict("dict.txt")
        # 全模式
        #text = "故宫的著名景点包括乾清宫、太和殿和黄琉璃瓦等"
        #seg_list = jieba.cut(text, cut_all=True)
        #print u"[全模式]: ", "/ ".join(seg_list)
        # 精确模式
        #seg_list = jieba.cut(text, cut_all=False)
        #print u"[精确模式]: ", "/ ".join(seg_list)
        # 搜索引擎模式
        #seg_list = jieba.cut_for_search(text)
        #print u"[搜索引擎模式]: ", "/ ".join(seg_list)

        if cut_type == 'jieba':
            temp = jieba.cut(raw_text, cut_all=False)
            temp = '.'.join(temp)
            tokenized_list = temp.split('.')
        else:
            tokenized_list = fool.cut(raw_text)
            # 确认效果
        # print(tokenized_list)

        #4 Text Normalization
        normalized_list = cn_text_normalization(tokenized_list)
        # 确认效果
        #print(normalized_text)

        #5 Stop word dropping
        final_list = text_stopword_dropping(normalized_list, stop_words)
        #print(final_list)

        #6 保存成文本
        save_document_terms(file_name=file_key, document_terms=final_list, file_folder='temp')

        #Index the documents that each term occurs in
        #documents_terms[ file_key]= final_list

    #return documents_terms

def main():
    get_cn_documents_terms()
