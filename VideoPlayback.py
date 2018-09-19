import datetime
import subprocess
import os, fnmatch

from builtins import print

file = open("Video-seq.txt",'r')
fileInput = file.read()
fileInput = fileInput.strip()

array = fileInput.split(",")

seq = array[0]
date = array[1]
lastSeq = array[2]

lastPlayedDate = datetime.datetime.strptime(date, '%m-%d-%Y')

print('seq: ' + seq)
print('lastSeq: ' + lastSeq)
print(lastPlayedDate)

file.close()

#padding the sequence
def getVideoSeqExp(seq):
    if len(seq) == 1:
        newSeq = '00' + seq + '_*'
    elif len(seq) == 2:
        newSeq = '0' + seq + '_*'
    else:
        newSeq = seq + '_*'
    
    return newSeq

def getVideoPathRegex(seq):
    if int(seq) <= int(lastSeq):
        regex = getVideoSeqExp(seq) + '.MP4'
    elif int(seq) > int(lastSeq):
        seq = '1'
        regex = getVideoSeqExp(seq) + '.MP4'
    print('pattern to search: ' + regex)    
    return regex


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


# print( os.path.exists("C:/Users/Dhruv/Desktop/Motivation/RiseShine.mp4"))
title = []
seqToPlay = int(seq)

while seqToPlay <= (int(lastSeq) + 1):
    regex = getVideoPathRegex(str(seqToPlay))
    print('regex ' + regex)
    title = find(regex, "\\\\RGDDallas\\Video\\Intranet")
    #title = find(regex, "C:\\Users\\Neelabh\\Documents\\RGD")
    print(title)
    if title:
        break
    else:
        seqToPlay = seqToPlay + 1
       
print(title)

todayDate = datetime.datetime.today()
print('Todays Date')
print(todayDate)

if seqToPlay < int(lastSeq):
    nextSeqToSave = seqToPlay
else:
    nextSeqToSave = 1

print('nextSeqToSave ' + str(nextSeqToSave))
if lastPlayedDate.date() != todayDate.date():
    if nextSeqToSave != 1:
        nextSeqToSave = nextSeqToSave + 1

strToFile = str(nextSeqToSave) + ',' + datetime.date.strftime(datetime.date.today(), '%m-%d-%Y') + ',' + lastSeq
print('strToFile: ' + strToFile)

file = open("Video-seq.txt",'w')
file.write(strToFile.strip())
file.close()

if title:
    p = subprocess.Popen(["C:/Program Files (x86)/VideoLAN/VLC/vlc.exe", title])
    #p = subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", title])
