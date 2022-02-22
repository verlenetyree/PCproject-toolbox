import math
import matplotlib.pyplot as plt

#создание текстового файла для записи пар значений широты на сфере
tabl=open('ellipse_to_sphere.txt','w')
tabl.write('L;fi\n')

#описание констант для эллипсоида Крассовского
a=6378245
b=6356863
#эксцентриситет меридианного сечения
e=math.sqrt(1-((b**2)/(a**2)))

#широта на эллипсоиде 
tabl_fi=open('tabl_fi.txt','w')
#долгота на эллипсоиде
tabl_l=open('tabl_l.txt','w')

#fi - широта на сфере
#B - широта на эллипсоиде
#L=lyambda
#расчёт и запись значений координат при переходе от эллипсоида к сфере
for L in range(-180,181,10):
    for B in range(-90,91,10):
        if B==-90 or B==90 or B==0:
            fi=B
        if -90<B<0 or 0<B<90:
            q=(1-e**2)*((math.sin(B*math.pi/180)/(1-(e**2)*math.sin(B*math.pi/180)**2))-((1/(2*e))*math.log((1-e*math.sin(B*math.pi/180))/(1+e*math.sin(B*math.pi/180)))))
            qp=1-(((1-e**2)/(2*e))*math.log((1-e)/(1+e)))
            Rq=a*math.sqrt(qp/2)
            fi=math.asin((q/qp))*180/math.pi
        #plt.scatter([L],[fi], s=300)
        #plt.gcf().set_size_inches((17.63, 10.88))
        #plt.savefig('ellipse_to_sphere.png')
        tabl_fi.write(str(fi)+'\n')
        tabl_l.write(str(L)+'\n') 
        
        tabl.write(str(round(L,4))+';'+str(round(fi, 4))+'\n')
tabl.close()
tabl_fi.close()
tabl_l.close()



tabl_fi=open('tabl_fi.txt','r')
tabl_l=open('tabl_l.txt','r')
tabl2=open('sphere_to_ellipse.txt','w')
tabl2.write('L;B\n')
#fi - широта на сфере
#B - широта на эллипсоиде
#L=lyambda
for l in tabl_l:
    l=float(l.strip())
    n=0
    for fi in tabl_fi:
        fi=float(fi.strip())
        if fi==-90 or fi==90 or fi==0:
            B=fi
        if -90<fi<0 or 0<fi<90:
            B=(fi*math.pi/180+((((e**2)/3)+((31*(e**4))/180)+((517*e**6)/5040))*math.sin(2*fi*math.pi/180))
            +((((23*e**4)/360)+((251*e**6)/3780))*math.sin(4*fi*math.pi/180))+(((761*e**6)/45360)*math.sin(6*fi*math.pi/180)))*180/math.pi
        plt.scatter([l],[B], s=300)
        plt.gcf().set_size_inches((17.63, 10.88))
        plt.savefig('sphere_to_ellipse.png')
        tabl2.write(str(round(l,4))+';'+str(round(B,4))+'\n')
        n=n+1
        if n>0:
            break
  
tabl2.close()
tabl_fi.close()
tabl_l.close()

