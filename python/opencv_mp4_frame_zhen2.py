import cv2

# 打开视频文件
cap = cv2.VideoCapture('./bad_apple.mp4')

# 获取总帧数和帧率
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 定义需要截取的时间区间（单位为秒）
start_time = 21
end_time = 25

# 计算对应的帧数区间
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)

# 移动到起始帧
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# 从起始帧开始遍历帧数区间内的每一帧
for i in range(start_frame, end_frame):
    # 读取下一帧
    ret, frame = cap.read()

    # 如果帧读取失败，退出循环
    if not ret:
        break

    # 将帧保存为图片
    filename = f'./image4/frame_{i}.jpg'
    cv2.imwrite(filename, frame)

# 释放视频文件句柄。
cap.release()
cv2.destroyAllWindows()