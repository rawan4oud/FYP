def count_similar_elements(list1, list2):
    count = 0
    for item1, item2 in zip(list1, list2):
        if isinstance(item1, tuple) and isinstance(item2, tuple):
            if item1 == item2:
                count += 1
        elif item1 == item2:
            count += 1
    return count

list1 = ['No Match', 'Match', 'Match', 'Match', 'Match', 'Match', 'Match', 'No Match', 'Match', 'Match', 'No Match', 'Match', ('Pitch Match', 'Duration Mismatch'), 'Match', 'Match', 'No Match', 'Match', 'No Match', ('Pitch Match', 'Duration Mismatch'), ('Pitch Match', 'Duration Mismatch'), 'Match']
list2 = ['No Match', 'Match', 'Match', 'Match', 'Match', 'Match', 'Match', 'No Match', 'Match', 'Match', 'No Match', 'Match', ('Pitch Match', 'Duration Mismatch'), 'Match', 'Match', 'No Match', 'Match', 'No Match', ('Pitch Match', 'Duration Mismatch'), ('Pitch Match', 'Duration Mismatch'), 'Match']
print(count_similar_elements(list1, list2), " Out of: ", len(list1))