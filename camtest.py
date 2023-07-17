
import cv2
import os
from datetime import datetime

import sys
from multiprocessing import shared_memory
import numpy as np
import pickle

'''
проверял на Win
'''

# путь для сохранения кадров
path = r'D:\test Shared\Bandicam'

# переходим по пути
os.chdir(path)

# счетчик для фреймов
i = 1

# Счетчик зажержки
wait = 0

# cv2.VideoCapture(n) - захватывает видео поток с камеры.
# n - порядковый номер камеры в системе
video = cv2.VideoCapture(0)
# (успех считывания(True/False), кадр) <= .read()
ret, img = video.read()

# создается Ячейка SharedMemory размером с кадр img.nbytes
shm = shared_memory.SharedMemory(create=True, size=img.nbytes)
# Использовал последовательнсоть ниже, чтобы передать через файл
# Данные для подключения к ячейке shm из сторонних потоков
f = []
f.append(sys.getsizeof(img))
f.append(type(img))
f.append(shm.name)
f.append(img.shape)
f.append(img.dtype)
# проверочная печать
print(f)
# тест сохрания и загрузки с печатью
with open('info.pickle', 'wb') as handle:
    pickle.dump(f, handle)
with open('info.pickle', 'rb') as handle:
    b = pickle.load(handle)
print('was loaded')
print(b)
print(str(b[1]))
print(type(b[1]))

while True:

	ret, img = video.read()
	# связываем b с shm.buf, задавая интерпретацию данных
	b = np.ndarray(img.shape, dtype=img.dtype, buffer=shm.buf)
	b[:] = img[:]
	# отрисовка на кадре текущего системного времени
	font = cv2.FONT_HERSHEY_PLAIN
	cv2.putText(img, str(datetime.now()), (20, 40),
				font, 2, (255, 255, 255), 2, cv2.LINE_AA)

	# отображаем фрейм с камеры в окне
	cv2.imshow('live video', img)

	
	
	
	# Задаем ожидание нажатия кнопки
	key = cv2.waitKey(100)

	# wait variable is to calculate waiting time
	wait = wait+100
	# по нажатию q выходим из программы
	if key == ord('q'):
		break
	# сохраняем каждый 100 расчетные ms кадр
	if wait == 100:
		filename = 'Frame_'+str(i)+'.jpg'
		
		# Save the images in given path
		cv2.imwrite(filename, img)
		i = i+1
		wait = 0

# Закрытие Shared_memory от процесса
shm.close()
# Очистка общей памяти, если никто больше не будет использовать Shared_memory
# После такого закрытия запрос от иных процессом может привести к ошибке доступа
shm.unlink()
# Закрываем камеру
video.release()
# Закрываем окна
cv2.destroyAllWindows()
