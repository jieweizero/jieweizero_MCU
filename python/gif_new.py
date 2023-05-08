from PIL import Image, ImageSequence, ImageOps


# 按照顺序提取图片并存储到列表中
images = []
for i in range(0, 239):
    filename = f'./image2/frame_{i}.jpg'
    im = Image.open(filename)
    images.append(im)

# 将列表中的图片保存为一个 GIF 文件
images[0].save('./movie.gif', save_all=True, append_images=images[1:], duration=10, loop=0)

with Image.open('movie.gif') as im:
    new_frames = []
    for frame in ImageSequence.Iterator(im):
        frame = ImageOps.fit(frame, (128,64), method=Image.ANTIALIAS)
        new_frames.append(frame)
    new_frames[0].save('movie_new.gif', save_all=True, append_images=new_frames[1:], loop=0)


    