import pathlib
from Tools.tools import load_data_as_lines, load_data, load_data_as_int, timeexecution
from aocd import submit
filepath = pathlib.Path(__file__).parent.resolve()
hand_ranking = {"all_same": [], "four_same":[], "house":[], "three_kind":[], "two_pairs":[], "one_pair":[], "nothing":[]}
card_value_rank = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
def sort_function(value):
    return value[0]
def assign_value(letter):
    if letter.isdigit():
        return int(letter)
    else:
        return card_value_rank[letter]
def check_hand(card: str):
    unique_cards = list(set(list(card)))
    hand = ""
    if len(unique_cards) == 1:
        hand = "all_same"
        values = assign_value(unique_cards[0])
    elif len(unique_cards) == 2:
        if card.count(unique_cards[0]) == 4:
            hand = "four_same"
            values = [assign_value(unique_cards[0]), assign_value(unique_cards[1])]
        elif card.count(unique_cards[1]) == 4:
            hand = "four_same"
            values = [assign_value(unique_cards[1]), assign_value(unique_cards[0])]
        elif card.count(unique_cards[0]) == 3:
            hand = "house"
            values = [assign_value(unique_cards[0]), assign_value(unique_cards[1])]
        elif card.count(unique_cards[1]) == 3:
            hand = "four_same"
            values = [assign_value(unique_cards[0]), assign_value(unique_cards[1])]
    elif len(unique_cards) == 3:
        if card.count(unique_cards[0]) == 3 or card.count(unique_cards[1]) == 3 or card.count(unique_cards[2]) == 3:
            hand = "three_kind"
            if card.count(unique_cards[0]) == 3:
                values = [assign_value(unique_cards[0])] + sorted([assign_value(unique_cards[1]), assign_value(unique_cards[2])], reverse=True)
            elif card.count(unique_cards[1]) == 3:
                values = [assign_value(unique_cards[1])] + sorted([assign_value(unique_cards[0]), assign_value(unique_cards[2])], reverse=True)
            elif card.count(unique_cards[2]) == 3:
                values = [assign_value(unique_cards[2])] + sorted([assign_value(unique_cards[1]), assign_value(unique_cards[0])], reverse=True)
        else:
            hand = "two_pairs"
            if card.count(unique_cards[0]) == 2 and card.count(unique_cards[1]) == 2:
                values = sorted([assign_value(unique_cards[0]), assign_value(unique_cards[1])], reverse=True) + [assign_value(unique_cards[2])]
            elif card.count(unique_cards[0]) == 2 and card.count(unique_cards[2]) == 2:
                values = sorted([assign_value(unique_cards[0]), assign_value(unique_cards[2])], reverse=True) + [assign_value(unique_cards[1])]
            elif card.count(unique_cards[1]) == 2 and card.count(unique_cards[2]) == 2:
                values = sorted([assign_value(unique_cards[1]), assign_value(unique_cards[2])], reverse=True) + [
                    assign_value(unique_cards[0])]
    elif len(unique_cards) == 4:
        hand = "one_pair"
        not_pairs = []
        pair = []
        for i in unique_cards:
            if card.count(i) == 2:
                pair.append(assign_value(i))
            else:
                not_pairs.append(assign_value(i))
        values = pair + sorted(not_pairs, reverse=True)
    else:
        values = []
        for i in unique_cards:
            values.append(assign_value(i))
        hand = "nothing"
        values = sorted(values, reverse=True)
    return hand, values


def get_my_answer():
    data = load_data_as_lines(filepath, example=False)
    cards, ranks = [], []
    total_draws = len(data)
    for draw in data:
        hand, rank = draw.split(" ")
        cards.append(hand)
        hand, values = check_hand(hand)
        hand_ranking[hand].append((values, int(rank)))

    for key, value in hand_ranking.items():
        if value:
            value = sorted(value, key=sort_function, reverse=True)
        hand_ranking[key] = value
    total_sum = 0
    for key in ["all_same", "four_same", "house", "three_kind", "two_pairs", "one_pair", "nothing"]:
        for hand in hand_ranking[key]:
            total_sum += hand[1]*total_draws
            total_draws-=1
    return total_sum



@timeexecution
def execution():
    submit_answer = False
    my_answer = get_my_answer()
    print(my_answer)
    this_day = int(str(filepath).split("\\")[-1][3:])
    if submit_answer:
        submit(my_answer, part="b", day=this_day, year=2023)
