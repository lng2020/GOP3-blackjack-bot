import pyautogui
from pyscreeze import screenshot
from cv2 import resize,matchTemplate,TM_CCOEFF_NORMED,imread,minMaxLoc
from sys import exit
from time import sleep,time
from warnings import simplefilter
import os
import sys


#这两行忽略了oyautogui的安全警告
simplefilter("ignore")
pyautogui.FAILSAFE = False
# 屏幕缩放系数 mac缩放是2 windows一般是1
screenScale=1
list1=(['H','H','H','H','H','H','H','H','H','H'],#5,H=要牌，D=加倍，S=停牌
       ['H','H','H','H','H','H','H','H','H','H'],#6
       ['H','H','H','H','H','H','H','H','H','H'],#7
       ['H','H','H','H','H','H','H','H','H','H'],#8
       ['H','D','D','D','D','H','H','H','H','H'],#9
       ['D','D','D','D','D','D','D','D','H','H'],#10
       ['D','D','D','D','D','D','D','D','H','H'],#11
       ['H','H','S','S','S','H','H','H','H','H'],#12
       ['S','S','S','S','S','H','H','H','H','H'],#13
       ['S','S','S','S','S','H','H','H','H','H'],#14
       ['S','S','S','S','S','H','H','H','S','H'],#15
       ['S','S','S','S','S','H','H','S','S','H'],#16
       ['S','S','S','S','S','S','S','S','S','S'],#17
       ['S','S','S','S','S','S','S','S','S','S'],#18
       ['S','S','S','S','S','S','S','S','S','S'],#19
       ['S','S','S','S','S','S','S','S','S','S'],#20
       ['S','S','S','S','S','S','S','S','S','S'],#21
       ['S','S','S','S','S','S','S','S','S','S'],#21
       ['S','S','S','S','S','S','S','S','S','S'],#22
       )#从左往右庄家手里的是23456789TA
list2=(['H','H','H','D','D','H','H','H','H','H'],#A2,H=要牌，D=加倍，S=停牌
       ['H','H','H','D','D','H','H','H','H','H'],#A3
       ['H','H','D','D','D','H','H','H','H','H'],#A4
       ['H','H','D','D','D','H','H','H','H','H'],#A5
       ['S','D','D','D','D','S','S','S','H','H'],#A6
       ['S','S','S','S','S','S','S','S','S','S'],#A7
       ['S','S','S','S','S','S','S','S','S','S'],#A8
       ['S','S','S','S','S','S','S','S','S','S'],#A9
       )
list3=(['P','P','P','P','P','P','H','H','H','H'],#Pair2,H=要牌，D=加倍，S=停牌
       ['P','P','P','P','P','P','H','H','H','H'],#Pair3
       ['H','H','H','P','P','P','H','H','H','H'],#Pair4
       ['D','D','D','D','D','D','D','D','H','H'],#Pair5
       ['P','P','P','P','P','H','H','H','H','H'],#Pair6
       ['P','P','P','P','P','P','H','H','H','H'],#Pair7
       ['P','P','P','P','P','P','P','P','S','H'],#Pair8
       ['P','P','P','P','P','S','P','P','S','S'],#Pair9
       ['S','S','S','S','S','S','S','S','S','S'],#PairT
       ['P','P','P','P','P','P','P','P','P','H'],#PairA
       )
handA=[range(895,912),range(1028,1040),range(744,762)]
handB=[range(939,953),range(1072,1084),range(789,803)]

def compare(target,temp):

    global max_loc,twidth,theight
    theight, twidth=target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp=resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    #stempheight, stempwidth = scaleTemp.shape[:2]
    # 匹配图片
    res = matchTemplate(scaleTemp, target, TM_CCOEFF_NORMED)
    
    mn_val, max_val, min_loc, max_loc = minMaxLoc(res)
    if(max_val>=0.9):#匹配成功
        print("比对成功",max_loc)
        return 1
    else:
        return 0
def clickz(top_left):
    tagHalfW=int(twidth/2)
    tagHalfH=int(theight/2)
    tagCenterX=top_left[0]+tagHalfW
    tagCenterY=top_left[1]+tagHalfH
    tagCenterR=tagCenterY-300#增加功能，使得点击过后鼠标向上移动，防止置于原处
    #左键点击屏幕上的这个位置
    pyautogui.click(tagCenterX,tagCenterY,button='left')
    pyautogui.moveTo(tagCenterX,tagCenterR)#增加功能，使得点击过后鼠标向上移动，防止置于原处

def Cursorpositionpause():#鼠标控制暂停函数
    #本段用于通过检测鼠标位置实现程序的暂停循环
    Curposition=pyautogui.position()
    i=2
    if(Curposition.y>=1076):
        while True:
            print("程序将暂停{}秒，鼠标移动至屏幕上、左、右侧边缘等待{}秒，程序将继续运行".format(i,i))
            sleep(i)
            if i<15:
                i=i+1
            Curposition=pyautogui.position()
            print("鼠标位置",Curposition)
            if(Curposition.y<=3 or Curposition.x>=1916 or Curposition.x<=3):
                print("程序继续\n\n")
                break
cpause=Cursorpositionpause 
def poke(h):#读牌转化函数
    if((h%13>=10 and h%13<=13)or h%13==0):
        return 10
    elif(h%13==1):
        return 11
    else:return h%13
def write_sentence(a, b, c, d, f, e):
    f_string = "win" if f else "lose"
    sentence = "操作:{}, 手牌:{}, 手牌:{}, 庄牌:{},{},胜率:{:>8.4f}".format(d, a, b, c, f_string,e)
    with open('data.txt', 'a') as file:
        file.write(sentence + '\n')
def Startupverification():#启动验证函数
    print("使用说明:\n启动本软件前检查image文件夹，须包含以下文件：1.png 10.png 11.png 12.png 13.png 14.png 15.png 16.png 17.png 18.png 19.png 2.png 20.png 21.png 22.png 23.png 24.png 25.png 26.png 27.png 28.png 29.png 3.png 30.png 31.png 32.png 33.png 34.png 35.png 36.png 37.png 38.png 39.png 4.png 40.png 41.png 42.png 43.png 44.png 45.png 46.png 47.png 48.png 49.png 5.png 50.png 51.png 52.png 6.png 7.png 8.png 9.png " 
          "bet100000k.png bet50000k.png bet20000k.png bet10000k.png bet5000k.png bet2500k.png bet1000k.png bet500k.png bet100k.png bet10k.png bet1k.png bet200k.png bet25k.png bet2k.png bet50k.png bet5k.png btn.png buyin.png double.png hit.png LIST.TXT screen.png split.png sss.bat stand.png，并确保本文件与image/在同一目录内\n"
          "启动后会根据当前屏幕内容反馈到当前窗口，按顺序打开GOP3并且启动21点挂机即可(版本号1.17)\n"#1.13更新了去掉再买入功能并添加鼠标暂停和继续功能，1.12更新了时间锁，1.11更新了全桌全类型下注
          "注意，请坐在中间位置以便脚本顺利捕获，建议选择“非公开牌局”\n"
          "目前参数适用1920*1080分辨率Windows电脑屏幕\n")
    #获取当前屏幕的分辨率
    sda=pyautogui.size()
    mysize=(sda.width,sda.height)
    print("当前屏幕分辨率是",mysize)
    if(mysize!=(1920, 1080)):
        print("\n\n***********屏幕分辨率错误，脚本将不能有效捕获************\n\n")
    else:print("屏幕分辨率符合要求\n")
def unfcs():
    temp = imread(r'image/screen.png',0)
    i=0
    while i<5:
        i=i+1
        target = imread(r'image/off'+str(i)+'.png',0)
        if compare(target, temp)==1:#匹配成功  
            top_left = max_loc
            clickz(top_left)
            sleep(0.01)
            return 0
    if compare(doubleexp, temp)==1 :
        pyautogui.click(130,1011,button='left')
        sleep(3)
        return 0
    pyautogui.click(92,52,button='left')
    
Startupverification()  

if not os.path.isfile('data.txt'):
    open('data.txt', 'w').close()

with open('data.txt', 'r') as f:
    lines = f.readlines()

betnum=input("在此输入默认下注额度：（1k请按1，2.5k按2，5k按3，10k按4，25k按5，50k按6，100k按7，200k按8，500k按9，1M按10，2.5M按11，5M按12，10M按13，20M按14，50M按15，100M按16）\n"
                 "请输入：\n")
print("您将以",betNo,"k持续下注,码空后停止")
print("已开始运行，请启动")
hit=imread(r"image/hit.png",0)
double=imread(r"image/double.png",0)
split=imread(r"image/split.png",0)
buyin=imread(r"image/buyin.png",0)
win=imread(r"image/win.png",0)
lose=imread(r"image/lose.png",0)
unfocused=imread(r"image/unfocused.png",0)
doubleexp=imread(r"image/doubleexp.png",0)


Nowin,Nolose,ersh,unrecognizable=0,0,0,0#胜场负场计数
SDir,Shand1,Shand2,Sdp=-1,-1,-1,-1#上局信息
S2Dir,S2hand1,S2hand2,S2dp=-1,-1,-1,-1

while True:
    start_time = time()
    getouttimes=0
    current_time1=0
    while True:#反复检测下注和停牌按钮
        #事先读取按钮截图
        
        stand= imread(r"image/stand.png",0)#(854, 968)
        bet=imread(r"image/bet"+str(betNo)+"k.png",0)
        #本段用于通过检测鼠标位置实现程序的暂停循环
        cpause()#鼠标控制暂停函数
        #本段实现程序主功能，下注和做出打牌操作
        # 先截图
        try:
            screenshot('image/screen.png')
        except:
            ersh=ersh+1
            print("截图出错",ersh)
            continue
        # 读取图片 灰色会快
        temp = imread(r'image/screen.png',0)
        if (compare(stand,temp)==1):
            getouttimes=0
            Dir=-1
            hand1=-1
            hand2=-1
            s=0
            print("找到停牌按钮")
            tempheight, tempwidth = temp.shape[:2]
            # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
            scaleTemp=resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))   
            i=0
            while i<52:
                i=i+1
                target = imread(r'image/'+str(i)+'.png',0)
                theight, twidth=target.shape[:2]
    
                # 匹配图片
                res = matchTemplate(scaleTemp, target, TM_CCOEFF_NORMED)
                mn_val, max_val, min_loc, max_loc = minMaxLoc(res)
    
                if(max_val>=0.95):#匹配成功
                    if(max_loc[1]<353 and Dir==-1):
                        x1, y1, x2, y2 =max_loc[0],max_loc[1],max_loc[0]+15,max_loc[1]+15
                        scaleTemp[y1:y2, x1:x2] = 0
                        print("匹配庄家牌成功",max_loc,i)
                        Dir=poke(i)
                        SDir=Dir
                        print("庄家牌是",Dir)
                        i=i-1
                    elif((max_loc[0] in [d1 for d2 in handA for d1 in d2]) and hand1==-1):
                        x1, y1, x2, y2 =max_loc[0],max_loc[1],max_loc[0]+15,max_loc[1]+15
                        scaleTemp[y1:y2, x1:x2] = 0
                        print("匹配手牌A成功",max_loc,i)
                        hand1=poke(i)
                        Shand1=hand1
                        s=s+hand1
                        print("手牌A为",hand1)
                        i=i-1
                    elif((max_loc[0] in [d3 for d4 in handB for d3 in d4]) and hand2==-1):
                        x1, y1, x2, y2 =max_loc[0],max_loc[1],max_loc[0]+15,max_loc[1]+15
                        scaleTemp[y1:y2, x1:x2] = 0
                        print("匹配手牌B成功",max_loc,i)
                        hand2=poke(i)
                        Shand2=hand2
                        s=s+hand2
                        print("手牌B为",hand2)
                        i=i-1
                if s>20:s=20
            if(hand1==-1 or hand2==-1 or Dir==-1):
                continue
    
            if(hand1==hand2):#两张手牌相等查表3
                temp=hand1
                lisp=list3
            elif(hand1==11 or hand2==11):#含有Ace查表2
                if(hand1==11):temp=hand2
                if(hand2==11):temp=hand1
                lisp=list2
            else:#其他情况查表1
                temp=s-3
                lisp=list1
            if(lisp[temp-2][Dir-2]=='S'):#执行停牌
                wz=(852, 969)
                print("执行停牌\n\n")
                clickz(wz)
                Sdp='S'
                sleep(0.9)
            elif(lisp[temp-2][Dir-2]=='H'):#执行要牌
                wz=(594, 967)
                print("执行要牌（每1.6秒）\n\n")
                clickz(wz)
                Sdp='H'
                sleep(1.6)
                clickz((854, 969))
            elif(lisp[temp-2][Dir-2]=='D'):#执行加倍
                wz=(1123, 969)
                print("执行加倍\n\n")
                Sdp='D'
                clickz(wz)
                sleep(0.6)
            elif(lisp[temp-2][Dir-2]=='P'):#执行分牌
                wz=(1373, 969)
                print("执行分牌\n\n")
                clickz(wz)
                Sdp='P'
                sleep(0.6)
    
        elif (compare(bet,temp)==1):
            getouttimes=0
            print("找到下注按钮，并且点击（每0.01秒）")
            top_left = max_loc
            clickz(top_left)
            sleep(0.01)
            
        elif (compare(win,temp)==1):
            getouttimes=0
            if [S2Dir,S2hand1,S2hand2,S2dp]==[SDir,Shand1,Shand2,Sdp]:
                continue
            Nowin=Nowin+1
            rate=Nowin/(Nolose+Nowin)
            print("获胜,胜场数"+str(Nowin)+" 胜率：%.4f"%rate)
            write_sentence(Shand1,Shand2,SDir,Sdp,True,rate)
            S2Dir,S2hand1,S2hand2,S2dp=SDir,Shand1,Shand2,Sdp
            sleep(2)
            
        elif (compare(lose,temp)==1):
            getouttimes=0
            if [S2Dir,S2hand1,S2hand2,S2dp]==[SDir,Shand1,Shand2,Sdp]:
                continue
            Nolose=Nolose+1
            rate=Nowin/(Nolose+Nowin)
            print("失败,负场数"+str(Nolose)+" 胜率：%.4f"%rate)
            write_sentence(Shand1,Shand2,SDir,Sdp,False,rate)
            S2Dir,S2hand1,S2hand2,S2dp=SDir,Shand1,Shand2,Sdp
            sleep(2)
        
        else:
            print ("没找到，或先启动GOP3,21点(每0.2秒)")
            getouttimes=getouttimes+1
            current_time1=current_time1+1
            if current_time1>25:
                current_time = time()  # 获取当前时间
                elapsed_time = current_time - start_time  # 计算已经运行的时间
                if elapsed_time > 1800:  # 判断已经运行了30分钟
                    print("运行时间超过30min跳出一次")
                    pyautogui.click(88,46,button='left')#单击home
                    sleep(0.01)
                    break  # 跳出循环
                else:
                    current_time1=0
                    print("时间未到不跳出")
            elif getouttimes>7:
                print("多次未寻牌，跳出")
                break
            sleep(0.15)
    unfcs()

        

