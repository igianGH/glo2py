import difflib as dfl
import traceback
import sys
import random as r
import importlib  #reload module
from contextlib import redirect_stdout

def testversion():
  '''
  Prints GHlib version
  '''
  print(">",end="")
  print("2804252320")

def interS(l1,l2):
  '''
  Returns the intersection of l1,l2
  l1
    container
  l2
    container
  '''
  return [i for i in l1 if i in l2]

def rword(w:str):
  '''
  Returns list of str. This is used for reserved word identification.
  '''
  return [w,w+' ',w+'\n']

def isindex(i):
  '''
  Returns valid index for positive integers
  '''
  try:
    if(i>0):
      return i-1
    else:
      return 1.
  except:
    raise RuntimeError("Μη έγκυρος δείκτης πίνακα")

def evaluate(code):
  '''
  Αποτιμά μεμονωμένη γραμμή κώδικα σε ΓΛΩΣΣΑ χωρίς μεταβλητές.
  code
    str με τον κώδικα του προγράμματος σε ΓΛΩΣΣΑ.
  '''
  fname="source"
  fOUT=open(fname+".py",'w')
  fOUT.write('''
import random as r
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
  X=xpr(list(code))
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
    print("Σφάλμα: "+errmsg+"\n--> "+X)
  

def editor(code,fname="source"):
  '''
  Αποθηκεύει στο δίσκο str με τον κώδικα του προγράμματος σε ΓΛΩΣΣΑ.
  code
    str με τον κώδικα του προγράμματος
  fname
    όνομα αρχείου, default "source"
  '''
  with open(fname,'w') as f:
    f.write(code)

def run(code,developer=False):
  '''
  Καλεί τον editor και τον interpreter
  code
    str με τον κώδικα του προγράμματος σε ΓΛΩΣΣΑ
  developer
    αν έχει τιμή True τότε σε περίπτωση σφάλματος θα εμφανίσει το πλήρες μήνυμα, default False
  '''
  editor(code)
  interpreter(developer=developer)
  
def interpreter(file="source",developer=False,dline=True,smart=False,report=False,randIN=True,test=False):
  '''
  Μεταγλωττίζει και επιχειρεί να εκτελέσει κάθε γραμμή προγράμματος σε ΓΛΩΣΣΑ με μέθοδο transpiler.
  file
    όνομα πηγαίου αρχείου, default str
  developer
    αν έχει τιμή True τότε σε περίπτωση σφάλματος θα εμφανίσει το πλήρες μήνυμα, default False
  dline
    αν έχει τιμή True τότε εμφανίζει την εκτιμώμενη γραμμή στην οποία εμφανίστηκε το σφάλμα, default True
  smart
    αν έχει τιμή True τότε αντί τυχαίων χαρακτήρων παράγονται ονόματα, default False
  report
    αν έχει τιμή True τότε όταν παράγεται μία τυχαία τιμή αντί εισόδου, αυτή εμφανίζεται. Default False
  randIN
    αν έχει τιμή True τότε αντί εισόδου παράγεται μία τυχαία τιμή με τον αντίστοιχο τύπο, default True
  test
    αν έχει τιμή True τότε στη μεταγλώττιση εμφανίζονται οι δηλωμένες μεταβλητές του προγράμματος, default False
  '''
  try:
    interpretM(file,smart=smart,report=report,randIN=randIN,test=test)
  except:
    errmsg2=""
    errmsg=str(sys.exc_info()[1])
    trb=str(traceback.format_exc())
    sb=trb[0:]
    if(developer):
      print("\n"+trb)
    ierr=trb.rfind("Error:")
    trb=trb[ierr+7:]
    if('%' in trb):
      imod=trb.find('%')
      trb=trb[:imod]+"MOD"+trb[imod+1:]
    if("\'type\'" in sb and "unsupported operand" in sb 
       or "not supported between instances" in sb and "\'type\'" in sb):
      linecorr=1
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:\n> ΑΠΟΤΥΧΙΑ ΑΠΟΤΙΜΗΣΗΣ ΕΚΦΡΑΣΗΣ, Κάποια μεταβλητή δεν έχει λάβει τιμή?"
    elif("yntax" in sb or "efined" in sb or "unsupported operand" in sb 
      or "only concatenate" in sb or "no attribute \'value\'" in sb): # or "TypeError"
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      linecorr=1
      if("comma" in sb):
        errmsg2+="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ, Μήπως ξεχάσατε κάποιο κόμμα?"
      elif("name" in sb and "not defined" in sb):
        vname=sb[sb.find("name \'")+6:sb.find("\' is not defined")]
        vname=vname if vname[0]!='_' else vname[1:]
        errmsg2+="\n> Η ΜΕΤΑΒΛΗΤΗ "+vname+" ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ"
      elif("unsupported operand" in sb or "only concatenate" in sb):
        errmsg2+="\n> ΠΡΑΞΗ ΜΕΤΑΞΥ ΑΣΥΜΒΑΤΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ"
      elif("no attribute \'value\'" in sb):
        errmsg2+="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ, αυτό το αντικείμενο δεν είναι πίνακας"
      else:
        errmsg2+="\n> "+trb.split('\n')[0].replace("invalid syntax","ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ")
    else:
      linecorr=1
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      if("invalid literal" in sb):
        errmsg2+="\n> ΕΚΧΩΡΗΣΗ ΤΙΜΗΣ ΛΑΝΘΑΣΜΕΝΟΥ ΤΥΠΟΥ"
      elif("index" in sb and "out of bounds" in sb or "valid indices" in sb
          or "indices must be integers" in sb or "index out of range" in sb):
        errmsg2+="\n> ΥΠΕΡΒΑΣΗ ΟΡΙΩΝ ΠΙΝΑΚΑ"
      elif("division by zero" in sb):
        errmsg2+="\n> ΔΙΑΙΡΕΣΗ ΜΕ 0 (ΜΗΔΕΝ)"
      elif("math domain error" in sb or "class \'complex\'" in sb):
        errmsg2+="\n> ΔΕΝ ΟΡΙΖΕΤΑΙ Η ΑΡΙΘΜΗΤΙΚΗ ΠΡΑΞΗ"
      elif("xceeds the limit" in sb or "OverflowError" in sb):
        errmsg2+="\n> ΠΟΛΥ ΜΕΓΑΛΟΣ ΑΡΙΘΜΟΣ"
      else:
        errmsg2+="\n"+trb.split('\n')[0]
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
          if("#//" in line):                   # εύρεση γραμμής όπου απέτυχε η μετάφραση/εκτέλεση
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
            if(dline):
              line=next(lines)
              snl+=1
              print("----> "+str(snl+0-linecorr)+". ",line[:])
            break
      except StopIteration:
        print(errmsg+"\n..\n"+errmsg2)

l=[chr(ord("a")+i) for i in range(26)]
l+=[chr(ord("A")+i) for i in range(26)]
l+=[chr(ord("α")+i) for i in range(25)]
l+=[chr(ord("Α")+i) for i in range(25) if i!=17]
letters=l
numbersP="(1234567890 "
Reserved='''ΠΡΟΓΡΑΜΜΑ,ΣΥΝΑΡΤΗΣΗ,ΔΙΑΔΙΚΑΣΙΑ,ΜΕΤΑΒΛΗΤΕΣ,ΣΤΑΘΕΡΕΣ,ΑΚΕΡΑΙΕΣ,ΠΡΑΓΜΑΤΙΚΕΣ,ΧΑΡΑΚΤΗΡΕΣ,
ΑΛΗΘΗΣ,ΨΕΥΔΗΣ,ΑΡΧΗ,ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ,ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ,ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ,ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ,
ΑΝ,ΤΟΤΕ,ΑΛΛΙΩΣ_ΑΝ,ΑΛΛΙΩΣ,ΤΕΛΟΣ_ΑΝ,ΕΠΙΛΕΞΕ,ΠΕΡΙΠΤΩΣΗ,ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ,ΟΣΟ,ΕΠΑΝΑΛΑΒΕ,ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ,
ΜΕΧΡΙΣ_ΟΤΟΥ,ΓΙΑ,ΑΠΟ,ΜΕΧΡΙ,ΜΕ_ΒΗΜΑ,ΗΜ,ΣΥΝ,ΕΦ,ΛΟΓ,Ε,Α_Τ,Α_Μ,Τ_Ρ,MOD,DIV,ΟΧΙ,ΚΑΙ,Ή
'''.replace("\n","").split(",")
with open("names",'r') as fNAMES:
  names={}#[]
  for line in fNAMES:
    line=line.replace(" ","")
    sep=line.find(":")
    names[line[:sep]]=line[sep+1:-1]#names.append(line[:-1])

def Rinput(v,report=False,smartV=""):
  '''
  Επιστρέφει τυχαία τιμή με τύπο τον τύπο της v
  v
    μεταβλητή που θα λάβει τυχαία τιμή
  report
    αν είναι True τότε εμφανίζεται ποια τυχαία τιμή αποδόθηκε στη v, default False
  smart
    αν έχει τιμή True τότε αντί τυχαίων χαρακτήρων παράγονται ονόματα, default True
  '''
  #v variable
  global letters
  global names
  ndigits=r.randrange(1,9)
  if(v==bool or type(v)==bool):
    raise SyntaxError("ΔΕ ΜΠΟΡΕΙ ΝΑ ΔΟΘΕΙ ΛΟΓΙΚΗ ΤΙΜΗ ΑΠΟ ΤΗΝ ΕΙΣΟΔΟ")
  if(v==int or type(v)==int):
    v=(r.randrange(-10**ndigits,10**ndigits))
  elif(v==float or type(v)==float):
    v=(r.random()*r.randrange(-10**ndigits,10**ndigits))
  elif(v==str or type(v)==str):
    v=("".join(r.choices(letters[-24:],k=ndigits)))
    if(smartV!=""):
      try:
        v=r.choice([i for i in names.keys() if names[i] in smartV])#.split(",")
      except:
        0==0
  if(report):
    print(">διαβάστηκε το",v)
  return v

def TCinput(prompt="> "):
  '''
  Λαμβάνει μία τιμή από την είσοδο και τη μετατρέπει από str στον κατάλληλο τύπο
  prompt
    εμφανίζεται για να δηλώσει ότι θα διαβαστεί τιμή από την είσοδο
  '''
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

def xpr(s,pblock=False,v=[]):
  '''
  Μετατρέπει λίστα χαρακτήρων σε έγκυρη έκφραση της ΓΛΩΣΣΑΣ
  s
    list από str με μήκος 1
  pblock
    αν είναι True τότε καλείται μέσα από ΔΙΑΔΙΚΑΣΙΑ, default False. DEPRECATED
  v
    λίστα με τις μεταβλητές της ΔΙΑΔΙΚΑΣΙΑΣ. DEPRECATED
  '''
  global numbersP
  if(type(s)==str):
    s=list(s)
  buffer=" "
  #s=[" "]+s
  pcmd=""
  sarr=sfunc=False
  while(s!=[]):
    #buffer+=s[0]
    if(s[0] in "\"\'"):
      pcmd+="\'"
      while(True):
        s.pop(0)
        if(s[0] in "\"\'" or s==[]):
          pcmd+="\'"
          s.pop(0)
          break
        else:
          pcmd+=s[0]
      if(s==[]):
        break
    elif(s[0]=="["):
      sarr=True
      pcmd+=".ΤΙΜΗ"+s.pop(0)+"_.isindex("   #.value
      buffer+="["
    elif(s[0]=='(' and sarr):
      sfunc=True
      pcmd+=s.pop(0)
      buffer+="("
    elif(s[0]==')' and sfunc and sarr): #array and function
      sfunc=False
      pcmd+=s.pop(0)
      buffer+=")"
    elif(s[0]=="]"):
      sarr=False
      pcmd+=")"+s.pop(0)
      buffer+="]"
    elif(s[0]=="," and sarr and not sfunc):
      pcmd+=")][_.isindex("
      s.pop(0)
      buffer+=","
    elif(s[:3]==list("ΟΧΙ") and (len(s)<4 or s[3] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" not "
      s=s[3:]
      buffer+="ΟΧΙ"
    elif(s[:3]==list("ΚΑΙ") and (len(s)<4 or s[3] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" and "
      s=s[3:]
      buffer+="ΚΑΙ"
    elif(s[:1]==list("Ή") and (len(s)<2 or s[1] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" or "
      s=s[1:]
      buffer+="Ή"
    elif(s[:2]==list("<>")):
      pcmd+="!="
      s=s[2:]
      buffer+="<>"
    elif(s[:2]==list("<=")):
      pcmd+="<="
      s=s[2:]
      buffer+="<="
    elif(s[:2]==list(">=")):
      pcmd+=">="
      s=s[2:]
      buffer+=">="
    elif(s[:3]==list("<--")):
      pcmd+="="
      s=s[3:]
      buffer+="<--"
    elif(s[0]=="+"):
      pcmd+="+0+"
      s.pop(0)
      buffer+="+"
    elif(s[0]=="*"):
      pcmd+="*N1*"
      s.pop(0)
      buffer+="*"
    elif(s[0]=="="):
      pcmd+="=="
      s.pop(0)
      buffer+="=="
    elif(s[0]=="^"):
      pcmd+="**"
      s.pop(0)
      buffer+="^"
    elif(s[:6]==list("ΑΛΗΘΗΣ") and (len(s)<7 or s[6] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" True "
      s=s[6:]
      buffer+="ΑΛΗΘΗΣ"
    elif(s[:6]==list("ΨΕΥΔΗΣ") and (len(s)<7 or s[6] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" False "
      s=s[6:]
      buffer+="ΨΕΥΔΗΣ"
    elif(s[:3]==list("DIV") and (len(s)<4 or s[3] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="//"
      s=s[3:]
      buffer+="DIV"
    elif(s[:3]==list("MOD") and (len(s)<4 or s[3] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="%"
      s=s[3:]
      buffer+="MOD"
    elif(s[:4]==list("Τ_Ρ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" m.sqrt("
      s=s[4:]
      buffer+="Τ_Ρ("
    elif(s[:4]==list("Α_Τ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" abs("
      s=s[4:]
      buffer+="Α_Τ("
    elif(s[:4]==list("Α_Μ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" int("
      s=s[4:]
      buffer+="Α_Μ("
    elif(s[:3]==list("ΗΜ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" m.sin(m.pi/180*"
      s=s[3:]
      buffer+="ΗΜ("
    elif(s[:4]==list("ΣΥΝ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" m.cos(m.pi/180*"
      s=s[4:]
      buffer+="ΣΥΝ("
    elif(s[:3]==list("ΕΦ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" m.tan(m.pi/180*"
      s=s[3:]
      buffer+="ΕΦ("
    elif(s[:4]==list("ΛΟΓ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" m.log("
      s=s[4:]
      buffer+="ΛΟΓ("
    elif(s[:2]==list("Ε(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=" m.exp("
      s=s[2:]
      buffer+="Ε("
    else:
      if(s[0] in letters[:52] and buffer[-1] not in letters[:52]):
        pcmd+="_"
      pcmd+=s[0]
      buffer+=s.pop(0)
    #print(buffer,"\ns:"+"".join(s).replace("\n",""),"\npcmd:"+pcmd.replace("\n",""))
  return(pcmd)

def isname(s):
  '''
  Επιστρέφει True αν το s είναι έγκυρο όνομα μεταβλητής
  s
    str, το όνομα που εξετάζεται αν είναι έγκυρο
  '''
  global letters
  if s[0] not in letters:
    return False
  for c in s[1:]:
    if c not in letters+list("_0123456789"):
      return False
  return True

def interpretM(file="source",randIN=True,cmp=False,aa=1,smart=False,report=False,test=False):
  segment=False
  import importlib
  global letters,Reserved
  fin=open(file+"_",'w')
  with open(file) as fraw:      #'&' στην αρχή πρότασης
    lineG=(line for line in fraw)
    line1=next(lineG)[:-1]
    while(True):
      try:
        line2=next(lineG)[:-1]
        if(line1.replace(" ","").replace("\n","")==""):
          fin.write(line1+"\n")
          line1=line2
          continue
        while(len(line2)>0 and line2[0]==' '):    # remove wspace from start
          line2=line2[1:]
        if(len(line2)>0 and line2[0]=='&'):  # merge 2+ lines
          line1+=' '+line2[1:]
        else:
          fin.write(line1+"\n")
          line1=line2[:]
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
  whv,whstep,whline,dwhline,ifline,swline,ALLblock,ALLline=[],[],[],[],[],[],[],[]
  blockdict={"if":"ΤΕΛΟΣ_ΑΝ","sw":"ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ","wh":"ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ","dwh":"ΜΕΧΡΙΣ_ΟΤΟΥ"}
  blockdict2={"if":"ΕΠΙΛΟΓΗΣ","sw":"ΕΠΙΛΟΓΗΣ","wh":"ΕΠΑΝΑΛΗΨΗΣ","dwh":"ΕΠΑΝΑΛΗΨΗΣ"}
  cdict,vdict={},{}
  intl=floatl=strl=booll=False
  acounter=0
  vblock=cblock=ablock=exe=tryblock=mblock=block=deblock=fblock=pblock=False
  errmsg=""
  vargs=[]
  fout.write('''
import random as r
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
    self.ΤΙΜΗ=A
    self.typos=typos
    self.dimension=d
  def __invert__(self):
    if(self.dimension==1 and len(self.ΤΙΜΗ)<21):
      print(self.ΤΙΜΗ)
      return \"-\"*75+\"\\nWarning: το ~ δεν επιτρέπεται στη ΓΛΩΣΣΑ\\n\"
    n=0
    for l in self.ΤΙΜΗ:
      n+=1
      print(n,l)
    return \"-\"*75+\"\\nWarning: το ~ δεν επιτρέπεται στη ΓΛΩΣΣΑ\\n\"
def assign(y,x):
  tGL={int:"ΑΚΕΡΑΙΑ",float:"ΠΡΑΓΜΑΤΙΚΗ",str:"ΧΑΡΑΚΤΗΡΑΣ",bool:"ΛΟΓΙΚΗ",myA:"ΠΙΝΑΚΑΣ"}
  tt,j={},1
  for i in [y,x]:
    if(i not in tGL.keys()):
      tt[j]=tGL[type(i)]
    else:
      tt[j]=tGL[i]
    j+=1
  if(tt[1]=="ΠΙΝΑΚΑΣ"):
    raise RuntimeError("Δεν επιτρέπεται εκχώρηση απευθείας σε Πίνακα")
  if(tt[2]==tt[1]):
    return x
  elif(tt[1]=="ΠΡΑΓΜΑΤΙΚΗ" and tt[2]=="ΑΚΕΡΑΙΑ"):
    return x
  raise RuntimeError("Δεν επιτρέπεται εκχώρηση τιμής τύπου "+tt[2]+" σε μεταβλητή τύπου "+tt[1])
\n'''+"#"*80+"\n")
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
      for i in range(cmpos-1,-1,-1):     # SPACES tail #range(cmpos-1,5,-1):
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
      if(line.count('\"')>0 or line.count('\'')%2==1):
        errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΧΡΗΣΗ ΕΙΣΑΓΩΓΙΚΩΝ"
        raise Exception
      while("\"" in lineNS):      # ignore "strings"
        pos1=lineNS.find("\"")
        pos2=lineNS[pos1+1:].find("\"")+pos1+1
        if("\'" in lineNS[pos1:pos2]):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΧΡΗΣΗ ΕΙΣΑΓΩΓΙΚΩΝ"
          raise Exception
        lineNS=lineNS[:pos1]+"_"+lineNS[pos2+1:]
      while("\'" in lineNS):      # ignore 'strings'
        pos1=lineNS.find("\'")
        pos2=lineNS[pos1+1:].find("\'")+pos1+1
        lineNS=lineNS[:pos1]+"_"+lineNS[pos2+1:]
      if("ΠΕΡΙΠΤΩΣΗ" in lineNS and ",..," in lineNS):
        lineNS=lineNS[:lineNS.find(",..,")]+lineNS[lineNS.find(",..,")+4:]
      for i in cflags:
        if(i in lineNS):
          errmsg="\n> ΜΗΠΩΣ ΞΕΧΑΣΑΤΕ ΚΑΠΟΙΟ ΟΡΙΣΜΑ?"
          raise Exception
      for i in range(len(lineNS)):
        if(lineNS[i]=='.' and (i in [0,len(lineNS)-1] 
          or lineNS[i-1] not in "0987654321"
          or lineNS[i+1] not in "0987654321")):
          errmsg = "\n> μη έγκυρη χρήση υποδιαστολής"
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
          errmsg="\n> ΠΛΕΟΝΑΖΟΥΣΑ ΔΕΞΙΑ ΠΑΡΕΝΘΕΣΗ"
          raise Exception
        elif(lc<rc):
          errmsg="\n> ΠΛΕΟΝΑΖΟΥΣΑ ΔΕΞΙΑ ΑΓΚΥΛΗ"
          raise Exception
      if(lpar>rpar):
        errmsg="\n> ΑΝΟΙΧΤΟ ΜΠΛΟΚ ΠΑΡΕΝΘΕΣΕΩΝ"
        raise Exception
      if(lc>rc):
        errmsg="\n> ΑΝΟΙΧΤΟ ΜΠΛΟΚ ΑΓΚΥΛΩΝ"
        raise Exception
      line=[w for w in line.split(" ") if w not in " "]
      for w in line:
        if(w[0]==" "):
          w.pop(0)
      line=" ".join(line)
      cmd=[c for c in line]

      if(line in " \n"):
        pcmd=xpr(cmd,pblock,vargs)
      elif(line[-1] not in letters+list("0123456789])\n\t\"\' ")):
        errmsg="\n> ΑΝΤΙΚΑΝΟΝΙΚΟΣ ΤΕΡΜΑΤΙΣΜΟΣ ΓΡΑΜΜΗΣ"
        raise Exception

      elif(line in rword("ΣΤΑΘΕΡΕΣ") and (tryblock or fblock or pblock)):               #CONSTANTS
        if(cblock+vblock+ablock):
          errmsg="\n> ΑΝΤΙΚΑΝΟΝΙΚΗ ΕΝΑΡΞΗ ΔΗΛΩΤΙΚΟΥ ΤΜΗΜΑΤΟΣ ΣΤΑΘΕΡΩΝ"
          raise Exception
        cblock=True
        pcmd="#"+line
      elif(line in rword("ΜΕΤΑΒΛΗΤΕΣ") and (tryblock or fblock or pblock)):            #VARIABLES
        if(vblock+ablock):
          errmsg="\n> ΑΝΤΙΚΑΝΟΝΙΚΗ ΕΝΑΡΞΗ ΔΗΛΩΤΙΚΟΥ ΤΜΗΜΑΤΟΣ ΜΕΤΑΒΛΗΤΩΝ"
          raise Exception
        cblock=False
        vblock=True
        pcmd="#"+line
      elif(line in rword("ΑΡΧΗ") and (tryblock or fblock or pblock)):                     #ΑΡΧΗ
        cblock=vblock=False
        acounter-=1
        ablock=True
        intl=floatl=strl=booll=False
        pcmd="#"+line
        if(test):
          print("ΥΠΟΠΡΟΓΡΑΜΜΑ:",fname,
                "ΣΤΑΘΕΡΕΣ:",list(cdict[fname].keys()),
                "ΜΕΤΑΒΛΗΤΕΣ:",list(vdict[fname].keys()))       #full variable report
      elif(cblock and (tryblock or fblock or pblock)):                                            #CBLOCK
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
          pcmd=xpr(cname)+"="+cvalue
        else:
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΣΤΑΘΕΡΑΣ"
          raise Exception
      elif(vblock and (tryblock or fblock or pblock)):                                               #VBLOCK
        if(line.count(":")!=1):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΜΕΤΑΒΛΗΤΩΝ"
          raise Exception
        clpos=line.find(":")
        vtype=line[:clpos]
        if(vtype[-1]==" "):
          vtype=vtype[:-1]
        match vtype:
          case "ΑΚΕΡΑΙΕΣ":
            vtype="int"
            if(intl):
              errmsg="\n> ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΑΚΕΡΑΙΩΝ"
              raise Exception
            intl=True
          case "ΠΡΑΓΜΑΤΙΚΕΣ":
            vtype="float"
            if(floatl):
              errmsg="\n> ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΠΡΑΓΜΑΤΙΚΩΝ"
              raise Exception
            floatl=True
          case "ΧΑΡΑΚΤΗΡΕΣ":
            vtype="str"
            if(strl):
              errmsg="\n> ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΧΑΡΑΚΤΗΡΩΝ"
              raise Exception
            strl=True
          case "ΛΟΓΙΚΕΣ":
            vtype="bool"
            if(booll):
              errmsg="\n> ΥΠΑΡΧΕΙ ΠΑΡΑΠΑΝΩ ΔΗΛΩΣΗ ΛΟΓΙΚΩΝ"
              raise Exception
            booll=True
          case default:
            errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΜΕΤΑΒΛΗΤΩΝ"
            raise Exception
        fvarpos=clpos+1
        while(cmd[fvarpos]==' '):
          fvarpos+=1
        line=line[fvarpos:]
        if(line in " "):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΜΕΤΑΒΛΗΤΩΝ"
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
          vval,vsub=vtype,""
          if("[" in v):
            lbrpos,rbrpos=v.find("["),v.find("]")
            vname,vsub=v[:lbrpos],".typos"
            if(vname[-1]==" "):
              vname=vname[:-1]
            vdim=(v[lbrpos+1:rbrpos].replace(" ",""))
            for i in range(len(vdim)-1,-1,-1):
              vval="("+xpr(list(vdim[i]))+")*["+vval+"]"              #expression in Shape
            vval="myA(["+vdim+"],"+vtype+")"
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
            vdict[fname][vname+".ΤΙΜΗ"]=vtype
          pcmd+="try:\n"+" "*(nsp+2)
          pcmd+=xpr(vname)+"=="+xpr(vname)+"\n"+" "*(nsp+2)
          pcmd+="assign("+vtype+","+xpr(vname)+vsub+")\n"+" "*(nsp)
          pcmd+="except NameError:\n"+" "*(nsp+2)
          pcmd+=xpr(vname)+"="+vval+"\n"+" "*(nsp)

      elif(line.count("<--")==1 and ablock and                                             #ASSIGNMENT
           not( fname in line and line[len(fname)] not in letters+list("0123456789_") )):   #return handled elsewhere
        aspos=line.find("<--")
        vname=line[:aspos]
        if(vname[-1]==" "):
          vname=vname[:-1]
        if("[" in vname):
          lbrpos=vname.find("[")
          vname=vname[:lbrpos]
        if(vname in cdict[fname].keys()):                                      #obsolete
          vname=vname if vname[0]!='_' else vname[1:]
          errmsg="\n> ΔΕΝ ΕΠΙΤΡΕΠΕΤΑΙ ΕΚΧΩΡΗΣΗ ΤΙΜΗΣ ΣΤΗ ΣΤΑΘΕΡΑ "+vname
          raise Exception
        if(vname not in vdict[fname].keys() and vname!=fname):
          vname=vname if vname[0]!='_' else vname[1:]
          errmsg="\n> ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ "+vname
          if(fname=="_main_"):
            print("ΤΟ ΠΡΟΓΡΑΜΜΑ",PROname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i])#list(vdict[fname].keys()))  #ΤΙΜΗ
          else:
            print("ΤΟ ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i])#,list(vdict[fname].keys()))
          raise Exception
        pcmd="try:\n"+" "*(nsp+2)
        pcmd+=xpr(list(line[:aspos]+"<--"))+"assign("+xpr(list(line[:aspos]+",")+cmd[aspos+3:],pblock,vargs)+")\n"+" "*(nsp)
        pcmd+="except Exception as e:\n"+" "*(nsp+2)
        pcmd+="raise RuntimeError(e) from e"                                #TYPE CHECK

      elif(cmd[:6]==list("ΓΡΑΨΕ ") and ablock):                                  #PRINT
        if(fblock):
          errmsg="η \'ΓΡΑΨΕ\' δεν επιτρέπεται μέσα σε ΣΥΝΑΡΤΗΣΗ"
          raise Exception
        pcmd="print("+xpr(cmd[6:],pblock,vargs)+")"
      elif(cmd[:8]==list("ΔΙΑΒΑΣΕ ") and ablock):                                #INPUT
        if(fblock):
          errmsg="η \'ΔΙΑΒΑΣΕ\' δεν επιτρέπεται μέσα σε ΣΥΝΑΡΤΗΣΗ"
          raise Exception
        if(interS("+,-,*,/,%, and , or , not , True , False ".split(","),xpr(line))!=[] or "(" in line):
          errmsg=("\n> δεν επιτρέπεται να δοθεί ΕΚΦΡΑΣΗ ως όρισμα στη ΔΙΑΒΑΣΕ")
          raise Exception
        temp=xpr(list(line[8:]))
        vars=temp.split(",")
        pcmd=",".join([(v) for v in vars])+"="
        for v in vars:
          vname = str(v)                              #ΕΛΕΓΧΟΣ ΔΗΛΩΣΗΣ ΜΕΤ/ΤΩΝ ΣΤΗΝ ΕΙΣΟΔΟ
          if(vname[0]=="_"):
            vname=vname[1:]
          if("[" in vname):
            lbrpos=vname.find("[")
            vname=vname[:lbrpos]
          if(vname not in vdict[fname].keys() and vname!=fname):
            vname=vname if vname[0]!='_' else vname[1:]
            errmsg="\n> ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ "+vname
            if(fname=="_main_"):
              print("ΤΟ ΠΡΟΓΡΑΜΜΑ",PROname,"ΕΧΕΙ","ΜΕΤΑΒΛΗΤΕΣ",[i for i in vdict[fname].keys() if "." not in i])#,list(vdict[fname].keys()))
            else:
              print("ΤΟ ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ",[i for i in vdict[fname].keys() if "." not in i])#,list(vdict[fname].keys()))
            raise Exception
          smartV= "" if not smart else comment[comment.find("#")+1:].replace(" ","")+","
          pcmd+=("_.Rinput("+(v)+","+str(report)+",\""+(smartV)+"\"),")*(randIN)+"_.TCinput(),"*(1-randIN)
        pcmd=pcmd[:-1]
      elif(cmd[:3]==list("ΑΝ ") and ablock):                    #IF
        ifN+=1
        ifline.append(str(nl))
        ALLline.append(str(nl))
        ALLblock.append("if")
        block=True
        pcmd="if("
        if(cmd[-4:]!=list("ΤΟΤΕ")):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΤΟΤΕ"
          raise Exception
        pcmd+=xpr(cmd[3:-5],pblock,vargs)+"):"
      elif(cmd[:10]==list("ΑΛΛΙΩΣ_ΑΝ ") and ablock):           #ELIF
        if(ifN<0):
          errmsg=("> unexpected \'ΑΛΛΙΩΣ_ΑΝ\'")
          raise Exception
        block=True
        nsp-=2
        pcmd="elif("
        if(cmd[-4:]!=list("ΤΟΤΕ")):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΤΟΤΕ"
          raise Exception
        pcmd+=xpr(cmd[10:-5],pblock,vargs)+"):"
      elif(line in rword("ΑΛΛΙΩΣ") and ablock):          #ELSE
        if(ifN<0):
          errmsg=("> unexpected \'ΑΛΛΙΩΣ\'")
          raise Exception          
        block=True
        nsp-=2
        pcmd="else:"
      elif(line in rword("ΤΕΛΟΣ_ΑΝ") and ablock):    #ENDIF
        ifN-=1
        if(ifN<0):
          errmsg=("> unexpected \'ΤΕΛΟΣ_ΑΝ\'")
          raise Exception
        if(ALLblock[-1]!="if"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]+"\n"
          errmsg+=("> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        ALLblock.pop(-1)
        ifline.pop(-1)
        ALLline.pop(-1)
        deblock=True
      elif(cmd[:8]==list("ΕΠΙΛΕΞΕ ") and ablock):           #SWITCH
        swN+=1
        swline.append(str(nl))
        ALLline.append(str(nl))
        ALLblock.append("sw")
        block=True
        pcmd="sw"+str(swN)+"="+xpr(cmd[8:],pblock,vargs)+"\n"+nsp*" "
        pcmd+="if(False):\n"+nsp*" "
        pcmd+="  0"
      elif(cmd[:10]==list("ΠΕΡΙΠΤΩΣΗ ") and ("ΑΛΛΙΩΣ" not in line) and ablock):   #CASE
        if(swN<0):
          errmsg="> unexpected \'ΠΕΡΙΠΤΩΣΗ\'"
          raise Exception
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
        if(swN<0):
          errmsg="> unexpected \'ΠΕΡΙΠΤΩΣΗ ΑΛΛΙΩΣ\'"
          raise Exception
        block=True
        nsp-=2
        pcmd="else:"
      elif(line in rword("ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ") and ablock):    #ENDSWITCH
        swN-=1
        if(swN<0):
          errmsg=("> unexpected \'ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ\'")
          raise Exception
        if(ALLblock[-1]!="sw"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]+"\n"
          errmsg+=("> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        ALLblock.pop(-1)
        swline.pop(-1)
        ALLline.pop(-1)
        deblock=True
      elif(cmd[:4]==list("ΟΣΟ ") and ablock):           #WHILE
        whN+=1
        ALLblock.append("wh")
        block=True
        whv.append("dummy")
        whstep.append("0")
        whline.append(str(nl))
        ALLline.append(str(nl))
        pcmd=whv[-1]+"=0\n"+nsp*' ' # for +
        pcmd+="while("
        if(cmd[-9:]!=list("ΕΠΑΝΑΛΑΒΕ")):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΕΠΑΝΑΛΑΒΕ"
          raise Exception
        pcmd+=xpr(cmd[4:-10],pblock,vargs)+"):"
      elif(cmd[:4]==list("ΓΙΑ ") and ablock):           # FOR ΜΕΣΩ WHILE
        whN+=1
        whline.append(str(nl))
        ALLline.append(str(nl))
        ALLblock.append("wh")
        if("ΑΠΟ " not in line or "ΜΕΧΡΙ " not in line 
           or line.count("ΓΙΑ")>1 or line.count("ΑΠΟ")>1 or line.count("ΜΕΧΡΙ")>1 or line.count("ΜΕ_ΒΗΜΑ")>1):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ ΤΗΣ ΕΝΤΟΛΗΣ ΓΙΑ"
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
            errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ ΤΗΣ ΕΝΤΟΛΗΣ ΓΙΑ"
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
          vname=vname if vname[0]!='_' else vname[1:]
          errmsg="\n> ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ "+vname
          if(fname=="_main_"):
            print("ΤΟ ΠΡΟΓΡΑΜΜΑ ΕΧΕΙ","ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i])#,list(vdict[fname].keys()))
          else:
            print("ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i])#,list(vdict[fname].keys()))
          raise Exception
        pcmd+=whv[-1]+"="+xpr(cmd[pos1+4:pos2],pblock,vargs)+"\n"+" "*nsp
        pcmd+="while("  #for "
        if("ΜΕ_ΒΗΜΑ" in line):
          pcmd+=xpr(cmd[4:pos1],pblock,vargs)+"*correction"+str(whN)+" <= "+xpr(cmd[pos2+6:pos3],pblock,vargs)+"*correction"+str(whN)+"):"
        else:
          pcmd+=xpr(cmd[4:pos1],pblock,vargs)+"<= "+xpr(cmd[pos2+6:],pblock,vargs)+"):\n"+" "*nsp
      elif(line in rword("ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ") and ablock):                                        #ENDFOR/WHILE
        whN-=1
        if(whN<0):
          errmsg=("> unexpected \'ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ\'")
          raise Exception
        if(ALLblock[-1]!="wh"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]+"\n"
          errmsg+=("> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        ALLblock.pop(-1)
        whline.pop(-1)
        ALLline.pop(-1)
        pcmd=whv.pop(-1)+"+="+whstep.pop(-1)   # for +
        deblock=True
      elif(line in rword("ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ") and ablock):    #DO
        dwhN+=1
        dwhline.append(str(nl))
        ALLline.append(str(nl))
        ALLblock.append("dwh")
        block=True
        pcmd="while(True):"
      elif(cmd[:12]==list("ΜΕΧΡΙΣ_ΟΤΟΥ ") and ablock):  #_WHILE
        dwhN-=1
        if(dwhN<0):
          errmsg=("> unexpected \'ΜΕΧΡΙΣ_ΟΤΟΥ\'")
          raise Exception
        if(ALLblock[-1]!="dwh"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]+"\n"
          errmsg+=("> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        ALLblock.pop(-1)
        dwhline.pop(-1)
        ALLline.pop(-1)
        deblock=True
        pcmd="if("+xpr(list("".join(cmd[12:])),pblock,vargs)
        pcmd+="):\n"+" "*(nsp+2)+"break"
      elif(cmd[:10]==list("ΠΡΟΓΡΑΜΜΑ ")):                     # MAIN  ---------------------------------------------------------------
        fname="_main_"
        PROname=line[10:]
        if(PROname[-1] in "\n "):
          PROname=PROname[:-1]
        if(not isname(PROname)):
          errmsg=PROname+" : ΜΗ ΕΓΚΥΡΟ ΟΝΟΜΑ ΠΡΟΓΡΑΜΜΑΤΟΣ"
          raise Exception
        cdict[fname],vdict[fname]=dict(),dict()
        if(fblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ"
          raise Exception
        if(pblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ"
          raise Exception
        if(tryblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ"
          raise Exception
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(swN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(dwhN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        block=True
        acounter+=1
        #mblock=True
        tryblock=True
        exe=True
        pcmd="def main():\n  N1=NUM()\n"
      elif(line in rword("ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ")+["ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ "+PROname]):     #END MAIN
        if(not tryblock):
          errmsg="\n> unexpected \'ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\'"
          raise Exception
        tryblock=False
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(swN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(dwhN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(not ablock):
          errmsg="\n> expected \'ΑΡΧΗ\'"
          raise Exception
        ablock=False
        nsp=0
        pcmd+="\n#ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\n"
      elif(cmd[:10]==list("ΣΥΝΑΡΤΗΣΗ ")):           #FUNCTION
        if(fblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ"
          raise Exception
        if(pblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ"
          raise Exception
        if(tryblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ"
          raise Exception
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(swN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(dwhN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
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
          errmsg="\n> ΜΗ ΕΓΚΥΡΟ ΟΝΟΜΑ ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ: "+fname
          raise Exception
        cdict[fname],vdict[fname]=dict(),dict()
        ftypos="".join(cmd[tpos+1:])
        if ftypos[0]==" ":
          ftypos=ftypos[1:]
        if ftypos=="ΑΚΕΡΑΙΑ":
          ftypos="int"
        elif ftypos=="ΠΡΑΓΜΑΤΙΚΗ":
          ftypos="float"
        elif ftypos=="ΧΑΡΑΚΤΗΡΑΣ":
          ftypos="str"
        elif ftypos=="ΛΟΓΙΚΗ":         #ΛΟΓΙΚΗ
          ftypos="bool"
        else:
          errmsg="ΜΗ ΕΓΚΥΡΟΣ ΤΥΠΟΣ ΣΥΝΑΡΤΗΣΗΣ"
          raise Exception

        pcmd+=xpr(fname)+"("
        lfn=len(fname)
        vargs="".join(cmd[len(fname)+1:tpos-1]).split(",")
        for a in vargs:
          pcmd+=xpr(a)+","
        pcmd=pcmd[:-1]+"): " #function parameter list
        pcmd+="#"+(ftypos)+"\n  "

        for a in vargs:
          pcmd+="_"+xpr(a)+","
        pcmd=pcmd[:-1]+"="  #backup values for mutable
        for a in vargs:
          pcmd+=xpr(a)+","
        pcmd=pcmd[:-1]+"\n"
        pcmd+=" "*(nsp+2)+"N1=NUM()\n"
      elif(fblock and fname==line[:lfn] and ("<--"==line[lfn:lfn+3] or " <--"==line[lfn:lfn+4])): #RETURN
        pcmd+="__"+xpr(fname)+xpr(list("<--"))+"assign("+ftypos+","+xpr(cmd[len(fname)+3:])+")"
        nfvalue=False
      elif(line in rword("ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ")):         #ENDFUNCTION
        if(not fblock):
          errmsg="\n> unexpected \'ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ\'"
          raise Exception
        if(not ablock):
          errmsg="\n> expected \'ΑΡΧΗ\'"
          raise Exception
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(swN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(dwhN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        ablock=False
        for a in vargs:
          pcmd+=xpr(a)+","
        pcmd=pcmd[:-1]+" = "  #restore values
        for a in vargs:
          pcmd+="_"+xpr(a)+","
        pcmd=pcmd[:-1]+"\n  "
        pcmd+="return "+"__"+xpr(fname)
        deblock=True
        fblock=False
        fname=""
        pcmd+="\n#ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ\n"
      elif(cmd[:11]==list("ΔΙΑΔΙΚΑΣΙΑ ")):           #PROCEDURE
        if(fblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ"
          raise Exception
        if(pblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ"
          raise Exception
        if(tryblock):
          errmsg="\n> expected \'ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ"
          raise Exception
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(swN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(dwhN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        pblock=True
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
          errmsg="\n> ΜΗ ΕΓΚΥΡΟ ΟΝΟΜΑ ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ: "+fname
          raise Exception
        cdict[fname],vdict[fname]=dict(),dict()
        pcmd+=xpr(fname)+"("
        vargs="".join(cmd[len(fname)+1:-1]).split(",")
        for a in vargs:
          pcmd+=xpr(a)+","
        pcmd=pcmd[:-1]+"):"+"\n"
        pcmd+=" "*(nsp+2)+"N1=NUM()\n"
      elif(line in rword("ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ")):    #ENDPROCEDURE
        if(not pblock):
          errmsg="\n> unexpected \'ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\'"
        if(not ablock):
          errmsg="\n> expected \'ΑΡΧΗ\'"
          raise Exception
        if(ifN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(swN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΙΛΟΓΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(whN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(dwhN!=0):
          errmsg=("ΑΝΟΙΧΤΗ ΔΟΜΗ ΕΠΑΝΑΛΛΗΨΗΣ in line "+ALLline.pop(-1))
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        if(not ablock):
          errmsg="\n> expected \'ΑΡΧΗ\'"
          raise Exception
        ablock=False
        pblock=False
        deblock=True
        pcmd="return "                             #procedure by return
        for a in vargs:
          pcmd+=xpr(a)+','
        pcmd=pcmd[:-1]
        fname=""
        pcmd+="\n#ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\n"
      elif(cmd[:7]==list("ΚΑΛΕΣΕ ") and ablock):          #ΚΑΛΕΣΕ
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
          if(v[0]=="_"):
            v=v[1:]
          if(v in vdict[fname]):
            pcmd+=xpr(v)+","
          else:
            pcmd+="_dummy,"
        pcmd=pcmd[:-1]+"="
        pcmd+="".join(Xcmd[7:])
      else:
        errmsg=""
        if(not(tryblock or fblock or pblock)):
          errmsg="\n> ΛΕΙΠΕΙ Η ΔΗΛΩΣΗ ΠΡΟΓΡΑΜΜΑΤΟΣ/ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ"
        elif(not vblock and ("ΑΚΕΡΑΙΕΣ" in line or "ΧΑΡΑΚΤΗΡΕΣ" in line or "ΠΡΑΓΜΑΤΙΚΕΣ" in line or "ΛΟΓΙΚΕΣ" in line)):
          errmsg="\n> expected \'ΜΕΤΑΒΛΗΤΕΣ\'"
        elif(not cblock and ("=" in line)):
          errmsg="\n> expected \'ΣΤΑΘΕΡΕΣ\'"
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
    if(tryblock):              #ΕΝΤΟΣ ΠΡΟΓΡΑΜΜΑΤΟΣ
      errmsg="\n> expected \'ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ"
      raise Exception
    if(fblock):              #ΕΝΤΟΣ ΣΥΝΑΡΤΗΣΗΣ
      errmsg="\n> expected \'ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ"
      raise Exception
    if(pblock):              #ΕΝΤΟΣ ΔΙΑΔΙΚΑΣΙΑΣ
      errmsg="\n> expected \'ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ\'"  #"ΛΕΙΠΕΙ ΤΟ ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ"
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
    print("-"*75+'\n'+"ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ: "+errmsg.replace("Exception()","> μη έγκυρη σύνταξη")+"\n----> "+str(nl)+". "+line)   #str(nl+1)
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
