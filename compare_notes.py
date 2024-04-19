from smith_waterman2 import alignment1, alignment2

def compare_note_groups(linked_notes1, adjusted_note_durations_list2):
    matches = []

    for index, (group1, group2) in enumerate(zip(linked_notes1, adjusted_note_durations_list2)):
        # Check if any note is None
        if group1 is None or group2 is None:
            matches.append("No Match")
        else:
            # Ensure that the lengths of the groups are the same
            if len(group1) != len(group2):
                matches.append("Len. Mismatch")
                continue
            else:
                # Check for pitch match
                if group1[1] != group2[1]:
                    matches.append("Pitch Mismatch")
                else:
                    # Check for duration match
                    if abs(group1[2] - group2[2])>200:
                        matches.append("Dur. Mismatch")
                    else:
                        matches.append("Dur. Match")

    return matches


# Example usage
matches = compare_note_groups(alignment1, alignment2)



# Print the matches
print("_______________")
print(matches)
print("_______________")





