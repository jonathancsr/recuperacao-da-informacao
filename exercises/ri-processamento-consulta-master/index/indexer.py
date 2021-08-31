from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup
import string
from datetime import datetime
from nltk.tokenize import word_tokenize
import nltk
import os

nltk.download('punkt')

class Cleaner:
    def __init__(self,stop_words_file:str,language:str,
                        perform_stop_words_removal:bool,perform_accents_removal:bool,
                        perform_stemming:bool):

        data_path = os.path.dirname(os.path.abspath(__file__))
        stop_words_file = os.sep.join([data_path] + [stop_words_file])
        self.set_stop_words = self.read_stop_words(stop_words_file)

        self.stemmer = SnowballStemmer(language)
        in_table =  "áéíóúâêôçãẽõü!?.:;,"
        out_table = "aeiouaeocaeou      "
        #altere a linha abaixo para remoção de acentos (Atividade 11)
        self.accents_translation_table = in_table.maketrans(in_table,out_table)
        self.set_punctuation = set(string.punctuation)

        #flags
        self.perform_stop_words_removal = perform_stop_words_removal
        self.perform_accents_removal = perform_accents_removal
        self.perform_stemming = perform_stemming

    def html_to_plain_text(self,html_doc:str) ->str:
        return BeautifulSoup(html_doc, 'html.parser').get_text()

    def read_stop_words(self,str_file):
        set_stop_words = set()
        with open(str_file, "r") as stop_words_file:
            for line in stop_words_file:
                arr_words = line.split(",")
                [set_stop_words.add(word) for word in arr_words]
        return set_stop_words

    def is_stop_word(self,term:str):
        if term in self.set_stop_words:
            return True
        return False

    def word_stem(self,term:str):
        return self.stemmer.stem(term)


    def remove_accents(self,term:str) ->str:
        return term.translate(self.accents_translation_table)


    def preprocess_word(self,term:str) -> str:
        term = term.lower()
        if self.perform_stop_words_removal is True and self.is_stop_word(term):
            term = ""

        if self.perform_accents_removal is True:
            term = self.remove_accents(term)

        if self.perform_stemming is True:
            term = self.word_stem(term)

        return term



class HTMLIndexer:
    cleaner = Cleaner(stop_words_file="stopwords.txt",
                        language="portuguese",
                        perform_stop_words_removal=True,
                        perform_accents_removal=True,
                        perform_stemming=True)
    def __init__(self,index):
        self.index = index

    def text_word_count(self,plain_text:str):
        dic_word_count = {}

        plain_text_tokenized = word_tokenize(plain_text)

        for word in plain_text_tokenized:
            word = self.cleaner.preprocess_word(word)
            if word not in ["", " "]:
                if word in dic_word_count:
                    dic_word_count[word] += 1
                else:
                    dic_word_count[word] = 1
        return dic_word_count

    def index_text(self,doc_id:int, text_html:str):
        text = HTMLIndexer.cleaner.html_to_plain_text(text_html)
        dic_words = self.text_word_count(text)

        for word in dic_words:
            self.index.index(word, doc_id, dic_words[word])

    def index_text_dir(self,path:str):
        count = 0
        for str_sub_dir in os.listdir(path):
            path_sub_dir = f"{path}/{str_sub_dir}"
            ## Condicional escrita para rodar o programa em pastas do MAC OS
            print(f"Arquivo -> {count}")
            if str_sub_dir not in '.DS_Store':
                for file_name in os.listdir(path_sub_dir):
                    file_path = f"{path_sub_dir}/{file_name}"
                    with open(file_path, "rb") as file:
                        intit_time = datetime.now()
                        self.index_text(int((file_name.split("."))[0]), file)
                        end_time = datetime.now()
                        spend_time = end_time - intit_time
                    with open("times.txt", "a", encoding="utf-8") as file:
                        file.write(file_path+":")
                        file.write(f"{spend_time.total_seconds()}\n")
                    count += 1
        with open("vocabulary.txt", "a", encoding="utf-8") as vocabulary_term:
            for str_term, obj_term in self.dic_index.items():
                vocabulary_term.write(f"Termo: {str_term} term_id: {obj_term.term_id}\n")
        self.index.finish_indexing()