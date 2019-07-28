# Image_quality_assessment
Full reference image quality assessment using statistical model and Machine Learning Regression (VIF)

This is the implementation of Full Reference Image quality Assessment based on Information fildelity criteria (Visual Information Fidility).
This implementation focuses on the Visual Information Fidelity (VIF) Index, or Sheikh-
Bovik Index, which is a specific and quite successful implementation of the
information fidelity–based approach.

For theorotical part you can refer to the original paper. 
Output of the method is value in between 0 and 1. We take two images for comparison
1. original image (img2o.jpg)
2. distorted image (img2c.jpg)
Note that the second image is the distorted image we get when we loss some of the information in communication channel.
Hence, one can note that size of the image(img2c.jpg) is less than the size of the original image.

Then we run our main function which calculates the VIF index.

Top-down Approaches for Full Reference Image Quality Assessment (Information Theoretical Approach)
1.	We calculate visual information fidelity index (VIF) of reference image and distorted image
a.	Main file: full_ref_tech.py
b.	sub files: utils.py
c.	Reference Image: img2o.jpg
d.	Distorted Image: img2c.jpg
e.	Rotated Image: img2cr.jpg

2.	Libraries installed in python: sciy, numpy, skimage (scikit-image).

3.	First go to the reference folder in which you have all your code files and images for testing and then go to 
python shell and run this commands.
a.	from skimage import io
b.	i = io.imread('img2o.jpg')
c.	i1 = io.imread('img2c.jpg')
d.	from full_ref_tech import vif
e.	vif(i,i1)       %this will return VIF index of above 2 images

you can try your own images but ideally size shoild be same. rotation is prohibited.

Thank you.
