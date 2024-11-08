from pydub import AudioSegment
import os

# Folder path where all your .m4a files are stored
input_folder = 'C:/Users/hp/Desktop/New folder'
output_folder = 'C:/Renan/Speaker'

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.wav')

    # Process .m4a files
    if filename.endswith('.m4a'):
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(22050)  # Set sample rate to 22050 Hz
        audio.export(output_path, format="wav")
        print(f"Converted {filename} to {output_path} with 22050 Hz sample rate")

    if filename.endswith('.mp4'):
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(22050)  # Set sample rate to 22050 Hz
        audio.export(output_path, format="wav")
        print(f"Converted {filename} to {output_path} with 22050 Hz sample rate")
    
    # Process .wav files
    elif filename.endswith('.wav'):
        audio = AudioSegment.from_file(input_path)
        # Check if the sample rate is already 22050 Hz
        if audio.frame_rate != 22050:
            audio = audio.set_frame_rate(22050)  # Resample if needed
        audio.export(output_path, format="wav")
        print(f"Exported {filename} to {output_path} with 22050 Hz sample rate")

print("All files have been processed.")
