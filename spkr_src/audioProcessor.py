__author__ = 'hafiz'
from scikits.audiolab import sndfile
from contextlib import closing
import matplotlib.pyplot as plt
import numpy as np
from scikits.talkbox import segment_axis
from scikits.audiolab import wavread
from sigtools.aubio_pitch import *

class AudioProcessor:
    # nframes = None
    # samplerate = None
    # channels = None
    def __init__(self,filename):
        self.filename = filename
        # inf = self.get_audioinfo(filename)
        # if inf is not None:
        #     self.nframes = inf['nframes']
        #     self.samplerate = inf['samplerate']
        #     self.channels = inf['channels']

    def set_filename(self,filename):
        self.filename = filename
        inf = self.get_audioinfo(filename)
        if inf is not None:
            self.nframes = inf['nframes']
            self.samplerate = inf['samplerate']
            self.channels = inf['channels']

    def get_samplerate(self):
        return self.samplerate

    def get_audioinfo(self,filename):
        import wave
        w = wave.open(filename,'r')
        # with closing wave.open(filename,'r') as f:
        info = {}
        info['nframes'] = w.getnframes()
        info['samplerate'] = w.getframerate()
        info['channels'] = w.getnchannels()
        w.close()
        return  info


    # def set_filelname(self,filename):
    #     self.filename = filename

    def make_frames(self,signal,fs,frame_duration,overlap=0.5):
        nsamples_pframe = fs*frame_duration/1000
        overlapframes = nsamples_pframe * overlap
        frames = segment_axis(signal,nsamples_pframe,overlapframes)
        return frames


    def parse_audio_w(self):
        """

        """
        # data: raw audio data
        # fs: sample rate
        sig, fs = wavread(self.filename)[:2]

        return sig
    def parse_audio(self):
        """

        """
        with closing(sndfile(self.filename)) as f:
            # print("sampling rate = {} Hz \nlength = {} samples\nchannels = {}\nencoding={}\nendianness={}\n".format(f.get_samplerate(), f.get_nframes(), f.get_channels(),f.get_encoding(),f.get_endianness()))

            sig = f.read_frames(f.get_nframes())

            # self.plot_time_domain_signal(sig)
            # plt.plot(sig)
            # plt.show()
            return sig,f.get_samplerate(),f.get_channels()

    def make_rawaudio_segment(self,seg_time=1):
        '''
        make audio segments each of which is length 1s, 2s, 3s, .... 10s.
        '''
        samplerate = 0
        stack = np.array(())
        with closing(sndfile(self.filename)) as f:
            fs  = f.get_samplerate() #number of samples in 1 second
            samplerate = fs
            num_samples = fs * seg_time # i th seconds total number samples
            nframes = f.get_nframes()

            j=0
            if num_samples < nframes:
                while j < nframes:
                    if num_samples < (nframes - j) :
                        samples = f.read_frames(num_samples)


                        if j==0:
                            stack = np.column_stack(np.array(samples)).T

                        else:
                            stack = np.column_stack((stack,np.array(samples)))
                        j = j + num_samples
                    else:
                        samples = f.read_frames(nframes - j)
                        # stack = np.column_stack((stack,samples))
                        j = j + num_samples
            else:
                samples = f.read_frames(nframes)
                stack = np.column_stack((samples))
        return stack,samplerate

    def pitchbased_preprocessing(self,config):

        slen = config.min_segment_length

        minvar = 9999
        maxnsegment = -9999

        self.segmentset = []
        self.pichset = []
        self.genderset = []
        self.segment_length = -1

        self.step = config.segmentlength_step
        self.maxseglen = config.max_segment_length
        self.segment_sample_set = np.array([])
        while slen <= self.maxseglen:
            obj_pitch = Pitch(self.filename,int(self.samplerate),slen,slen/2.0)
            segments,pitches,confidences,var,covar, nseg,genders,seg_samples = obj_pitch.get_pitch()
            # print '###########################################'
            # print 'segment length::'
            # print slen
            # print 'number of segment::'
            # print nseg
            # print 'segments::'
            # print segments
            # print 'pitches::'
            # print pitches
            # print 'variance and covariance::'
            # print var
            # print covar
            # print 'confidence score:'
            # print confidences


            if var==minvar and nseg > maxnsegment:
                maxnsegment = nseg
                self.segmentset = segments
                self.pichset = pitches
                self.segment_length = slen
                self.genderset = genders
                self.segment_sample_set = seg_samples
            elif var < minvar:
                minvar = var
                maxnsegment = nseg
                self.segmentset = segments
                self.pichset = pitches
                self.segment_length = slen
                self.genderset = genders
                self.segment_sample_set = seg_samples
            slen +=self.step

        print '#######################################'
        print 'selected segments::'
        print self.segmentset
        print 'segment length::'
        print self.segment_length
        print "genders::"
        print self.genderset
        print 'pitches::'
        print self.pichset
        # print 'seg_samples shape'
        # print self.segment_sample_set.shape
        return self.segment_length,self.segmentset,self.pichset,self.genderset,self.segment_sample_set



if __name__ == '__main__':
    ap = AudioProcessor()
    stack = ap.make_rawaudio_segment(1)
    sig,fs = ap.parse_audio()
    # mfc = mfcc(sig,nwin=400)
    # from mfccTool.mfcc  import *
    # m = mfcc(stack)
    print stack.shape

    # nwin = 32
    #
    # print nfft
    # mfcc(audio, nwin=256, nfft=512, fs=8000, nceps=13)
    # print mfc.shape
    #mfcc(input, nwin=256, nfft=512, fs=16000, nceps=13):
    # print (stack.shape)
    row,col = stack.shape
    str = 0
    # plt.plot(stack.T)
    # plt.show()
    # segment = stack[:,str]
    # frames = segment_axis(segment,320,160) # 20 ms each frames with 50% overlap with 16000sampling rate
    # frames = frames.T
    #
    # print segment.shape
    # print frames.shape
    # while (str<col):
    #
    #
    #     plt.plot((stack[:,str]))
    #
    #     plt.show()
    #     str = str + 1
    #     if str == 1:
    #         break;
