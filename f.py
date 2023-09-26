import random as r
Dint,Dfl,Dstr,Dlg={},{},{},{}
def type(v):
  x=str(v)
  tnu=True
  for c in x:
    if c not in "-0123456789.":
      tnu=False
      break
  if tnu:
    s=x.count("-")
    if(s>1 or (s==1 and x[0]!="-")):
      return "str"
    p=x.count(".")
    if(p==0):
      return "int"
    if(p==1):
      return "fl"
  return "str"

l=[chr(ord("a")+i) for i in range(26)]
l+=[chr(ord("A")+i) for i in range(26)]
l+=[chr(ord("α")+i) for i in range(25)]
l+=[chr(ord("Α")+i) for i in range(25) if i!=17]
letters=l

def Rinput(v):
  #v variable
  global letters
  if type(v)=="int":
    v=r.randrange(-100,100)
  if type(v)=="fl":
    v=r.random()*r.randrange(-100,100)
  if type(v)=="str":
    v="".join(r.choices(letters,k=r.randrange(1,10)))
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
      pcmd="print("+xpr(cmd[6:])+")"
    elif(cmd[:9]==list("ΑΚΕΡΑΙΕΣ:")):   #TYPES
      vars=line[10:-1].split(",")
      pcmd=",".join(vars)+"="
      for v in vars:
        pcmd+="0,"
      pcmd=pcmd[:-1]
    elif(cmd[:12]==list("ΠΡΑΓΜΑΤΙΚΕΣ:")):
      vars=line[13:-1].split(",")
      pcmd=",".join(vars)+"="
      for v in vars:
        pcmd+="0.0,"
      pcmd=pcmd[:-1]
      if fblock:
        pcmd="#"+pcmd
    elif(cmd[:11]==list("ΧΑΡΑΚΤΗΡΕΣ:")):
      vars=line[12:-1].split(",")
      pcmd=",".join(vars)+"="
      for v in vars:
        pcmd+="\"Α\","
      pcmd=pcmd[:-1]
      if fblock:
        pcmd="#"+pcmd
    elif(cmd[:8]==list("ΛΟΓΙΚΕΣ:")):
      vars=line[9:-1].split(",")
      pcmd=",".join(vars)+"="
      for v in vars:
        pcmd+="False,"
      pcmd=pcmd[:-1]
      if fblock:
        pcmd="#"+pcmd
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
    elif(cmd[:16]==list("ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ")):    #ENDWHILE
      deblock=True
    elif(cmd[:9]==list("ΣΥΝΑΡΤΗΣΗ")):           #FUNCTION
      fblock=True
      block=True
      pcmd="def "
      cmd=cmd[10:]
      fname=""
      for i in cmd:
        if(i=="("):
          break
        fname+=i
      pcmd+=fname
      pcmd+=xpr(cmd[len(fname):])+":"
    elif(fblock and fname in line):             #RETURN
      pcmd="return"+xpr(cmd[len(fname):])[2:]
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
