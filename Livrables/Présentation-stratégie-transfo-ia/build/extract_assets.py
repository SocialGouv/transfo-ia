from PIL import Image

p1 = Image.open("page-01.png").convert("RGB")
p2 = Image.open("page-02.png").convert("RGB")
W1,H1 = p1.size
W2,H2 = p2.size
print("page1", p1.size, "page2", p2.size)

def crop_frac(im, x0,y0,x1,y1):
    W,H = im.size
    return im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))

def trim_white(im, thr=245):
    # bbox of non-white-ish pixels
    from PIL import ImageChops, Image as I
    bg = I.new("RGB", im.size, (255,255,255))
    diff = ImageChops.difference(im, bg)
    # amplify
    mask = diff.convert("L").point(lambda p: 255 if p>10 else 0)
    bbox = mask.getbbox()
    return im.crop(bbox) if bbox else im

# LOGO (page2, white bg) -> trim
logo = crop_frac(p2, 0.055, 0.028, 0.150, 0.155)
logo = trim_white(logo)
logo.save("assets/logo.png")
print("logo", logo.size)

# SPARKLE (page1, on blue) - square crop
spark = crop_frac(p1, 0.103, 0.527, 0.207, 0.713)
spark.save("assets/sparkle.png")
print("sparkle", spark.size)

# STRIPES (page1, bottom-right on blue)
stripes = crop_frac(p1, 0.735, 0.735, 0.970, 0.962)
stripes.save("assets/stripes.png")
print("stripes", stripes.size)

# also full-corner previews to calibrate
crop_frac(p1, 0.0,0.45,0.30,0.80).save("assets/_dbg_sparkle_region.png")
crop_frac(p1, 0.65,0.65,1.0,1.0).save("assets/_dbg_stripes_region.png")
