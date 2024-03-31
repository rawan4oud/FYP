from pydub import AudioSegment
import noisereduce as nr
import librosa
import soundfile as sf


# Load the audio file
audio_file_path = 'Test Files/file_example_WAV_1MG.wav'
audio = AudioSegment.from_file(audio_file_path)

# Amplify the audio
amplified_audio = audio + 6

# Normalize the amplified audio
normalized_audio = amplified_audio.normalize()

# Export the amplified and normalized audio
amplified_audio.export("amplified_audio.wav", format="wav")
normalized_audio.export("normalized_audio.wav", format="wav")

# Load an audio file (librosa loads audio files as floating point time series)
y, sr = librosa.load(audio_file_path, sr=None)  # sr=None ensures the original sampling rate is used

# Perform noise reduction without providing a specific noise clip
# This will let noisereduce attempt to automatically estimate the noise profile from the audio clip
reduced_noise_audio = nr.reduce_noise(y=y, sr=sr)

# Save the noise-reduced audio to a new file
output_file_path = 'cleaned_audio.wav'
sf.write(output_file_path, reduced_noise_audio, sr)
