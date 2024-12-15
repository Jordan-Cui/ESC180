import math

def cosine_similarity(vec1, vec2):

    if vec1 == {} or vec2 == {}:
        return -1
    
    numerator = 0
    vec1sum = 0
    vec2sum = 0

    for i in vec1:
        if i in vec2:
            numerator += vec1[i]*vec2[i]
        vec1sum += vec1[i] ** 2
    
    for i in vec2:
        vec2sum += vec2[i] ** 2
    
    return numerator/math.sqrt(vec1sum * vec2sum)

def addDicts(dict1, dict2):
    if len(dict1) < len(dict2):
        for i in dict1:
            if i in dict2:
                dict2[i] += dict1[i]
            else:
                dict2[i] = dict1[i]
        return dict2
    for i in dict2:
        if i in dict1:
            dict1[i] += dict2[i]
        else:
            dict1[i] = dict2[i]
    return dict1

def build_semantic_descriptors(sentences):
    semantic_descriptors = {}

    for i in sentences:
        words = {}
        for j in i:
            if not j in words:
                words[j] = 1
        
        for j in words:
            newwords = words.copy()
            del newwords[j]
            
            #add to semantic descriptors
            if not j in semantic_descriptors:
                semantic_descriptors[j] = newwords
            else:
                semantic_descriptors[j] = addDicts(semantic_descriptors[j], newwords)
    
    return semantic_descriptors


def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for file in filenames:
        f = open(file, "r", encoding="latin1")
        text = f.read()
        f.close()

        word = ""
        sentence = []
        for char in text:
            if char in [",", "-", ":", ";", "\n", "\t"]:
                continue
            if char in [".", "!", "?", " "]:
                if word != "":
                    sentence.append(word)
                    word = ""
            else:
                word += char.lower()
            if char in [".", "!", "?"] and sentence != []:
                sentences.append(sentence)
                sentence = []
        
        if sentence != []:
            sentences.append(sentence)


    return build_semantic_descriptors(sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    maxScore = -1
    maxChoice = choices[0]
    if not word in semantic_descriptors:
        return maxChoice

    for i in choices:
        if not i in semantic_descriptors:
            continue
        score = similarity_fn(semantic_descriptors[word], semantic_descriptors[i])
        if score > maxScore:
            maxScore = score
            maxChoice = i
    
    return maxChoice


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file = open(filename, 'r')
    countCorrect = 0
    countLine = 0
    for line in file:
        countLine += 1
        line = line.strip().split()
        word = line[0]
        answer = line[1]
        choices = line[2:]

        if answer == most_similar_word(word, choices, semantic_descriptors, similarity_fn):
            countCorrect += 1

    file.close()
    return countCorrect/countLine * 100


# if __name__ == "__main__":
#     semantic_descriptors = build_semantic_descriptors_from_files(["war.txt", "swan.txt"])
#     print(run_similarity_test("test.txt", semantic_descriptors, cosine_similarity))

