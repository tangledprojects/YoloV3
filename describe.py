import os
import argparse
from PIL import Image
import numpy as np

def describe(indir):
    in_img = os.path.join(indir, "images")
    n = 0
    s = np.zeros(3)
    sq = np.zeros(3)
    for filename in os.listdir(in_img):  
        infile = os.path.join(in_img, filename)
        try:
            im = Image.open(infile)
            x = np.array(im)/255
            s += x.sum(axis=(0,1))
            sq += np.sum(np.square(x), axis=(0,1))
            n += x.shape[0]*x.shape[1]
            
        except:
            pass
    mu = s/n
    std = np.sqrt((sq/n - np.square(mu)))
    print(mu, sq/n, std, n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', type=str, required=True)  
    opt = parser.parse_args()
    print(opt)
    describe(opt.indir)
    