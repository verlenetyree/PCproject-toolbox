import math
import matplotlib.pyplot as plt

#ввод входных параметров
#проекция Соловьёва: k=1, fik=45, fi0=75, lyambda0=-80, lyambdam=100
K=float(input('Введите K: ')) #k=0,1 или бесконечность
fik=float(input('Введите fik: ')) #fik=0 - проекция Уэтча,fik=45 - проекция Голла
#задать координаты условного полюса
fi0=float(input('Введите fi0: '))
lyambda0=float(input('Введите lyambda0: '))

#описание констант
R=6371116
C=K+math.cos(fik*math.pi/180)
alpha=R*math.cos(fik*math.pi/180)

#переход к косой полярной системе координат, географические координаты
#расчёт и запись в текстовый файл условной широты 
fi_usl_tab=open('fi_usl_tab.txt','w')
for fi in range(-90,91,10):
    for lyambda in range(-180,181,10):
        la=(lyambda-lyambda0)
        sin_fiusl=math.sin(fi0*math.pi/180)*math.sin(fi*math.pi/180)+math.cos(fi0*math.pi/180)*math.cos(fi*math.pi/180)*math.cos(la*math.pi/180)
        fiusl=math.asin(sin_fiusl)
        fi_usl_tab.write(str(fiusl)+'\n')
fi_usl_tab.close()


#расчёт и запись в текстовый файл условной долготы 
lyambda_usl_tab=open('lyambda_usl_tab.txt','w')
for fi in range(-90,91,10):
    for lyambda in range(-180,181,10):
        la=(lyambda-lyambda0)
        if math.cos(fi0*math.pi/180)*math.sin(fi*math.pi/180)-math.sin(fi0*math.pi/180)*math.cos(fi*math.pi/180)*math.cos(la*math.pi/180)==0:
            continue
        sin=math.cos(fi*math.pi/180)*math.sin(la*math.pi/180)
        cos=math.cos(fi0*math.pi/180)*math.sin(fi*math.pi/180)-(math.sin(fi0*math.pi/180)*math.cos(fi*math.pi/180)*math.cos(la*math.pi/180))
        az=math.atan2(sin,cos)
        lyambdausl=-az 
        lyambda_usl_tab.write(str(lyambdausl)+'\n')
lyambda_usl_tab.close()        

#пересчёт условных географичексих координат в прямоугольные 
tabl_kosaya=open('tabl_kosaya_SOLOV.txt','w')
tabl_x=open('tabl_x.txt','w')
tabl_y=open('tabl_y.txt','w')
tabl_kosaya.write('X;Y\n')


fi_usl_tab=open('fi_usl_tab.txt','r')
lyambda_usl_tab=open('lyambda_usl_tab.txt','r')
for line_fi in fi_usl_tab:
    line_fi=float(line_fi.strip())
    x=C*R*(math.sin(line_fi)/(K+math.cos(line_fi)))
    tabl_x.write(str(x)+'\n')
    n=0
    for line_lyambda in lyambda_usl_tab:
        line_lyambda=float(line_lyambda.strip())
        y=alpha*line_lyambda
        #plt.scatter([line_lyambda],[line_fi], s=300)
        #plt.gcf().set_size_inches((17.63, 10.88))
        tabl_y.write(str(y)+'\n')
        tabl_kosaya.write(str(round(x,3))+';'+str(round(y,3))+'\n')
        n=n+1
        if n>0:
            break
        print(n)
fi_usl_tab.close()
lyambda_usl_tab.close()
tabl_kosaya.close()
tabl_x.close()
tabl_y.close()


'''Обратный пересчёт'''

#открытие для прочтения текстовых файлов с записями значений условных широти долгот узловых точек сетки
tabl_x=open('tabl_x.txt','r')
tabl_y=open('tabl_y.txt','r')
#создание текстовых файлов для записи значений геогрфических условных координат 
fi_tab=open('fiusl_tab.txt','w')
lyambda_tab=open('lyambdausl_tab.txt','w')
#создание текстового файла для записи пар значений геогрфических условных координат узлов сетки
tabl_kreverse=open('tabl_kreverse.txt','w')
tabl_kreverse.write('fi;lyambda\n')

#вычисление географических полярных координат (условной широты и условной долготы)
for line_x in tabl_x:
    line_x=float(line_x.strip())
    if line_x==0:
            fi=0
    elif line_x>0:
    #дискриминант для квадратного уравнения
        D=-(K**2)+((R**2)*(C**2)/line_x**2)+1
        fi=(math.asin((((K*R*C)/line_x)+math.sqrt(D))/(D+(K**2)))*180/math.pi)
    elif line_x<0:
        D=-(K**2)+((R**2)*(C**2)/line_x**2)+1
        fi=(math.asin((((K*R*C)/line_x)-math.sqrt(D))/(D+(K**2)))*180/math.pi)
    n=0
    for line_y in tabl_y:
        line_y=float(line_y.strip())
        lyambda=(line_y/alpha)*180/math.pi
        #plt.scatter([lyambda],[fi])
        fi_tab.write(str(fi)+'\n')
        tabl_kreverse.write(str(fi)+';'+str(lyambda)+'\n')
        lyambda_tab.write(str(lyambda)+'\n')
        n=n+1
        if n>0:
            break
        print(n)
tabl_kosaya.close()
tabl_kreverse.close()
tabl_x.close()
tabl_y.close()
fi_tab.close()
lyambda_tab.close()


fi_tab=open('fiusl_tab.txt','r')
lyambda_tab=open('lyambdausl_tab.txt','r')
fi_tab_final=open('fi_tab_final.txt','w')
lyambda_tab_final=open('lyambda_tab_final.txt','w')
tabl_kreverse_final=open('tabl_kreverse_SOLOV.txt','w')
tabl_kreverse_final.write('fi;lyambda\n')

#переход к нормальной ориентировке
for line_fi in fi_tab:
    line_fi=float(line_fi.strip())
    n=0
    for line_lyambda in lyambda_tab:
        line_lyambda=float(line_lyambda.strip())
        
        if line_fi==90:
            fi=fi0
            lyambda=lyambda0
        elif line_fi==-90:
            fi=-fi0
            lyambda=lyambda0+180
        else:    
            sinfi=math.cos(line_fi*math.pi/180)*math.cos(-line_lyambda*math.pi/180)*math.cos(fi0*math.pi/180)+math.sin(fi0*math.pi/180)*math.sin(line_fi*math.pi/180)
            fi=math.asin(sinfi)*180/math.pi
            sin=(math.cos(line_fi*math.pi/180)*math.sin(-line_lyambda*math.pi/180))/(math.cos(fi*math.pi/180))
            cos=(math.sin(line_fi*math.pi/180)-math.sin(fi*math.pi/180)*math.sin(fi0*math.pi/180))/(math.cos(fi0*math.pi/180)*(math.cos(fi*math.pi/180)))
            la=math.atan2(sin,cos)*180/math.pi
            lyambda=la
            if lyambda > 360:
                lyambda=lyambda-360
        plt.scatter([lyambda],[fi], s=300)
        plt.gcf().set_size_inches((17.63, 10.88))
        tabl_kreverse_final.write(str(round(fi,3))+';'+str(round(lyambda,3))+'\n')
        n=n+1
        if n>0:
            break
        
fi_tab_final.close()
lyambda_tab_final.close()
tabl_kreverse_final.close()
fi_tab.close()
lyambda_tab.close()
