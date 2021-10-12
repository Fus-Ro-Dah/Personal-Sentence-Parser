import pandas as pd

dict = pd.read_csv('百度分词词库.txt', sep = ' ', names=['len', 'word'])
word_list = dict['word'].tolist()

#print(dict)
#print(dict['word'])
#print(word_list)

sentence = input('请输入一个句子：')
length = len(sentence)
results = []
temp_arr = []
while((len(sentence) > 1)):
    #筛除长度为3的词
    if (len(sentence) > 3):
        temp_arr = []
        temp_arr.append(sentence[-1])
        temp_arr.append(sentence[-2])
        temp_arr.append(sentence[-3])
        temp_arr_reversed = temp_arr[::-1]
        temp = ''.join(temp_arr_reversed)
        #print(temp_arr)
        #print(temp_arr_reversed)
        #print(temp)
        if temp in word_list:
            results.append(temp)
            temp_arr = []
            sentence = sentence.replace(temp, '')
            #print(sentence)
    #筛除长度为2的词
    if (len(sentence) > 2):
        temp_arr = []
        temp_arr.append(sentence[-1])
        temp_arr.append(sentence[-2])
        temp_arr_reversed = temp_arr[::-1]
        temp = ''.join(temp_arr_reversed)
        #print(temp_arr)
        #print(temp_arr_reversed)
        #print(temp)
        if temp in word_list:
            results.append(temp)
            temp_arr = []
            sentence = sentence.replace(temp, '')
            #print(sentence)
    #筛除长度为1的词
    if (len(sentence) > 1):
        temp_arr = []
        temp_arr.append(sentence[-1])
        temp_arr_reversed = temp_arr[::-1]
        temp = ''.join(temp_arr_reversed)
        #print(temp_arr)
        #print(temp_arr_reversed)
        #print(temp)
        if temp in word_list:
            results.append(temp)
            temp_arr = []
            sentence = sentence.replace(temp, '')
            #print(sentence)
results.append(sentence)
results = results[::-1]
final = []
#结合可以结合的单字
i = 0
while i < (len(results) - 1):
    temp = results[i] + results[i + 1]
    #print(temp)
    if(temp in word_list):
        final.append(temp)
        i += 2
    else:
        final.append(results[i])
        i += 1
if(final[-1] != results[-1]):
    final.append(results[-1])

f = []
i = 0
while i < (len(results) - 2):
    temp = results[i] + results[i + 1] + results[i + 2]
    #print(temp)
    if(temp in word_list):
        f.append(temp)
        i += 3
    else:
        f.append(final[i])
        i += 1
if(f[-1] != final[-1]):
    f.append(final[-1])

parsed_result = '/'.join(f)


#print(results)
print(parsed_result)
#print(final)