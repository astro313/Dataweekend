"""

The unnecessary words to remove are "a", "be", "to", "the", "that", "this", "or"


"""

def remove_end_words(inphrase):

    import copy

    endwords = ["a", "be", "to", "the", "that", "this", "or"]

    a = inphrase.split(' ')
    b = copy.deepcopy(a)

    for ind, word in enumerate(b):
        if word.lower() in endwords:
            a.remove(word)

    a = ' '.join(a)

    return a

inphrase = "To be or not to be - that is the question: Whether it is nobler in the mind to suffer"

assert remove_end_words(inphrase) ==  "not - is question: Whether it is nobler in mind suffer"


inphrase = "the slings and arrows of outrageous fortune. Or to take up arms against a sea of troubles, and by opposing end them"
remove_end_words(inphrase)



