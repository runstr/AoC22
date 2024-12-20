import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
import functools

filepath = pathlib.Path(__file__).parent.resolve()

def get_my_answer():
    @functools.cache
    def check_word(word):
        if not word:
            return True
        if word[0] in patterns:
            test_patterns = patterns[word[0]]
        else:
            return False
        for pattern in test_patterns:
            if word.startswith(pattern):
                if check_word(word[len(pattern):]):
                    return True
        return False

    data = load_data(filepath, example=False)
    a, b = data.split("\n\n")
    patterns = {}
    for i in a.split(", "):
        try:
            patterns[i[0]].append(i)
        except:
            patterns[i[0]] = [i]
    all_words = []
    list_words = b.split("\n")
    for word in list_words:
        if check_word(word):
            all_words.append(word)
    print(len(all_words))



@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="a", day=this_day, year=2024)
