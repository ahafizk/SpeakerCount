__author__ = 'hafiz'
#speaker counter algorithm goes here
import numpy as np
from sigtools.mfcc import *
from sigtools.rms import *
from sigtools.yin import *
# from sigtools.yin_pitch import *
from sigtools.sigutility import *
from distances import *
from draw.cplot import CustomPlot
from sets import Set
from sigtools.ste import *
class SpeakerCounter():

    def __init__(self,fs, segment_length,segmentsetidx,pichset,genderset,segment_sample_set):
        self.segment_length = segment_length
        self.segment_set = segment_sample_set
        self.seg_idx_set = np.array(segmentsetidx)
        self.pitch_set = np.array(pichset)
        self.gender_set = np.array(genderset)
        self.fs = fs
        self.dist = Distance()
        self.threshold = 15
    def set_threshold(self,th):
        self.threshold = th
    def determine_people(self,segment_set):
        mseg = segment_set.shape[0] #take the rows number
        print mseg
        angles = []
        for i in range(mseg):
            sig = segment_set[i]
            ceps,frames,mspec = mfcc(sig,self.fs,0.032,0.016,20,45)
            rms_val = rms(frames) #each row contains single rms value for single frame
            st = get_ste(frames)
            idx = np.where(rms_val > 0.0015)

            ceps = ceps[idx] #filterred ceps
            frames = frames[idx] # filterred frames
            row,col = ceps.shape

            theta = self.dist.cosine_distance(ceps)
            angles +=[theta]
        angles = np.array(angles)

        angles = np.sort(angles) #sorted array
        idx= np.where(angles!=-1)
        angles = angles[idx]
        count = 0
        print angles
        r = angles.shape[0]
        if r>0:
            count = 1
            if r>1:
                for i in range(r)[1:]:
                    if abs(angles[i]- angles[i-1])>6.500001: #5 #6.000001
                        count +=1
        return  count

    def estimate_people_count1(self,segment_set): #most recent added function 9-9-14
        mseg = segment_set.shape[0] #take the rows number
        angles = []
        for i in range(mseg):
            sig = segment_set[i]
            ceps,frames,mspec = mfcc(sig,self.fs,0.032,0.016,20,45)
            rms_val = rms(frames) #each row contains single rms value for single frame
            st = get_ste(frames)
            idx = np.where(rms_val > 0.0015)

            ceps = ceps[idx] #filterred ceps
            frames = frames[idx] # filterred frames
            row,col = ceps.shape

            theta = self.dist.cosine_distance(ceps)
            angles +=[theta]
        angles = np.array(angles)

        angles = np.sort(angles) #sorted array
        idx= np.where(angles!=-1)
        angles = angles[idx]
        count = 0
        print angles
        r = angles.shape[0]
        if r>0:
            count = 1
            if r>1:
                for i in range(r)[1:]:
                    if abs(angles[i]- angles[i-1])>6.500001: #5 #6.000001
                        count +=1
        return  count

    def calculate_mean(self,data):
        if (len(data.shape)==1):
            data_mean = data
        else:
            data_mean = np.mean(data,axis=0)
        return data_mean




    def estimate_people_count3(self,segment_set): #most recent added function 20-9-14
        mseg = segment_set.shape[0] #take the rows number
        angles = []
        marked_list = []
        similar_person =Set([])
        found = False
        mfcc_set = []

        for i in range(mseg):
            sig = segment_set[i]
            ceps,frames,mspec = mfcc(sig,self.fs,0.032,0.016,20,45)
            rms_val = rms(frames)
            # idx = np.where(rms_val > 0.0015)
            # ceps = ceps[idx]
            # frames = frames[idx]
            # row,col = ceps.shape
            # if row < 4:
            #     continue

            ceps_mean = self.calculate_mean(ceps)
            # print ceps.shape
            mfcc_set +=[ceps_mean]

        mfcc_set  = np.array(mfcc_set)
        similar_person = Set([])
        # print mfcc_set.shape
        mseg,col = mfcc_set.shape
        for i in range(mseg):
            mfc1 = mfcc_set[i]
            s = [i]
            for j in range(mseg)[(i+1):]:
                mfc2 = mfcc_set[j]
                theta = self.dist.cosine_distancebetween_segment(mfc1,mfc2)

                if theta<=self.threshold:
                    s.append(j)
            # print Set(s)
            if len(similar_person)==0 and len(s)>=1:
                similar_person.add(Set(s))
            else:
                added = False
                st = Set(s)
                temp = Set([])
                for s1 in similar_person:
                    if len(st.intersection(s1))>0:
                        st.union_update(s1)
                        added = True
                        # break;
                        temp.add(st)
                    else:
                        temp.add(s1)

                    # else: #different list
                #if not added previously in the list now add it to the set
                similar_person = temp
                if added==False:
                    if (len(s)>=1):
                        similar_person.add(st)
        # print similar_person

        return len(similar_person)


    def estimate_people_count_latest(self,segment_set): #most recent added function 9-9-14
        mseg = segment_set.shape[0] #take the rows number
        angles = []
        marked_list = []
        similar_person =Set([])
        found = False
        mfcc_set = []

        for i in range(mseg):
            sig = segment_set[i]
            ceps,frames,mspec = mfcc(sig,self.fs,0.032,0.016,20,45)
            rms_val = rms(frames)
            # idx = np.where(rms_val > 0.0015)
            # ceps = ceps[idx]
            # frames = frames[idx]
            # row,col = ceps.shape
            # if row < 4:
            #     continue

            ceps_mean = self.calculate_mean(ceps)
            # print ceps.shape
            mfcc_set +=[ceps_mean]

        mfcc_set  = np.array(mfcc_set)
        similar_person = Set([])
        # print mfcc_set.shape
        mseg,col = mfcc_set.shape
        people_count = 0
        marked_list = []
        for i in range(mseg):
            mfc1 = mfcc_set[i]

            if i in marked_list:
                continue
            else:
                marked_list.append(i) # already visited

                for j in range(mseg)[(i+1):]:
                    if j in marked_list:
                        continue
                    else:

                        mfc2 = mfcc_set[j]
                        theta = self.dist.cosine_distancebetween_segment(mfc1,mfc2)

                        if theta<=15:
                            marked_list.append(j)
                            # merge two mfcc
                            l = [mfc1.tolist(),mfc2.tolist()]
                            mfc1 = np.mean(l,axis=0)
                        elif theta>15 and theta<30:
                            marked_list.append(j)
                people_count +=1


        return people_count

    def estimate_people_count2(self,segment_set): #most recent added function 9-9-14
        mseg = segment_set.shape[0] #take the rows number
        angles = []
        marked_list = []
        similar_person =Set([])
        found = False
        mfcc_set = []

        for i in range(mseg):
            sig = segment_set[i]
            ceps,frames,mspec = mfcc(sig,self.fs,0.032,0.016,20,45)


            ceps_mean = self.calculate_mean(ceps)
            # print ceps.shape
            mfcc_set +=[ceps_mean]

        mfcc_set  = np.array(mfcc_set)
        similar_person = Set([])
        # print mfcc_set.shape
        mseg,col = mfcc_set.shape
        for i in range(mseg):
            mfc1 = mfcc_set[i]
            s = [i]
            for j in range(mseg)[(i+1):]:
                mfc2 = mfcc_set[j]
                theta = self.dist.cosine_distancebetween_segment(mfc1,mfc2)

                if theta<=self.threshold:
                    s.append(j)
            # print Set(s)
            if len(similar_person)==0 and len(s)>1:
                similar_person.add(Set(s))
            else:
                added = False
                st = Set(s)
                temp = Set([])
                for s1 in similar_person:
                    if len(st.intersection(s1))>0:
                        st.union_update(s1)
                        added = True
                        # break;
                        temp.add(st)
                    else:
                        temp.add(s1)

                    # else: #different list
                #if not added previously in the list now add it to the set
                similar_person = temp
                if added==False:
                    if (len(s)>1):
                        similar_person.add(st)
        # print similar_person

        return len(similar_person)


    def get_people_count(self):
        angles = []
        cplt = CustomPlot()
        nseg,nsample =  self.segment_set.shape
        # tf = open('features/theta.txt', 'a')
        # print nseg

        female_idx = np.where(self.gender_set=='F')
        male_idx = np.where(self.gender_set=='M')
        undefined_idx = np.where(self.gender_set=='U')

        #extract different genders segment from total gender set
        male_segment_set = self.segment_set[male_idx]
        female_segment_set =self.segment_set[female_idx]
        undefined_idx = self.segment_set[undefined_idx]
        speaker_count = 0
        print 'male\n'
        # male_count = self.determine_people(male_segment_set)
        # female_count = self.determine_people(female_segment_set)
        # print "total my supported algo"+str(male_count+female_count)
        male_count = 0
        male_count = self.estimate_people_count3(male_segment_set)
        #
        #
        print 'female\n'
        female_count = 0;
        female_count = self.estimate_people_count3(female_segment_set)

        total_people = male_count + female_count
        # total_people = 0
        # print 'total number of people:'
        # c1 = self.estimate_people_count_latest(male_segment_set)
        # c2 = self.estimate_people_count_latest(female_segment_set)
        # print c1 + c2
        return total_people
