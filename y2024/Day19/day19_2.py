import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
import functools

def get_my_answer():
    all_words = [0]
    @functools.cache
    def check_word(word):
        if word == "":
            return 1
        if word[0] in patterns:
            test_patterns = patterns[word[0]]
        else:
            return False
        ans=0
        for pattern in test_patterns:
            if word.startswith(pattern):
                ans += check_word(word[len(pattern):])


        return ans

    data = load_data(filepath, example=False)
    a, b = data.split("\n\n")
    patterns = {}
    for i in a.split(", "):
        try:
            patterns[i[0]].append(i)
        except:
            patterns[i[0]] = [i]

    list_words = b.split("\n")
    all_words=0
    for word in list_words:
        all_words+= check_word(word)
    return all_words


@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2024)
