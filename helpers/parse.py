import os, sys
import glob

from slugify import slugify

from pydub import AudioSegment
from pydub.silence import split_on_silence


def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


for d in glob.glob("./words/*Y.mp3"):

    src = os.path.basename(d)
    letter = src.split('.')[2]
    print('Start: ' + letter)
    song = AudioSegment.from_mp3(d)

# Split track where the silence is 2 seconds or more and get chunks using 
# the imported function.
    chunks = split_on_silence (
        # Use the loaded audio.
        song, 
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len = 500,
        keep_silence=650,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = -40
    )

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk
       # audio_chunk =  chunk

        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        # Export the audio chunk with new bitrate.
        print("Exporting {1}_{0}.mp3.".format(i,letter))
        normalized_chunk.export(
            "./words/output/{1}_{0}.mp3".format(i,letter),
            bitrate = "320k",
            format = "mp3"
        )

exit()

# Load your audio.
