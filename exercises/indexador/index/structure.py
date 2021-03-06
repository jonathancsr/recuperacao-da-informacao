from IPython.display import clear_output
from typing import List, Set, Union
from abc import abstractmethod
from functools import total_ordering
from os import path
import os
import pickle
import gc


class Index:
    def __init__(self):
        self.dic_index = {}
        self.set_documents = set()

    def index(self, term: str, doc_id: int, term_freq: int):
        int_term_id = 0
        if term not in self.dic_index:
            int_term_id = len(self.dic_index)
            self.dic_index[term] = self.create_index_entry(int_term_id)
        else:
            int_term_id = self.get_term_id(term)

        self.add_index_occur(self.dic_index[term], doc_id, int_term_id, term_freq)
        self.set_documents.add(term)

    @property
    def vocabulary(self) -> List:
        return self.dic_index.keys()

    @property
    def document_count(self) -> int:
        return len(self.set_documents)

    @abstractmethod
    def get_term_id(self, term: str):
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")

    @abstractmethod
    def create_index_entry(self, termo_id: int):
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")

    @abstractmethod
    def add_index_occur(self, entry_dic_index, doc_id: int, term_id: int, freq_termo: int):
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")

    @abstractmethod
    def get_occurrence_list(self, term: str) -> List:
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")

    @abstractmethod
    def document_count_with_term(self, term: str) -> int:
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")

    def finish_indexing(self):
        pass

    def __str__(self):
        arr_index = []
        for str_term in self.vocabulary:
            arr_index.append(f"{str_term} -> {self.get_occurrence_list(str_term)}")

        return "\n".join(arr_index)

    def __repr__(self):
        return str(self)


@total_ordering
class TermOccurrence:
    def __init__(self, doc_id: int, term_id: int, term_freq: int):
        self.doc_id = doc_id
        self.term_id = term_id
        self.term_freq = term_freq

    def write(self, idx_file):
        pickle.dump(self, idx_file)

    def __hash__(self):
        return hash((self.doc_id, self.term_id))

    def __eq__(self, other_occurrence: "TermOccurrence"):
        return False if other_occurrence is None else (
                self.doc_id == other_occurrence.doc_id and self.term_id == other_occurrence.term_id)

    def __lt__(self, other_occurrence: "TermOccurrence"):
        if other_occurrence is None:
            return True

        if self.term_id < other_occurrence.term_id:
            return True
        elif self.term_id == other_occurrence.term_id:
            return self.doc_id < other_occurrence.doc_id
        else:
            return False

    def __str__(self):
        return f"(term_id:{self.term_id} doc: {self.doc_id} freq: {self.term_freq})"

    def __repr__(self):
        return str(self)


# HashIndex é subclasse de Index
class HashIndex(Index):
    def get_term_id(self, term: str):
        return self.dic_index[term][0].term_id

    def create_index_entry(self, termo_id: int) -> List:
        return []

    def add_index_occur(self, entry_dic_index: List[TermOccurrence], doc_id: int, term_id: int, term_freq: int):
        entry_dic_index.append(TermOccurrence(doc_id, term_id, term_freq))

    def get_occurrence_list(self, term: str) -> List:
        return self.dic_index[term] if term in self.dic_index else []

    def document_count_with_term(self, term: str) -> int:
        return len(self.dic_index[term]) if term in self.dic_index else 0


class TermFilePosition:
    def __init__(self, term_id: int, term_file_start_pos: int = None, doc_count_with_term: int = None):
        self.term_id = term_id

        # a serem definidos após a indexação
        self.term_file_start_pos = term_file_start_pos
        self.doc_count_with_term = doc_count_with_term

    def __str__(self):
        return f"term_id: {self.term_id}, doc_count_with_term: {self.doc_count_with_term}, term_file_start_pos: {self.term_file_start_pos}"

    def __repr__(self):
        return str(self)


class FileIndex(Index):
    TMP_OCCURRENCES_LIMIT = 100000000

    def __init__(self):
        super().__init__()

        self.lst_occurrences_tmp = []
        self.idx_file_counter = 0
        self.str_idx_file_name = None

    def get_term_id(self, term: str):
        return self.dic_index[term].term_id

    def create_index_entry(self, term_id: int) -> TermFilePosition:
        return TermFilePosition(term_id)

    def add_index_occur(self, entry_dic_index: TermFilePosition, doc_id: int, term_id: int, term_freq: int):
        self.lst_occurrences_tmp.append(TermOccurrence(doc_id, term_id, term_freq))

        if len(self.lst_occurrences_tmp) >= FileIndex.TMP_OCCURRENCES_LIMIT:
            self.save_tmp_occurrences()

    def next_from_list(self) -> TermOccurrence:
        try:
            next_element = self.lst_occurrences_tmp.pop(0)
            return None if not next_element else next_element
        except:
            return None

    def next_from_file(self, file_idx) -> TermOccurrence:
        try:
            next_from_file = pickle.load(file_idx)
            return None if not next_from_file else TermOccurrence(next_from_file.doc_id, next_from_file.term_id,
                                                                  next_from_file.term_freq)
        except:
            return None

    def save_tmp_occurrences(self):
        # Para eficiencia, todo o codigo deve ser feito com o garbage
        # collector desabilitado
        filename = ""
        gc.disable()

        # ordena pelo term_id, doc_id
        self.lst_occurrences_tmp.sort()
        if self.str_idx_file_name is None:
            self.str_idx_file_name = f"occur_index_{self.idx_file_counter}.idx"
            idx_file = open(self.str_idx_file_name, "wb")
        else:
            idx_file = open(self.str_idx_file_name, "rb")
            self.idx_file_counter = self.idx_file_counter + 1
            self.str_idx_file_name = f"occur_index_{self.idx_file_counter}.idx"
        with open(self.str_idx_file_name, "wb") as new_idx_file:
            term_ocurrence_from_file = self.next_from_file(idx_file)
            term_ocurrence_from_list = self.next_from_list()
            while term_ocurrence_from_file != None or term_ocurrence_from_list != None:
                if term_ocurrence_from_file < term_ocurrence_from_list:
                    next_save = term_ocurrence_from_file
                    term_ocurrence_from_file = self.next_from_file(idx_file)
                else:
                    next_save = term_ocurrence_from_list
                    term_ocurrence_from_list = self.next_from_list()
                next_save.write(new_idx_file)

        self.lst_occurrences_tmp = []
        idx_file.close()
        gc.enable()

    # melhorar o codigo
    def finish_indexing(self):
        if len(self.lst_occurrences_tmp) > 0:
            self.save_tmp_occurrences()




        dic_ids_por_termo = {}
        for str_term, obj_term in self.dic_index.items():
            dic_ids_por_termo[obj_term.term_id] = str_term
        list_count_ocurrence = {}

        with open(self.str_idx_file_name, 'rb') as idx_file:
            term_ocurrence_from_file = self.next_from_file(idx_file)
            int_size_of_occur = idx_file.tell()

            while term_ocurrence_from_file != None:
                if term_ocurrence_from_file.term_id not in list_count_ocurrence:
                   list_count_ocurrence[term_ocurrence_from_file.term_id] = 1
                else:
                    list_count_ocurrence[term_ocurrence_from_file.term_id] += 1
                term_ocurrence_from_file = self.next_from_file(idx_file)

            for id_elemnt, obj_element in list_count_ocurrence.items():
                if id_elemnt > 1:
                    count_terms = self.dic_index[dic_ids_por_termo[id_elemnt - 1]].doc_count_with_term
                    last_byte_position = self.dic_index[dic_ids_por_termo[id_elemnt - 1]].term_file_start_pos
                    bytes_start_position = last_byte_position + count_terms * int_size_of_occur
                else:
                    bytes_start_position = 0
                new_term_file_position = TermFilePosition(id_elemnt, bytes_start_position, obj_element)
                self.dic_index[dic_ids_por_termo[id_elemnt]] = new_term_file_position

    def get_occurrence_list(self, term: str) -> List:
        occurrency_list = []
        if term in self.dic_index:
            term_id = self.dic_index[term].term_id

            with open(self.str_idx_file_name, "rb") as idx_file:
                term_ocurrence_from_file = self.next_from_file(idx_file)
                while term_ocurrence_from_file is not None:
                    if term_ocurrence_from_file.term_id == term_id:
                        occurrency_list.append(term_ocurrence_from_file)

                    term_ocurrence_from_file = self.next_from_file(idx_file)

        return occurrency_list

    def document_count_with_term(self, term: str) -> int:
        count_documents_with_term = 0
        if term in self.dic_index:
            term_id = self.dic_index[term].term_id

            with open(self.str_idx_file_name, "rb") as idx_file:
                term_ocurrence_from_file = self.next_from_file(idx_file)
                while term_ocurrence_from_file is not None:
                    if term_ocurrence_from_file.term_id == term_id:
                        count_documents_with_term += 1

                    term_ocurrence_from_file = self.next_from_file(idx_file)

        return count_documents_with_term