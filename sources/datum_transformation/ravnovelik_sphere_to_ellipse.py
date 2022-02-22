import math
import matplotlib.pyplot as plt

#создание текстового файла для записи пар значений широты после перехода к эллипсоиду
tabl=open('sphere_to_ellipse.txt','w')
#широта на эллипсоиде 
tabl_B=open('tabl_B.txt','w')
#долгота на эллипсоиде
tabl_L=open('tabl_L.txt','w')
tabl.write('L;B\n')

#описание констант (эллипсоид Красовского)
a=6378245
b=6356863
#эксцентриситет меридианного сечения
e=math.sqrt(1-((b**2)/(a**2)))

#fi - широта на сфере
#B - широта на эллипсоиде
#L=lyambda
for l in range(-180,181,10):
    for fi in range(-90,91,10):
        if fi==-90 or fi==90 or fi==0:
            B=fi
        if -90<fi<0 or 0<fi<90:
            B=(fi*math.pi/180+((((e**2)/3)+((31*(e**4))/180)+((517*e**6)/5040))*math.sin(2*fi*math.pi/180))
            +((((23*e**4)/360)+((251*e**6)/3780))*math.sin(4*fi*math.pi/180))+(((761*e**6)/45360)*math.sin(6*fi*math.pi/180)))*180/math.pi
        #plt.scatter([L],[B], s=300)
        #plt.gcf().set_size_inches((17.63, 10.88))
        tabl.write(str(round(l,4))+';'+str(round(B,4))+'\n')
        tabl_B.write(str(B)+'\n')
        tabl_L.write(str(l)+'\n')  

tabl.close()
tabl_B.close()
tabl_L.close()


#создание текстового файла для записи пар значений широты после перехода обратно к шару
tabl=open('ellipse_to_sphere.txt','w')

tabl2=open('sphere_to_ellipse.txt','r')
tabl_B=open('tabl_B.txt','r')
tabl_L=open('tabl_L.txt','r')

tabl.write('L;fi\n')


#расчёт и запись значений координат при переходе от эллипсоида к сфере
for L in tabl_L:
    L=float(L.strip())
    n=0
    for B in tabl_B:
        B=float(B.strip())
        if B==-90 or B==90 or B==0:
            fi=B
        if -90<B<0 or 0<B<90:
            q=(1-e**2)*((math.sin(B*math.pi/180)/(1-(e**2)*math.sin(B*math.pi/180)**2))-((1/(2*e))*math.log((1-e*math.sin(B*math.pi/180))/(1+e*math.sin(B*math.pi/180)))))
            qp=1-(((1-e**2)/(2*e))*math.log((1-e)/(1+e)))
            Rq=a*math.sqrt(qp/2)
            fi=math.asin((q/qp))*180/math.pi
        plt.scatter([L],[fi], s=300)
        plt.gcf().set_size_inches((17.63, 10.88))
        tabl.write(str(round(L,4))+';'+str(round(fi,4))+'\n')   
        n=n+1
        if n>0:
            break
tabl.close()
tabl2.close()




            
            
            
        
        
        
        
        
    






