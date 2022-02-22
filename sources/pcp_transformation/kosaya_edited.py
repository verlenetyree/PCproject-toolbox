import math

#для проекции Соловьёва K=1, fik=45, fi0=75, lyambda0=-80
K=float(input('Введите K: ')) #k=0,1 или бесконечность
fik=float(input('Введите fik: ')) #fik=0 - проекция Уэтча,fik=45 - проекция Голла
#задать координаты условного полюса
fi0=float(input('Введите fi0: '))
lyambda0=float(input('Введите lyambda0: '))

R=6371116
C=K+math.cos(fik*math.pi/180)
alpha=R*math.cos(fik*math.pi/180)

#расчёт условной широты 
fi_usl_tab=open('fi_usl_tab.txt','w')
for fi in range(-90,91,1):
    for lyambda in range(-180,181,1):
        sin_fiusl=math.sin(fi0*math.pi/180)*math.sin(fi*math.pi/180)+math.cos(fi0*math.pi/180)*math.cos(fi*math.pi/180)*math.cos(lyambda*math.pi/180)
        fiusl=math.asin(sin_fiusl)*180/math.pi
        fi_usl_tab.write(str(fiusl)+'\n')
fi_usl_tab.close()

#расчёт условной долготы 
lyambda_usl_tab=open('lyambda_usl_tab.txt','w')
for fi in range(-90,91,1):
    for lyambda in range(-180,181,1): 
        if math.cos(fi0*math.pi/180)*math.sin(fi*math.pi/180)-math.sin(fi0*math.pi/180)*math.cos(fi*math.pi/180)*math.cos(lyambda*math.pi/180)==0:
            continue
        tg_lyambdausl=math.cos(fi*math.pi/180)*math.sin(lyambda*math.pi/180)/(math.cos(fi0*math.pi/180)*math.sin(fi*math.pi/180)-math.sin(fi0*math.pi/180)*math.cos(fi*math.pi/180)*math.cos(lyambda*math.pi/180))
        lyambdausl=math.atan(tg_lyambdausl)*180/math.pi
        lyambda_usl_tab.write(str(lyambdausl)+'\n')
lyambda_usl_tab.close()

#пересчёт в косую ориентировку, прямоугольные координаты
tabl_kosaya=open('tabl_kosaya.txt','w')
tabl_kosaya.write('X;Y\n')

fi_usl_tab=open('fi_usl_tab.txt','r')
lyambda_usl_tab=open('lyambda_usl_tab.txt','r')
for line_fi in fi_usl_tab:
    line_fi=float(line_fi.strip())
    x=C*R*(math.sin(line_fi*math.pi/180)/(K+math.cos(line_fi*math.pi/180)))
    #print(line_fi)
    #print(x)
    #tabl_kosaya.write(str(x)+';')
    n=0
    for line_lyambda in lyambda_usl_tab:
        line_lyambda=float(line_lyambda.strip())
        y=alpha*line_lyambda
        tabl_kosaya.write(str(x)+';'+str(y)+'\n')
        n=n+1
        if n>0:
            break
        print(n)
fi_usl_tab.close()
lyambda_usl_tab.close()
tabl_kosaya.close()