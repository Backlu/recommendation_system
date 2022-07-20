#!/usr/bin/env python
# coding: utf-8

"""
History
0627: implement keyword extraction
"""

from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from keyphrase_vectorizers import KeyphraseCountVectorizer
import spacy
import jieba
from sklearn.feature_extraction.text import CountVectorizer

class Keyword_Extractor(object):
    _defaults = {
        }
    
    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"        

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        self.__dict__.update(kwargs)
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        #self.sentence_model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

        self.kw_model = KeyBERT(model=self.sentence_model)
        self.nlp = spacy.load("zh_core_web_sm")

    def text_clean(self, text):
        '''
        1. 刪除空白
        2. 刪除url, email
        '''
        new_tokens=[]
        tokens_whitespace = []
        tokens = self.nlp(text)
        for token in tokens:
            if token.orth_.isspace():
                continue
            elif (token.like_url) or (token.like_email):
                continue
            else:
                new_tokens.append(token.lower_)
                tokens_whitespace.append(bool(token.whitespace_))
                
        #new_text = spacy.tokens.doc.Doc(self.nlp.vocab, words=new_tokens, spaces=tokens_whitespace).text
        new_text = ' '.join(new_tokens)
        return new_text
    

    #def tokenize_zh(self, text):
    #    words = jieba.lcut(text)
    #    return words

    def keyword_extract(self, doc, use_mmr=True, diversity=0.5, top_n=3, seed_keywords=None):
        '''
        steps:
            1. text clean (刪除空白, url, email)
            2. document embedding
            3. keywords extarction
            4. keyphrases extraction
        '''
        ret_dict = {}
        clean_text = self.text_clean(doc)
        ret_dict['clean_text'] = clean_text
        doc_embedding = self.sentence_model.encode(clean_text)
        ret_dict['doc_embedding'] = doc_embedding
        
        #vectorizer = CountVectorizer(tokenizer=self.tokenize_zh)    
        
        keywords = self.kw_model.extract_keywords(clean_text, top_n=top_n, keyphrase_ngram_range=(1, 1), stop_words='english', use_mmr=use_mmr, diversity=diversity, seed_keywords=seed_keywords, highlight=False)
        keywords_embs = []
        for k,s in keywords:
            emb = self.sentence_model.encode(k)
            keywords_embs.append((k,s,emb))
        ret_dict['keywords'] = keywords_embs

        vectorizer = KeyphraseCountVectorizer()
        keyphrases = self.kw_model.extract_keywords(clean_text, top_n=top_n, vectorizer=vectorizer, stop_words='english', use_mmr=use_mmr, diversity=diversity, seed_keywords=seed_keywords, highlight=False)
        keyphrases_embs = []
        for k,s in keyphrases:
            emb = self.sentence_model.encode(k)
            keyphrases_embs.append((k,s,emb))
        ret_dict['keyphrases'] = keyphrases_embs
        return ret_dict 

