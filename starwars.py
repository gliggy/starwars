import numpy as np
from skimage import transform as tf

from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient


# RESOLUTION 
w = 720
h = w*9//16 
moviesize = w,h


#INSERT THE RAW TEXT (here: "A New Hope")

txt = "\n".join([
"It is a period of civil war. Rebel",
"spaceships, striking from a",
"hidden base, have won their",
"first victory against the evil",
"Galactic Empire. During the battle,",
"Rebel spies managed to steal secret",
"plans to the Empire’s ultimate weapon,",
"the DEATH STAR, an armored space station",
"with enough power to destroy an entire planet."
"",
"",
"",
"",
"",
"",
"",
"",
"",
])

# Add blanks before and after text
txt = 10*"\n" +txt + 10*"\n"

# CREATE THE TEXT IMAGE
clip_txt = TextClip(txt,color='cyan', align='Center',fontsize=25,
                    font='Xolonium-Bold', method='label')
                    
# SCROLL THE TEXT IMAGE BY CROPPING A MOVING AREA
txt_speed = 10 
fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+h,:]
moving_txt= clip_txt.fl(fl, apply_to=['mask'])

# ADD A VANISHING EFFECT ON THE TEXT WITH A GRADIENT MASK
grad = color_gradient(moving_txt.size,p1=(0,2*h/3),
                p2=(0,h/4),col1=0.0,col2=1.0)
gradmask = ImageClip(grad,ismask=True)
fl = lambda pic : np.minimum(pic,gradmask.img)
moving_txt.mask = moving_txt.mask.fl_image(fl)

# WARP THE TEXT INTO A TRAPEZOID (PERSPECTIVE EFFECT)
def trapzWarp(pic,cx,cy,ismask=False):
    Y,X = pic.shape[:2]
    src = np.array([[0,0],[X,0],[X,Y],[0,Y]])
    dst = np.array([[cx*X,cy*Y],[(1-cx)*X,cy*Y],[X,Y],[0,Y]])
    tform = tf.ProjectiveTransform()
    tform.estimate(src,dst)
    im = tf.warp(pic, tform.inverse, output_shape=(Y,X))
    return im if ismask else (im*255).astype('uint8')

fl_im = lambda pic : trapzWarp(pic,0.2,0.3)
fl_mask = lambda pic : trapzWarp(pic,0.2,0.3, ismask=True)
warped_txt= moving_txt.fl_image(fl_im)
warped_txt.mask = warped_txt.mask.fl_image(fl_mask)

# BACKGROUND IMAGE, DARKENED HERE AT 60%
stars = ImageClip('~/baleine.png')
stars_darkened = stars.fl_image(lambda pic: (0.6*pic).astype('int16'))

# COMPOSE THE MOVIE
final = CompositeVideoClip([
         stars_darkened,
         warped_txt.set_pos(('center','bottom'))],
         size = moviesize)


# WRITE TO A FILE
# duration here set to 35 seconds, with 18 frames per second
final.set_duration(35).write_videofile("star_wars_crawl.avi", 
                                       fps=18, codec='rawvideo')



