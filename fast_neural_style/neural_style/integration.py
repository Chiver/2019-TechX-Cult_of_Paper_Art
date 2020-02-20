'''
Imports 
'''
from gensim.models import Word2Vec
import pandas as pd
import string
import numpy
from argparse import Namespace

# Training Size 
TOTAL_SIZE=30000
data= pd.read_csv("train.csv")
dataX = [[word.lower() for word in sentence.replace("\n", "").translate(str.maketrans('', '', string.punctuation)).split(" ")] \
for sentence in data["comment_text"].values][:TOTAL_SIZE]

# Word Matrix Creating 
def cossim(vA,vB):
  cos = numpy.dot(vA, vB) / (numpy.sqrt(numpy.dot(vA,vA)) * numpy.sqrt(numpy.dot(vB,vB)))
  return cos

# Creating Word2Vec Model
wordModel = Word2Vec(dataX, min_count=1)

# Global Definition of Word Dictionary
words = {"festival": ["festival", "christmas", "easter"],
         "plants": ["flower"],
         "human": ["human", "father", "mother", "sister", "grandma", "grandpa", "parent", "family", "friends"],
         "animals": ["animals", "cat", "pig", "duck", "animal", "monkey", "bull", "bird"],
         "characters": ["words", "characters", "chinese", "english", "spanish", "language", "literature"],
         "others": ["others", "no"],
         "landscape": ["mountain", "water", "wind", "bridge", "land", "wind"]}

# Get user input word for testing 
inputs = input("Input your word for word2vec: ")   ############################# input word #################################
#print("The word you inputted: {}".format(inputs))


def get_classified_type(words, wordModel, input_word):
    biggest = 0
    for i in words:
        for j in words[i]:
            try:
                prop = cossim(wordModel.wv[j], wordModel.wv[input_word])

                # Obtain the best fir word
                if prop > biggest:
                    real_type = i
                    biggest = prop

            except Exception:
                print('This is not a typical paper cutting theme.')
                real_type = "others"
                break
    return real_type 

real_type = get_classified_type(words, wordModel)


#print("The type of the word is:   {}".format(real_type))
#print("The class name is: {}".format(type(real_type)))


########## 得到初始图片所在的类文件夹的位置 ############

def return_address(key):
    for i in keydict:

        if i == key:
            return keydict["{}".format(i)]
'''
需要手动输入各个folder的绝对地址
'''
keydict = {"festival": "C:\Hackathon_2019\Integrated Software\dataset\festival_pre",
           "plants": "C:\Hackathon_2019\Integrated Software\dataset\plants_pre",
           "human": "C:\Hackathon_2019\Integrated Software\dataset\human_pre",
           "characters": "C:\Hackathon_2019\Integrated Software\dataset\characters_pre",
           "others": "C:\Hackathon_2019\Integrated Software\dataset\others_pre",
           "landscape": "C:\Hackathon_2019\Integrated Software\dataset\landscape_pre",
           "animals": "C:\Hackathon_2019\Integrated Software\dataset\animals_pre"
           }

print(real_type)

address = return_address("characters")  # 此处的输入就是从W2V中返回的类名称，即real_type

print(address, type(address))


########### 获取初始图片的地址 ############
import os
import random
import cv2
from PIL import Image

rootdir = address # 此处填写上一个block通过return_address得到的地址，即address

file_names = []

for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    file_names = filenames
    # for filename in filenames:                        #输出文件信息
    #     print("parent is" + parent)
    #     print("filename is:" + filename)
    #     print("the full name of the file is:" + os.path.join(parent, filename))
x = random.randint(0, len(file_names)-1)

name = file_names[x] # 获取图片的名字

pic_address = "{}\{}".format(rootdir,name) ##################################################### 返回图片的地址，用作神经网络的输入

# print(pic_address)

# im = Image.open("{}\{}".format(rootdir,name))  # 图片路径



# im.show() # 打开通过NLP选择的图片

print("the picture selected is: {}".format(file_names[x]))



##################################################神经网络 Style Transfer############################################
import neural_style as ns



# if ns.__name__ == "__main__":

    #main()

ns.stylize(Namespace(**{
    "content_image": pic_address, ################### 输入图片的地址，在上方可以获得 pic address
    "output_image": "../images/output-images/temp.jpg", ### style transfer 图片的位置 名字为temp.jpg
    "model": "../saved_models/new2.model",
    "content_scale": None,
    "cuda": 0,
    "export_onnx": None,
    "subcommand": "eval",
}))


#################################################矢量化################################################################

import postimage as psi

path = '../images/output-images/'
houzhui = 'temp.jpg'
psi.postImage(path, houzhui) ## 将生成的svg存在 "..\Integrated Software\fast_neural_style\images\output-images"

## cheng xu yuan cong lai bu kan warning


