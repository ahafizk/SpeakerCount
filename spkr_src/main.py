#! /usr/bin/env python
__author__ = 'hafiz'

from audioProcessor import *
from ConfigReader import  *
# from sigtools.mfcc import *
from speakerCounter import *
# from sigtools.yin_pitch import Yin
# from aubio import pitch
from sigtools.ste import *
def get_files():
    from os.path import isfile, join
    from os import listdir
    import wave as w
    path = 'audio_dir/'
    files = [ f for f in listdir(path) if isfile(join(path,f)) ]
    return files
def process():
    config = ConfigReader()
    config.read_config()  #read the configuration file
    ap = AudioProcessor(config.fullfilename)
    file_list = get_files()
    # print config.audio_dir
    # print file_list
    # f = open('output.txt','a')
    th_list= [10,15,20,25,30]
    th_list= [15]
    for th in th_list:
        for file in file_list:
            filename = config.audio_dir + file
            print 'start processing: '+str(file)
            ap.set_filename(filename)
            fs = ap.get_samplerate()

            segment_length,segmentsetidx,pichset,genderset,segment_sample_set = ap.pitchbased_preprocessing(config)
            sc = SpeakerCounter(fs,segment_length,segmentsetidx,pichset,genderset,segment_sample_set )
            sc.set_threshold(th)
            count = sc.get_people_count()
            # out ="# people in ("+str(file)+") :: "+str(count)+'\n'

            ac = 4
            erc = abs(ac - count)
            print [str(file), str(count),  str(ac), str(erc), str(th)]
            # f.write(out)

            # print out
    # f.close()
if __name__=='__main1__':
    process()

if __name__=='__main__':


    config = ConfigReader()
    config.read_config()  #read the configuration file
    ap = AudioProcessor(config.fullfilename)
    ap.set_filename(config.fullfilename)
    fs = ap.get_samplerate()
    # sig,fs,chnl = ap.parse_audio()
    segment_length,segmentsetidx,pichset,genderset,segment_sample_set = ap.pitchbased_preprocessing(config)
    

    sc = SpeakerCounter(fs,segment_length,segmentsetidx,pichset,genderset,segment_sample_set )
    sc.set_threshold(15)
    c= sc.get_people_count()
    print c

