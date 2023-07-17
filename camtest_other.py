
import cv2
import os
from datetime import datetime

import sys
from multiprocessing import shared_memory
import numpy as np
import pickle

wait = 0

video = cv2.VideoCapture(0)
ret, img = video.read()


# Грузим файл, сохраненный другим процессом
with open('info.pickle', 'rb') as handle:
    f = pickle.load(handle)

# Печатаем содержимое файла
print('was loaded')
print(f)

# Назначаем данные для подключения и интерпретации общей памяти
f_name = f[2]
f_shape = f[3]
f_dtype = f[4]

# Инициализируем shm в данном процессе по загруженным данным
existing_shm = shared_memory.SharedMemory(name=f_name)
# Note that a.shape is (6,) and a.dtype is np.int64 in this example
img = np.ndarray(f_shape, dtype=f_dtype, buffer=existing_shm.buf)

while True:

	font = cv2.FONT_HERSHEY_PLAIN
	cv2.putText(img, 'OTHER ' + str(datetime.now()), (20, 40),
				font, 2, (255, 0, 255), 2, cv2.LINE_AA)
	
	cv2.imshow('live video', img)

	key = cv2.waitKey(100)

	wait = wait+100

	if key == ord('q'):
		break


# Закрытие(Отключение от) Shared_memory со стороны процесса
shm.close()
# close the camera
video.release()

# close open windows
cv2.destroyAllWindows()
