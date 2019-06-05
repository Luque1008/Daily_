import jieba
import os
import re
import pandas as pd
import collections
import numpy as np
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt


def is_chinese(char) :
    if '\u4e00' <= char <= '\u9fff' :
        return True
    else :
        return False


class words2graph():

    def __init__(self, path, name) :
        self.path = path
        self.file = os.path.join(path, name)

    def read_text(self, encoder) :
        with open( self.file, 'r', encoding=encoder ) as text :
            strings = text.read()
        return strings

    def _chinese_split(self, strings) :
        chinese_str = ''
        chinese_stopwords = ["、"]
        for i in strings :
            if is_chinese( i ) and i not in chinese_stopwords:
                chinese_str = chinese_str + i
        chin_list = list( jieba.cut_for_search( chinese_str ) )
        return chin_list

    def _english_split(self, strings) :
        #有空把replace换成re.sub
        english_str = ''
        for k in strings.split( ' ' ) :
            k = k.replace( "\t", '' ).replace( "\n", ' ' ).replace( ":", ' ' ).replace( ".", ' ' ).replace(
            "\"", ' ' ).replace( ",", ' ' ).replace( "?", ' ' ).replace( ";", ' ' ).replace( "；", ' ' ).split( ' ' )
            for j in k:
                if not is_chinese( j ) :
                    english_str = english_str + ' ' + j
        # pattern = '[\\t\\n\:\.\,\?\;\；\-]*'
        # strings = re.sub(pattern, '', strings)
        # pattern_1 = "[\"]*"
        # strings = re.sub(pattern_1, ' ', strings)
        # for k in strings.split( ' '):
        #     if not is_chinese( k ) :
        #         english_str = english_str + ' ' + k
        eng_list = english_str.split( ' ' )
        return eng_list

    def words_count(self, chin_list: list, eng_list=list) :
        dic = {}
        all_list = chin_list + eng_list
        for word in all_list:
            if word not in dic :
                dic[word] = 1
            else :
                dic[word] = dic[word] + 1
        return dic

    def words_cloud(self, chin_list: list, eng_list: list,
                    rm_words=None) :
        if rm_words is None :
            rm_words = ['', 'and', 'to', 'the', 'a', 'for', 'our', 'we', 'with', 'in', 'of', 'We', '的',
                        'be', 'that', 'their', 'as', 'on', 'an', 'is', '和', 'have', 'are', 'by',
                        'most', '-', 'where', 'its']
        words_list = []
        remove_words = rm_words
        all_list = chin_list + eng_list
        for word in all_list :
            if word not in remove_words :
                words_list.append( word )
        word_counts = collections.Counter( words_list )
        mask = np.array( Image.open( './wordcloud.jpg' ) )
        wc = wordcloud.WordCloud(
            font_path='/r2/dockerfile/py2/fonts/simhei.ttf',  # 设置字体格式
            mask=mask,
            scale=4,
            background_color='white',
            max_words=2000,
            max_font_size=100
        )
        wc.generate_from_frequencies( word_counts )
        image_colors = wordcloud.ImageColorGenerator( mask )
        wc.recolor( color_func=image_colors )
        plt.imshow( wc.recolor( color_func=image_colors ), interpolation="bilinear" )
        plt.axis( 'off' )
        wc.to_file( f'{self.path}/word_cloud.jpg' )

    def gen_cloud(self, encoder) :
        self.words_cloud( self._chinese_split( self.read_text( encoder ) ),
                          self._english_split( self.read_text( encoder ) ) )

    def gen_df(self, encoder) :
        df = pd.DataFrame(self.words_count( self._chinese_split( self.read_text( encoder ) ),
                                            self._english_split( self.read_text( encoder ) ) ), index = [0])

        df.to_csv( f'{self.path}/df.csv', encoding='utf-8' )



if __name__ == '__main__' :
    file_name = '123.txt'
    file_path = '/home/yan/桌面/'
    words2graph(file_path, file_name).gen_cloud('gbk')
    print( 'done' )
