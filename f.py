import random as r

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

def ΤΙΜΗ(v):
  if type(v) in {stat,var}:
    return v.timi
  return v

class stat:
  def __init__(self,timi):
    self.timi=timi
    self.typos=type(timi)

class var:
  def __init__(self,typos):
    self.typos=typos

  def ins(self,timi):
    if(type(timi)==self.typos):
      self.timi=timi
    else:
      print("λάθος τύπος δεδομένων")

  def __add__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self + v_
      if self.typos==other.typos and self.typos!=str:
        vtemp=var(self.typos)
        vtemp.ins(self.timi + other.timi)
        return vtemp
      if {self.typos,other.typos}=={float,int}:
        vtemp=var(float)
        vtemp.ins(self.timi + other.timi)
        return vtemp
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __sub__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self - v_
      if self.typos==other.typos and self.typos!=str:
        vtemp=var(self.typos)
        vtemp.ins(self.timi - other.timi)
        return vtemp
      if {self.typos,other.typos}=={float,int}:
        vtemp=var(float)
        vtemp.ins(self.timi - other.timi)
        return vtemp
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __mul__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self * v_
      if self.typos==other.typos and self.typos!=str:
        vtemp=var(self.typos)
        vtemp.ins(self.timi * other.timi)
        return vtemp
      if {self.typos,other.typos}=={float,int}:
        vtemp=var(float)
        vtemp.ins(self.timi * other.timi)
        return vtemp
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __truediv__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self / v_
      if self.typos==other.typos and self.typos!=str:
        vtemp=var(self.typos)
        vtemp.ins(self.timi / other.timi)
        return vtemp
      if {self.typos,other.typos}=={float,int}:
        vtemp=var(float)
        vtemp.ins(self.timi / other.timi)
        return vtemp
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __floordiv__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self // v_
      if {self.typos,other.typos}=={int}:
        vtemp=var(int)
        vtemp.ins(self.timi // other.timi)
        return vtemp
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __mod__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self % v_
      if {self.typos,other.typos}=={int}:
        vtemp=var(int)
        vtemp.ins(self.timi % other.timi)
        return vtemp
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __pow__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self ** v_
      if self.typos==other.typos and self.typos!=str:
        vtemp=var(self.typos)
        vtemp.ins(self.timi ** other.timi)
        return vtemp
      if {self.typos,other.typos}=={float,int}:
        vtemp=var(float)
        vtemp.ins(self.timi ** other.timi)
        return vtemp
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __lt__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self < v_
      if self.typos==other.typos:
        return self.timi < other.timi
      if {self.typos,other.typos}=={float,int}:
        return self.timi < other.timi
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __gt__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self > v_
      if self.typos==other.typos:
        return self.timi > other.timi
      if {self.typos,other.typos}=={float,int}:
        return self.timi > other.timi
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __le__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self <= v_
      if self.typos==other.typos:
        return self.timi <= other.timi
      if {self.typos,other.typos}=={float,int}:
        return self.timi <= other.timi
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __ge__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self >= v_
      if self.typos==other.typos:
        return self.timi >= other.timi
      if {self.typos,other.typos}=={float,int}:
        return self.timi >= other.timi
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __eq__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self == v_
      if self.typos==other.typos:
        return self.timi == other.timi
      if {self.typos,other.typos}=={float,int}:
        return self.timi == other.timi
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __ne__(self,other):
    try:
      if type(other) not in {stat,var}:
        v_=var(type(other))
        v_.ins(other)
        return self != v_
      if self.typos==other.typos:
        return self.timi != other.timi
      if {self.typos,other.typos}=={float,int}:
        return self.timi != other.timi
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

  def __neg__(self):
    try:
      if self.typos in {float,int}:
        return -self.timi
      print("λάθος τύπος δεδομένων")
    except:
      print("λάθος τύπος δεδομένων")

l=[chr(ord("a")+i) for i in range(26)]
l+=[chr(ord("A")+i) for i in range(26)]
l+=[chr(ord("α")+i) for i in range(25)]
l+=[chr(ord("Α")+i) for i in range(25) if i!=17]
letters=l

def _print(*t):
  s=""
  for i in t:
    if type(i) in {var,stat}:
      s+=str(i.timi)
    else:
      s+=str(i)
    s+=" "
  print(s)

def Rinput(v):
  #v variable
  global letters
  if v.typos==int:    #type(v)==int:
    v.ins(r.randrange(-100,100))
  if v.typos==float:  #type(v)==float:
    v.ins(r.random()*r.randrange(-100,100))
  if v.typos==str:    #type(v)==str:
    v.ins("".join(r.choices(letters,k=r.randrange(1,10))))
  print(">διαβάστηκε το",ΤΙΜΗ(v))
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

def xpr(s):
  #s list of characters
  pcmd=""
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
    if(s[0]=="!"):
      pcmd+="#"
      s.pop(0)
    if(s[:4]==list(" ΟΧΙ")):
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
    elif(s[:4]==list("ΑΡΧΗ") or s[:9]==list("ΠΡΟΓΡΑΜΜΑ") or s[:10]==list("ΜΕΤΑΒΛΗΤΕΣ") or s[:18]==list("ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ")):
      pcmd+="#"+"".join(s)
      s=[]
    else:
      pcmd+=s.pop(0)
  return(pcmd)

def interpret(fname="source"):
  fin=open(fname,'r')
  fout=open("source.py",'w')
  nsp=0
  nl=0
  block=deblock=fblock=pblock=False
  fout.write("import random as r\nimport math as m\nimport f as f\n")
  for line in fin:
    #print(fblock)
    pcmd=""
    nl+=1
    line=[w for w in line.split(" ") if w!=""]
    line=" ".join(line)
    cmd=[c for c in line][:-1]
    if(cmd[:5]==list("ΓΡΑΨΕ")):       #PRINT
      pcmd="f._print("+xpr(cmd[6:])+")"
    elif(cmd[:9]==list("ΑΚΕΡΑΙΕΣ:")):   #TYPES
      vars=line[10:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=f.var(int)\n"+" "*(nsp)
    elif(cmd[:12]==list("ΠΡΑΓΜΑΤΙΚΕΣ:")):
      vars=line[13:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=f.var(float)\n"+" "*(nsp)
    elif(cmd[:11]==list("ΧΑΡΑΚΤΗΡΕΣ:")):
      vars=line[12:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=f.var(str)\n"+" "*(nsp)
    elif(cmd[:8]==list("ΛΟΓΙΚΕΣ:")):
      vars=line[9:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=f.var(bool)\n"+" "*(nsp)
    elif(cmd[:7]==list("ΔΙΑΒΑΣΕ")):      #INPUT
      vars=line[8:-1].split(",")
      pcmd=",".join(vars)+"="
      for v in vars:
        pcmd+="f.Rinput("+str(v)+"),"
      pcmd=pcmd[:-1]
    elif(cmd[:2]==list("ΑΝ")):           #IF
      block=True
      pcmd="if("
      if(cmd[-4:]!=list("ΤΟΤΕ")):
        print(nl,":  λείπει η λέξη ΤΟΤΕ\n")
        cmd.append(" ΤΟΤΕ")
      pcmd+=xpr(cmd[3:-5])+"):"
    elif(cmd[:9]==list("ΑΛΛΙΩΣ_ΑΝ")):           #ELIF
      block=True
      nsp-=2
      pcmd="elif("
      if(cmd[-4:]!=list("ΤΟΤΕ")):
        print(nl,":  λείπει η λέξη ΤΟΤΕ\n")
        cmd.append(" ΤΟΤΕ")
      pcmd+=xpr(cmd[10:-5])+"):"
    elif(cmd[:6]==list("ΑΛΛΙΩΣ")):           #ELSE
      block=True
      nsp-=2
      pcmd="else:"
    elif(cmd[:8]==list("ΤΕΛΟΣ_ΑΝ")):    #ENDIF
      deblock=True
    elif(cmd[:3]==list("ΟΣΟ")):           #WHILE
      block=True
      pcmd="while("
      if(cmd[-9:]!=list("ΕΠΑΝΑΛΑΒΕ")):
        print(nl,":  λείπει η λέξη ΕΠΑΝΑΛΑΒΕ\n")
        cmd.append(" ΤΟΤΕ")
      pcmd+=xpr(cmd[4:-10])+"):"
    elif(cmd[:3]==list("ΓΙΑ")):           #FOR
      block=True
      pcmd="for "
      pos1=4
      while(pos1<len(cmd)):
        if(cmd[pos1:pos1+3]==list("ΑΠΟ")):
          break
        pos1+=1
      pcmd+=xpr(cmd[4:pos1])+" in range("
      pos2=pos1+4
      while(pos2<len(cmd)):
        if(cmd[pos2:pos2+5]==list("ΜΕΧΡΙ")):
          break
        pos2+=1
      pcmd+=xpr(cmd[pos1+4:pos2])+","
      pos3=pos2+6
      while(pos3<len(cmd)):
        if(cmd[pos3:pos3+7]==list("ΜΕ_ΒΗΜΑ")):
          break
        pos3+=1
      pos4=pos3+8
      if("ΜΕ_ΒΗΜΑ" in line):
        pcmd+=xpr(cmd[pos2+6:pos3])+"+1,"+xpr(cmd[pos4:])+"):"
      else:
        pcmd+=xpr(cmd[pos2+6:])+"+1):"
    elif(cmd[:16]==list("ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ")):    #ENDFOR/WHILE
      deblock=True
    elif(cmd[:15]==list("ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ")):    #DO
      block=True
      pcmd="while(True):"
    elif(cmd[:11]==list("ΜΕΧΡΙΣ_ΟΤΟΥ")):  #_WHILE
      deblock=True
      pcmd="if("+xpr(list("".join(cmd[12:])))+"):\n"+" "*(nsp+2)+"break"
    elif(cmd[:9]==list("ΣΥΝΑΡΤΗΣΗ")):           #FUNCTION
      fblock=True
      block=True
      pcmd="def "
      cmd=cmd[10:]
      for tpos in range(len(cmd)):
        if(cmd[tpos]==":"):
          cmd[tpos]="!"
          break
      fname=""
      for i in cmd:
        if(i=="("):
          break
        fname+=i
      pcmd+=fname+"("
      vargs="".join(cmd[len(fname)+1:tpos-1]).split(",")
      for a in vargs:
        pcmd+=a+"_,"
      pcmd=pcmd[:-1]+"):\n"
      #pcmd+=xpr(cmd[len(fname):tpos])+":"
      #pcmd+=" "*(nsp+2)+fname+"_V={}\n"
      #for a in vargs:
      #  pcmd+=" "*(nsp+2)+fname+"_V.add("+a+")\n"
      for a in vargs:
        pcmd+=" "*(nsp+2)+a+"="+a+"_\n"
        #f.ΤΙΜΗ("+a+"_)\n"
      pcmd=pcmd[:-1]
    elif(fblock and fname in line):             #RETURN
      pcmd="return "+xpr(cmd[len(fname):])[2:]
    elif(cmd[:16]==list("ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ")):    #ENDFUNCTION
      deblock=True
      fblock=False
      fname=""
    else:
      pcmd=xpr(cmd)
    if(pcmd not in ["","\n"]):
      fout.write(nsp*" "+pcmd+"\n")
    if(block):
      nsp+=2
      block=False
    elif(deblock):
      nsp-=2
      deblock=False
  fin.close()
  fout.close()
