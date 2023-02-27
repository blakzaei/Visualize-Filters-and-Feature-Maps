# -*- coding: utf-8 -*-
"""Visualize_Filters_and_FeatureMaps.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WPrrOtWY4hk7SN42kPAIm3aR7QJzu0K_
"""

##-- Imports -------------------------------------------------------------------
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input
from keras.utils import load_img
from keras.utils import img_to_array
from keras.models import Model

from matplotlib import pyplot as plt
from numpy import expand_dims
import math

##-- Create Model --------------------------------------------------------------
model = VGG19()
model.summary()

#-- Number of All Layers -------------------------------------------------------
n_layers = len(model.layers)
print('Number of Layers= %d' % n_layers)

#-- Conv Layers ----------------------------------------------------------------
n_conv_layers = 0
index = 0

#-- key: conv_number : value:index --
conv_layers_index = {} 

for layer in model.layers:
  if 'conv' in layer.name:  
    n_conv_layers +=1  
    conv_layers_index[n_conv_layers] = index 

    filters, biases = layer.get_weights()
    print(n_conv_layers , layer.name, filters.shape)
  
  index += 1

print('\nNumber of Conv Layers= %d' % n_conv_layers)
print('\nConv Layers Index:\n' , conv_layers_index)

#-- Select Con Layer to Visualize ----------------------------------------------
conv_layer_index = int(input('Which Conv Layer do you want to visualize (1,%d)?' %n_conv_layers))

if conv_layer_index not in range(1,n_conv_layers+1):
  print('Please Enter a value between 1 and %d' %n_conv_layers)

#-- Select Number of Filters and Channels to Visualize -------------------------
layer_index = conv_layers_index[conv_layer_index]
print('Selected Layer: %s'  %model.layers[layer_index].name)

filters, biases = model.layers[layer_index].get_weights()

number_of_filters = filters.shape[3]
print('Number of Filters = %d' %number_of_filters)

number_of_channels = filters.shape[2]
print('Number of Channels = %d' %number_of_channels)

number_of_filters_to_visualize = int(input('How many filters do you want to visualize (1,%d)?' %number_of_filters))

if number_of_filters_to_visualize not in range(1,number_of_filters+1):
  print('Please Enter a value between 1 and %d' %number_of_filters)


number_of_channels_to_visualize = int(input('How many channels do you want to visualize (1,%d)?' %number_of_channels))

if number_of_channels_to_visualize not in range(1,number_of_channels+1):
  print('Please Enver a value between 1 and %d' %number_of_channels)

#-- Plot Filters ---------------------------------------------------------------

#-- Normalize Values to the Range 0-1 --
f_min, f_max = filters.min(), filters.max()
filters = (filters - f_min) / (f_max - f_min)

n_filters, ix = number_of_filters_to_visualize, 1
n_channels = number_of_channels_to_visualize

#-- Set Figure Size --
fig = plt.figure(figsize=(n_channels,n_filters ))

for i in range(n_filters):
  #-- Get the Filter --
  f = filters[:, :, :, i]

  #-- Plot Each Channel Separately --
  for j in range(n_channels):

    #-- Specify Subplot and Turn of Axis --    
    ax = plt.subplot(n_filters, n_channels, ix)
    ax.set_xticks([]) 
    ax.set_yticks([])

    #-- Set Title: Channle#-Filter# --
    ax.set_title(str(i+1) + '-' + str(j+1))

    #-- Plot Filter Channel in Grayscale --
    plt.imshow(f[:, :, j], cmap='gray') 
    ix += 1


plt.tight_layout()
plt.show()

#-- Output Size of Layers ------------------------------------------------------
index = 1
for layer in model.layers:
  if 'conv' not in layer.name:
    continue
    
  print(index , layer.name, layer.output.shape)
  
  index +=1

#-- Select Conv Layer to Visualize Feature Maps --------------------------------
conv_layer_index = int(input('Which Layer do you want to visualize Feature Maps (1,%d)?' %n_conv_layers))

if conv_layer_index not in range(1,n_conv_layers+1):
  print('Please Enter a value between 1 and %d' %n_conv_layers)

#-- Create a Sub-Model ---------------------------------------------------------
layer_index = conv_layers_index[conv_layer_index]
print(model.layers[layer_index].name)

#-- Redefine Model to Output Right After the Selected Layer
refined_model = Model(inputs=model.inputs, outputs=model.layers[layer_index].output)

refined_model.summary()

#-- Load Image to Visualize ----------------------------------------------------
input_size = refined_model.layers[0].input.shape
img_size = (input_size[1] , input_size[2])

#-- Load the Image with the Required Shape --
img = load_img('bird.jpg', target_size=img_size)

#-- Conver Image to an Array, Expand it and Preprocess -------------------------

#-- Convert the Image to an Array --
img = img_to_array(img)

#-- Expand Dimensions so that it Represents a Single 'sample' --
img = expand_dims(img, axis=0)

#-- Prepare the Image (e.g. scale pixel values for the vgg) --
img = preprocess_input(img)

#-- Get Feature Maps -----------------------------------------------------------

#-- Get Feature Map for Selected Layer --
feature_maps = refined_model.predict(img)

#-- Show output Size --
print(feature_maps.shape)

#-- Select Feature Maps to Visialize -------------------------------------------
number_of_feature_maps = feature_maps.shape[3]
print('Number of Feature Maps = %d' %number_of_feature_maps)

number_of_feature_maps_to_visualize = int(input('How many feature maps do you want to visualize (1,%d)?' %number_of_feature_maps))

if number_of_feature_maps_to_visualize not in range(1,number_of_feature_maps+1):
  print('Please Enter a value between 1 and %d' %number_of_feature_maps)

#-- Visualize Selected Feature Maps --------------------------------------------

#-- Set size of Figure --
h = int(math.sqrt(number_of_feature_maps_to_visualize))
w = math.ceil(number_of_feature_maps_to_visualize/h)
fig = plt.figure(figsize=(h*2,w*2 ))

ix = 1
for _ in range(w):
  for _ in range(h):

    #-- Specify Subplot And Turn of Axis --
    ax = plt.subplot(w, h, ix)
    ax.set_xticks([])
    ax.set_yticks([])

    #-- Set Title: feature_map# --
    ax.set_title(ix)

		#-- Plot Feature Maps --
    plt.imshow(feature_maps[0, :, :, ix-1], cmap='gray')

    ix += 1
    if ix>number_of_feature_maps_to_visualize:
      break

plt.tight_layout()
plt.show()

#-- Show Conv Layers index -----------------------------------------------------
n_conv_layers = 0
index = 0

#-- key: conv_number : value:index --
conv_layers_index = {} 

for layer in model.layers:
  if 'conv' in layer.name:  
    n_conv_layers +=1      
    filters, biases = layer.get_weights()
    print(index , n_conv_layers , layer.name, filters.shape)
  
  index += 1

#-- Redefine Model -------------------------------------------------------------
ixs = [2, 5, 10, 15, 20]
outputs = [model.layers[i].output for i in ixs]
refined_model = Model(inputs=model.inputs, outputs=outputs)

refined_model.summary()

#-- Get Feture Maps for All Blocks ---------------------------------------------

#-- Load the Image --
img = load_img('bird.jpg', target_size=(224, 224))

#-- Convert the Image to an Array --
img = img_to_array(img)

#-- Expand Dimensions --
img = expand_dims(img, axis=0)

#-- Prepare the Image --
img = preprocess_input(img)

#-- Get Feature Maps --
feature_maps = refined_model.predict(img)

#--Plot Feture Maps for All Blocks ---------------------------------------------
square = 8

for fmap in feature_maps:
  print("=====================================================================")
  fig = plt.figure(figsize=(square*2 , square*2 ))
  #-- Plot 64 Maps in an 8x8 Squares
  ix = 1
  for _ in range(square):
    for _ in range(square):
      #-- Specify Subplot and Turn of Axis
      ax = plt.subplot(square, square, ix)
      ax.set_xticks([])
      ax.set_yticks([])
			#-- Plot Filter Channel in Grayscale
      plt.imshow(fmap[0, :, :, ix-1], cmap='gray')
      ix += 1
	# show the figure
  plt.show()
  print("=====================================================================")