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



l=[chr(ord("a")+i) for i in range(26)]
l+=[chr(ord("A")+i) for i in range(26)]
l+=[chr(ord("α")+i) for i in range(25)]
l+=[chr(ord("Α")+i) for i in range(25) if i!=17]
letters=l
i0=r.randrange(-10**10,10**10)
f0=i0/r.randrange(1,10**10)
s0="".join(r.choices(letters,k=r.randrange(100,1000)))

def Rinput(v):
  #v variable
  global letters
  if v==int:
    v=(r.randrange(-100,100))
  elif v==float:
    v=(r.random()*r.randrange(-100,100))
  elif v==str:
    v=("".join(r.choices(letters,k=r.randrange(1,10))))
  elif type(v)==int:
    v=(r.randrange(-100,100))
  elif type(v)==float:
    v=(r.random()*r.randrange(-100,100))
  elif type(v)==str:
    v=("".join(r.choices(letters,k=r.randrange(1,10))))
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
  global i0,f0,s0
  fin=open(fname,'r')
  fout=open("source.py",'w')
  nsp=0
  nl=0
  block=deblock=fblock=pblock=False
  fout.write("import random as r\nimport math as m\nimport f as f\n\n")
  #fout.write("letters=[chr(ord(\"a\")+i) for i in range(26)]\n")
  #fout.write("letters+=[chr(ord(\"A\")+i) for i in range(26)]\n")
  #fout.write("letters+=[chr(ord(\"α\")+i) for i in range(25)]\n")
  #fout.write("letters+=[chr(ord(\"Α\")+i) for i in range(25) if i!=17]\n")
  #fout.write("i0=r.randrange(-10**10,10**10)\nf0=i0/r.randrange(1,10**10)\n")
  #fout.write("s0=\"\".join(r.choices(letters,k=r.randrange(100,1000)))\n\n")
  for line in fin:
    pcmd=""
    nl+=1
    line=[w for w in line.split(" ") if w!=""]
    line=" ".join(line)
    cmd=[c for c in line][:-1]
    if(cmd[:5]==list("ΓΡΑΨΕ")):       #PRINT
      pcmd="print("+xpr(cmd[6:])+")"
    elif(cmd[:9]==list("ΑΚΕΡΑΙΕΣ:")):   #TYPES
      vars=line[10:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=int\n"+" "*(nsp)
    elif(cmd[:12]==list("ΠΡΑΓΜΑΤΙΚΕΣ:")):
      vars=line[13:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=float\n"+" "*(nsp)
    elif(cmd[:11]==list("ΧΑΡΑΚΤΗΡΕΣ:")):
      vars=line[12:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=str\n"+" "*(nsp)
    elif(cmd[:8]==list("ΛΟΓΙΚΕΣ:")):
      vars=line[9:-1].split(",")
      pcmd=""
      for v in vars:
        pcmd+="try:\n"+" "*(nsp+2)+v+"=="+v+"\n"+" "*(nsp)+"except:\n"+" "*(nsp+2)+v+"=bool\n"+" "*(nsp)
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
          break
      fname=""
      for i in cmd:
        if(i=="("):
          break
        fname+=i
      pcmd+=fname+"("
      vargs="".join(cmd[len(fname)+1:tpos-1]).split(",")
      for a in vargs:
        pcmd+=a+","
      pcmd=pcmd[:-1]+"):\n"
      pcmd+="  global i0,f0,s0"
    elif(fblock and fname in line):             #RETURN
      pcmd="return "+xpr(cmd[len(fname):])[2:]
    elif(cmd[:16]==list("ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ")):    #ENDFUNCTION
      deblock=True
      fblock=False
      fname=""
      pcmd=" \n"
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
