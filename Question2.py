# -*- coding: utf-8 -*-
"""Untitled21.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16edUPzKHxpvvtufL4ahkhPfKdYC2q7Yh
"""

!pip install wandb

import wandb

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.datasets import mnist, fashion_mnist
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns

ImageClasses = ["Pullover","Shirt","Coat","Trouser","Dress","Sandal","Bag","Sneaker","Ankle boot","T-shirt/top"]

from keras.datasets import fashion_mnist
(x_train,y_train),(x_test,y_test) = fashion_mnist.load_data()

wandb.init(project = "Assignment 1" ,name = "Question 1")

fig,axs = plt.subplots(2 , 5 , figsize = (20 , 6))
axs = axs.flatten()
class_images = []
for i in range(10):
  index = np.argmax(y_train == i)
  axs[i].imshow(x_train[index] , cmap = "gray")
  axs[i].set_title(ImageClasses[i])
  Image = wandb.Image(x_train[index] , caption = [ImageClasses[i]])
  class_images.append(Image)
wandb.log({"examples" : class_images})

class ActivationFunction:
  '''all activation functions are defined here'''
  def sigmoid(x):
    return  1 / (1 + np.exp(-x))
  def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)
  def softmax_derivative(self,x):
    return self.softmax(x) * (1-self.softmax(x))

class NeuralNetwork:
  '''n_layers = total number of layers except input layer
    n_neurons =  number of neurons in hidden and output layer
    n_input = number of inputs
    n_outputs = number of outputs
    activation_function = default is sigmoid activation function
    weights = weights of each connecting layer , size = (previous Layer Size , Current Layer Size)
    biases = biases of each connecting layer , size = (Current Layer Size , 1)
    input = input layer's input'''
  n_layers = 0
  activation_function = ""
  n_input = 0
  n_output = 0
  n_neurons = []
  input = []
  weights = []
  biases = []


  def __init__(self,num_neurons_in_hidden_layers,input,n_output):
    self.n_layers = len(num_neurons_in_hidden_layers) + 1
    self.activation_function = "sigmoid"
    self.input = input
    self.n_input = input.shape[0]
    self.n_output = n_output
    self.n_neurons = num_neurons_in_hidden_layers
    self.n_neurons.append(self.n_output)
    self.n_neurons.insert(0 , self.n_input)
    


    prevLayer = self.n_input
    for i in range(1,len(self.n_neurons)): 
      currLayer = self.n_neurons[i]
      w = np.random.rand(prevLayer,currLayer)
      prevLayer = currLayer
      self.weights.append(w)
    for i in range(1,len(self.n_neurons)): 
      b = np.random.rand(self.n_neurons[i],1)
      self.biases.append(b)

  def linear_forward(self,H,W,b):
    return np.dot(W.T,H) + b
  
  def active_forward(self,A):
    return ActivationFunction.sigmoid(A)
  def output(self,A):
    return ActivationFunction.softmax(A)
  def predict(self):
    A = []
    H = []
    prevLayer = self.input
    prevLayer_A = self.input
    for i in range(self.n_layers):
      A = self.linear_forward(prevLayer,self.weights[i],self.biases[i])
      H = self.active_forward(A)
      prevLayer = H
      prevLayer_A = A

    out = self.output(prevLayer_A)
    return out

a,b,c = x_train.shape
d = x_test.shape[0]

x_testT = np.transpose(x_test.reshape((d , b * c)))
x_trainT = np.transpose(x_train.reshape((a , b * c)))
y_train = y_train.reshape((a,1))
y_test = y_test.reshape((d,1))

NN = NeuralNetwork([3,3],x_trainT,2)

NN.predict()