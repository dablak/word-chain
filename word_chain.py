"""
Aberdeen Python dojo of 26th November 2014

@author: Daniel Blasco
"""


def read_words_from_file(file_path):
    words = []
    with file(file_path, 'r') as all_words:
        for word in all_words:
            word = word.strip()

            # To make the problem more simple, we just use three characters words
            if len(word) == 3:
                words.append(word)

    return words


def word_distance(word1, word2):
    # Only works with words of the same distance
    distance = 0
    for i in xrange(len(word1)):
        if word1[i] != word2[i]:
            distance += 1

    return distance


def create_neighbours_graph(words):
    """ Creates a graph where the neighbours of each word are other words with a distance of 1.
        Returns a dictionary like:
        {
            "dog": ["cog", "doc"],
            "cog": ["dog"],
            "cot": ["cat", "cog"],
            "doc": ["dog"],
            "cat": ["cot"],
        }
    """
    words_graph = {}
    for word in words:
        neighbours = set()  # use a set to avoid duplicated
        for neighbour in words:
            if word_distance(word, neighbour) == 1:
                neighbours.add(neighbour)

        words_graph[word] = neighbours

    return words_graph


def find_word_chain(from_word, to_word, words_graph, parcial_chain=None):
    """ With brute force and recursively find a path from from_word to to_word.
        This is not the most efficient way and it doesn't find the shortest path.

        :param from_word: The starting word
        :param to_word: The last word of the chain
        :param words_graph: a dictionary where the keys are the words and the values are their 1-distance neighbours
        :param parcial_chain: The chain found until now
        :return: A word chain between from_word and to_word
    """
    if parcial_chain is None:
        parcial_chain_copy = []
    else:
        # We need to make a copy of parcial_chain because parcial_chain is shared between
        # calls and we only want to mute it differently in each ramification of the algorithm
        parcial_chain_copy = parcial_chain[:]

    # Keep track of the current step
    parcial_chain_copy.append(from_word)
    word_chain = []
    neighbours = words_graph[from_word]
    if to_word in neighbours:
        # If we reach the 'to_word' then we have finished searching
        word_chain.append(to_word)
    else:
        for neighbour in neighbours:
            if neighbour in parcial_chain_copy:
                continue  # Avoid loops in the graph

            # Find chains from the neighbours of 'from_ford to 'to_word'
            word_subchain = find_word_chain(neighbour, to_word, words_graph, parcial_chain_copy)
            if to_word in word_subchain:
                word_chain = word_subchain
                break

    # Prepend from_word to the solution
    word_chain.insert(0, from_word)
    return word_chain


def main(from_word, to_word):
    print "Word chain from {} to {}".format(from_word, to_word)

    words_file_path = "words.txt"
    words = read_words_from_file(words_file_path)
    words_graph = create_neighbours_graph(words)
    word_chain = find_word_chain(from_word, to_word, words_graph)
    print word_chain


if __name__ == "__main__":
    main("cat", "dog")