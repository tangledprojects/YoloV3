import os
import shutil 
import argparse
import cv2
import numpy as np

def dataprep2(indir, outdir, minsize, pathprefix):
  in_img = os.path.join(indir, "images")
  in_lbl = os.path.join(indir, "labels")
  out_img = os.path.join(outdir, "images")
  out_lbl = os.path.join(outdir, "labels")

  count = 0
  shapesfile = open(os.path.join(outdir, "shapes.txt"), 'w')
  filedata = open(os.path.join(outdir, "files.txt"), 'w')
  
  for filename in os.listdir(in_img):  
    infile = os.path.join(in_img, filename)
    name, ext = os.path.splitext(filename)
    scale = 3.5
    if not ext: 
        continue
    inlabel = os.path.join(in_lbl, f"{name.lower()}.txt")
    #print(infile, inlabel)
    try:
        img = cv2.imread(infile)
        img = cv2.resize(img,None,fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
        height, width, channels = img.shape
        print(filename, width, height)
        if height>= minsize and width >= minsize:
            print(filename, height, width, channels)
            shapesfile.write(f"{width} {height}\n")
            
            _, ext = os.path.splitext(infile)
            count += 1
            outfile = os.path.join(out_img, f"image{count:0>4d}{ext}".lower())
            filedata.write(f"{pathprefix}/images/image{count:0>4d}{ext.lower()}\n")
            cv2.imwrite(outfile, img)
            with open(os.path.join(out_lbl, f"image{count:0>4d}.txt"), "w") as outlabel:
                d = open(inlabel, 'r').read().splitlines()
                n = int(d[0])
                for i in range(1, n+1):
                    x1, y1, x2, y2 = map(lambda x: int(x)*scale, d[i].split())
                    cx = ((x1+x2)/2)/width
                    cy = ((y1+y2)/2)/height
                    hx = (x2-x1)/width
                    hy = (y2-y1)/width
                    outlabel.write(f"0 {cx} {cy} {hx} {hy}\n")
                d.close()
    except:
        pass

  shapesfile.close()
  filedata.close()

def dataprep(indir, outdir, minsize, pathprefix):
  in_img = os.path.join(indir, "images")
  in_lbl = os.path.join(indir, "labels")
  out_img = os.path.join(outdir, "images")
  out_lbl = os.path.join(outdir, "labels")

  count = 0
  shapesfile = open(os.path.join(outdir, "shapes.txt"), 'w')
  filedata = open(os.path.join(outdir, "files.txt"), 'w')

  for filename in os.listdir(in_img):  
    infile = os.path.join(in_img, filename)
    name, ext = os.path.splitext(filename)
    if not ext: 
        continue
    inlabel = os.path.join(in_lbl, f"{name.lower()}.txt")
    #print(infile, inlabel)
    try:
        img = cv2.imread(infile)
        height, width, channels = img.shape
        if height>= minsize and width >= minsize:
            print(filename, height, width, channels)
            shapesfile.write(f"{width} {height}\n")
            
            _, ext = os.path.splitext(infile)
            count += 1
            outfile = os.path.join(out_img, f"image{count:0>4d}{ext}".lower())
            filedata.write(f"{pathprefix}/images/image{count:0>4d}{ext.lower()}\n")
            outlabel = os.path.join(out_lbl, f"image{count:0>4d}.txt")
            shutil.copy(infile, outfile) 
            shutil.copy(inlabel, outlabel) 
    except:
        pass

  shapesfile.close()
  filedata.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', type=str, required=True)  
    parser.add_argument('--pathprefix', type=str, required=True)  
    parser.add_argument('--outdir', type=str, required=True)  
    parser.add_argument('--minsize', type=int, default=416)  
    parser.add_argument('--transform', type=bool, default=False)  
    opt = parser.parse_args()
    print(opt)
    assert os.path.exists(opt.indir), f"{opt.indir} does not exist"
    assert os.path.exists(os.path.join(opt.indir, "images")), f"{opt.indir}/images does not exist"
    assert os.path.exists(os.path.join(opt.indir, "labels")), f"{opt.indir}/labels does not exist"

    if not os.path.exists(opt.outdir):
        os.mkdir(opt.outdir)
        os.mkdir(os.path.join(opt.outdir, "images"))
        os.mkdir(os.path.join(opt.outdir, "labels"))

    if not opt.transform:
        dataprep(opt.indir, opt.outdir, opt.minsize, opt.pathprefix)
    else:
        dataprep2(opt.indir, opt.outdir, opt.minsize, opt.pathprefix)
    