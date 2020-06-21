# Texture-Synthesis
Texture synthesis is a technique of generating new images by stitching together patches of existing images. The purpose of study is to understand
patched based method for generating arbitrarily large textures from small real-world samples. The study is implementation of the paper 
[Image Quilting for Texture Synthesis and Transfer](https://people.eecs.berkeley.edu/~efros/research/quilting.html),
based on the work of [Alexei Efros and William Freeman](https://github.com/lschlessinger1/image-quilting). 

# Dependencies
1. numpy
2. skimage
3. PIL
4. argparse
5. pyqt5 (For GUI Implementation)

# How to execute the code :
**Using Command Line :**
1. You will first have to download the repository and then extract the contents into a folder.
2. Make sure you have the correct version of Python installed on your machine. This code runs on Python 3.6 above.
3. Install all dependencies mentioned above.
4. You can open the folder and run texture_synthesis.py on command prompt.
> `python texture_synthesis.py --image_path <image_path> --block_size <int_value> --num_block <int_value> --mode <Random/Best/Cut>`

For example :

> `python texture_synthesis.py --image_path data/input1.jpg --block_size 60 --num_block 8 --mode Best`

The default values of block_size is 50, num_block is 6 and mode is "Cut".

**Using GUI :**
1. Go to Texture_Synthesis_GUI folder, and run
> `Texture_Synthesis_GUI.py`
2. The above file will open GUI then you can run it.

**The default values of block_size is 50, num_block is 6 and mode is "Cut" and can not be changed.** 
# Results
![Outpu1](https://github.com/Devashi-Choudhary/Texture-Synthesis/blob/master/Results/output1.jpg)
![Outpu2](https://github.com/Devashi-Choudhary/Texture-Synthesis/blob/master/Results/output2.jpg)
**Note :** For more details of texture synthesis using patch based method, go through [Texture Synthesis : Generating arbitrarily large textures from image patches.](https://medium.com/@Devashi_Choudhary/texture-synthesis-generating-arbitrarily-large-textures-from-image-patches-32dd49e2d637)
