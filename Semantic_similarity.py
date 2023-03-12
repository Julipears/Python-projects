'''Semantic Similarity: starter code provided by Prof. Michael Guerzhoy.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot_prod = 0

    # getting a copy of all the keys

    keys = []
    for key in vec1.keys():
        keys.append(key)
    for key in vec2.keys():
        keys.append(key)
    keys_a = set(keys)

    # keys_a = set(list(vec1.keys()) + list(vec2.keys()))

    # updating the dot product
    for key in keys_a:
        dot_prod += vec1.get(key, 0) * vec2.get(key, 0)

    # getting sum of the vectors
    sum_vec1 = 0
    sum_vec2 = 0
    for key in vec1.keys():
        sum_vec1 += vec1[key]**2
    for key in vec2.keys():
        sum_vec2 += vec2[key]**2

    return dot_prod / math.sqrt(sum_vec1 * sum_vec2)


# def build_semantic_descriptors(sentences):
#     words_dict = {}
#     for sent in sentences:
#         for word in sent:
#             if word not in words_dict.keys():
#                 words_dict[word] = {}

#     for sent in sentences:
#         for word in sent:
#             for word_key in sent:
#                 cur_value = words_dict[word_key].get(word, 0)
#                 if word != word_key:
#                     words_dict[word_key].update({word: cur_value+1})
#     return words_dict


# def build_semantic_descriptors(sentences):
#     words_dict = {}
#     for sent in sentences:
#         for word_key in sent:
#             # Initilize each value of words_dict as a dictionary
#             if word_key not in words_dict.keys():
#                 words_dict[word_key] = {}

#             # Within the dictionary of the dictionary, check
#             # build a frequency table
#             for word in sent:
#                 # Don't add the word to its own frequnecy table
#                 if word != word_key:
#                     cur_value = words_dict[word_key].get(word, 0)
#                     words_dict[word_key].update({word: cur_value + 1})

#     return words_dict

# def build_semantic_descriptors(sentences):
#     words_dict = {}
#     for sent in sentences:
#         for word_key in sent:
#             # Initilize each value of words_dict as a dictionary
#             if word_key not in words_dict.keys():
#                 words_dict[word_key] = {}

#             # Within the dictionary of the dictionary, check
#             # build a frequency table
#             for word in sent:
#                 # Don't add the word to its own frequnecy table
#                 if word != word_key:
#                     cur_value = words_dict[word_key].get(word, 0)
#                     words_dict[word_key].update({word: cur_value + 1})

#     return words_dict


def build_semantic_descriptors(sentences):
    words_dict = {}
    for sent in sentences:
        words_in_sent = set(sent)
        for word_key in words_in_sent:
            # Initilize each value of words_dict as a dictionary
            if word_key not in words_dict.keys():
                words_dict[word_key] = {}

            # Within the dictionary of the dictionary, check
            # build a frequency table
            for word in words_in_sent:
                # Don't add the word to its own frequency table
                if word != word_key:
                    cur_value = words_dict[word_key].get(word, 0)
                    words_dict[word_key].update({word: cur_value + 1})

    return words_dict

def build_semantic_descriptors_from_files(filenames):
    comb_txt = ""
    symb = [",", "-", "--", ":", ";"]
    end_symb = [".", "!", "?"]
    for i in range(len(filenames)):
        file = open(filenames[i], "r", encoding="latin1")
        txt = file.read()
        txt = txt.replace("\n", " ")

        # FIDDLE AROUND THIS PART

        txt = txt.lower()
        for punc in symb:
            txt = txt.replace(punc, " ")
        for punc in end_symb:
            txt = txt.replace(punc, ".")
        comb_txt += txt
        file.close()
    txt_list = comb_txt.split(".")
    sent_list = []
    for sent in txt_list:
        split_sent = sent.split()
        sent_list.append(split_sent)

    comb_dict = build_semantic_descriptors(sent_list)

    return comb_dict



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    cur_max_sim = choices[0]
    for alt in choices:
        # Are both words in the semantic_descriptors
        if word in semantic_descriptors and alt in semantic_descriptors:
            v = semantic_descriptors[alt]
            w = semantic_descriptors[word]
            cur_sim = similarity_fn(v, w)

            # Check if our cur_max is in the descriptor
            if cur_max_sim in semantic_descriptors:
                cur_max = similarity_fn(w, semantic_descriptors[cur_max_sim])
            else:
                # Set as -1 if it can't be determined
                cur_max = -1
            
            if cur_sim > cur_max:
                cur_max_sim = alt
        else:
            # Can't be determined, set -1
            cur_sim = -1
            continue
    return cur_max_sim


# def run_similarity_test(filename, semantic_descriptors, similarity_fn):
#     file = open(filename, "r", encoding="latin1")
#     file_length = len(file.readlines())
#     count = 0
#     correct = 0
#     while count < file_length:
#         line = file.readline().split(" ")
#         choices = line[2:]
#         guess = most_similar_word(line[0], choices, semantic_descriptors,
#                                   similarity_fn)
#         if guess == line[1]:
#             correct += 1
#         count += 1
#     file.close()
#     # Return answer as a percentage
#     return correct / file_length * 100


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file = open(filename, "r", encoding="latin1")
    
    # count is the file length
    count = 0
    correct = 0
    while True:

        # Read the line
        line_str = file.readline()
        # Reached end of file

####### TO DO FIX THIS

        if line_str == "":
            break
        line_str = line_str.replace("\n", "")
        line_str = line_str.lower()


        # Line in a list format
        line = line_str.split(" ")
        
        choices = line[2:]
        guess = most_similar_word(line[0], choices, semantic_descriptors,
                                  similarity_fn)
        if guess == line[1]:
            correct += 1
        count += 1
    file.close()
    # Return answer as a percentage
    return correct / count * 100


def cosine_similarity_test():
    vec1 = {"a": 1, "b": 2, "c": 3}
    vec2 = {"b": 4, "c": 5, "d": 6}
    assert cosine_similarity(vec1, vec2) - 0.7 < 0.01


def build_semantic_descriptors_test():
    s = [["i", "am", "a", "sick", "man"], ["i", "am", "a", "spiteful", "man"],
         ["i", "am", "an", "unattractive", "man"],
         ["i", "believe", "my", "liver", "is", "diseased"],
         [
             "however", "i", "know", "nothing", "at", "all", "about", "my",
             "disease", "and", "do", "not", "know", "for", "certain", "what",
             "ails", "me"
         ]]
    # print(build_semantic_descriptors(s))
    f = open("testcase.txt", "w")
    f.write(str(build_semantic_descriptors(s)))
    f.close()

import time

def similarity_test():
    start_time = time.time()
    filenames = ["txt1.txt", "txt3.txt"]
    semantic_descriptors = build_semantic_descriptors_from_files(filenames)
    print(run_similarity_test("test.txt", semantic_descriptors, cosine_similarity))
    print("My program took", time.time() - start_time, "to run")


if __name__ == "__main__":
    cosine_similarity_test()
    build_semantic_descriptors_test()
    similarity_test()
