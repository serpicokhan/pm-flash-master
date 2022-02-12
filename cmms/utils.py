Cycles=1
Cycles_g=2
Hours=3
Kilometers=4
Kilopascals=5
Litres=6
Meters=7
Miles=8
poundsPerSquareInch=9
ProductionHours=10
Revolutions=11
Metric=(
          (Cycles,'Cycles (cycles)'),
          (Cycles_g,'Cycles (g)'),
          (Hours,'Hours (h)'),
          (Kilometers,'Kilometers (km)'),
          (Kilopascals,'Kilopascals (kPa)'),
          (Litres,'Litres (l)'),
          (Meters,'Meters (m)'),
          (Miles,'Miles (mi)'),
          (poundsPerSquareInch,'Pounds per square inch (PSI)'),
          (ProductionHours,'ProductionHours (ph)'),
          (Revolutions,'Revolutions (rev)'),
      )
################################################################
coastType1=1
coastType2=2
coastType3=3
coastType4=4
CoastType=(
    (coastType1,'هزینه1'),
    (coastType2,'هزینه2'),
    (coastType3,'هزینه3'),
    (coastType4,'هزینه4'),

)
currency=((0,'Us Dollar'),(1,'Rial'))
woStatus=dict()
woStatus['waitingforparts']=9
utilSeason=('z','p','t','b')
utilMonth=('اسفند','بهمن','دی','آذر','آبان','مهر','شهریور','مرداد','تیر','خرداد','اردیبهشت','فروردین')

utilSDate={}
utilMDate={}
utilSDate['z']=('10-01','12-29')
utilSDate['p']=('07-01','09-30')
utilSDate['t']=('04-01','06-31')
utilSDate['b']=('01-01','03-31')

utilMDate['فروردین']=('01-01','01-31')

utilMDate['اردیبهشت']=('02-01','02-31')
utilMDate['خرداد']=('03-01','03-31')
utilMDate['تیر']=('04-01','04-31')
utilMDate['مرداد']=('05-01','05-31')
utilMDate['شهریور']=('06-01','06-31')
utilMDate['مهر']=('07-01','07-30')
utilMDate['آبان']=('08-01','08-30')
utilMDate['آذر']=('09-01','09-30')
utilMDate['دی']=('10-01','10-30')
utilMDate['بهمن']=('11-01','11-30')
utilMDate['اسفند']=('12-01','12-29')



Requested=1
onHold=2
Draft=3
Assigned=4
Open=5
workInProgress=6
closedComplete=7
closedIncomplete=8
waitingForPart=9
invisible=-1
Highest=1
High=2
Medium=3
Low=4
Lowest=5
Status=(
     (Requested,'درخواست شده')  ,
     (onHold,'متوقف'),
     (Assigned,'تخصیص داده شده'),
     (Open,'باز'),
     (workInProgress,'در حال پیشرفت'),
     (closedComplete,'بسته شده کامل'),
     (closedIncomplete,'بسته شده، ناقص'),
     (waitingForPart,'در انتظار قطعه'),

 )
