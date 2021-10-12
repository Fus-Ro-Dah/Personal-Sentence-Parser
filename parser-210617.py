import pandas as pd

dict = pd.read_csv('百度分词词库.txt', sep = ' ', names=['len', 'word'])
word_list = dict['word'].tolist()

conjunctions_arr = ['.', ',', '?', '!', ';', '，', '。', '？', '；', '！', '、', '【', '】']
#print(dict)
#print(dict['word'])
#print(word_list)

#识别标点符号并分割句子，返回分好的句子和标点符号，保留原顺序
def recognizeConjunction(whole_sentence):
    splited_sentences = []
    start_index = 0
    conjunctions_num = 0
    for i in range(len(whole_sentence)):
        if(whole_sentence[i] in conjunctions_arr):
            splited_sentences.append(whole_sentence[start_index:i])
            splited_sentences.append(whole_sentence[i:i + 1])
            start_index = i + 1
            conjunctions_num += 1
    if(conjunctions_num != 0 and start_index!= len(whole_sentence)):
        splited_sentences.append(whole_sentence[start_index:])
    if(conjunctions_num == 0):
        splited_sentences.append(whole_sentence)
    for splited_sentence in splited_sentences:
        if(splited_sentence == ''):
            splited_sentences.remove('')
    return splited_sentences


#识别是否全是英文/含有中文，全是英文的输出False，含有中文输出True
def has_Chinese(sentence):
    '''
    num_non_English = 0
    for char in sentence:
        if(char.isalpha() == 0 and char != ' '):
            num_non_English += 1
    if(num_non_English == 0):
        return 0
    else:
        return 1
    '''
    for ch in sentence:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
    
#给全是英文的句子分词，返回分好的单词
def parse_English_sentence(sentence):
    parsed_words = []
    start_index = 0
    for i in range(len(sentence)):
        if(sentence[i] == ' '):
            parsed_words.append(sentence[start_index:i])
            start_index = i + 1
    parsed_words.append(sentence[start_index:])
    return parsed_words


#双向给中文句子分词并输出较好结果，依据百度词库，返回分好的词，保留原有顺序。最大词长默认为5。混入的英文词先按字母分割
def parse_Chinese_sentence(sentence):
    backward_parse_results = backward_parse_Chinese_sentence(sentence, [])
    forward_parse_results = forward_parse_Chinese_sentence(sentence, [])
    #开始比较前后向分词的结果
    backward_parse_num = len(backward_parse_results)
    forward_parse_num = len(forward_parse_results)
    if (backward_parse_num > forward_parse_num):
        return forward_parse_results
    elif (backward_parse_num < forward_parse_num):
        return backward_parse_results
    else:
        if (backward_parse_results == forward_parse_results):
            return backward_parse_results
        else:
            #比较单字数量，取单字数量较少的
            single_backward_num = 0
            single_forward_num = 0
            for word in backward_parse_results:
                if (len(word) == 1):
                    single_backward_num += 1
            for word in forward_parse_results:
                if (len(word) == 1):
                    single_forward_num += 1

            if (single_backward_num < single_forward_num):
                return backward_parse_results
            else:
                return forward_parse_results




#逆向给中文句子分词，依据百度词库，返回分好的词，保留原有顺序。最大词长默认为5。混入的英文词先按字母分割
def backward_parse_Chinese_sentence(sentence, parsed_words):
    maximum_length = 5
    if len(sentence) == 0:
        parsed_words_reversed = parsed_words[::-1]
        for char in parsed_words_reversed:
            if(char == ' '):
                parsed_words_reversed.remove(' ')
        return parsed_words_reversed
    else:
        for i in range(maximum_length + 1)[::-1]:
            if sentence[-i:] in word_list:
                match_word = sentence[-i:]
                unparsed_part = sentence[:-i]
                parsed_words.append(match_word)
                break
        else:
            match_word = sentence[-1]
            unparsed_part = sentence[:-1]
            parsed_words.append(match_word)
        return backward_parse_Chinese_sentence(unparsed_part, parsed_words)





#正向给中文句子分词，依据百度词库，返回分好的词，保留原有顺序。最大词长默认为5。混入的英文词先按字母分割
def forward_parse_Chinese_sentence(sentence, parsed_words):
    maximum_length = 5
    if len(sentence) == 0:
        for char in parsed_words:
            if(char == ' '):
                parsed_words.remove(' ')
        return parsed_words
    else:
        for i in range(maximum_length + 1)[::-1]:
            if sentence[:i] in word_list:
                match_word = sentence[:i]
                unparsed_part = sentence[i:]
                parsed_words.append(match_word)
                break
        else:
            match_word = sentence[0]
            unparsed_part = sentence[1:]
            parsed_words.append(match_word)
        return forward_parse_Chinese_sentence(unparsed_part, parsed_words)





if __name__ == '__main__':
    #输入语段
    sentences = input('请输入一个语段：')
    
    length = len(sentences)
    results = []
    #temp_arr = []

    #获得按顺序分出句子和标点符号的arr
    separated_sentences = recognizeConjunction(sentences)
    #print(separated_sentences)
    #print(recognizeConjunction(sentences))


    #遍历句子和标点符号的arr，句子就判断中英文并分词，标点符号就按顺序加在末尾。中文的话用正向和逆向分词，之后再比较单字数量并取效果较好的
    for sentence in separated_sentences:
        if(sentence in conjunctions_arr):
            results.append(sentence)
        else:
            if(has_Chinese(sentence) == False):
                #results.append(parse_English_sentence(sentence))
                for char in parse_English_sentence(sentence):
                    results.append(char)
            else:
                #results.append(parse_Chinese_sentence(sentence, []))
                for char in parse_Chinese_sentence(sentence):
                    results.append(char)
    #print(has_Chinese(sentences))
    #print(parse_English_sentence(sentence))
    #print(parse_Chinese_sentence(sentences, []))

    #print(results)

    print('逆向分词：')
    print('/'.join(backward_parse_Chinese_sentence(sentences, [])))

    
    print('正向分词：')
    print('/'.join(forward_parse_Chinese_sentence(sentences, [])))

    parsed_result = '/'.join(results)
    print('分词结果：')
    print(parsed_result)