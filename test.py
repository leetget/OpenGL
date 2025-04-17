from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Глобальные переменные
xRot = 0.0
yRot = 0.0
choice = 0  # По умолчанию — рисуем пружину
bCull = False
bDepth = True
bOutline = False
asdasdasdas = 0
bEdgeFlag = True
fire = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x01, 0xf0,
    0x00, 0x00, 0x07, 0xf0, 0x0f, 0x00, 0x1f, 0xe0,
    0x1f, 0x80, 0x1f, 0xc0, 0x0f, 0xc0, 0x3f, 0x80,
    0x07, 0xe0, 0x7e, 0x00, 0x03, 0xf0, 0xff, 0x80,
    0x03, 0xf5, 0xff, 0xe0, 0x07, 0xfd, 0xff, 0xf8,
    0x1f, 0xfc, 0xff, 0xe8, 0xff, 0xe3, 0xbf, 0x70,
    0xde, 0x80, 0xb7, 0x00, 0x71, 0x10, 0x4a, 0x80,
    0x03, 0x10, 0x4e, 0x40, 0x02, 0x88, 0x8c, 0x20,
    0x05, 0x05, 0x04, 0x40, 0x02, 0x82, 0x14, 0x40,
    0x02, 0x40, 0x10, 0x80, 0x02, 0x64, 0x1a, 0x80,
    0x00, 0x92, 0x29, 0x00, 0x00, 0xb0, 0x48, 0x00,
    0x00, 0xc8, 0x90, 0x00, 0x00, 0x85, 0x10, 0x00,
    0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00
]
# Число Пи
GL_PI = 3.1415

# Функция рисования пружины точками
def Points():
    global xRot, yRot

    glPushMatrix()

    # Повороты по x и y
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glBegin(GL_POINTS)

    z = -50.0
    angle = 0.0

    while angle <= 2.0 * GL_PI * 3.0:
        x = 50.0 * math.sin(angle)
        y = 50.0 * math.cos(angle)
        glVertex3f(x, y, z)
        z += 0.5
        angle += 0.1

    glEnd()

    glPopMatrix()

# Функция рендера сцены
def RenderScene():
    global choice
    glClear(GL_COLOR_BUFFER_BIT)
    if choice == 1:
        Points()
    elif choice == 2:
        PointsZ()
    elif choice == 3:
        Lines()
    elif choice == 4:
        LinesW()
    elif choice == 5:
        LinesStipple()
    elif choice == 6:
        Triangle()
    elif choice == 7:
        PolygonStipple()
    elif choice == 8:
        Star()
    else: Prompt()

    glFlush()

# Обработка изменения размеров окна
def ChangeSize(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspectRatio = width / height
    nRange = 100.0

    if width <= height:
        glOrtho(-nRange, nRange, -nRange / aspectRatio, nRange / aspectRatio, -nRange, nRange)
    else:
        glOrtho(-nRange * aspectRatio, nRange * aspectRatio, -nRange, nRange, -nRange, nRange)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
def Prompt():
    global xRot, yRot
    
    # Сохраняем текущий цвет
    current_color = glGetFloatv(GL_CURRENT_COLOR)
    
    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)
    
    # Устанавливаем зелёный цвет для треугольников
    glColor3f(0.0, 1.0, 0.0)
    
    # Рисуем два треугольника
    glBegin(GL_TRIANGLES)
    # Первый треугольник (справа)
    glVertex2f(0.0, 0.0)     # V0
    glVertex2f(25.0, 25.0)   # V1
    glVertex2f(50.0, 0.0)    # V2
    
    # Второй треугольник (слева)
    glVertex2f(-50.0, 0.0)   # V3
    glVertex2f(-75.0, 50.0)  # V4
    glVertex2f(-25.0, 0.0)   # V5
    glEnd()
    
    glPopMatrix()

    glColor(*current_color) ## сейвим зеленый цвет
def Triangle():
    global xRot, yRot, bCull, bDepth, bOutline
    
    # Устанавливаем плоское затенение
    glShadeModel(GL_FLAT)
    
    # Направление обхода по часовой стрелке
    glFrontFace(GL_CW)
    
    # Очищаем буферы
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Управление отбором граней
    if bCull:
        glEnable(GL_CULL_FACE)
    else:
        glDisable(GL_CULL_FACE)
    
    # Управление тестом глубины
    if bDepth:
        glEnable(GL_DEPTH_TEST)
    else:
        glDisable(GL_DEPTH_TEST)
    
    # Режим отображения задних граней
    if bOutline:
        glPolygonMode(GL_BACK, GL_LINE)
    else:
        glPolygonMode(GL_BACK, GL_FILL)
    
    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)
    
    # Рисуем конус (веер треугольников)
    glBegin(GL_TRIANGLE_FAN)
    # Вершина конуса (ближе к наблюдателю)
    glVertex3f(0.0, 0.0, 75.0)
    
    iColor = 1
    angle = 0.0
    while angle <= 2.0 * GL_PI:
        x = 50.0 * math.sin(angle)
        y = 50.0 * math.cos(angle)
        
        # Чередуем цвета
        if iColor % 2:
            glColor3f(0.0, 1.0, 0.0)  # Зеленый
        else:
            glColor3f(1.0, 1.0, 0.0)  # Желтый
        
        iColor += 1
        glVertex2f(x, y)
        angle += GL_PI / 8.0
    glEnd()
    
    # Рисуем основание конуса
    glBegin(GL_TRIANGLE_FAN)
    # Центр основания
    glVertex2f(0.0, 0.0)
    
    angle = 0.0
    while angle <= 2.0 * GL_PI:
        x = 50.0 * math.sin(angle)
        y = 50.0 * math.cos(angle)
        
        # Чередуем цвета
        if not (iColor % 2):
            glColor3f(0.0, 0.0, 1.0)  # Синий
        else:
            glColor3f(1.0, 0.0, 0.0)  # Красный
        
        iColor += 1
        glVertex2f(x, y)
        angle += GL_PI / 8.0
    glEnd()
    
    glPopMatrix()
    
    # Восстанавливаем настройки
    glDisable(GL_CULL_FACE)
    glDisable(GL_DEPTH_TEST)
    glPolygonMode(GL_BACK, GL_FILL)
    glColor3f(0.0, 1.0, 0.0)  # Восстанавливаем зеленый цвет
def PointsZ():
    global xRot, yRot

    # Сохраняем текущую матрицу
    glPushMatrix()

    # Применяем повороты
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    # Получаем диапазон допустимых размеров точек
    sizes = glGetFloatv(GL_POINT_SIZE_RANGE)
    step = glGetFloatv(GL_POINT_SIZE_GRANULARITY)
    curSize = sizes[0]

    z = -50.0
    angle = 0.0

    while angle <= 2.0 * GL_PI * 3.0:
        x = 50.0 * math.sin(angle)
        y = 50.0 * math.cos(angle)

        # Устанавливаем текущий размер точки
        glPointSize(curSize)

        glBegin(GL_POINTS)
        glVertex3f(x, y, z)
        glEnd()

        z += 0.5
        curSize += step
        angle += 0.1

    # Восстанавливаем матрицу
    glPopMatrix()

    # Возвращаем размер точки к начальному
    glPointSize(sizes[0])
def Lines():
    global xRot, yRot

    glPushMatrix()

    # Применяем повороты
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    z = 0.0
    angle = 0.0

    glBegin(GL_LINES)

    # 20 пар точек на окружности (верхняя и нижняя половина)
    while angle <= GL_PI:
        # Верхняя половина
        x1 = 50.0 * math.sin(angle)
        y1 = 50.0 * math.cos(angle)
        glVertex3f(x1, y1, z)

        # Нижняя половина (на 180 градусов смещённая)
        x2 = 50.0 * math.sin(angle + GL_PI)
        y2 = 50.0 * math.cos(angle + GL_PI)
        glVertex3f(x2, y2, z)

        angle += (GL_PI / 20.0)

    glEnd()

    glPopMatrix()
def LinesW():
    global xRot, yRot
    
    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)
    
    # Получаем диапазон и шаг изменения ширины линий
    sizes = glGetFloatv(GL_LINE_WIDTH_RANGE)
    step = glGetFloatv(GL_LINE_WIDTH_GRANULARITY)
    curSize = sizes[0]  # Начинаем с минимальной ширины
    
    # Рисуем 10 горизонтальных линий с увеличивающейся шириной
    for y in range(-90, 91, 20):
        glLineWidth(curSize)
        glBegin(GL_LINES)
        glVertex2f(-90.0, y)
        glVertex2f(90.0, y)
        glEnd()
        curSize += 3.0 * step  # Увеличиваем ширину
    
    glPopMatrix()
    glLineWidth(sizes[0])  # Восстанавливаем минимальную ширину
def LinesStipple():
    global xRot, yRot
    
    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)
    
    # Получаем диапазон ширины линий
    sizes = glGetFloatv(GL_LINE_WIDTH_RANGE)
    glLineWidth(sizes[0])  # Устанавливаем минимальную ширину
    
    # Включаем режим пунктирных линий
    glEnable(GL_LINE_STIPPLE)
    
    factor = 1          # Начальный множитель шаблона
    pattern = 0x5555    # Шаблон 0101010101010101
    
    # Рисуем 10 горизонтальных линий с разной фактурой
    y = -90.0
    while y <= 90.0:
        glLineStipple(factor, pattern)
        
        glBegin(GL_LINES)
        glVertex2f(-90.0, y)
        glVertex2f(90.0, y)
        glEnd()
        
        factor += 3  # Увеличиваем множитель шаблона
        y += 20.0
    
    glPopMatrix()
    glDisable(GL_LINE_STIPPLE)  # Выключаем режим пунктирных линий
def PolygonStipple():
    global xRot, yRot, fire
    
    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()
    
    # Применяем вращение
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)
    
    # Устанавливаем красный цвет
    glColor3f(1.0, 0.0, 0.0)
    
    # Включаем режим текстурирования многоугольника
    glEnable(GL_POLYGON_STIPPLE)
    
    # Устанавливаем маску текстуры
    glPolygonStipple((GLubyte * len(fire))(*fire))
    
    # Рисуем восьмиугольник (дорожный знак)
    glBegin(GL_POLYGON)
    glVertex2f(-20.0, 50.0)
    glVertex2f(20.0, 50.0)
    glVertex2f(50.0, 20.0)
    glVertex2f(50.0, -20.0)
    glVertex2f(20.0, -50.0)
    glVertex2f(-20.0, -50.0)
    glVertex2f(-50.0, -20.0)
    glVertex2f(-50.0, 20.0)
    glEnd()
    
    # Восстанавливаем настройки
    glColor3f(0.0, 1.0, 0.0)  # Зеленый цвет по умолчанию
    glDisable(GL_POLYGON_STIPPLE)
    glPopMatrix()
def TriangleExecuteMenu(option):
    global bCull, bDepth, bOutline, choice
    
    if option == 0:  # Сброс к настройкам по умолчанию
        bCull = False
        bDepth = True
        bOutline = False
    elif option == 1:  # Переключение отбора граней
        bCull = not bCull
    elif option == 2:  # Переключение теста глубины
        bDepth = not bDepth
    elif option == 3:  # Переключение каркасного режима
        bOutline = not bOutline
    
    # Устанавливаем режим отображения конуса
    choice = 6
    
    # Обновляем отображение
    glutPostRedisplay()
def Star():
    # Очистка кадра
    glClear(GL_COLOR_BUFFER_BIT)

    # Режим «каркас» для передней и задней сторон
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Сохраняем матрицу
    glPushMatrix()

    # Два поворота сцены
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    # ---------- Внутренние треугольники ----------
    glBegin(GL_TRIANGLES)
    glEdgeFlag(bEdgeFlag)

    glVertex2f(0.0, 0.0)        # центр
    glVertex2f(-18.0, 26.0)
    glVertex2f(18.0, 26.0)

    glVertex2f(0.0, 0.0)
    glVertex2f(18.0, 26.0)
    glVertex2f(30.0, -10.0)

    glVertex2f(0.0, 0.0)
    glVertex2f(30.0, -10.0)
    glVertex2f(0.0, -32.0)

    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, -32.0)
    glVertex2f(-30.0, -10.0)

    glVertex2f(0.0, 0.0)
    glVertex2f(-30.0, -10.0)
    glVertex2f(-18.0, 26.0)
    glEnd()

    # ---------- Внешние треугольники ----------
    glBegin(GL_TRIANGLES)

    glEdgeFlag(True)
    glVertex2f(-18.0, 26.0)
    glVertex2f(0.0, 80.0)
    glEdgeFlag(False)
    glVertex2f(18.0, 26.0)

    glEdgeFlag(True)
    glVertex2f(18.0, 26.0)
    glVertex2f(80.0, 26.0)
    glEdgeFlag(False)
    glVertex2f(30.0, -10.0)

    glEdgeFlag(True)
    glVertex2f(30.0, -10.0)
    glVertex2f(50.0, -68.0)
    glEdgeFlag(False)
    glVertex2f(0.0, -32.0)

    glEdgeFlag(True)
    glVertex2f(0.0, -32.0)
    glVertex2f(-50.0, -68.0)
    glEdgeFlag(False)
    glVertex2f(-30.0, -10.0)

    glEdgeFlag(True)
    glVertex2f(-30.0, -10.0)
    glVertex2f(-80.0, 26.0)
    glEdgeFlag(False)
    glVertex2f(-18.0, 26.0)
    glEnd()

    # Восстановление матрицы
    glPopMatrix()
    # Возвращаем режим заполнения
    glPolygonMode(GL_BACK, GL_FILL)
# Инициализация
def StarMenuExecute(starOption):
    global choice,bEdgeFlag
    if starOption == 1:
        bEdgeFlag = True
    if starOption == 2:
        bEdgeFlag = False
    choice = 8
    glutPostRedisplay()
def SetupRC():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # черный фон
    glColor3f(0.0, 1.0, 0.0)         # зелёный цвет для рисования

# Обработка специальных клавиш (стрелок)
def SpecialKeys(key, x, y):
    global xRot, yRot

    if key == GLUT_KEY_UP:
        xRot -= 5.0
    elif key == GLUT_KEY_DOWN:
        xRot += 5.0
    elif key == GLUT_KEY_LEFT:
        yRot -= 5.0
    elif key == GLUT_KEY_RIGHT:
        yRot += 5.0

    # Ограничим вращение от 0 до 360
    xRot = xRot % 360
    yRot = yRot % 360

    glutPostRedisplay()

# Обработка выбора из меню (если нужно)
def ExecuteMenu(option):
    global choice, xRot, yRot
    xRot = 0.0
    yRot = 0.0
    choice = option
    
    glutPostRedisplay()

# Главная функция
def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 600)

    # Название окна — только ASCII
    title = "OpenGL - Spring & Lines".encode("ascii")
    glutCreateWindow(title)

    glutDisplayFunc(RenderScene)
    glutReshapeFunc(ChangeSize)
    glutSpecialFunc(SpecialKeys)

    main_menu = glutCreateMenu(ExecuteMenu)
    glutAddMenuEntry("Normal Spring", 1)
    glutAddMenuEntry("Growing Points Spring", 2)
    glutAddMenuEntry("Fan of Lines", 3)
    glutAddMenuEntry("Wide Lines",4)
    glutAddMenuEntry("Strippled Lines",5)
    glutAddMenuEntry("Cone with Triangles",6)
    glutAddMenuEntry("Textured Polygon",7)
    glutAttachMenu(GLUT_RIGHT_BUTTON)
    # Подменю для управления конусом
    triangle_menu = glutCreateMenu(TriangleExecuteMenu)
    glutAddMenuEntry("Reset to Default", 0)
    glutAddMenuEntry("Toggle Culling", 1)
    glutAddMenuEntry("Toggle Depth Test", 2)
    glutAddMenuEntry("Toggle Outline Mode", 3)
    star_menu = glutCreateMenu(StarMenuExecute)
    glutAddMenuEntry("Toggle Outline",1)
    glutAddMenuEntry("OFf outline",2)
    glutSetMenu(main_menu)
    glutAddSubMenu("Cone settings",triangle_menu)
    glutAddSubMenu("Star settings",star_menu)
    SetupRC()
    glutMainLoop()

if __name__ == "__main__":
    main()