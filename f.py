import random as r
import importlib  #reload module
from contextlib import redirect_stdout

iset,fset,cset,bset={},{},{},{}
def ΤΥΠΟΣ(v):
  global iset,fset,cset,bset
  if(v in iset):
    return int
  if(v in fset):
    return float
  if(v in bset):
    return bool
  return str

l=[chr(ord("a")+i) for i in range(26)]
l+=[chr(ord("A")+i) for i in range(26)]
l+=[chr(ord("α")+i) for i in range(25)]
l+=[chr(ord("Α")+i) for i in range(25) if i!=17]
letters=l

def Rinput(v):
  #v variable
  global letters
  ndigits=r.randrange(1,9)
  if v==int:
    v=(r.randrange(-10**ndigits,10**ndigits))
  elif v==float:
    v=(r.random()*r.randrange(-10**ndigits,10**ndigits))
  elif v==str:
    v=("".join(r.choices(letters,k=ndigits)))
  elif type(v)==int:
    v=(r.randrange(-10**ndigits,10**ndigits))
  elif type(v)==float:
    v=(r.random()*r.randrange(-10**ndigits,10**ndigits))
  elif type(v)==str:
    v=("".join(r.choices(letters,k=ndigits)))
  print(">διαβάστηκε το",v)
  return v

def TCinput(prompt=">"):
  temp=input(prompt)
  tfl=True
  for c in temp:
    if c not in "-0123456789.":
      tfl=False
      break
  if(tfl):
    s=temp.count("-")
    if(s>1 or (s==1 and temp[0]!="-")):
      return temp
    p=temp.count(".")
    if(p==0):
      return int(temp)
    if(p==1):
      return float(temp)
  return temp

def print2D(A):
  for r in range(1,A.shape[0]):
    row=""
    for c in range(1,A.shape[1]):
      row+=str(A[r][c])+" "
    print(row)

def xpr(s,pblock=False,v=[]):
  # s list of characters
  pcmd=""
  sarr=False
  while(s!=[]):
    if(s[0] in "\"\'"):
      pcmd+="\""
      while(True):
        s.pop(0)
        if(s[0] in "\"\'" or s==[]):
          pcmd+="\""
          s.pop(0)
          break
        else:
          pcmd+=s[0]
      if(s==[]):
        break
    elif(s[0]=="["):
      sarr=True
      pcmd+=s.pop(0)
    elif(s[0]=="]"):
      sarr=False
      pcmd+=s.pop(0)
    elif(s[0]=="," and sarr):
      pcmd+="]["
      s.pop(0)
    elif(s[:4]==list(" ΟΧΙ")):
      pcmd+=" not"
      s=s[4:]
    elif(s[:4]==list(" ΚΑΙ")):
      pcmd+=" and"
      s=s[4:]
    elif(s[:2]==list(" Ή")):
      pcmd+=" or"
      s=s[2:]
    elif(s[:2]==list("<>")):
      pcmd+="!="
      s=s[2:]
    elif(s[:2]==list("<=")):
      pcmd+="<="
      s=s[2:]
    elif(s[:2]==list(">=")):
      pcmd+=">="
      s=s[2:]
    elif(s[:3]==list("<--")):
      pcmd+="="
      s=s[3:]
    elif(s[0]=="="):
      pcmd+="=="
      s.pop(0)
    elif(s[0]=="^"):
      pcmd+="**"
      s.pop(0)
    elif(s[:6]==list("ΑΛΗΘΗΣ")):
      pcmd+="True"
      s=s[6:]
    elif(s[:6]==list("ΨΕΥΔΗΣ")):
      pcmd+="False"
      s=s[6:]
    elif(s[:3]==list("DIV")):
      pcmd+="//"
      s=s[3:]
    elif(s[:3]==list("MOD")):
      pcmd+="%"
      s=s[3:]
    elif(s[:4]==list("Τ_Ρ(")):
      pcmd+="m.sqrt("
      s=s[4:]
    elif(s[:4]==list("Α_Τ(")):
      pcmd+="abs("
      s=s[4:]
    elif(s[:4]==list("Α_Μ(")):
      pcmd+="int("
      s=s[4:]
    elif(s[:3]==list("ΗΜ(")):
      pcmd+="m.sin("
      s=s[3:]
    elif(s[:4]==list("ΣΥΝ(")):
      pcmd+="m.cos("
      s=s[4:]
    elif(s[:3]==list("ΕΦ(")):
      pcmd+="m.tan("
      s=s[3:]
    elif(s[:4]==list("ΛΟΓ(")):
      pcmd+="m.log("
      s=s[4:]
    elif(s[:2]==list("Ε(")):
      pcmd+="m.exp("
      s=s[2:]
    elif(s[:4]==list("ΑΡΧΗ") or s[:10]==list("ΜΕΤΑΒΛΗΤΕΣ")):
      pcmd+="#"+"".join(s)
      s=[]
    else:
      if(pblock):
        iINs=False
        for i in v:
          if list(i)==s:
            iINs=True
            pcmd+=i+"[0]"
            s=s[len(i):]
            break
          elif len(s)>len(i) and list(i)==s[:len(i)] and s[len(i)] in " +-*/^()=<>[":
            iINs=True
            pcmd+=i+"[0]"
            s=s[len(i):]
            break
      if(not pblock or not iINs):
        pcmd+=s.pop(0)
  return(pcmd)

def interpret(randIN=True,cmp=False,aa=1):
  fname="source"
  import importlib
  fin=open(fname,'r')
  fout=open(fname+".py",'w')
  nsp=0
  nl=0
  ifN=whN=dwhN=0
  exe=tryblock=mblock=block=deblock=fblock=pblock=False
  errmsg=""
  vargs=[]
  fout.write('''import random as r\nimport math as m\nimport numpy as np\nimport f as f\n
def _init(A,B):
  X=B.split(',')
  if(A[0]==int):
    for i in range(1,len(A)):
      A[i]=int(X[i-1])
  elif(A[0]==float):
    for i in range(1,len(A)):
      A[i]=float(X[i-1])
  else:
    A[1:]=X
\n''')
  try:
    for line in fin:
      pcmd=""
      comment=""
      for cmpos in range(len(line)):    #COMMENTS
        if(line[cmpos]=="!"):
          comment="   #"+line[cmpos+1:]
          line=line[:cmpos]
          break
      for i in range(cmpos-1,5,-1):     # SPACES tail
        if(line[i] not in " \n"):
          line=line[:i+1]
          break
      nl+=1
      line=[w for w in line.split(" ") if w!=""]
      line=" ".join(line)
      cmd=[c for c in line]

      if(line in " \n"):
        pcmd=xpr(cmd,pblock,vargs)
      elif(line[-1] in ",.@#$%^*(+={}[;:?/|"):
        errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ"
        raise Exception
      elif(cmd[:7]==list("ΓΡΑΨΕ2")):       #print2D
        pcmd="f.print2D("+xpr(cmd[8:],pblock,vargs)+")"
      elif(cmd[:6]==list("ΓΡΑΨΕ_")):       #print(line,end=' ')
        pcmd="print("+xpr(cmd[7:],pblock,vargs)+",end=\" \")"
      elif(cmd[:5]==list("ΓΡΑΨΕ")):                             #PRINT
        pcmd="print("+xpr(cmd[6:],pblock,vargs)+")"

      elif(cmd[:9]==list("ΑΚΕΡΑΙΕΣ:")):   #TYPES INT
        if(cmd[9]==' '):
          fvarpos=10
        else:
          fvarpos=9
        vars=line[fvarpos:].split(",")
        pcmd=""
        arr=False
        for v in vars:
          if("[" in v):
            vname="".join(v.split("[")[0])
            vdim1="".join([c for c in v.split("[")[1] if c!="]"])
            pcmd+="try:\n"+" "*(nsp+2)+vname+"=="+vname+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)
            arr=True
            dim=1
            pcmd+=vname+"=np.array((1+"+vdim1+")*["
            if("]" in v):
              arr=False
              pcmd+="int"+("]")+")\n"+" "*(nsp)
          elif("]" in v):
            dim+=1
            arr=False
            pcmd+="(1+"+v[:-1]+")*[int"+("]")*dim+")\n"+" "*(nsp)
          elif(arr):
            dim+=1
            pcmd+="(1+"+v+")*["
          else:
            pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=int\n"+" "*(nsp)
      elif(cmd[:12]==list("ΠΡΑΓΜΑΤΙΚΕΣ:")):   #TYPES FLOAT
        if(cmd[12]==' '):
          fvarpos=13
        else:
          fvarpos=12
        vars=line[fvarpos:].split(",")
        pcmd=""
        arr=False
        for v in vars:
          if("[" in v):
            vname="".join(v.split("[")[0])
            vdim1="".join([c for c in v.split("[")[1] if c!="]"])
            pcmd+="try:\n"+" "*(nsp+2)+vname+"=="+vname+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)
            arr=True
            dim=1
            pcmd+=vname+"=np.array((1+"+vdim1+")*["
            if("]" in v):
              arr=False
              pcmd+="float"+("]")+")\n"+" "*(nsp)
          elif("]" in v):
            dim+=1
            arr=False
            pcmd+="(1+"+v[:-1]+")*[float"+("]")*dim+")\n"+" "*(nsp)
          elif(arr):
            dim+=1
            pcmd+="(1+"+v+")*["
          else:
            pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=float\n"+" "*(nsp)
      elif(cmd[:11]==list("ΧΑΡΑΚΤΗΡΕΣ:")):   #TYPES STR
        if(cmd[11]==' '):
          fvarpos=12
        else:
          fvarpos=11
        vars=line[fvarpos:].split(",")
        pcmd=""
        arr=False
        for v in vars:
          if("[" in v):
            vname="".join(v.split("[")[0])
            vdim1="".join([c for c in v.split("[")[1] if c!="]"])
            pcmd+="try:\n"+" "*(nsp+2)+vname+"=="+vname+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)
            arr=True
            dim=1
            pcmd+=vname+"=np.array((1+"+vdim1+")*["
            if("]" in v):
              arr=False
              pcmd+="str"+("]")+")\n"+" "*(nsp)
          elif("]" in v):
            dim+=1
            arr=False
            pcmd+="(1+"+v[:-1]+")*[str"+("]")*dim+")\n"+" "*(nsp)
          elif(arr):
            dim+=1
            pcmd+="(1+"+v+")*["
          else:
            pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=str\n"+" "*(nsp)
      elif(cmd[:8]==list("ΛΟΓΙΚΕΣ:")):   #TYPES BOOL
        if(cmd[8]==' '):
          fvarpos=9
        else:
          fvarpos=8
        vars=line[fvarpos:].split(",")
        pcmd=""
        arr=False
        for v in vars:
          if("[" in v):
            vname="".join(v.split("[")[0])
            vdim1="".join([c for c in v.split("[")[1] if c!="]"])
            pcmd+="try:\n"+" "*(nsp+2)+vname+"=="+vname+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)
            arr=True
            dim=1
            pcmd+=vname+"=np.array((1+"+vdim1+")*["
            if("]" in v):
              arr=False
              pcmd+="bool"+("]")+")\n"+" "*(nsp)
          elif("]" in v):
            dim+=1
            arr=False
            pcmd+="(1+"+v[:-1]+")*[bool"+("]")*dim+")\n"+" "*(nsp)
          elif(arr):
            dim+=1
            pcmd+="(1+"+v+")*["
          else:
            pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=bool\n"+" "*(nsp)
      elif(cmd[:7]==list("ΔΙΑΒΑΣΕ")):      #INPUT
        temp=list(line[8:])
        parr=False
        for i in range(len(temp)):
          if(temp[i]=='['):
            parr=True
          elif(parr and temp[i]==','):
            temp[i]=']['
          elif(temp[i]==']'):
            parr=False
        temp="".join(temp)
        vars=temp.split(",")
        pcmd=",".join(vars)+"="
        for v in vars:
          pcmd+=("f.Rinput("+str(v)+"),")*(randIN)+"f.TCinput(),"*(1-randIN)
        pcmd=pcmd[:-1]
      elif(cmd[:2]==list("ΑΝ")):           #IF
        ifN+=1
        block=True
        pcmd="if("
        if(cmd[-4:]!=list("ΤΟΤΕ")):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ"
          raise Exception
        pcmd+=xpr(cmd[3:-5],pblock,vargs)+"):"
      elif(cmd[:9]==list("ΑΛΛΙΩΣ_ΑΝ")):           #ELIF
        block=True
        nsp-=2
        pcmd="elif("
        if(cmd[-4:]!=list("ΤΟΤΕ")):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ"
          raise Exception
        pcmd+=xpr(cmd[10:-5],pblock,vargs)+"):"
      elif(cmd[:6]==list("ΑΛΛΙΩΣ")):           #ELSE
        block=True
        nsp-=2
        pcmd="else:"
      elif(cmd[:8]==list("ΤΕΛΟΣ_ΑΝ")):    #ENDIF
        ifN-=1
        if(ifN<0):
          errmsg=(str(nl+1)+": ΠΕΡΙΣΣΟΤΕΡΕΣ ΤΕΛΟΣ_ΑΝ ΑΠΟ ΑΝ")
          raise Exception
        deblock=True
      elif(cmd[:3]==list("ΟΣΟ")):           #WHILE
        whN+=1
        block=True
        pcmd="while("
        if(cmd[-9:]!=list("ΕΠΑΝΑΛΑΒΕ")):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ"
          raise Exception
        pcmd+=xpr(cmd[4:-10],pblock,vargs)+"):"
      elif(cmd[:3]==list("ΓΙΑ")):           # FOR #
        whN+=1
        if("ΑΠΟ" not in line or "ΜΕΧΡΙ" not in line):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ"
          raise Exception
        block=True
        pos1=4
        while(pos1<len(cmd)):
          if(cmd[pos1:pos1+3]==list("ΑΠΟ")):
            break
          pos1+=1
        pos2=pos1+4
        while(pos2<len(cmd)):
          if(cmd[pos2:pos2+5]==list("ΜΕΧΡΙ")):
            break
          pos2+=1
        pos3=pos2+6
        while(pos3<len(cmd)):
          if(cmd[pos3:pos3+7]==list("ΜΕ_ΒΗΜΑ")):
            break
          pos3+=1
        pos4=pos3+8
        
        if("ΜΕ_ΒΗΜΑ" in line):
          pcmd="correction=1-2*("+xpr(cmd[pos4:],pblock,vargs)+"<0)\n"+" "*nsp
        else:
          pcmd="correction=1\n"+" "*nsp
        pcmd+="for "
        pcmd+=xpr(cmd[4:pos1],pblock,vargs)+" in range("
        pcmd+=xpr(cmd[pos1+4:pos2],pblock,vargs)+","
        if("ΜΕ_ΒΗΜΑ" in line):
          pcmd+=xpr(cmd[pos2+6:pos3],pblock,vargs)+"+correction,"+xpr(cmd[pos4:],pblock,vargs)+"):"
        else:
          pcmd+=xpr(cmd[pos2+6:],pblock,vargs)+" +1):"
      elif(cmd[:16]==list("ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ")):    #ENDFOR/WHILE
        whN-=1
        if(whN<0):          
          errmsg=(str(nl+1)+": ΠΕΡΙΣΣΟΤΕΡΕΣ ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ ΑΠΟ ΔΟΜΕΣ ΕΠΑΝΑΛΗΨΗΣ")
          raise Exception
        deblock=True
      elif(cmd[:15]==list("ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ")):    #DO
        dwhN+=1
        block=True
        pcmd="while(True):"
      elif(cmd[:11]==list("ΜΕΧΡΙΣ_ΟΤΟΥ")):  #_WHILE
        dwhN-=1
        if(dwhN<0):          
          errmsg=(str(nl+1)+": ΠΕΡΙΣΣΟΤΕΡΕΣ ΜΕΧΡΙΣ_ΟΤΟΥ ΑΠΟ ΔΟΜΕΣ ΕΠΑΝΑΛΗΨΗΣ")
          raise Exception
        deblock=True
        pcmd="if("+xpr(list("".join(cmd[12:])),pblock,vargs)
        pcmd+="):\n"+" "*(nsp+2)+"break"
      elif(cmd[:9]==list("ΠΡΟΓΡΑΜΜΑ")):                     # MAIN
        if(fblock or pblock or tryblock):
          errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
          raise Exception
        block=True
        mblock=True
        tryblock=True
        exe=True
        pcmd="def main():\n  try:"
      elif(cmd[:18]==list("ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ")):    #END MAIN
        tryblock=False
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ")
          raise Exception
        if(dwhN+whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ")
          raise Exception
        nsp=0
        pcmd="  except Exception as e:\n    print(\"ΒΡΕΘΗΚΕ ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ...\")\n    print(getattr(e, 'message', repr(e)))"
        pcmd+="\n#ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\n"
      elif(cmd[:9]==list("ΣΥΝΑΡΤΗΣΗ")):           #FUNCTION
        if(fblock or pblock or tryblock):
          errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
          raise Exception
        fblock=True
        block=True
        pcmd="def "
        cmd=cmd[10:]
        for tpos in range(len(cmd)):
          if(cmd[tpos]==":"):
            break
        fname=""
        for i in cmd:
          if(i=="("):
            break
          fname+=i
        ftypos="".join(cmd[tpos+1:])
        if ftypos[0]==" ":
          ftypos=ftypos[1:]
        if ftypos=="ΑΚΕΡΑΙΑ":
          ftypos=int
        elif ftypos=="ΠΡΑΓΜΑΤΙΚΗ":
          ftypos=float
        elif ftypos=="ΧΑΡΑΚΤΗΡΑΣ":
          ftypos=str
        else:         #ΛΟΓΙΚΗ
          ftypos=bool

        pcmd+=fname+"("
        vargs="".join(cmd[len(fname)+1:tpos-1]).split(",")
        for a in vargs:
          pcmd+=a+","
        pcmd=pcmd[:-1]+"):\n  " #function parameter list

        pcmd+="#"+str(ftypos)+"\n  "

        for a in vargs:
          pcmd+="_"+a+","
        pcmd=pcmd[:-1]+"="  #backup values for mutable
        for a in vargs:
          pcmd+=a+","
        pcmd=pcmd[:-1]
      elif(fblock and fname in line):                   #RETURN
        pcmd="_"+fname+" ="+xpr(cmd[len(fname):])[2:]
      elif(cmd[:16]==list("ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ")):         #ENDFUNCTION
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ")
          raise Exception
        if(dwhN+whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ")
          raise Exception
        for a in vargs:
          pcmd+=a+","
        pcmd=pcmd[:-1]+" = "  #restore values
        for a in vargs:
          pcmd+="_"+a+","
        pcmd=pcmd[:-1]+"\n  "
        pcmd+="return "+"_"+fname
        deblock=True
        fblock=False
        fname=""
        pcmd+="\n#ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ\n"
      elif(cmd[:10]==list("ΔΙΑΔΙΚΑΣΙΑ")):           #PROCEDURE
        if(fblock or pblock or tryblock):
          errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
          raise Exception
        pblock=True
        block=True
        pcmd="def "
        cmd=cmd[11:]
        fname=""
        for i in cmd:
          if(i=="("):
            break
          fname+=i
        pcmd+=fname+"("
        vargs="".join(cmd[len(fname)+1:-1]).split(",")
        for a in vargs:
          pcmd+=a+","
        pcmd=pcmd[:-1]+"):"
      elif(cmd[:17]==list("ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ")):    #ENDPROCEDURE
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ")
          raise Exception
        if(dwhN+whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ")
          raise Exception
        pblock=False
        deblock=True
        fname=""
        pcmd="\n#ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\n"
      elif(cmd[:6]==list("ΚΑΛΕΣΕ")):          #ΚΑΛΕΣΕ
        for i in range(len(cmd)):
          if cmd[i]=="(":
            break
        fname="".join(cmd[7:i])
        pV=[v for v in "".join(cmd[i+1:-1]).split(",")]
        pcmd=""
        for v in pV:
          pcmd+=v+","
        pcmd=pcmd[:-1]+"="
        for v in pV:
          pcmd+="["+v+"],"
        pcmd=pcmd[:-1]+"\n"                               #load
        pcmd+=" "*(nsp)+"".join(cmd[7:])+"\n"+" "*(nsp)   #call
        for v in pV:                                      #unload
          pcmd+=v+","
        pcmd=pcmd[:-1]+"="
        for v in pV:
          pcmd+=v+"[0],"
        pcmd=pcmd[:-1]
      elif("<--" in line):
        pcmd=xpr(cmd,pblock,vargs)
      elif("ΜΕΤΑΒΛΗΤΕΣ" in line):
        pcmd=xpr(cmd,pblock,vargs)
      elif("ΑΡΧΗ" in line):
        pcmd=xpr(cmd,pblock,vargs)
      elif("_" in line[:1]):
        pcmd=xpr(cmd,pblock,vargs)
      else:
        errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ"
        raise Exception

      if(pcmd not in ["","\n"]):              # save line
        fout.write(nsp*" "+pcmd+comment+"\n")
      if(block):
        nsp+=2
        block=False
      elif(deblock):
        nsp-=2
        deblock=False
      if(mblock):
        nsp+=2
        mblock=False

    if(fblock+pblock+tryblock!=0):              #ΤΕΛΟΣ ΠΡΟΓΡΑΜΜΑΤΟΣ
      errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
      raise Exception
    fin.close()
    fout.close()
  except:
    print("[error] "+errmsg+"\n> "+str(nl+1)+". "+line)
    return
  import source
  importlib.reload(source)
  if(exe):
    if(cmp):
      with open('log'+str(aa),'w') as lfile:
        with redirect_stdout(lfile):
          source.main()
    else:
      source.main()
