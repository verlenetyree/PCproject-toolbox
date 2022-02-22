import math
import matplotlib.pyplot as plt

#ввод входных параметров
K=float(input('Введите K: ')) #k=0,1 или бесконечность
fik=float(input('Введите fik: ')) #fik=0 - проекция Уэтча,fik=45 - проекция Голла

#создание текстового файла для записи пар значений прямоугольных координат узлов сетки
tabl=open('pryamaya_GALL.txt','w')
tabl.write('X;Y\n')
#создание текстовых файлов для отдельной записи значений широты и долготы узловых точек сетки
tabl_x=open('tabl_x.txt','w')
tabl_y=open('tabl_y.txt','w')

#описание констант
R=6371116
C=K+math.cos(fik*math.pi/180)
alpha=R*math.cos(fik*math.pi/180)

#расчёт и запись значений прямоугольных координат узлов сетки
for fi in range(-90,91,10):
    x=C*R*(math.sin(fi*math.pi/180)/(K+math.cos(fi*math.pi/180)))
    for lyambda in range(-180,181,10):
        y=alpha*lyambda*math.pi/180
        #plt.scatter([y],[x])
        tabl.write(str(round(x,3))+';'+str(round(y,3))+'\n')
        tabl_x.write(str(x)+'\n')
        tabl_y.write(str(y)+'\n')

tabl.close()
tabl_x.close()
tabl_y.close()

'''Обратный пересчёт'''

#открытие для прочтения текстовых файлов с записями значений широты и долготы узловых точек сетки
tabl_x=open('tabl_x.txt','r')
tabl_y=open('tabl_y.txt','r')
#создание текстового файла для записи пар значений геогрфических координат узлов сетки
tabl_preverse=open('tabl_preverse_GALL.txt','w')
tabl_preverse.write('fi;lyambda\n')


#обратный пересчёт и запись значений географических координат узлов сетки
for line_x in tabl_x:
    line_x=float(line_x.strip())
    if line_x==0:
            fi=0
    elif line_x>0:
    #расчёт дискриминанта квадратного уравнения
        D=-(K**2)+((R**2)*(C**2)/line_x**2)+1
        fi=(math.asin((((K*R*C)/line_x)+math.sqrt(D))/(D+(K**2)))*180/math.pi)
    elif line_x<0:
        D=-(K**2)+((R**2)*(C**2)/line_x**2)+1
        fi=(math.asin((((K*R*C)/line_x)-math.sqrt(D))/(D+(K**2)))*180/math.pi)
    n=0
    for line_y in tabl_y:
        line_y=float(line_y.strip())
        lyambda=(line_y/alpha)*180/math.pi
    plt.scatter([lyambda],[fi])
    tabl_preverse.write(str(round(fi,3))+';'+str(round(lyambda,3)+'\n')
    n=n+1
    if n>0:
        break
        print(n)
tabl_x.close() 
tabl_y.close()
tabl_preverse.close()
    
    