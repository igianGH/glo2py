import difflib as dfl
import traceback
import sys
import random as r
import importlib  #reload module
from contextlib import redirect_stdout

def testversion():
  print(">",end="")
  print("1604250144")
def rword(w):
  return [w,w+' ',w+'\n']
def isindex(i):
  if(i>0):
    return i-1
  return 1.

def evaluate(fname="source"):
  fOUT=open(fname+".py",'w')
  fOUT.write('''import random as r
import math as m
import numpy as np
import __ as _
import sys
import traceback

class NUM:
  def __init__(self,value=1):
    self.value=value
  def __mul__(self,x):
    return self.value*x**1
  def __rmul__(self,x):
    return NUM(x**1)
\n''')  
  with open(fname,'r') as fIN:
    X=xpr([c for c in fIN.read()])
    fOUT.write("def main():\n  N1=NUM()\n")
    fOUT.write("  print("+X+')\n')
  fOUT.close()
  ##EXECUTION
  source=__import__(fname)
  importlib.reload(source)
  try:
    source.main()
  except Exception as e:
    errmsg=getattr(e, 'message', repr(e))
    print("[error] "+errmsg+"\n--> "+X)
  

def source(code,fname="source"):
  with open(fname,'w') as f:
    f.write(code)

def interpret(file="source",ftrb=False,dline=True,segment=False,report=False,randIN=True,test=False):
  try:
    interpretM(file,segment=segment,report=str(report),randIN=randIN,test=test)
  except:
    errmsg2=""
    errmsg=str(sys.exc_info()[1])
    trb=str(traceback.format_exc())
    sb=trb[0:]
    if(ftrb):
      print("\n"+trb)
    ierr=trb.find("Error:")
    trb=trb[ierr:]
    if('%' in trb):
      imod=trb.find('%')
      trb=trb[:imod]+"MOD"+trb[imod+1:]
    if("\'type\' and \'type\'" in sb and "unsupported operand" in sb 
       or "not supported between instances" in sb and "\'type\'" in sb):
      linecorr=1
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:\nΑΠΟΤΥΧΙΑ ΑΠΟΤΙΜΗΣΗΣ ΕΚΦΡΑΣΗΣ, Κάποια μεταβλητή δεν έχει λάβει τιμή?"
    elif("yntax" in sb or "efined" in sb or "unsupported operand" in sb 
    or "only concatenate" in sb or "no attribute \'value\'" in sb): # or "TypeError"
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      linecorr=1
      if("comma" in sb):
        errmsg2+="\nΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ, Μήπως ξεχάσατε κάποιο κόμμα?"
      elif("name" in sb and "not defined" in sb):
        errmsg2+="\nΗ ΜΕΤΑΒΛΗΤΗ "+sb[sb.find("name \'")+6:sb.find("\' is not defined")]+" ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ"
      elif("unsupported operand" in sb or "only concatenate" in sb):
        errmsg2+="\nΠΡΑΞΗ ΜΕΤΑΞΥ ΑΣΥΜΒΑΤΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ"
      elif("no attribute \'value\'" in sb):
        errmsg2+="\nΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ, αυτό το αντικείμενο δεν είναι πίνακας"
      else:
        errmsg2+="\n> "+trb.split('\n')[0]
    else:
      linecorr=1
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      if("invalid literal" in sb):
        errmsg2+="\nΕΚΧΩΡΗΣΗ ΤΙΜΗΣ ΛΑΝΘΑΣΜΕΝΟΥ ΤΥΠΟΥ"
      elif("index" in sb and "out of bounds" in sb or "valid indices" in sb
          or "indices must be integers" in sb):
        errmsg2+="\nΥΠΕΡΒΑΣΗ ΟΡΙΩΝ ΠΙΝΑΚΑ"
      elif("division by zero" in sb):
        errmsg2+="\nΔΙΑΙΡΕΣΗ ΜΕ 0 (ΜΗΔΕΝ)"
      elif("math domain error" in sb):
        errmsg2+="\nΔΕΝ ΟΡΙΖΕΤΑΙ Η ΜΑΘΗΜΑΤΙΚΗ ΠΡΑΞΗ"
      else:
        errmsg2+="\n> "+trb.split('\n')[0]
    print("-"*75+'\n'+errmsg2)
    msnl=snl=0
    msnl=sb[:]
    foundline=False
    while("#//" in msnl):
      foundline=True
      msnl=msnl[msnl.find("#//")+3:]
    if(foundline):
      for i in range(len(msnl)):
        if(msnl[i] not in "0123456789"):
          msnl=msnl[:i]
          break
      msnl=int(msnl)
    else:
      with open(file+".py",'r') as fin:
        msize=0
        for line in fin:
          if("#//" in line):            # εύρεση γραμμής όπου απέτυχε η μετάφραση/εκτέλεση
            snl=int(line[line.find("#//")+3:])
          ics=dfl.SequenceMatcher(None,line,sb).find_longest_match()
          if(msize<ics.size):
            msize=ics.size
            cssq=line
            msnl=snl
    if(foundline or msize>0):
      fin=open(file,'r')
      snl=linecorr
      lines=(line for line in fin)
      try:
        while(True):
          line=next(lines)
          snl+=1
          if(snl==msnl):
            while(line[0]==' '):
              line=line[1:]
            #print(" "*6+str(snl+0-linecorr)+". ",line[:-1])
            if(dline):
              line=next(lines)
              snl+=1
              print("----> "+str(snl+0-linecorr)+". ",line[:])
            break
      except StopIteration:
        print("reached EOF")

def compare(fn1="source1",fn2="source2",randIN=True):
  interpretM(fname=fn1,cmp=True,aa=1,randIN=True)
  interpretM(fname=fn2,cmp=True,aa=2,randIN=True)
  f1,f2=open("log1",'r'),open("log2",'r')
  l1,l2=(line for line in f1),(line for line in f2)
  try:
    while(True):
      line1,line2 = next(l1),next(l2)
      if(line1!=line2):
        print(line1[:-1]+" | "+line2)
  except StopIteration:
    f1.close()
    f2.close()

def typos(x):
  x0=x
  try:
    for i in range(len(x.shape)):
      x0=x0[0]
  except:
    x0=x
  if(x0 in {int,float,str,bool}):
    return x0
  else:
    return type(x0)

l=[chr(ord("a")+i) for i in range(26)]
l+=[chr(ord("A")+i) for i in range(26)]
l+=[chr(ord("α")+i) for i in range(25)]
l+=[chr(ord("Α")+i) for i in range(25) if i!=17]
letters=l
Reserved="ΠΡΟΓΡΑΜΜΑ,ΣΥΝΑΡΤΗΣΗ,ΔΙΑΔΙΚΑΣΙΑ,ΜΕΤΑΒΛΗΤΕΣ,ΣΤΑΘΕΡΕΣ,ΑΚΕΡΑΙΕΣ,ΠΡΑΓΜΑΤΙΚΕΣ,ΧΑΡΑΚΤΗΡΕΣ,ΑΛΗΘΗΣ,"
Reserved+="ΑΡΧΗ,ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ,ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ,ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ,ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ,ΤΕΛΟΣ_ΑΝ,"
Reserved+="ΑΝ,ΤΟΤΕ,ΑΛΛΙΩΣ_ΑΝ,ΑΛΛΙΩΣ,ΕΠΙΛΕΞΕ,ΠΕΡΙΠΤΩΣΗ,ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ,ΟΣΟ,ΕΠΑΝΑΛΑΒΕ,ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ,"
Reserved+="ΜΕΧΡΙΣ_ΟΤΟΥ,ΓΙΑ,ΑΠΟ,ΜΕΧΡΙ,ΜΕ_ΒΗΜΑ,ΗΜ,ΣΥΝ,ΕΦ,ΛΟΓ,Ε,Α_Τ,Α_Μ,Τ_Ρ,MOD,DIV,ΟΧΙ,ΚΑΙ,Ή,ΨΕΥΔΗΣ"
Reserved=Reserved.split(",")

def Rinput(v,report=False):
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
  if(report):
    print(">διαβάστηκε το",v)
  return v

def TCinput(prompt="> "):
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
  sarr=sfunc=False
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
      pcmd+=".value"+s.pop(0)+"_.isindex("
    elif(s[0]=='(' and sarr):
      sfunc=True
      pcmd+=s.pop(0)
    elif(s[0]==')' and sfunc and sarr): #array and function
      sfunc=False
      pcmd+=s.pop(0)
    elif(s[0]=="]"):
      sarr=False
      pcmd+=")"+s.pop(0)
    elif(s[0]=="," and sarr and not sfunc):
      pcmd+=")][_.isindex("
      s.pop(0)
    elif(s[:4]==list("ΟΧΙ ") or s[:4]==list("ΟΧΙ(")):
      pcmd+="not"
      s=s[3:]
    elif(s[:4]==list("ΚΑΙ ") or s[:4]==list("ΚΑΙ(")):
      pcmd+="and"
      s=s[3:]
    elif(s[:2]==list("Ή ") or s[:2]==list("Ή(")):
      pcmd+="or"
      s=s[1:]
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
    elif(s[0]=="+"):
      pcmd+="+0+"
      s.pop(0)
    elif(s[0]=="*"):
      pcmd+="*N1*"
      s.pop(0)
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
      pcmd+="m.sin(m.pi/180*"
      s=s[3:]
    elif(s[:4]==list("ΣΥΝ(")):
      pcmd+="m.cos(m.pi/180*"
      s=s[4:]
    elif(s[:3]==list("ΕΦ(")):
      pcmd+="m.tan(m.pi/180*"
      s=s[3:]
    elif(s[:4]==list("ΛΟΓ(")):
      pcmd+="m.log("
      s=s[4:]
    elif(s[:2]==list("Ε(")):
      pcmd+="m.exp("
      s=s[2:]
    else:
      if(pblock):
        iINs=False
        for i in v:
          if list(i)==s:
            iINs=True
            pcmd+=i+"[0]"
            s=s[len(i):]
            break
          elif len(s)>len(i) and list(i)==s[:len(i)] and s[len(i)] in " +-*/^()=<>[\n":
            iINs=True
            pcmd+=i+"[0]"
            s=s[len(i):]
            break
      if(not pblock or not iINs):
        pcmd+=s.pop(0)
  return(pcmd)

def isname(s):
  global letters
  if s[0] not in letters:
    return False
  for c in s[1:]:
    if c not in letters+list("_0123456789"):
      return False
  return True

def interpretM(file="source",randIN=True,cmp=False,aa=1,segment=False,report="False",test=False):
  import importlib
  global letters,Reserved
  fin=open(file+"_",'w')
  with open(file) as fraw:      #'&' στην αρχή πρότασης
    lineG=(line for line in fraw)
    line1=next(lineG)[:-1]
    while(True):
      try:
        line2=next(lineG)[:-1]
        while(len(line2)>0 and line2[0]==' '):    # remove wspace from start
          line2=line2[1:]
        if(len(line2)<1 or line2[0]=='&'):  # merge 2+ lines
          line1+=' '+line2[1:]
        else:#elif(line1!=""):
          fin.write(line1+"\n")
          line1=line2[:]
        #else:
          #line1=line2[:]
      except:
        fin.write(line1+"\n")
        break
  fin.close()
  fin=open(file+"_",'r')
  fout=open(file+".py",'w') #import conflict
  nsp=0
  nl=0
  PROname=fname=pline=""
  swN=ifN=whN=dwhN=0
  whv,whstep=[],[]
  cdict,vdict={},{}
  intl=floatl=strl=booll=False
  acounter=0
  vblock=cblock=ablock=exe=tryblock=mblock=block=deblock=fblock=pblock=False
  errmsg=""#"ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: L289"
  vargs=[]
  fout.write('''import random as r
import math as m
import numpy as np
import __ as _
import sys
import traceback

class NUM:
  def __init__(self,value=1):
    self.value=value
  def __mul__(self,x):
    return self.value*x**1
  def __rmul__(self,x):
    return NUM(x**1)
class myA:
  def __init__(self,shape,typos):
    A=[typos for i in range(shape.pop(-1))]
    d=1
    while(shape!=[]):
      d+=1
      A=[A[:] for i in range(shape.pop(-1))]
    self.value=A
    self.typos=typos
    self.dimension=d
  def COPY(self,other):
    self.value=other
    print(\"_\"*75+\"\\nΠΡΟΣΟΧΗ: δεν επιτρέπεται στη ΓΛΩΣΣΑ\\n\")
  def ΤΙΜΕΣ(self):
    if(self.dimension==1 and len(self.value)<21):
      print(self.value)
      return \"_\"*75+\"\\nΠΡΟΣΟΧΗ: δεν επιτρέπεται στη ΓΛΩΣΣΑ\\n\"
    n=0
    for l in self.value:
      n+=1
      print(n,l)
    return \"_\"*75+\"\\nΠΡΟΣΟΧΗ: δεν επιτρέπεται στη ΓΛΩΣΣΑ\\n\"
\n''')
  if(segment):
    nsp=2
    exe=True
    fout.write("def main():\n")
  try:
    for line in fin:
      nl+=1
      pcmd=""
      comment=""
      if(pline!=""):
        line=pline+line
        pline=""
      for cmpos in range(len(line)):    #COMMENTS
        if(line[cmpos]=="!"):
          comment=("   #"+line[cmpos+1:]).replace("\n","")
          line=line[:cmpos]
          break
      for i in range(cmpos-1,5,-1):     # SPACES tail
        if(line[i] not in " \n"):
          line=line[:i+1]
          break
      if(line!="" and line[-1]=='&'):
        pline=line[:-1]
        continue
      while(True):
        if("  " not in line):
          break
        dsp=line.find("  ")
        line=line[:dsp]+line[dsp+1:]
      lineNS,cflags=line.replace(" ",""),"[] [, ,] (, ,) ,, .. ,. .,".split(" ")
      if(line.count('\"')%2==1 or line.count('\'')%2==1):
        errmsg="ΜΗ ΕΓΚΥΡΗ ΧΡΗΣΗ ΕΙΣΑΓΩΓΙΚΩΝ"
        raise Exception
      while("\"" in lineNS):      # ignore "strings"
        pos1=lineNS.find("\"")
        pos2=lineNS[pos1+1:].find("\"")+pos1+1
        if("\'" in lineNS[pos1:pos2]):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΧΡΗΣΗ ΕΙΣΑΓΩΓΙΚΩΝ"
          raise Exception
        lineNS=lineNS[:pos1]+lineNS[pos2+1:]
      while("\'" in lineNS):      # ignore 'strings'
        pos1=lineNS.find("\'")
        pos2=lineNS[pos1+1:].find("\'")+pos1+1
        lineNS=lineNS[:pos1]+lineNS[pos2+1:]
      if("ΠΕΡΙΠΤΩΣΗ" in lineNS and ",..," in lineNS):
        lineNS=lineNS[:lineNS.find(",..,")]+lineNS[lineNS.find(",..,")+4:]
      for i in cflags:
        if(i in lineNS):
          errmsg="ΜΗΠΩΣ ΞΕΧΑΣΑΤΕ ΚΑΠΟΙΟ ΟΡΙΣΜΑ?"
          raise Exception
      lpar=rpar=lc=rc=0
      for i in line:
        match i:
          case '(':
            lpar+=1
          case ')':
            rpar+=1
          case '[':
            lc+=1
          case ']':
            rc+=1
        if(lpar<rpar):
          errmsg="ΠΛΕΟΝΑΖΟΥΣΑ ΔΕΞΙΑ ΠΑΡΕΝΘΕΣΗ"
          raise Exception
        elif(lc<rc):
          errmsg="ΠΛΕΟΝΑΖΟΥΣΑ ΔΕΞΙΑ ΑΓΚΥΛΗ"
          raise Exception
      if(lpar>rpar):
        errmsg="ΑΝΟΙΧΤΟ ΜΠΛΟΚ ΠΑΡΕΝΘΕΣΕΩΝ"
        raise Exception
      if(lc>rc):
        errmsg="ΑΝΟΙΧΤΟ ΜΠΛΟΚ ΑΓΚΥΛΩΝ"
        raise Exception
      line=[w for w in line.split(" ") if w not in " "] # != ""," "
      for w in line:
        if(w[0]==" "):
          w.pop(0)
      line=" ".join(line)
      cmd=[c for c in line]

      if(line in " \n"):
        pcmd=xpr(cmd,pblock,vargs)
      elif(line[-1] not in letters+list("0123456789])\n\t\"\' ")):
        #in ",.@#$%^*(+={}[;:?/|"):
        errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: ΑΝΤΙΚΑΝΟΝΙΚΟΣ ΤΕΡΜΑΤΙΣΜΟΣ ΓΡΑΜΜΗΣ"
        raise Exception

      elif(line in rword("ΣΤΑΘΕΡΕΣ")):               #CONSTANTS
        if(cblock+vblock+ablock):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: ΑΝΤΙΚΑΝΟΝΙΚΗ ΕΝΑΡΞΗ ΔΗΛΩΤΙΚΟΥ ΤΜΗΜΑΤΟΣ ΣΤΑΘΕΡΩΝ"
          raise Exception
        cblock=True
        #cdict[fname]=dict()
        pcmd="#"+line
      elif(line in rword("ΜΕΤΑΒΛΗΤΕΣ")):            #VARIABLES
        if(vblock+ablock):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: ΑΝΤΙΚΑΝΟΝΙΚΗ ΕΝΑΡΞΗ ΔΗΛΩΤΙΚΟΥ ΤΜΗΜΑΤΟΣ ΜΕΤΑΒΛΗΤΩΝ"
          raise Exception
        cblock=False
        vblock=True
        #vdict[fname]=dict()
        pcmd="#"+line
      elif(line in rword("ΑΡΧΗ")):                     #ΑΡΧΗ
        cblock=vblock=False
        acounter-=1
        ablock=True
        intl=floatl=strl=booll=False
        pcmd="#"+line
        if(test):
          print("ΥΠΟΠΡΟΓΡΑΜΜΑ:",fname,
                "ΣΤΑΘΕΡΕΣ:",list(cdict[fname].keys()),
                "ΜΕΤΑΒΛΗΤΕΣ:",list(vdict[fname].keys()))       #full variable report
      elif(cblock):                                            #CBLOCK
        if(line.count('=')==1):
          eqpos=line.find('=')
          cname=line[:eqpos]
          if(cname[-1]==" "):
            cname=cname[:-1]
          if(not isname(cname)):
            errmsg=cname+" : ΜΗ ΕΓΚΥΡΟ ΟΝΟΜΑ ΣΤΑΘΕΡΑΣ"
            raise Exception
          cvalue=line[eqpos+1:]
          if(cvalue[-1]==" "):
            cvalue=cvalue[:-1]
          if(cname in cdict[fname].keys()):
            errmsg=cname+" : ΕΧΕΙ ΔΗΛΩΘΕΙ ΠΑΡΑΠΑΝΩ"
            raise Exception
          elif(cname in Reserved):
            errmsg=cname+" : ΔΕΣΜΕΥΜΕΝΗ ΛΕΞΗ"
            raise Exception
          else:
            cdict[fname][cname]=cvalue
          pcmd=cname+"="+cvalue
        else:
          errmsg="ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΣΤΑΘΕΡΑΣ"# / <cname> = <cvalue>"
          raise Exception
      elif(vblock):                                               #VBLOCK
        if(line.count(":")!=1):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΜΕΤΑΒΛΗΤΩΝ"
          raise Exception
        clpos=line.find(":")
        vtype=line[:clpos]
        if(vtype[-1]==" "):
          vtype=vtype[:-1]
        match vtype:
          case "ΑΚΕΡΑΙΕΣ":
            vtype="int"
            if(intl):
              errmsg="ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΑΚΕΡΑΙΩΝ"
              raise Exception
            intl=True
          case "ΠΡΑΓΜΑΤΙΚΕΣ":
            vtype="float"
            if(floatl):
              errmsg="ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΠΡΑΓΜΑΤΙΚΩΝ"
              raise Exception
            floatl=True
          case "ΧΑΡΑΚΤΗΡΕΣ":
            vtype="str"
            if(strl):
              errmsg="ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΧΑΡΑΚΤΗΡΩΝ"
              raise Exception
            strl=True
          case "ΛΟΓΙΚΕΣ":
            vtype="bool"
            if(booll):
              errmsg="ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΛΟΓΙΚΩΝ"
              raise Exception
            booll=True
          case default:
            errmsg="ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΜΕΤΑΒΛΗΤΩΝ"
            raise Exception
        fvarpos=clpos+1
        while(cmd[fvarpos]==' '):
          fvarpos+=1
        line=line[fvarpos:]
        if(line in " "):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΜΕΤΑΒΛΗΤΩΝ"
          raise Exception
        tvars=(line.replace(' ','')).split(",")
        vars=[tvars.pop(0)]
        for v in tvars:
          if(vars[-1].count('[')==vars[-1].count(']')):
            vars.append(v)
          else:
            vars[-1]+=(','+v)
        pcmd=""
        for v in vars:
          vval=vtype
          if("[" in v):
            lbrpos,rbrpos=v.find("["),v.find("]")
            vname=v[:lbrpos]#+".value"
            if(vname[-1]==" "):
              vname=vname[:-1]
            vdim=(v[lbrpos+1:rbrpos].replace(" ",""))#.split(",")
            for i in range(len(vdim)-1,-1,-1):
              vval="("+xpr(list(vdim[i]))+")*["+vval+"]"              #expression in Shape
            vval="myA(["+vdim+"],"+vtype+")"#"np.array("+vval+")"
          else:
            vname=v
            if(vname[-1]==" "):
              vname=vname[:-1]
          if(vname in vdict[fname].keys() or vname in cdict[fname].keys()):
            errmsg=vname+" : ΕΧΕΙ ΔΗΛΩΘΕΙ ΠΑΡΑΠΑΝΩ"
            raise Exception
          elif(vname in Reserved):
            errmsg=vname+" : ΔΕΣΜΕΥΜΕΝΗ ΛΕΞΗ"
            raise Exception
          elif(not isname(vname)):
            errmsg=vname+" : ΜΗ ΕΓΚΥΡΟ ΟΝΟΜΑ ΜΕΤΑΒΛΗΤΗΣ"
            raise Exception
          else:
            vdict[fname][vname]=vtype
            vdict[fname][vname+".value"]=vtype
          pcmd+="try:\n"+" "*(nsp+2)+vname+"=="+vname+"\n"+" "*(nsp)
          pcmd+="except:\n"+" "*(nsp+2)
          pcmd+=vname+"="+vval+"\n"+" "*(nsp)

      elif(line.count("<--")==1 and ablock and                                             #ASSIGNMENT
           not( fname in line and line[len(fname)] not in letters+list("0123456789_") )):   #return handled elsewhere
        aspos=line.find("<--")
        vname=line[:aspos]
        if(vname[-1]==" "):
          vname=vname[:-1]
        if("[" in vname):
          lbrpos=vname.find("[")
          vname=vname[:lbrpos]
        if(vname not in vdict[fname].keys() and vname!=fname):
          errmsg="ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ "+vname
          if(fname=="_main_"):
            print("ΤΟ ΠΡΟΓΡΑΜΜΑ",PROname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ:",list(vdict[fname].keys()))
          else:
            print("ΤΟ ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ:",list(vdict[fname].keys()))
          raise Exception
        if(vname in cdict[fname].keys()):                                      #obsolete
          errmsg="ΔΕΝ ΕΠΙΤΡΕΠΕΤΑΙ ΕΚΧΩΡΗΣΗ ΤΙΜΗΣ ΣΤΗ ΣΤΑΘΕΡΑ "+vname
          raise Exception
        pcmd=xpr(cmd,pblock,vargs)
        #pcmd+="\n"+" "*(nsp)                                                      #TYPE CHECK
        #pcmd+="if(type("+vname+")!="+vdict[fname][vname]+"):\n"
        #pcmd+=" "*(nsp+2)+"print(\"-\"*75+\"\\nΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:\\nΕΚΧΩΡΗΣΗ ΛΑΝΘΑΣΜΕΝΟΥ ΤΥΠΟΥ\\n\")\n"
        #pcmd+=" "*(nsp+2)+"print(\"----> "+str(nl)+". "+line.replace("\n","")+"\\n\")\n"
        #pcmd+=" "*(nsp+2)+"raise Exception\n"+" "*(nsp)

      elif(cmd[:6]==list("ΓΡΑΨΕ ") and ablock):                                  #PRINT
        pcmd="print("+xpr(cmd[6:],pblock,vargs)+")"
      elif(cmd[:8]==list("ΔΙΑΒΑΣΕ ") and ablock):                                #INPUT
        temp=list(line[8:])
        parr=False
        for i in range(len(temp)):
          if(temp[i]=='['):
            temp[i]='.value[-1+'
            parr=True
          elif(parr and temp[i]==','):
            temp[i]='][-1+'
          elif(temp[i]==']'):
            parr=False
        temp="".join(temp)
        vars=temp.split(",")
        pcmd=",".join(vars)+"="
        for v in vars:
          vname = str(v)                              #ΕΛΕΓΧΟΣ ΔΗΛΩΣΗΣ ΜΕΤ/ΤΩΝ ΣΤΗΝ ΕΙΣΟΔΟ
          if("[" in vname):
            lbrpos=vname.find("[")
            vname=vname[:lbrpos]
          if(vname not in vdict[fname].keys() and vname!=fname):
            errmsg="ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ "+vname
            if(fname=="_main_"):
              print("ΤΟ ΠΡΟΓΡΑΜΜΑ",PROname,"ΕΧΕΙ","ΜΕΤΑΒΛΗΤΕΣ",list(vdict[fname].keys()))
            else:
              print("ΤΟ ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ",list(vdict[fname].keys()))
            raise Exception
          pcmd+=("_.Rinput("+str(v)+","+report+"),")*(randIN)+"_.TCinput(),"*(1-randIN)
        pcmd=pcmd[:-1]
      elif(cmd[:3]==list("ΑΝ ") and ablock):           #IF
        ifN+=1
        block=True
        pcmd="if("
        if(cmd[-4:]!=list("ΤΟΤΕ")):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΤΟΤΕ"
          raise Exception
        pcmd+=xpr(cmd[3:-5],pblock,vargs)+"):"
      elif(cmd[:10]==list("ΑΛΛΙΩΣ_ΑΝ ") and ablock):           #ELIF
        block=True
        nsp-=2
        pcmd="elif("
        if(cmd[-4:]!=list("ΤΟΤΕ")):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΤΟΤΕ"
          raise Exception
        pcmd+=xpr(cmd[10:-5],pblock,vargs)+"):"
      elif(line in rword("ΑΛΛΙΩΣ") and ablock):           #ELSE  ##cmd[:6]==list("ΑΛΛΙΩΣ")
        block=True
        nsp-=2
        pcmd="else:"
      elif(line in rword("ΤΕΛΟΣ_ΑΝ") and ablock):    #ENDIF
        ifN-=1
        if(ifN<0):
          errmsg=("ΠΕΡΙΣΣΟΤΕΡΕΣ ΤΕΛΟΣ_ΑΝ ΑΠΟ ΑΝ")
          raise Exception
        deblock=True
      elif(cmd[:8]==list("ΕΠΙΛΕΞΕ ") and ablock):           #SWITCH
        ifN+=1
        swN+=1
        block=True
        pcmd="sw"+str(swN)+"="+xpr(cmd[8:],pblock,vargs)+"\n"+nsp*" "
        pcmd+="if(False):\n"+nsp*" "
        pcmd+="  0"
      elif(cmd[:10]==list("ΠΕΡΙΠΤΩΣΗ ") and ("ΑΛΛΙΩΣ" not in line) and ablock):   #CASE
        block=True
        nsp-=2
        pcmd="elif(sw"+str(swN)
        if("<" not in line and "=" not in line and ">" not in line and ",..," not in line):
          pcmd+=" in ("+xpr(cmd[10:],pblock,vargs)+",)):"
        elif(",..," in line):
          casepos=line.find(",..,")
          swRa=xpr(cmd[10:casepos],pblock,vargs)
          swRb=xpr(cmd[casepos+4:],pblock,vargs)
          pcmd+=" in list(range("+swRa+","+swRb+"+("+swRa+"<="+swRb+")))+list(range("+swRb+","+swRa+"+("+swRa+">"+swRb+")))):"
        else:
          pcmd+=xpr(cmd[10:],pblock,vargs)+"):"
      elif(line in rword("ΠΕΡΙΠΤΩΣΗ ΑΛΛΙΩΣ") and ablock):           #CASE DEFAULT
        block=True
        nsp-=2
        pcmd="else:"
      elif(line in rword("ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ") and ablock):    #ENDSWITCH
        ifN-=1
        swN-=1
        if(swN<0):
          errmsg=("ΠΕΡΙΣΣΟΤΕΡΕΣ ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ ΑΠΟ ΕΠΙΛΕΞΕ")
          raise Exception
        deblock=True
      elif(cmd[:4]==list("ΟΣΟ ") and ablock):           #WHILE
        whN+=1
        block=True
        whv.append("dummy")
        whstep.append("0")
        pcmd=whv[-1]+"=0\n"+nsp*' ' # for +
        pcmd+="while("
        if(cmd[-9:]!=list("ΕΠΑΝΑΛΑΒΕ")):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΕΠΑΝΑΛΑΒΕ"
          raise Exception
        pcmd+=xpr(cmd[4:-10],pblock,vargs)+"):"
      elif(cmd[:4]==list("ΓΙΑ ") and ablock):           # FOR ΜΕΣΩ WHILE
        whN+=1
        if("ΑΠΟ " not in line or "ΜΕΧΡΙ " not in line 
           or line.count("ΓΙΑ")>1 or line.count("ΑΠΟ")>1 or line.count("ΜΕΧΡΙ")>1 or line.count("ΜΕ_ΒΗΜΑ")>1):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ ΤΗΣ ΕΝΤΟΛΗΣ ΓΙΑ"
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
          if("ΜΕ_ΒΗΜΑ " not in line):
            errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ ΤΗΣ ΕΝΤΟΛΗΣ ΓΙΑ"
            raise Exception
          pcmd="correction"+str(whN)+"=1-2*("+xpr(cmd[pos4:],pblock,vargs)+"<0)\n"+" "*nsp
          step=xpr(cmd[pos4:],pblock,vargs)
        else:
          pcmd="correction"+str(whN)+"=1\n"+" "*nsp
          step="1"
        whv.append(xpr(cmd[4:pos1-1],pblock,vargs))
        whstep.append(step)
        vname=whv[-1]
        if(vname not in vdict[fname].keys() and vname!=fname):
          errmsg="ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ "+vname
          if(fname=="_main_"):
            print("ΤΟ ΠΡΟΓΡΑΜΜΑ ΕΧΕΙ","ΜΕΤΑΒΛΗΤΕΣ:",list(vdict[fname].keys()))
          else:
            print("ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ:",list(vdict[fname].keys()))
          raise Exception
        pcmd+=whv[-1]+"="+xpr(cmd[pos1+4:pos2],pblock,vargs)+"\n"+" "*nsp
        pcmd+="while("  #for "
        if("ΜΕ_ΒΗΜΑ" in line):
          pcmd+=xpr(cmd[4:pos1],pblock,vargs)+"*correction"+str(whN)+" <= "+xpr(cmd[pos2+6:pos3],pblock,vargs)+"*correction"+str(whN)+"):"
        else:
          pcmd+=xpr(cmd[4:pos1],pblock,vargs)+"<= "+xpr(cmd[pos2+6:],pblock,vargs)+"):\n"+" "*nsp
      elif(line in rword("ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ") and ablock):    #ENDFOR/WHILE
        whN-=1
        if(whN<0):
          errmsg=("ΠΕΡΙΣΣΟΤΕΡΕΣ ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ ΑΠΟ ΔΟΜΕΣ ΕΠΑΝΑΛΗΨΗΣ")
          raise Exception
        pcmd=whv.pop(-1)+"+="+whstep.pop(-1)   # for +
        deblock=True
      elif(line in rword("ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ")):#"ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ" in line and ablock):    #DO
        dwhN+=1
        block=True
        pcmd="while(True):"
      elif(cmd[:12]==list("ΜΕΧΡΙΣ_ΟΤΟΥ ") and ablock):  #_WHILE
        dwhN-=1
        if(dwhN<0):
          errmsg=("ΠΕΡΙΣΣΟΤΕΡΕΣ ΜΕΧΡΙΣ_ΟΤΟΥ ΑΠΟ ΔΟΜΕΣ ΕΠΑΝΑΛΗΨΗΣ")
          raise Exception
        deblock=True
        pcmd="if("+xpr(list("".join(cmd[12:])),pblock,vargs)
        pcmd+="):\n"+" "*(nsp+2)+"break"
      elif(cmd[:10]==list("ΠΡΟΓΡΑΜΜΑ ")):                     # MAIN  ___________________________
        fname="_main_"
        PROname=line[10:]
        if(PROname[-1] in "\n "):
          PROname=PROname[:-1]
        cdict[fname],vdict[fname]=dict(),dict()
        if(fblock or pblock or tryblock):
          errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
          raise Exception
        block=True
        acounter+=1
        #mblock=True
        tryblock=True
        exe=True
        pcmd="def main():\n  N1=NUM()\n"
      elif(line in rword("ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ")+["ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ "+PROname]):    #END MAIN
        tryblock=False
        if(ifN!=0):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ"
          raise Exception
        if(dwhN+whN!=0):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ"
          raise Exception
        if(not ablock):
          errmsg="ΛΕΙΠΕΙ Η ΛΕΞΗ ΑΡΧΗ"
          raise Exception
        ablock=False
        nsp=0
        #pcmd='''  except Exception as e:
    #print(\"ΒΡΕΘΗΚΕ ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ...\")
    #print(getattr(e, 'message', repr(e)))'''
        pcmd+="\n#ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\n"
      elif(cmd[:10]==list("ΣΥΝΑΡΤΗΣΗ ")):           #FUNCTION
        if(fblock or pblock or tryblock):
          errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
          raise Exception
        fblock=True
        block=True
        acounter+=1
        nfvalue=True
        pcmd="def "
        cmd=cmd[10:]
        if(":" not in cmd):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΣΥΝΑΡΤΗΣΗΣ"
          raise Exception
        for tpos in range(len(cmd)):
          if(cmd[tpos]==":"):
            break
        fname=""
        for i in cmd:
          if(i=="("):
            break
          fname+=i
        if(not isname(fname)):
          errmsg="ΜΗ ΕΓΚΥΡΟ ΟΝΟΜΑ ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ: "+fname
          raise Exception
        cdict[fname],vdict[fname]=dict(),dict()
        ftypos="".join(cmd[tpos+1:])
        if ftypos[0]==" ":
          ftypos=ftypos[1:]
        if ftypos=="ΑΚΕΡΑΙΑ":
          ftypos=int
        elif ftypos=="ΠΡΑΓΜΑΤΙΚΗ":
          ftypos=float
        elif ftypos=="ΧΑΡΑΚΤΗΡΑΣ":
          ftypos=str
        elif ftypos=="ΛΟΓΙΚΗ":         #ΛΟΓΙΚΗ
          ftypos=bool
        else:
          errmsg="ΜΗ ΕΓΚΥΡΟΣ ΤΥΠΟΣ ΣΥΝΑΡΤΗΣΗΣ"
          raise Exception

        pcmd+=fname+"("
        lfn=len(fname)
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
      elif(fblock and fname==line[:lfn] and ("<--"==line[lfn:lfn+3] or " <--"==line[lfn:lfn+4])): #RETURN
        pcmd="_"+fname+xpr(cmd[len(fname):])#[2:]
        nfvalue=False
      elif(line in rword("ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ")):         #ENDFUNCTION
        if(not ablock):
          errmsg="ΛΕΙΠΕΙ Η ΛΕΞΗ ΑΡΧΗ"
          raise Exception
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ")
          raise Exception
        if(dwhN+whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ")
          raise Exception
        if(nfvalue):
          errmsg=("ΔΕΝ ΕΧΕΙ ΥΠΟΛΟΓΙΣΤΕΙ Η ΤΙΜΗ ΤΗΣ ΣΥΝΑΡΤΗΣΗΣ")
          raise Exception
        if(not ablock):
          errmsg="ΛΕΙΠΕΙ Η ΛΕΞΗ ΑΡΧΗ"
          raise Exception
        ablock=False
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
      elif(cmd[:11]==list("ΔΙΑΔΙΚΑΣΙΑ ")):           #PROCEDURE
        if(fblock or pblock or tryblock):
          errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
          raise Exception
        #pblock=True
        block=True
        acounter+=1
        pcmd="def "
        cmd=cmd[11:]
        fname=""
        for i in cmd:
          if(i=="("):
            break
          fname+=i
        if(not isname(fname)):
          errmsg="ΜΗ ΕΓΚΥΡΟ ΟΝΟΜΑ ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ: "+fname
          raise Exception
        cdict[fname],vdict[fname]=dict(),dict()
        pcmd+=fname+"("
        vargs="".join(cmd[len(fname)+1:-1]).split(",")
        for a in vargs:
          pcmd+=a+","
        pcmd=pcmd[:-1]+"):"
      elif(line in rword("ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ")):    #ENDPROCEDURE
        if(not ablock):
          errmsg="ΛΕΙΠΕΙ Η ΛΕΞΗ ΑΡΧΗ"
          raise Exception
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ")
          raise Exception
        if(dwhN+whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ")
          raise Exception
        if(not ablock):
          errmsg="ΛΕΙΠΕΙ Η ΛΕΞΗ ΑΡΧΗ"
          raise Exception
        ablock=False
        pblock=False
        deblock=True
        pcmd="return "                             #procedure by return
        for a in vargs:
          pcmd+=a+','
        pcmd=pcmd[:-1]
        fname=""
        pcmd+="\n#ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\n"
      elif(cmd[:7]==list("ΚΑΛΕΣΕ ")):          #ΚΑΛΕΣΕ
        for posP in range(len(cmd)):
          if cmd[posP]=="(":
            break
        Xcmd=xpr(cmd)
        nP=0  #number of open left(
        for i in range(len(Xcmd)):
          if(Xcmd[i]=='('):
            nP+=1
          elif(Xcmd[i]==')'):
            nP-=1
          elif(Xcmd[i]==',' and nP==1):
            Xcmd=Xcmd[:i]+'$'+Xcmd[i+1:]
        pV=[v for v in Xcmd[posP+1:-1].split("$")]  #split at the correct commas
        pV=[v.replace('$',',') for v in pV]
        Xcmd=[v.replace('$',',') for v in Xcmd]
        pcmd=""
        for v in pV:
          if(v in vdict[fname]):
            pcmd+=v+","
          else:
            pcmd+="_dummy,"
        pcmd=pcmd[:-1]+"="
        pcmd+="".join(Xcmd[7:])
      elif("<--" in line and False):          #DEPRECATED
        pcmd=xpr(cmd,pblock,vargs)
      elif("ΜΕΤΑΒΛΗΤΕΣ" in line and False):          #DEPRECATED
        pcmd=xpr(cmd,pblock,vargs)
      elif("ΑΡΧΗ" in line and False):          #DEPRECATED
        pcmd=xpr(cmd,pblock,vargs)
      elif("_" in line[:1] and False):          #DEPRECATED
        pcmd=xpr(cmd,pblock,vargs)
      else:
        errmsg=""#"ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: Τ800"
        #if(acounter!=0):
          #errmsg="ΛΕΙΠΕΙ Η ΛΕΞΗ ΑΡΧΗ"
        raise Exception

      if(pcmd not in ["","\n"]):              # save line
        if(pcmd[-1]=="\n"):
          pcmd=pcmd[:-1]
        fout.write(nsp*" "+pcmd+comment+"#//"+str(nl)+"\n")
      else:
        nl+=0
      if(block):
        nsp+=2
        block=False
      elif(deblock):
        nsp-=2
        deblock=False
      if(mblock):
        nsp+=2
        mblock=False

    if(segment):
      nsp=0
      tryblock=0
      #fout.write('''  except Exception as e:
    #print(\"ΒΡΕΘΗΚΕ ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ...\")
    #print(getattr(e, 'message', repr(e)))''')
    if(fblock+pblock+tryblock!=0):              #ΤΕΛΟΣ ΠΡΟΓΡΑΜΜΑΤΟΣ
      errmsg="ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_<ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ>"
      raise Exception
    fin.close()
    fout.close()
  except Exception as e:
    #if(acounter!=0 and errmsg==""):
      #errmsg="ΛΕΙΠΕΙ Η ΛΕΞΗ ΑΡΧΗ"
    if(errmsg==""):
      errmsg=getattr(e, 'message', repr(e))
      if("invalid syntax" in errmsg):
        errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ"
    print("-"*75+'\n'+"ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:\n"+errmsg.replace("Exception()","> μη έγκυρη σύνταξη")+"\n----> "+str(nl)+". "+line)   #str(nl+1)
    return

  #import source                 #EXECUTION
  source=__import__(file)
  importlib.reload(source)
  if(exe):
    if(cmp):
      with open('log'+str(aa),'w') as lfile:
        with redirect_stdout(lfile):
          source.main()
    else:
      source.main()
      try:
        0==0#source.main()
      except:
        0==0#print("το πηγαίο έχει τις εξής συναρτήσεις: "+dir(source))#"\n<ΑΝΤΙΚΑΝΟΝΙΚΟΣ ΤΕΡΜΑΤΙΣΜΟΣ>")#
