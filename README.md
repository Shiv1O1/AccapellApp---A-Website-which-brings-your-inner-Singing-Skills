# AcapellaApp
Website for singers to record voice, combine with background music, compare with original song with engaging visualizers and many more

Music plays a central role in the entertainment industry and is a major form of artistic expression. Since today's era of internet and digitization has led to a revolution in the way music reaches its audience, there are still many things which can be improved with respect to the ways in which people interact with musical content. The ability of interacting with different parts of music (e.g. the vocals and music) would enable diverse applications such as separation of vocals and music, mixing of music and vocals and comparison of voices of different singers. 
So, the main aim is to design an end to end web application which enables its users to perform all sorts of interactive actions like audio voice separation, record their voice,combine voice with music, voice comparison and visualization.
# Related Work
There have been various previous approaches related to this, some of them are used to separate music from vocals, some are used for visualizations, some are used to record your voice and then combine it with music
There are websites like splitter.ai, vocalremover.com, remove-vocals.com to separate vocals from music. Smule, StarMaker all these android apps are available for music vocal combiners. Staella, Audio Glow Music Visualizer, Muviz Edge are available for music visualization
But none of these provide every feature we do. We even added a new feature comparison of user vocals with singer vocals in our website

# Technologies Used
![aa](https://user-images.githubusercontent.com/49364681/86735738-a10b2400-c050-11ea-8cd2-ecfd8219d3b6.png)

# Architecture of System - User Interaction
![archi](https://user-images.githubusercontent.com/49364681/86736295-08c16f00-c051-11ea-9292-ce4ae0e2af7e.png)

# Voice Music Separator:
Separating vocals and music is an important task to compare user voice with singer vocals or combine user song with background music. To split vocals and background music, we used spleeter which is an open source AI, specially designed to separate audio tracks known as stems.
Spleeter is a simple tool to use and user-friendly. To know more information about spleeter click here. Spleeter can be implemented through the command line:
                                       
                                       spleeter separate -i audioexample.mp3 -o output
                                       
The software takes this audio file "audioexample.mp3" and later splits it into two stems containing vocals and music. These two stems are stored in folder named "output" in '.wav' format. These files are named as vocals and accompaniment for storing vocals and music stems respectively.
Spleeter may not give 100% results but produces better results. It is computationally expensive for songs with great time length on the website. It took nearly 1min 4sec to split a song with run length 4min 47sec. If a song is about 6 or 7 minutes, time taken to split the song is expensive.
So a user who wishes to combine his vocals with music, needs to upload his song and wait until the song is divided into music and vocals every time. So the better solution to this problem is to save the original song, vocals, music so that the user can use these files whenever he wishes
# Saving a File
On the website, to save audio, vocals, music a model named file is created. So the user whoever wants to save his file needs to provide a name, and set a Boolean field privacy to True or False. So if the privacy field is set False, any user can have access to these files and if privacy field is set True, only the user who saved the files can have to these files
# Recording Voice
On the website, a recorder is placed so that the user can record his voice. While voice is recorded, background music is played, so the user can sing his song according to the music
# Combining Vocals and Music:
Two audio segments can be combined with following code:
from pydub import AudioSegment

                            sound1 = AudioSegment.from_file("/path/to/accompaniment.wav")
                            sound2 = AudioSegment.from_file("/path/to/recordedvoice.wav")
                            combined = sound1.overlay(sound2)
                            combined.export("/path/to/combined.wav", format='wav')

Here sound1.overlay(sound2) overlays recorded voice over accompaniment file and this combined sound is saved in '.wav' format.
# Comparing two voices:
Two voices are compared by plotting one on another across time vs amplitude so that user can understand difference between amplitudes over time. By placing recorder voice over singer vocals, we can understand difference between their voices(amplitudes) over time
# Visualization
Visualization is done by using languages like HTML5, CSS3 and JavaScript. FFT method is used for Visualization. For single bar visualization we used a fixed position in fillRect function of canvas. For Multiple bars visualization we used multiple positions in a canvas. For Circular multiple bars visualization we changed the path of canvas from straight line to circle and further part was the same as for multiple bars visualization

# Future Scope:
As discussed spleeter doesn't produce 100% results and takes too much time for voice music separation on the website. So one can work on reduction of time required for music voice separation and improve separation results
Moreover this work can be extended by developing an android app for the same purpose.
# Conclusion
Thus the website discussed above helps the singer to split a song into vocals and music, record voice, combine his voice with background music, compare his voice with singer voice and many more.

