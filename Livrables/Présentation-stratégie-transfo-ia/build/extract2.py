from PIL import Image

p1 = Image.open("page-01.png").convert("RGB")
W,H = p1.size

# sample the block blue
bx, by = int(0.5*W), int(0.45*H)
blue = p1.getpixel((bx,by))
print("sampled blue", blue, "#%02X%02X%02X"%blue)

def recolor_near_white(im, to, thr=238):
    px = im.load()
    w,h = im.size
    for y in range(h):
        for x in range(w):
            r,g,b = px[x,y]
            if r>=thr and g>=thr and b>=thr:
                px[x,y] = to
    return im

# SPARKLE tight square
spark = p1.crop((396,1118,726,1448))
spark = recolor_near_white(spark, blue)
spark.save("assets/sparkle.png")
print("sparkle", spark.size)

# STRIPES: crop then recolor whites to blue
stripes = p1.crop((int(0.735*W),int(0.735*H),int(0.972*W),int(0.985*H)))
stripes = recolor_near_white(stripes, blue)
stripes.save("assets/stripes.png")
print("stripes", stripes.size)
