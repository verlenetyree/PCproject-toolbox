import math
import matplotlib.pyplot as plt

#ввод входных параметров
K=float(input('Введите K: ')) #k=0,1 или бесконечность
fik=float(input('Введите fik: ')) #fik=0 - проекция Уэтча,fik=45 - проекция Голла

#создание текстового файла для записи пар значений прямоугольных координат узлов сетки
tabl=open('pryamaya_10_145.txt','w')
tabl.write('X;Y\n')

#описание констант
R=6371116
C=K+math.cos(fik*math.pi/180)
alpha=R*math.cos(fik*math.pi/180)

#расчёт и запись значений прямоугольных координат узлов сетки
for fi in range(-90,91,10):
    x=C*R*(math.sin(fi*math.pi/180)/(K+math.cos(fi*math.pi/180)))
    for lyambda in range(-180,181,10):
        y=alpha*lyambda*math.pi/180
        plt.scatter([lyambda],[fi], s=300)
        plt.gcf().set_size_inches((17.63, 10.88))
        tabl.write(str(x)+';'+str(y)+'\n')

tabl.close()
