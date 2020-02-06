__author__ = 'hafiz'
import ConfigParser as confParser


class ConfigReader():

    #global class variables
    audio_dir = ''
    filename = ''
    fextension = ''
    segment_length = None
    frame_length = None
    overlap_frame_length = None
    nmfcc_coefficients = None
    naudio_file_process = None
    fullfilename = ''
    min_segment_length = None
    max_segment_length = None
    segmentlength_step = None
    pitch_tolerance = None

    def __init__(self):
        self.filename = 'config.cfg'
        # print 'config reader'

    def read_config(self):
        config = confParser.ConfigParser()
        config.read(self.filename)
        # print config
        # print self.filename
        sections = config.sections()
        # sec = sections
        # print sections[0]
        self.audio_dir = str(config.get(sections[0],'AudioDirectory'))
        self.filename = str(config.get(sections[0],'FileName'))
        self.fextension = str(config.get(sections[0],'FileExtension'))
        self.segment_length = float(config.get(sections[0],'SegmentLength'))
        self.frame_length = float(config.get(sections[0],'FrameLength'))
        self.overlap_frame_length = float(config.get(sections[0],'OverlapFrameLength'))
        self.nmfcc_coefficients = int(config.get(sections[0],'MfccCoefficients'))
        self.naudio_file_process = int(config.get(sections[0],'NumberOfAudioFileProcess'))
        self.fullfilename = self.audio_dir+self.filename+"."+self.fextension
        self.min_segment_length = float(config.get(sections[0],'MinSegmentLength'))
        self.max_segment_length = float(config.get(sections[0],'MaxSegmentLength'))
        self.segmentlength_step = float(config.get(sections[0],'SegmentLengthStep'))
        self.pitch_tolerance = float(config.get(sections[0],'PitchTolerance'))

        return config



if __name__ =='__main__':
    reader = ConfigReader()
    reader.read_config()
    print reader.audio_dir