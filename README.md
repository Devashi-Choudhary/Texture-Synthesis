# Texture-Synthesis
Texture synthesis is a technique of generating new images by stitching together patches of existing images. The purpose of study is to understand
patched based method for generating arbitrarily large textures from small real-world samples. The study is implementation of the paper 
[Image Quilting for Texture Synthesis and Transfer](https://people.eecs.berkeley.edu/~efros/research/quilting.html),
based on the work of Alexei Efros and William Freeman.

# Dependencies
1. numpy
2. skimage
3. PIL
4. argparse

# How to execute the code :
1. You will first have to download the repository and then extract the contents into a folder.
2. Make sure you have the correct version of Python installed on your machine. This code runs on Python 3.6 above.
3. Install all dependencies mentioned above.
4. You can open the folder and run texture_synthesis.py on command prompt.
> `python texture_synthesis.py --image_path <image_path> --block_size <int_value> --num_block <int_value> --mode <Random/Best/Cut>`
##### For example :
> `python texture_synthesis.py --image_path texture6.jpg --block_size 60 --num_block 8 --mode Best`

The default values of block_size is 50, num_block is 6 and mode is Cut.

**Note :** For more details of texture synthesis using patch based method, go through
