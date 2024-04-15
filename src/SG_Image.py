import scipy.misc
import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv2
from random import randint
import glob
from PIL import Image
import random
import os

def final_allscale(synt,real_image_stack,flag,thres):

	rMin=[]
	sMin=[]
	rMax=[]
	sMax=[]
	sMean=[]
	rMean=[]
	ImN=[]
	cnt=0
	for i in range(3):
		while(np.shape(rMin)[0]!=3 and np.shape(sMin)[0]!=3 and np.shape(rMax)[0]!=3 and np.shape(sMax)[0]!=3 or cnt>=5):#0.3
			num=randint(0, flag-1)
			cnt=cnt+1
			stemp=synt[:,:,i]
			rtemp=real_image_stack[num,:,:,i]
			sMean=(np.mean(stemp.flatten()))
			rMean=(np.mean(rtemp.flatten()))
			if(abs(sMean-rMean)<=thres):
				rMin.append(min(rtemp.flatten()))
				sMin.append(min(stemp.flatten()))
				rMax.append(max(rtemp.flatten()))
				sMax.append(max(stemp.flatten()))

			if(cnt>=5):
				norma=synt
				break
				print('Could not pre-process the input')

	if(np.shape(rMin)[0]==3 and np.shape(sMin)[0]==3 and np.shape(rMax)[0]==3 and np.shape(sMax)[0]==3):
		for j in range(3):
			#Shift distribution to zero
			temp1=(synt[:,:,j]-sMin[j])
			#scale max of the real-min of the real
			temp2=temp1*((rMax[j]-rMin[j])/(sMax[j]-sMin[j]))
			# Add the minimum value from the real imagery
			temp3=temp2+rMin[j]
			#Converting scale.
			ImN.append(temp3)
		norma=np.moveaxis(ImN, 0, 2)

	return norma

def main():

	name=0
	for filename in glob.glob(os.path.join(synthetic_path,'*.PNG')):
		syn=scipy.misc.imread(filename)
		na=(filename.split("/")[-1])
		synt=cv2.normalize(syn.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
		normali=final_allscale(synt,real_image_stack,flag,thres)
		scipy.misc.imsave('/home/path/to/target/{}'.format(na),  normali)
		name=name+1
	print('Preprocessed {} chips'.format(name))

if __name__ == "__main__":

	thres=0.05 #Change threshold accordingly
	real_path='/home/path/to/real/*.png' #Path to real images for comparing
	synthetic_path='/home/Path/to/synthetic' #Path to simulated imagery for preprocessing
	real_image_stack = np.stack([np.expand_dims(((Image.open(filename).resize((80,80)))),-1) for filename in glob.glob(real_path)],0)
	real_image_stack=np.squeeze(real_image_stack)
	real_image_stack=cv2.normalize(real_image_stack.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
	flag=(np.shape(real_image_stack))[0]

	main()