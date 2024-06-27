# импортируем библиотеку pygame
import pygame
# импортируем библиотеку random для генерации случайных чисел
import random
# импортируем библиотеку copy для глубокого копирования
import copy

# инициализация всех модулей pygame
pygame.init()

# количество столбцов сетки
columns = 11
# количество строк сетки
strings = 21

# ширина окна игры
screen_x = 250
# высота окна игры
screen_y = 500

# создаём окно игры
screen = pygame.display.set_mode((screen_x, screen_y))
# устанавливаем заголовок окна
pygame.display.set_caption("Tetris CODE")
# создаём объект для отслеживания времени
clock = pygame.time.Clock()

# ширина одной ячейки сетки
cell_x = screen_x / (columns - 1)
# высота одной ячейки сетки
cell_y = screen_y / (strings - 1)

# частота кадров в секунду
fps = 60

# создаём пустой список для хранения сетки
grid = []

# проходим по каждому столбцу
for i in range(columns):
   # добавляем пустой список для каждого столбца
   grid.append([])
   # создаём кол-во ячеек, равное строкам,
   # и заполняем их значениями 1 (ячейка свободна)
   for j in range(strings):
       grid[i].append([1])

# проходим по каждой ячейке ещё раз
for i in range(columns):
   for j in range(strings):
       # добавляем ещё два параметра: создаём область прямоугольника и задаём цвет для каждой ячейки
       grid[i][j].append(pygame.Rect(i * cell_x, j * cell_y, cell_x, cell_y))
       grid[i][j].append(pygame.Color("Gray"))

# описание фигур Тетриса
details = [
   # линия
   [[-2, 0], [-1, 0], [0, 0], [1, 0]],
   # L-образная
   [[-1, 1], [-1, 0], [0, 0], [1, 0]],
   # обратная L-образная
   [[1, 1], [-1, 0], [0, 0], [1, 0]],
   # квадрат
   [[-1, 1], [0, 1], [0, 0], [-1, 0]],
   # Z-образная
   [[1, 0], [1, 1], [0, 0], [-1, 0]],
   # обратная Z-образная
   [[0, 1], [-1, 0], [0, 0], [1, 0]],
   # T-образная
   [[-1, 1], [0, 1], [0, 0], [1, 0]],
]

# создаём список для хранения всех 7 фигур
det = [[], [], [], [], [], [], []]

# инициализация фигур: проходим по списку с описанием координат
for i in range(len(details)):
   for j in range(4):
       # создаём прямоугольные области для каждого составного квадрата
       det[i].append(pygame.Rect(details[i][j][0] * cell_x + cell_x * (columns // 2), details[i][j][1] * cell_y, cell_x, cell_y))

# создаём область Rect для одной ячейки фигуры
detail = pygame.Rect(0, 0, cell_x, cell_y)
# выбираем случайную фигуру
det_choice = copy.deepcopy(random.choice(det))
# счётчик для управления скоростью падения фигур
count = 0
# флаг для управления игровым циклом
game = True
# флаг для управления поворотом фигур
rotate = False

# запускаем бесконечный цикл: он работает, пока флаг цикла равен True
while game:
   # изменение по оси x
   delta_x = 0
   # изменение по оси y (движение вниз)
   delta_y = 1

   # выход из игры при закрытии окна
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           exit()
       # обработка нажатий клавиш
       if event.type == pygame.KEYDOWN:
           # движение влево
           if event.key == pygame.K_LEFT:
               delta_x = -1
           # движение вправо
           elif event.key == pygame.K_RIGHT:
               delta_x = 1
           # поворот
           elif event.key == pygame.K_UP:
               rotate = True

   # получаем текущее состояние всех зажатых клавиш на клавиатуре
   key = pygame.key.get_pressed()

   # ускорение падения фигуры
   if key[pygame.K_DOWN]:
       count = 31 * fps

   # заполняем экран фоном
   screen.fill(pygame.Color(222, 248, 116, 100))

   # отрисовка сетки
   for i in range(columns):
       for j in range(strings):
           pygame.draw.rect(screen, grid[i][j][2], grid[i][j][1], grid[i][j][0])

   # проверка границ
   for i in range(4):
       # по горизонтали
       if ((det_choice[i].x + delta_x * cell_x < 0) or (det_choice[i].x + delta_x * cell_x >= screen_x)):
           delta_x = 0
       # по вертикали
       if ((det_choice[i].y + cell_y >= screen_y) or (
           grid[int(det_choice[i].x // cell_x)][int(det_choice[i].y // cell_y) + 1][0] == 0)):
           delta_y = 0
           # берём координаты x и y у каждого квадрата, из которых состоит остановившаяся фигура
           for i in range(4):
               x = int(det_choice[i].x // cell_x)
               y = int(det_choice[i].y // cell_y)
               # отмечаем в основном списке сетки, что такая ячейка занята
               grid[x][y][0] = 0
               # меняем цвет установленной фигуры на синий
               grid[x][y][2] = pygame.Color(45, 109, 234, 100)
           # сбрасываем координаты новой фигуры
           detail.x = 0
           detail.y = 0
           # выбираем новую фигуру
           det_choice = copy.deepcopy(random.choice(det))

   # перемещение по x
   for i in range(4):
       det_choice[i].x += delta_x * cell_x

   # каждый цикл увеличиваем счётчик количества кадров на 1 секунду
   count += fps

   # перемещение по y
   if count > 30 * fps:
       for i in range(4):
           det_choice[i].y += delta_y * cell_y
       count = 0

   # отрисовка текущей фигуры по 4 квадратам
   for i in range(4):
       detail.x = det_choice[i].x
       detail.y = det_choice[i].y
       pygame.draw.rect(screen, pygame.Color("White"), detail)

   # определяем центр фигуры, у нас это всегда третий квадрат в списке
   C = det_choice[2]
   if rotate:
       # поворачиваем фигуру по часовой стрелке
       for i in range(4):
           # считаем новые координаты
           x = det_choice[i].y - C.y
           y = det_choice[i].x - C.x
           # присваиваем их каждому квадрату по очереди
           det_choice[i].x = C.x - x
           det_choice[i].y = C.y + y
       rotate = False

   # проверка на заполненные ряды — идём по строкам сетки снизу вверх
   for j in range(strings - 1, -1, -1):
       # создаём счётчик заполненных ячеек
       count_cells = 0
       # идём по каждой ячейке из 10 в строке
       for i in range(columns):
           # если ячейка заполнена, увеличиваем счётчик
           if grid[i][j][0] == 0:
               count_cells += 1
           # если хоть одна ячейка не заполнена, то прерываем цикл и проверяем дальше
           elif grid[i][j][0] == 1:
               break
       # проверяем, набралось ли 10 полных ячеек
       if count_cells == (columns - 1):
           # если да, идём по этой строке...
           for l in range(columns):
               # ...и стираем заполненные ячейки
               grid[l][0][0] = 1
           # потом идём по строкам снизу вверх, начиная от удалённого ряда
           for k in range(j, -1, -1):
               for l in range(columns):
                   grid[l][k][0] = grid[l][k - 1][0]  # сдвигаем ряды вниз

   # обновляем экран
   pygame.display.flip()
   # задаём частоту обновления кадров
   clock.tick(fps)
