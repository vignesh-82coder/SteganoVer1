from itertools import permutations
import random

from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import time

from .DH import findPrimitive, public, secret

start_time=time.time()

def index(request):
    return render(request,'index.html')



def encrypt(request):
    return render(request,'encrypt.html')

def decrypt(request):
    return render(request,'decrypt.html')


def generate(request):
    return render(request,'generate.html')

def PubKey(request):
    prime= request.GET.get('Prime number','none')
    n=int(prime)
    root = findPrimitive(n)
    pri = request.GET.get('Private key','none')
    private=int(pri)
    publickey = public(private,root,n)
    params={'PubKey':publickey , 'result':'Public key is :'}
    
    return render(request,"key.html",params)

def  eprocess(request):
    #creating an image object
    img=request.GET.get('png','none')
    imgpath="C:/Users/Jeevitha/Desktop/crypto/mini/static/mini/images/" + img
    im=Image.open(imgpath)
    
    #encrypt
    def encrypt(text):
        li = []

        def allPermutations(s):
            permList = permutations(s)
            for perm in list(permList):
                li.append("".join(perm))

        s = 'ACGT'
        allPermutations(s)
        ra = random.choice(li)

        textlist = []
        textlist = text
        Asciilist = []
        for i in textlist:
            c = ord(i)
            Asciilist.append(c)
        Binarylist = []
        for i in Asciilist:
            b = format(i, '08b')
            Binarylist.append(b)

        DnaPhaseone = []
        for i in Binarylist:
            e = i
            a = (e[6:])
            b = (e[4:6])
            c = (e[2:4])
            d = (e[0:2])
            DnaPhaseone.append(d)
            DnaPhaseone.append(c)
            DnaPhaseone.append(b)
            DnaPhaseone.append(a)
        DnaPhasetwo = []
        for i in range(len(ra)):
            DnaPhasetwo.append(ra[i])
    
        for i in DnaPhaseone:
            if i == "00":
                co = ra[0]
            elif i == "01":
                co = ra[1]
            elif i == "10":
                co = ra[2]
            else:
                co = ra[3]
            DnaPhasetwo.append(co)
        DnaPhasetwo.append("S")
    
        return DnaPhasetwo

    #loading the pixel data of image
    pix=im.load()
    lst=[]
    count=0
    lstp=[]
    size=im.width*im.height
    
    n=int(request.GET.get('Prime number','none'))
    root=findPrimitive(n)

    pS =request.GET.get('Private key of sender','none')
    privateSender=int(pS)
    pR=request.GET.get('Public key of receiver','none')
    publicReceiver=int(pR)
    SecretSender =secret(publicReceiver,privateSender,n)
    print('Secret sender', SecretSender)
    limitcheck =0
    lstdna=[]
    
    t=request.GET.get('Enter the message','none')
    lstdna=encrypt(t)
    i,e=0,0

    #for loop to extract and print all pixels
    for x in range(im.width):
        for y in range(im.height):
            count +=1

            if(count % SecretSender ==0):
                if y + SecretSender> im.height and x ==im.width -1:
                    limitcheck +=1
                co=x,y
                try:
                    if i ==len(lstdna):
                        e=i
                        break

                    [r,g,b]=im.getpixel(co)
                    c=im.getpixel(co)
                    b=b
                    e=lstdna[i]
                    b=ord(e)
                    val=(r,g,b)
                    im.putpixel(co,val)
                    pi = (im.getpixel((x,y)))
                    lst.append(c)
                    lst.append(pi)
                    i+=1

                except:
                    if i ==len(lstdna):
                        e=i
                        break
                    [r,g,b,a]=im.getpixel(co)
                    c=im.getpixel(co)
                    b=b
                    e=lstdna[i]
                    b=ord(e)
                    val=(r,g,b,a)
                    im.putpixel(co,val)
                    pi=(im.getpixel((x,y)))
                    lst.append(c)
                    lstp.append(pi)
                    i+=1

        if e ==len(lstdna):
            break
        if (limitcheck>0):
            return HttpResponse("limit reached please either change the image size or reduce the message")
    # print('lst val', lstdna)
    ename=request.GET.get('Name of encrypted image to be saved','none')
    
    sp='C:/Users/Jeevitha/Desktop/crypto/mini/static/mini/images/'+ename

    im.save(sp)
    
    return render(request,'edone.html')

def dprocess(request):

    #decrypt
    def decrypt (lst):
        se = []
        Binlst = []
        
        for i in range(4):
            se.append(lst[i])
    
        for i in range(4,len(lst)):
            
            if i == len(lst):
                break
            else:
                if lst[i] == se[0]:
                    Binlst.append("00")
                elif lst[i] == se[1]:
                    Binlst.append("01")
                elif lst[i]== se[2]:
                    Binlst.append("10")
                else:
                    Binlst.append("11")

    


        Asciilst = []
        for i in range(0, len(Binlst), 4):
            if i == len(Binlst):
                break
            e = Binlst[i]
            f = Binlst[i + 1]
            g = Binlst[i + 2]
            h = Binlst[i + 3]
            j = e + f + g + h
            Asciilst.append(j)

            Finallst = []
        for i in Asciilst:
            e = int(i, 2)
            st = chr(e)
            Finallst.append(st)
            sq = ''
            for i in Finallst:
                sq = sq + i
        
        return sq





    #loading the image
    img=request.GET.get('png','none')
    image="C:/Users/Jeevitha/Desktop/crypto/mini/static/mini/images/" + img
    im=Image.open(image)
    
    #loading the pixel data of the image
    pix=im.load()
    count=0
    lstdnaa=[]
    
    n=int(request.GET.get('Prime number','none'))
    root=findPrimitive(n)

    privateReceiver=int(request.GET.get('Private key of receiver','none'))
    publicSender=int(request.GET.get('Public key of sender','none'))

    SecretReceiver = secret(publicSender,privateReceiver,n)
    print('Secret Rec', SecretReceiver)

    e=''
    for x in range(im.width):
        for y in range(im.height):
            count+=1
            if (count%SecretReceiver==0):
                co =x,y
                try:
                    [r,g,b] =im.getpixel(co)
                    e=b
                    e = chr(e)
                    if e =="S":
                        break
                    lstdnaa.append(e)


                except:
                    [r,g,b,a]=im.getpixel(co)
                    e =b
                    e = chr(e)
                    if e =="S":
                        break
                    lstdnaa.append(e)


        if e =="S":
            break
    msg= decrypt(lstdnaa)
    param={'text':'The secret message is :','result':msg}

    return render(request,'ddone.html',param)