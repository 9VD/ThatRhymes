from flask import Flask, render_template, request, flash

app = Flask(__name__)

def file_reader(pfile):
    '''
    Reads the file inputed and places the words in a dictonary mapped to all
    it's possible phonemes.
    Parameters: 
            fname -- The name of the file that gets read
    Returns: 
            rhyme_dict -- A dictionary with the values being a list of lists
    '''
    rhyme_file = open(pfile, 'r')
    rhyme_list = []
    rhyme_dict = {}
    # The loop below splits the lines whitespaces 
    # in a file and places them into a list
    for line in rhyme_file:
        rhyme_list.append(line.split())
    # This loop below takes rhyme_list and parces through it in order
    # to turn it into a dictionary with the first element being the key 
    for line in rhyme_list:
        if line[0] in rhyme_dict:
            rhyme_dict[line[0]].append(line[1:])
        else:
            rhyme_dict[line[0]] = [line[1:]]
    return rhyme_dict

rhyme_dict = file_reader("PronunciationDictionary.txt")

def get_phonemes(word, rhyme_dict):
    '''
    Takes the word inputed and returns the location/index 
    of where the primary stress syllables are.
    Parameters: 
            word -- The word that is inputed by the user. Used to find rhymes
            rhyme_dict -- A dictionary with the values being a list of lists
    Returns: 
            stress_i -- a list of integers which are 
            the indexes of the primary stress syllables
            in the mulitple pronunciations of the word inputed
    '''
    if word == '':
        return["Results..."]
    elif word not in rhyme_dict.keys():
        return["Word not recognized"]
    stress_i = []
    # The for loop below checks if the elemnt in the list
    # is a primary stress phoneme by checkign the last character 
    # and placing the locations (indexes) into a list
    for line in rhyme_dict[word]:
        for phoneme in line:
            if phoneme[-1] == "1":
                stress_i.append(line.index(phoneme))
    return stress_i

def get_rhyming_words(word, rhyme_dict, stress_i):
    '''
    Reads the file inputed and
    Parameters: 
            word -- The word that is inputed by the user. Used to find rhymes
            rhyme_dict -- A dictionary with the values being a list of lists
            stress_i -- a list of integers which are 
            the indexes of the primary stress syllables
            in the mulitple pronunciations of the word inputed
    Returns: 
            rhyming_words -- An unsorted list of all the 
            words that are rhymes with "word"
            
    '''
    if word == '':
        return ["Results..."]
    elif word not in rhyme_dict.keys():
        return["Word not recognized"]
    rhyming_words = []
    i = 0
    # The outer loop goes through the different pronunciations
    # while the three inner loops go through the dictinoary since
    # it's a dictinoary of a 2d list, it needs 3 loops
    for phonemes in rhyme_dict[word]:
        for key in rhyme_dict:
            for line in rhyme_dict[key]:
                for phoneme in line:
                    if phoneme[-1] == "1":
                        stress_index = line.index(phoneme)                      
                        if line[stress_index - 1] != phonemes[stress_i[i] - 1]:
                            if line[stress_index:] == phonemes[stress_i[i]:]:
                                rhyming_words.append(key.title())

        i += 1
    return rhyming_words

rhyming_words = ["Results..."]

@app.route("/")
def index():
    return render_template("index.html", rhyming_words=rhyming_words)

@app.route("/rhymes", methods=["POST","GET"])
def rhymes():
    stress_i = get_phonemes(str(request.form.get('word')).upper(), rhyme_dict)
    rhyming_words = get_rhyming_words(str(request.form.get('word')).upper(), rhyme_dict, stress_i)
    return render_template("index.html", rhyming_words=rhyming_words)

if __name__ == '__main__':
    app.run(debug=True, port=8000)



