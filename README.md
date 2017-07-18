## LinuxMusicSync
# Python/Tkinter GUI to sync music from a source to a destination, with encoding by LAME.

Requires Tkinter. Written for Python 2. Also uses os, time, and glob, but you'll probably have those.

Currently, this is a Tkinter GUI which loads a directory structure from a path stipulated by the string variable "external_source," two directories deep (one layer for artists, the other for albums). It will display all directories down these two layers and cross reference them with directories in the string variable "destination." Example directories are provided in the file. Any directories found existing in both the source and destination will be highlighted. The user then selects other directories containing music files (.mp3, .aac, .wav, and .flac are hard coded in, but can be changed) that should be transferred from the source to the destination. 

The code calls os.system (not the recommended way anymore, but it hasn't been changed) with a LAME command to do encoding. If you don't want it to re-encode your files, then you can deselect the box and it should just copy the music files over. If you do want encoding (to reduce file size for your mobile device, perhaps), you can select either constant bit rate (CBR) or variable bit rate (VBR), and stipulate your quality (the options are -b<quality> for CBR and -V<quality> for VBR, with some comments given on selection in the file). It will then call LAME <http://lame.sourceforge.net/>, which must be on your PATH, or you can change the command in the code to point to a specific location for the LAME executable. 

The script has been checked with file names with UTF-8 encoding, but I have had some errors with other encodings and simply found it easier to change filenames than fiddle with the code. 

If you deselect a directory, it will be deleted from the destination. The code won't touch the source.

There is also multithreading, if you switch the boolean on line 4 to true, set to run on 4 threads. If you have trouble, turn it off, as it is by default. 

I just wrote this today because I had trouble with the Windows-based syncing solution that I had been using previously for the SD card on my Android phone. If I need more features in the future, I may update this, but otherwise, it will likely not be updated or maintained very often (if ever).
