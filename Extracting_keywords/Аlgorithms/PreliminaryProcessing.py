
import re

# Предватительная обработка данных и выделение кандидатов
import pymorphy2

from Thematic_dictionary.TextIO import TextIO


class PreliminaryProcessing:

    def __init__(self, text):
        self.text = text
        self.PrelProc()

    def PrelProc(self):
        self.Tokenization()
        self.Lemma_POS_Tag()
        self.Keywords_Candidate()
        IOport = TextIO()
        IOport.WriteJson(self.fin_dict_Cand, 'Text_dis_alg.json')



    # Токенизация по словам и предложениям
    def Tokenization(self):
        test1 = re.split(r'[\.,\?,\!,\.\.\.] ([А-Я])', self.text)

        for i in test1:
            i.strip(' ')

        text2 = []
        i = 0
        while i < len(test1):
            if len(test1[i]) == 1:
                text2.append((test1[i] + test1[i + 1]).rstrip('\. '))
                i += 1
            else:
                text2.append(test1[i])
            i += 1

        self.t_text = []
        for num_sentence in range(len(text2)):
            sentence = re.split('[\,]', text2[num_sentence])
            for i in sentence:
                i.strip(' ')
            t_sentence = []
            for num_part_sentence in range(len(sentence)):
                part_sentence = re.split('[^A-Я,а-я,0-9,\-]', sentence[num_part_sentence])
                t_part_sentence = []
                for num_words in range(len(part_sentence)):
                    if part_sentence[num_words] != '':
                        t_part_sentence.append(part_sentence[num_words])

                t_sentence.append(t_part_sentence)

            self.t_text.append(t_sentence)

        print(self.t_text)
        print('Fin Tokenization')

    def Lemma_POS_Tag(self):
        self.morph = pymorphy2.MorphAnalyzer()
        t = self.morph.parse(self.t_text[0][0][7])[0].tag
        for sentence in range(len(self.t_text)):
            for part_sentence in range(len(self.t_text[sentence])):
                for words in range(len(self.t_text[sentence][part_sentence])):
                    if 'LATN' in self.morph.parse(self.t_text[sentence][part_sentence][words])[0].tag:
                        self.t_text[sentence][part_sentence][words] = \
                            [self.morph.parse(self.t_text[sentence][part_sentence][words])[0].normal_form, 'LATN']

                    else:
                        self.t_text[sentence][part_sentence][words] = \
                            [self.morph.parse(self.t_text[sentence][part_sentence][words])[0].normal_form, \
                             self.morph.parse(self.t_text[sentence][part_sentence][words])[0].tag.POS]

        print(self.t_text)
        print('Fin Lemma_POS_Tag')

    def Keywords_Candidate(self):
        self.t_nsw_text = []
        for sentence in range(len(self.t_text)):
            for part_sentence in range(len(self.t_text[sentence])):
                for words in range(len(self.t_text[sentence][part_sentence])):
                    try:
                        if self.t_text[sentence][part_sentence][words][1] == 'LATN':
                            self.t_nsw_text.append(self.t_text[sentence][part_sentence][words])
                    except ValueError:
                        if self.t_text[sentence][part_sentence][words][1] in ['NOUN', 'ADJF', 'ADVB', 'INFN']:
                            self.t_nsw_text.append(self.t_text[sentence][part_sentence][words])

        dict_Cand = {}
        self.fin_dict_Cand = {}
        for n in self.t_nsw_text:
            if n[0] in dict_Cand:
                dict_Cand[n[0]] = [dict_Cand[n[0]][0], dict_Cand[n[0]][1] + 1]
            else:
                dict_Cand[n[0]] = [n[1], 1]

        for n in dict_Cand:
            if dict_Cand[n][1] > 2 and len(n) > 2:
                self.fin_dict_Cand[n] = [dict_Cand[n][0], dict_Cand[n][1]]

        print(self.fin_dict_Cand)
        print('Fin Keywords_Candidate')

# base_text = TextIO()
# f = PreliminaryProcessing(base_text.ReadTeaxt('tren_text_1.txt'))
