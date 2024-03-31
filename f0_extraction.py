import librosa
import numpy as np
import soundfile as sf

def extract_dominant_notes(audio_file, hop_length=512, frame_length=2048):
    # Load audio file
    y, sr = librosa.load(audio_file)


    # Pitch estimation using librosa's yin algorithm
    f0, voiced_flag, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C1'), fmax=librosa.note_to_hz('C8'),
                                      sr=sr, frame_length=frame_length, hop_length=hop_length)

    # Initialize array to store dominant notes
    dominant_notes = np.zeros_like(f0)

    # Select the most dominant note for each time frame
    for i in range(len(f0)):
        if voiced_flag[i]:  # If the frame is voiced
            dominant_notes[i] = f0[i]

    return dominant_notes

def regenerate_audio(audio_file, dominant_notes, hop_length=512):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Initialize array to store regenerated audio
    regenerated_audio = np.zeros_like(y)

    # Generate regenerated audio using the dominant notes
    for i in range(len(dominant_notes)):
        if dominant_notes[i] != 0:
            t = np.arange(0, hop_length) / sr
            sine_wave = np.sin(2 * np.pi * dominant_notes[i] * t)

            # Insert the sine wave into the regenerated audio array
            start_idx = i * hop_length
            end_idx = min(start_idx + hop_length, len(y))
            regenerated_audio[start_idx:end_idx] = sine_wave[:end_idx - start_idx]

    return regenerated_audio, sr

# Example usage
audio_file = 'Test Files/ok.wav'
dominant_notes = extract_dominant_notes(audio_file)
regenerated_audio, sr = regenerate_audio(audio_file, dominant_notes)

# Save the regenerated audio as a new WAV file
output_file = 'test.wav'
sf.write(output_file, regenerated_audio, sr)

print(f"Regenerated audio saved as {output_file}")
