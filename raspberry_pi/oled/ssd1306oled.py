
import os
import time
import threading
from PIL import Image, ImageSequence
from PIL import ImageFont, ImageDraw
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306



serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# 打开GIF文件并为每一帧创建Image对象
frames = []
with Image.open("./movie_new.gif") as img:
    for frame in ImageSequence.Iterator(img):
        frames.append(frame.convert("1").resize((128,64)))


# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])



def draw_text(text,width,height,fontsize):
    font = ImageFont.truetype("arial.ttf", fontsize)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        w, h = draw.textsize(text, font)
        x = (width - w) // 2
        y = (height - h) // 2
        draw.text((x, y), text, font=font, fill="white")

 # 逐一显示每个图像
def image_gif():
    for frame in frames:
        device.display(frame)
        time.sleep(0.01)

def computer_resources(flag):
    while not flag.is_set():
        # CPU informatiom
        CPU_use = getCPUuse()
        CPU_temp = getCPUtemperature()
        # RAM information
        # Output is in kb, here I convert it in Mb for readability
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000,1)
        RAM_used = round(int(RAM_stats[1]) / 1000,1)
        RAM_free = round(int(RAM_stats[2]) / 1000,1)

        # Disk information
        DISK_stats = getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_used = DISK_stats[1]
        DISK_perc = DISK_stats[3]


        draw_text("CPU_use:"+CPU_use+"\n", device.width, device.height, 20)
        draw_text("CPU_temp:"+CPU_temp+"\n", device.width, device.height, 20)
        draw_text("RAM_s:"+RAM_stats+"|t:"+RAM_total+"|u:"+RAM_used +"|f:"+RAM_free+"\n", device.width, device.height, 20)
        draw_text("DISK_s:"+DISK_stats+"|t:"+DISK_total+"|u:"+DISK_used+"|p:"+DISK_perc+"\n", device.width, device.height, 20)




if __name__ == '__main__':
    flag = threading.Event()
    t = threading.Thread(target=computer_resources,args=(flag,))
    while True:
        draw_text("www.spotpear.cn\n"+"www.spotpear.com\n", device.width, device.height, 20)
        time.sleep(2)
        #draw_text("TEST:"+getCPUuse(), device.width, device.height, 20)
        t.start()
        time.sleep(5)
        flag.set()
        t.join()
        flag.clear()
        t = threading.Thread(target=computer_resources,args=(flag,))
       # draw_text("T:"+DISK_stats[0], device.width, device.height, 20)
        time.sleep(2)
        image_gif()

