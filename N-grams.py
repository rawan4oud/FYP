from preprocessing import main  

if __name__ == "__main__":
    midi_file_path = "Star Wars - The Imperial March [MIDIfind.com].mid"
    string_sequences = main(midi_file_path)

print(string_sequences)