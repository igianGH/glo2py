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
  print("0405250020")

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
  global IGpreamble
  fname="source"
  fOUT=open(fname+".py",'w')
  fOUT.write(IGpreamble)
  X=xpr(list(code))
  fOUT.write("def main():\n  N1,N0,B1=NUM(1),NUM(0),myB()\n")
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
  
def interpreter(file="source",developer=False,dline=True,smart=True,report=False,randIN=True,test=False):
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
    tGL={'int':"ΑΚΕΡΑΙΑ",'float':"ΠΡΑΓΜΑΤΙΚΗ",'str':"ΧΑΡΑΚΤΗΡΑΣ",'bool':"ΛΟΓΙΚΗ",'myA':"ΠΙΝΑΚΑΣ",'pholder':"NULL"}
    errmsg2=""
    errmsg=str(sys.exc_info()[1])
    trb=str(traceback.format_exc())
    sb=trb[0:]
    if(developer):
      print("\n"+trb)
    ierr=trb.rfind("Error:")
    trb=trb[ierr+7:]
    linecorr=1
    if('%' in trb):
      imod=trb.find('%')
      trb=trb[:imod]+"MOD"+trb[imod+1:]
      imod=sb.find('%')
      sb=sb[:imod]+"MOD"+sb[imod+1:]
    #if("not supported between instances" in sb and "\'type\'" in sb):
    #if("\'pholder\'" in sb and "unsupported operand" in sb):
      #errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:\n> αποτυχία ΑΠΟΤΙΜΗΣΗΣ, δεν έχουν λάβει τιμή όλες οι ΜΕΤΑΒΛΗΤΕΣ"
    if( ("not supported between instances" in trb or "unsupported operand" in trb) and "\'pholder\'" in trb):
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:\n> η πράξη δεν ορίζεται μεταξύ"
      rall={trb.rfind(ri):ri for ri in tGL.keys() if trb.rfind(ri)>-1}
      fr1,fr2=min(rall.keys()),max(rall.keys())
      errmsg2+=" \'"+tGL[rall[fr1]]+"\' και \'"+tGL[rall[fr2]]+"\'"
      errmsg2+=" (πρέπει να λάβουν ΤΙΜΗ όλες οι ΜΕΤΑΒΛΗΤΕΣ)"
    elif("cannot access local variable" in trb):
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:\n> ΑΠΟΤΥΧΙΑ ΑΠΟΤΙΜΗΣΗΣ, η μεταβλητή \'"
      rpos=trb.rfind("cannot access local variable")
      errmsg2+=trb[trb[rpos:].find("\'")+1 : trb.rfind("\'")]+"\' δεν έχει λάβει τιμή"
    #elif("yntax" in sb or "efined" in sb or "unsupported operand" in sb 
      #or "only concatenate" in sb or "no attribute \'value\'" in sb or "not supported between instances of" in sb
      #or "object is not subscriptable" in sb or "object is not callable" in sb): # or "TypeError"'ΤΙΜΗ'
      #errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
    elif("comma" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ, Μήπως ξεχάσατε κάποιο κόμμα, κενό ή τελεστή?"
    elif("cannot assign to expression" in trb or "aybe you meant \'==\' instead of \'=\'" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> δεν επιτρέπεται να εκχωρηθεί τιμή σε ΕΚΦΡΑΣΗ"
    elif("object is not subscriptable" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> ΛΑΝΘΑΣΜΕΝΗ ΔΙΑΣΤΑΣΗ αντικειμένου"#sb[sb.find("\'")+1 : sb.rfind("\'")]+"\'"
    elif("name" in trb and "not defined" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      vname=trb[trb.find("name \'")+6:trb.find("\' is not defined")]
      vnamecl=vname if vname[0]!='_' else vname[1:]
      errmsg2+="\n> ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ \'"+vnamecl+"\'"
    elif("only concatenate" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> μη επιτρεπτή πράξη σε ΧΑΡΑΚΤΗΡΕΣ"
    elif("unsupported operand" in trb or "not supported between instances of" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> πράξη μεταξύ ΑΣΥΜΒΑΤΩΝ αντικειμένων"
      rall={trb.rfind(ri):ri for ri in tGL.keys() if trb.rfind(ri)>-1}
      fr1,fr2=min(rall.keys()),max(rall.keys())
      errmsg2+=" \'"+tGL[rall[fr1]]+"\' και \'"+tGL[rall[fr2]]+"\'"
    elif("no attribute \'ΤΙΜΗ\'" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ, αυτό το αντικείμενο δεν είναι ΠΙΝΑΚΑΣ"
    elif("object is not callable" in trb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ, αυτό το αντικείμενο δεν είναι ΣΥΝΑΡΤΗΣΗ"
    elif("yntax" in sb or "efined" in sb):
      errmsg2+="ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ:"
      errmsg2+="\n> "+trb.split('\n')[0].replace("invalid syntax","ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ")
    elif("invalid literal for int" in trb or "bad operand type for abs" in trb or "must be real number" in trb):
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      errmsg2+="\n> το όρισμα έπρεπε να είναι ΑΡΙΘΜΗΤΙΚΗ ΤΙΜΗ"
    elif("index" in trb and "out of bounds" in trb or "valid indices" in trb
      or "indices must be integers" in trb or "index out of range" in trb):
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      errmsg2+="\n> ΥΠΕΡΒΑΣΗ ΟΡΙΩΝ ΠΙΝΑΚΑ"
    elif("division by zero" in trb):
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      errmsg2+="\n> ΔΙΑΙΡΕΣΗ ΜΕ 0 (ΜΗΔΕΝ)"
    elif("math domain error" in trb or "class \'complex\'" in trb):
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      errmsg2+="\n> ΔΕΝ ΟΡΙΖΕΤΑΙ Η ΑΡΙΘΜΗΤΙΚΗ ΠΡΑΞΗ"
    elif("xceeds the limit" in trb or "OverflowError" in trb):
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      errmsg2+="\n> ΠΟΛΥ ΜΕΓΑΛΟΣ αριθμός"
    else:
      errmsg2+="ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΚΤΕΛΕΣΗ:"
      errmsg2+="\n"+trb.split('\n')[0]
    print("-"*75+'\n'+errmsg2)
    msnl=snl=0
    msnl=sb[:]
    foundline=False
    while("#<" in msnl):    #//
      foundline=True
      msnl=msnl[msnl.find("#<")+2 : msnl.find(">#")]
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
          if("#<" in line):                   # εύρεση γραμμής όπου απέτυχε η μετάφραση/εκτέλεση #//
            snl=int(line[line.find("#<")+2 : line.find(">#")])
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
    names[line[:sep]]=line[sep+1:-1]

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
  try:
    v==v
  except:
    return TCinput()
  global letters
  global names
  ndigits=r.randrange(1,9)
  if(type(v)==bool or hasattr(v,'typos') and v.typos==bool):
    raise SyntaxError("ΔΕ μπορεί να δοθεί ΛΟΓΙΚΗ ΤΙΜΗ από την ΕΙΣΟΔΟ")
  if(type(v)==int or hasattr(v,'typos') and v.typos==int):
    v=(r.randrange(-10**ndigits,10**ndigits))
  elif(type(v)==float or hasattr(v,'typos') and v.typos==float):
    v=(r.random()*r.randrange(-10**ndigits,10**ndigits))
  elif(type(v)==str or hasattr(v,'typos') and v.typos==str):  
    v=("".join(r.choices(letters[-24:],k=ndigits)))  
    if(smartV!=""):
      try:
        v=r.choice([i for i in names.keys() if names[i] in smartV])
      except:
        v=("".join(r.choices(letters[-24:],k=ndigits)))
      if("," in smartV):
        v2=[j for j in smartV.split(",") if [i for i in names.keys() if names[i] in j]==[]]
        v = v if (r.randrange(1,101)>5 or v2==[]) else r.choice(v2)
  elif(hasattr(v,'ΤΙΜΗ')):
    raise RuntimeError("> δεν επιτρέπεται να δοθεί όρισμα ΠΙΝΑΚΑΣ στη ΔΙΑΒΑΣΕ")
  if(report):
    print(">διαβάστηκε το",v)
  return v

def TCinput(prompt="ΕΙΣΟΔΟΣ: "):
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

def eprint(*PP):
  '''
  Καλεί την print εκτός αν κάποια τιμή είναι type ή myA, οπότε διακόπτει την εκτέλεση
  '''
  for p in PP:
    if(hasattr(p,'typos')):
      raise RuntimeError("> κάποια μεταβλητή δεν έχει λάβει τιμή")
    if(hasattr(p,'ΤΙΜΗ')):
      raise SyntaxError("δεν επιτρέπεται να δοθεί όρισμα ΠΙΝΑΚΑΣ στη ΓΡΑΨΕ")
    print(p,end=" ")
  print("")

def xpr(s,pblock=False,v=[],swflag=False,ptype="ΓΛΩΣΣΑ"):
  '''
  Μετατρέπει λίστα χαρακτήρων σε έγκυρη έκφραση της ΓΛΩΣΣΑΣ
  s
    list από str με μήκος 1
  pblock
    αν είναι True τότε καλείται μέσα από ΔΙΑΔΙΚΑΣΙΑ, default False. DEPRECATED
  v
    λίστα με τις μεταβλητές της ΔΙΑΔΙΚΑΣΙΑΣ. DEPRECATED
  swflag
    αν είναι True τότε επιστρέφεται μία λιγότερη '(' στην αρχή της έκφρασης
    γιατί καλείται από ΕΠΙΛΕΞΕ
  ptype
    str, αν είναι 'math' τότε ακολουθείται η ΜΑΘΗΜΑΤΙΚΗ προτεραιότητα για το ^
  '''
  global numbersP
  if(type(s)==str):
    s=list(s)
  buffer=" "
  s=["("]+s+[")"]
  bflag=False
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
      pcmd+="not "
      s=s[3:]
      bflag=True
      buffer+="ΟΧΙ"
    elif(s[:3]==list("ΚΑΙ") and (len(s)<4 or s[3] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=") & B1 & ("
      s=s[3:]
      bflag=True
      buffer+="ΚΑΙ"
    elif(s[:1]==list("Ή") and (len(s)<2 or s[1] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+=") | B1 | ("
      s=s[1:]
      bflag=True
      buffer+="Ή"
    elif(s[:2]==list("<>")):
      pcmd+="!="
      s=s[2:]
      bflag=True
      buffer+="<>"
    elif(s[:2]==list("<=")):
      pcmd+="<="
      s=s[2:]
      bflag=True
      buffer+="<="
    elif(s[:2]==list(">=")):
      pcmd+=">="
      s=s[2:]
      bflag=True
      buffer+=">="
    elif(s[:3]==list("<--")):
      pcmd+="="
      s=s[3:]
      buffer+="<--"
    elif(s[0]=="+"):
      pcmd+="+N0+"
      s.pop(0)
      buffer+="+"
    elif(s[0]=="*"):
      pcmd+="*N1*"
      s.pop(0)
      buffer+="*"
    elif(s[0]=="/"):
      pcmd+="/N1/"
      s.pop(0)
      buffer+="/"
    elif(s[0]=="="):
      pcmd+="=="
      s.pop(0)
      bflag=True
      buffer+="=="
    elif(s[0]=="^"):
      if(ptype=="math"):
        pcmd+="**N1**"
      else:
        pcmd+="^N1^"
      s.pop(0)
      buffer+="^"
    elif(s[:6]==list("ΑΛΗΘΗΣ") and (len(s)<7 or s[6] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="True "
      s=s[6:]
      bflag=True
      buffer+="ΑΛΗΘΗΣ"
    elif(s[:6]==list("ΨΕΥΔΗΣ") and (len(s)<7 or s[6] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="False "
      s=s[6:]
      bflag=True
      buffer+="ΨΕΥΔΗΣ"
    elif(s[:3]==list("DIV") and (len(s)<4 or s[3] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="//N1//"
      s=s[3:]
      buffer+="DIV"
    elif(s[:3]==list("MOD") and (len(s)<4 or s[3] not in letters+["_"]) and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="%N1%"
      s=s[3:]
      buffer+="MOD"
    elif(s[:4]==list("Τ_Ρ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="m.sqrt("
      s=s[4:]
      buffer+="Τ_Ρ("
    elif(s[:4]==list("Α_Τ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="abs("
      s=s[4:]
      buffer+="Α_Τ("
    elif(s[:4]==list("Α_Μ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="int("
      s=s[4:]
      buffer+="Α_Μ("
    elif(s[:3]==list("ΗΜ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="m.sin(m.pi/180*"
      s=s[3:]
      buffer+="ΗΜ("
    elif(s[:4]==list("ΣΥΝ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="m.cos(m.pi/180*"
      s=s[4:]
      buffer+="ΣΥΝ("
    elif(s[:3]==list("ΕΦ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="m.tan(m.pi/180*"
      s=s[3:]
      buffer+="ΕΦ("
    elif(s[:4]==list("ΛΟΓ(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="m.log("
      s=s[4:]
      buffer+="ΛΟΓ("
    elif(s[:2]==list("Ε(") and (len(buffer)<1 or buffer[-1] not in letters+["_"])):
      pcmd+="m.exp("
      s=s[2:]
      buffer+="Ε("
    else:
      if(s[0] in letters[:52] and buffer[-1] not in letters[:52]):
        pcmd+="_"
      pcmd+=s[0]
      if(s[0] in "<>"):
        bflag=True
      buffer+=s.pop(0)
  telestes="+,-,*,/,//,%,^,|,&,<,>,=,==,<>,<=,>=,**".split(",")#,(,)
  teldict,teli={},[]
  ss=pcmd
  for i in range(len(ss)-1):
    if( ss[i:i+2] in telestes ):
      teldict[i]=ss[i:i+2]
      teli.append(i)
    if( ss[i:i+1] in telestes ):
      teldict[i]=ss[i:i+1]
      teli.append(i)
  powblock=False
  for j in range(len(teli)-1,0,-1):
    if(teldict[teli[j-1]] == "^" and not powblock):
      powblock=True
      ss=ss[:teli[j]]+")"+ss[teli[j]:]
    elif(teldict[teli[j]] != "^" and powblock):
      powblock=False
      ss=ss[:teli[j]+len(teldict[teli[j]])]+"("+ss[teli[j]+len(teldict[teli[j]]):]
  if(powblock):
    ss="("+ss
  if(ss[0]=="(" and ss[-1]==")"):
    ss=ss[1:-1]
  pcmd=ss
  return( ("(" if (bflag and not swflag) else "") +pcmd+ (") == B1" if (bflag) else "") )  #and not swflag

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

IGpreamble='''
import random as r
import math as m
import numpy as np
import __ as _
import sys
import traceback
from copy import deepcopy as cdc
class NUM:
  def __init__(self,value=1):
    self.value=value
  def __mul__(self,x):  #NUM*x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return self.value*x**1
  def __rmul__(self,x): #x*NUM
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
  def __add__(self,x):  #NUM0+x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return self.value+x**1
  def __radd__(self,x): #x+NUM0
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
  def __sub__(self,x):  #NUM0-x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return self+(-x)
  def __rsub__(self,x): #x-NUM0
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
  def __truediv__(self,x):  #NUM1/x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return self.value/x**1
  def __rtruediv__(self,x): #x/NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
  def __floordiv__(self,x):  #NUM1//x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return self.value//x**1
  def __rfloordiv__(self,x): #x//NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
  def __mod__(self,x):  #NUM1%x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return self.value%x**1
  def __rmod__(self,x): #x%NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
  def __pow__(self,x):  #NUM1**x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
  def __rpow__(self,x): #x**NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return x**self.value
  def __xor__(self,x):  #NUM1**x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return self.value**x
  def __rxor__(self,x): #x**NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    return NUM(x**1)
class myA:
  def __init__(self,shape,typos):
    A=[typos for i in range(shape.pop(-1))]
    d=1
    while(shape!=[]):
      d+=1
      A=[cdc(A) for i in range(shape.pop(-1))]
    self.ΤΙΜΗ=A
    self.typos=typos
    self.dimension=d
  def __invert__(self):
    if(self.dimension==1 and len(self.ΤΙΜΗ)<21):
      if( hasattr(self.ΤΙΜΗ[0],'typos') ):
        raise RuntimeError(\"> κάποια μεταβλητή δεν έχει λάβει τιμή\")
      print(\"[\"+str(self.ΤΙΜΗ[0]),end=\", \")
      for i in self.ΤΙΜΗ[1:-1]:
        if( hasattr(i,'typos') ):
          print(\"\")
          raise RuntimeError(\"> κάποια μεταβλητή δεν έχει λάβει τιμή\")
        print(i,end=\", \")
      if( hasattr(self.ΤΙΜΗ[-1],'typos') ):
        print(\"\")
        raise RuntimeError(\"> κάποια μεταβλητή δεν έχει λάβει τιμή\")
      print(str(self.ΤΙΜΗ[-1])+\"]\")
      return \"-\"*75+\"\\nWarning: το ~ δεν επιτρέπεται στη ΓΛΩΣΣΑ\\n\"
    n=0
    for l in self.ΤΙΜΗ:
      n+=1
      print(str(n)+\".\",l)
    return \"-\"*75+\"\\nWarning: το ~ δεν επιτρέπεται στη ΓΛΩΣΣΑ\\n\"
class myB:
  def __init__(self,value=True):
    self.Bvalue=value
  def __and__(self,other):
    if(type(other)==bool):
      return self.Bvalue and other
    elif(hasattr(other,'Bvalue')):
      return myB(self.Bvalue and other.Bvalue)
    else:
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
  def __rand__(self,other):
    if(type(other)==bool):
      return myB(other and True)
    elif(hasattr(other,'Bvalue')):
      return myB(other.Bvalue and True)
    else:
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
  def __or__(self,other):
    if(type(other)==bool):
      return self.Bvalue or other
    elif(hasattr(other,'Bvalue')):
      return myB(self.Bvalue or other.Bvalue)
    else:
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
  def __ror__(self,other):
    if(type(other)==bool):
      return myB(other or False)
    elif(hasattr(other,'Bvalue')):
      return myB(other.Bvalue or False)
    else:
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
  def __eq__(self,other):
    if(type(other)==bool or hasattr(other,'Bvalue')):
      return other
    else:
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
class pholder:
  def __init__(self,typos):
    self.typos=typos
def assign2(y,x,segment=False,nl=1):
  tGL={int:"ΑΚΕΡΑΙΑ",float:"ΠΡΑΓΜΑΤΙΚΗ",str:"ΧΑΡΑΚΤΗΡΑΣ",bool:"ΛΟΓΙΚΗ",myA:"ΠΙΝΑΚΑΣ"}
  tt,j={},1
  for i in [y,x]:
    if( i in tGL.keys() ):
      tt[j]=tGL[i]
    elif( type(i) in tGL.keys() ):
      tt[j]=tGL[type(i)]
    else:
      tt[j]=tGL[i.typos]
    j+=1
  if(tt[2]=="ΠΙΝΑΚΑΣ"):
    raise RuntimeError("> Δεν επιτρέπεται εκχώρηση απευθείας από ΠΙΝΑΚΑ")
  if(tt[1]=="ΠΙΝΑΚΑΣ"):
    raise RuntimeError("> Δεν επιτρέπεται εκχώρηση απευθείας σε ΠΙΝΑΚΑ")
  if(tt[2]==tt[1]):
    return x
  elif(tt[1]=="ΠΡΑΓΜΑΤΙΚΗ" and tt[2]=="ΑΚΕΡΑΙΑ"):
    return x
  raise RuntimeError("> Δεν επιτρέπεται εκχώρηση τιμής τύπου "+tt[2]+" σε μεταβλητή τύπου "+tt[1])
\n'''+"#"*80+"\n"

def interpretM(file="source",randIN=True,cmp=False,aa=1,smart=False,report=False,test=False):
  segment,segblock=True,False
  with open(file,"r") as fin:     # ΤΜΗΜΑ ΠΡΟΓΡΑΜΜΑΤΟΣ -------------------------
    for line in fin:
      strseg=False
      linecl=""
      for c in line:
        if(c=="\'" and not strseg):
          strseg=True
        elif(c=="\'" and strseg):
          strseg=False
        elif(not strseg):
          linecl+=c
      if(interS(["ΠΡΟΓΡΑΜΜΑ","ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ","ΣΥΝΑΡΤΗΣΗ","ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ","ΔΙΑΔΙΚΑΣΙΑ","ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ"],linecl[:linecl.find("!")])!=[]):
        segment=False
  import importlib
  global letters,Reserved,IGpreamble
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
  fout.write(IGpreamble)                       # PREAMBLE ^^^^^^^^^^^^^^^^^^^^^^
  if(segment and not segblock):      # ΤΜΗΜΑ ΠΡΟΓΡΑΜΜΑΤΟΣ ----------------------
    randIN=False
    segblock=True
    tryblock=True
    ablock=True
    fname="_main_"
    cdict[fname],vdict[fname]=dict(),dict()
    block=True
    acounter+=1
    exe=True
    print("-"*75+"\nΤΜΗΜΑ ΠΡΟΓΡΑΜΜΑΤΟΣ:\n"+"-"*75)
    fout.write('''
def main():
  N1,N0,B1,A1=NUM(1),NUM(0),myB(),myA([1],int)
\n''')
  try:
    for line in fin:
      nl+=1
      pcmd=""
      comment=""
      if(pline!=""):
        line=pline+line
        pline=""
      for cmpos in range(len(line)):    #COMMENTS
        if(line[cmpos]=="!" and line[:cmpos].count("\'")%2==0):
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
      lineNS,cflags=line.replace(" ",""),"[] [, ,] (, ,) ,, .. ,. ., "
      cflags+="[+ +] [* *] [/ /] [MOD MOD] [DIV DIV] -] [^ ^] "
      cflags+="(+ +) (* *) (/ /) (MOD MOD) (DIV DIV) -) (^ ^)"
      cflags=cflags.split(" ")
      if(line.count('\"')>0 or line.count('\'')%2==1):
        errmsg="\n> ΜΗ ΕΓΚΥΡΗ χρήση ΕΙΣΑΓΩΓΙΚΩΝ"
        raise Exception
      while("\"" in lineNS):      # ignore "strings"
        pos1=lineNS.find("\"")
        pos2=lineNS[pos1+1:].find("\"")+pos1+1
        if("\'" in lineNS[pos1:pos2]):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ χρήση ΕΙΣΑΓΩΓΙΚΩΝ"
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
      if("@" in lineNS or "#" in lineNS or "$" in lineNS or "%" in lineNS or "?" in lineNS 
        or ";" in lineNS or "\\" in lineNS or "΅" in lineNS or "`" in lineNS or "¨" in lineNS):
        errmsg="\n> ΜΗ ΕΠΙΤΡΕΠΤΟΣ ΧΑΡΑΚΤΗΡΑΣ"
        raise Exception
      #if(":" in lineNS and not vblock and len(line)>9 and "ΣΥΝΑΡΤΗΣΗ "!=line[:10]):
        #errmsg="\n> unexpected ':' εκτός δήλωσης ΜΕΤΑΒΛΗΤΩΝ"
        #raise Exception
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
            errmsg="> το \'"+cname+"\' είναι ΜΗ ΕΓΚΥΡΟ όνομα ΣΤΑΘΕΡΑΣ"
            raise Exception
          cvalue=line[eqpos+1:]
          if(cvalue[-1]==" "):
            cvalue=cvalue[:-1]
          if(cname in cdict[fname].keys()):
            errmsg="> η \'"+cname+"\' έχει δηλωθεί 2 φορές"
            raise Exception
          elif(cname in Reserved):
            errmsg="> το \'"+cname+"\' είναι ΔΕΣΜΕΥΜΕΝΗ ΛΕΞΗ"
            raise Exception
          else:
            cdict[fname][cname]=cvalue
          pcmd=xpr(cname)+"="+cvalue
        else:
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΔΗΛΩΣΗ ΣΤΑΘΕΡΑΣ"
          raise Exception
      elif(vblock and (tryblock or fblock or pblock)
        or segment and interS(["ΑΚΕΡΑΙΕΣ","ΠΡΑΓΜΑΤΙΚΕΣ","ΧΑΡΑΚΤΗΡΕΣ","ΛΟΓΙΚΕΣ"],line)!=[]): #VBLOCK
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
              errmsg="\n> υπάρχει παραπάνω δήλωση ΑΚΕΡΑΙΩΝ"
              raise Exception
            intl=True
          case "ΠΡΑΓΜΑΤΙΚΕΣ":
            vtype="float"
            if(floatl):
              errmsg="\n> υπάρχει παραπάνω δήλωση ΠΡΑΓΜΑΤΙΚΩΝ"
              raise Exception
            floatl=True
          case "ΧΑΡΑΚΤΗΡΕΣ":
            vtype="str"
            if(strl):
              errmsg="\n> υπάρχει παραπάνω δήλωση ΧΑΡΑΚΤΗΡΩΝ"
              raise Exception
            strl=True
          case "ΛΟΓΙΚΕΣ":
            vtype="bool"
            if(booll):
              errmsg="\n> υπάρχει παραπάνω δήλωση ΛΟΓΙΚΩΝ"
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
            vval="myA( ["+vdim+"],pholder("+vtype+") )"
          else:
            vval="pholder("+vtype+")"
            vname=v[:-1] if v[-1]==" " else v[:]
          if(vname in vdict[fname].keys() or vname in cdict[fname].keys()):
            errmsg="\n> η \'"+vname+"\' έχει δηλωθεί 2 φορές"
            raise Exception
          elif(vname in Reserved):
            errmsg="\n> το \'"+vname+"\' είναι ΔΕΣΜΕΥΜΕΝΗ ΛΕΞΗ"
            raise Exception
          elif(not isname(vname)):
            errmsg="\n> το \'"+vname+"\' είναι ΜΗ ΕΓΚΥΡΟ όνομα ΜΕΤΑΒΛΗΤΗΣ"
            raise Exception
          elif(vname in vdict.keys() or vname in cdict.keys()):
            errmsg="\n> \'"+vname+"\' είναι όνομα ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ"
            raise Exception
          elif(vname==PROname):
            errmsg="\n> \'"+vname+"\' είναι το όνομα του ΠΡΟΓΡΑΜΜΑΤΟΣ"
            raise Exception
          else:
            vdict[fname][vname]=vtype
            vdict[fname][vname+".ΤΙΜΗ"]=vtype
          pcmd+="try:#<"+str(nl)+">#\n"+" "*(nsp+2)  #//
          pcmd+=xpr(vname)+"=="+xpr(vname)+"#<"+str(nl)+">#\n"+" "*(nsp+2)
          pcmd+="assign2("+vtype+","+xpr(vname)+vsub+")#<"+str(nl)+">#\n"+" "*(nsp)
          pcmd+="except NameError:\n"+" "*(nsp+2)
          pcmd+=xpr(vname)+"="+vval+"\n"+" "*(nsp)
      elif(":" in lineNS and not vblock and len(line)>9 and "ΣΥΝΑΡΤΗΣΗ "!=line[:10]):
        errmsg="\n> unexpected ':' εκτός δήλωσης ΜΕΤΑΒΛΗΤΩΝ"
        raise Exception

      elif(line.count("<--")==1 and ablock and                                  #ASSIGNMENT
           not( fname==line[:len(fname)] 
           and line[len(fname)] not in letters+list("0123456789_") )):   #return handled elsewhere
        aspos=line.find("<--")
        vname=line[:aspos]
        if(vname[-1]==" "):
          vname=vname[:-1]
        if("[" in vname):
          lbrpos=vname.find("[")
          vname=vname[:lbrpos]
        if(vname in Reserved):
          errmsg="\n> το \'"+vname+"\' είναι ΔΕΣΜΕΥΜΕΝΗ ΛΕΞΗ"
          raise Exception
        if(not segment and vname in cdict[fname].keys()):                                      
          #vnamecl=vname if vname[0]!='_' else vname[1:]
          errmsg="\n> ΔΕΝ ΕΠΙΤΡΕΠΕΤΑΙ ΕΚΧΩΡΗΣΗ τιμής στη ΣΤΑΘΕΡΑ \'"+vname+"\'"#cl
          raise Exception
        if(not isname(vname)):
          errmsg="\n> ΕΚΧΩΡΗΣΗ επιτρέπεται ΜΟΝΟ σε ΜΕΤΑΒΛΗΤΗ"
          raise Exception
        if(segment):                                # αν δεν έχει πάρει τιμή δεν ελέγχεται ο τύπος
          pcmd="try:#<"+str(nl)+">#\n"+" "*(nsp+2)  #//
          pcmd+=xpr(vname)+"=="+xpr(vname)+"\n"+" "*(nsp)
          pcmd+="except NameError:\n"+" "*(nsp+2)
          pcmd+="try:#<"+str(nl)+">#\n"+" "*(nsp+4)
          pcmd+=xpr(vname)+"="+xpr(cmd[aspos+3:])+"#<"+str(nl)+">#\n"+" "*(nsp+2)
          pcmd+="except Exception as e:\n"+" "*(nsp+4)
          pcmd+="raise RuntimeError(str(e)+\"\\n#<"+str(nl)+">#\")\n"+" "*(nsp) #//
          #pcmd+=xpr(vname)+"="+xpr(cmd[aspos+3:])+"\n"+" "*(nsp)

        if(not segment and vname not in vdict[fname].keys()):# and vname!=fname):
          #vnamecl=vname[1:] if (vname[0]=='_' and vname[1] in letters[52:]) else vname
          if(vname in vdict.keys() or vname in cdict.keys()):
            errmsg="\n> \'"+vname+"\' είναι όνομα ΥΠΟΠΡΟΓΡΑΜΜΑΤΟΣ"
            raise Exception
          if(vname==PROname):
            errmsg="\n> \'"+vname+"\' είναι το όνομα του ΠΡΟΓΡΑΜΜΑΤΟΣ"
            raise Exception
          errmsg="\n> ΔΕΝ έχει δηλωθεί η ΜΕΤΑΒΛΗΤΗ \'"+vname+"\'"#cl
          if(fname=="_main_"):
            print("το ΠΡΟΓΡΑΜΜΑ \'"+PROname+"\' έχει ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i]) #ΤΙΜΗ
          else:
            print("το ΥΠΟΠΡΟΓΡΑΜΜΑ \'"+fname+"\' έχει ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i]) #ΤΙΜΗ
          raise Exception
        pcmd+="try:#<"+str(nl)+">#\n"+" "*(nsp+2)  #//
        pcmd+=xpr(list(line[:aspos]+"<--"))+"assign2("+xpr(list(line[:aspos]+",")+cmd[aspos+3:],pblock,vargs)+")#<"+str(nl)+">#\n"+" "*(nsp)
        pcmd+="except Exception as e:\n"+" "*(nsp+2)
        pcmd+="raise RuntimeError(str(e)+\"\\n#<"+str(nl)+">#\")"        #TYPE CHECK

      elif(cmd[:6]==list("ΓΡΑΨΕ ") and ablock):                                  #PRINT
        if(fblock):
          errmsg="\n> η \'ΓΡΑΨΕ\' δεν επιτρέπεται μέσα σε ΣΥΝΑΡΤΗΣΗ"
          raise Exception
        pcmd="_.eprint("+xpr(cmd[6:],pblock,vargs)+")"
      elif(cmd[:8]==list("ΔΙΑΒΑΣΕ ") and ablock):                                #INPUT
        if(fblock):
          errmsg="\n> η \'ΔΙΑΒΑΣΕ\' δεν επιτρέπεται μέσα σε ΣΥΝΑΡΤΗΣΗ"
          raise Exception
        if(False): #and interS("+,-,*,/,%, and , or , not , True , False ".split(","),xpr(line))!=[] or "(" in line):
          errmsg=("\n> δεν επιτρέπεται να δοθεί ΕΚΦΡΑΣΗ ως όρισμα στη ΔΙΑΒΑΣΕ")
          raise Exception
        temp=xpr(list(line[8:]))
        vars=temp.split(",")
        pcmd=",".join([(v) for v in vars])+"=" if not segment else ""
        for v in vars:                        #ΕΛΕΓΧΟΣ ΔΗΛΩΣΗΣ ΜΕΤ/ΤΩΝ ΣΤΗΝ ΕΙΣΟΔΟ
          vname = str(v)                      # έχει προέλθει από xpr
          vnamecl=vname if vname[0]!='_' else vname[1:]
          if(".ΤΙΜΗ[" in vnamecl):
            lbrpos=vnamecl.find(".ΤΙΜΗ[")  #.ΤΙΜΗ[
            vnamecl=vnamecl[:lbrpos-1] if vnamecl[lbrpos-1] == " " else vnamecl[:lbrpos]
          if(not segment and vnamecl not in vdict[fname].keys() and vnamecl!=fname):
            if(interS(list("+-*/^")+[" ΚΑΙ "," Ή "," ΟΧΙ "],vnamecl)!=[]):
              errmsg="\n> δεν επιτρέπεται να εκχωρηθεί τιμή σε ΕΚΦΡΑΣΗ"
              raise Exception
            if("(" not in line):
              errmsg="\n> ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ \'"+vnamecl+"\'"
              if(fname=="_main_"):
                print("το ΠΡΟΓΡΑΜΜΑ",PROname,"έχει","ΜΕΤΑΒΛΗΤΕΣ",[i for i in vdict[fname].keys() if "." not in i])
              else:
                print("το ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"έχει ΜΕΤΑΒΛΗΤΕΣ",[i for i in vdict[fname].keys() if "." not in i])
              raise Exception
          smartV= "" if not smart else comment[comment.find("#")+1:].replace(" ","")#+","
          #pcmd+=("_.Rinput("+(v)+","+str(report)+",\""+(smartV)+"\"),")*(randIN)+"_.TCinput(),"*(1-randIN)
          if(not segment):
            pcmd+=("_.Rinput("+(v)+","+str(report)+",\""+(smartV)+"\"),")*(randIN)+"_.TCinput(),"*(1-randIN)
          else:                                # αν έχει πάρει τιμή ελέγχεται ο τύπος
            pcmd+="try:#<"+str(nl)+">#\n"+" "*(nsp+2)
            pcmd+=(v)+"=="+(v)+"\n"+" "*(nsp+2)
            pcmd+="try:#<"+str(nl)+">#\n"+" "*(nsp+4)
            pcmd+=v+"=assign2("+v+",_.TCinput())#<"+str(nl)+">#\n"+" "*(nsp+2)
            pcmd+="except Exception as e:\n"+" "*(nsp+4)
            pcmd+="raise RuntimeError(str(e)+\"\\n#<"+str(nl)+">#\")\n"+" "*(nsp) #//
            pcmd+="except NameError:\n"+" "*(nsp+2)
            pcmd+=v+"=_.TCinput()#<"+str(nl)+">#\n"+" "*(nsp) #διότι είναι μέσα στη for
        pcmd=pcmd[:-1] if pcmd[-1]=="," else pcmd #delete comma..
      elif(cmd[:3]==list("ΑΝ ") and ablock):                    #IF
        ifN+=1
        ifline.append(str(nl))
        ALLline.append(str(nl))
        ALLblock.append("if")
        block=True
        pcmd="if( ("
        if(cmd[-4:]!=list("ΤΟΤΕ") or cmd[-5] in letters+["_"]):
          errmsg="ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΤΟΤΕ"
          raise Exception
        pcmd+=xpr(cmd[3:-4],pblock,vargs)+") == B1):"  #against tuple
      elif(cmd[:10]==list("ΑΛΛΙΩΣ_ΑΝ ") and ablock):                  #ELIF
        if(ifN<0):
          errmsg=("\n> unexpected \'ΑΛΛΙΩΣ_ΑΝ\' εκτός δομής επιλογής")
          raise Exception
        block=True
        nsp-=2
        pcmd="elif( ("
        if(cmd[-4:]!=list("ΤΟΤΕ") or cmd[-5] in letters+["_"]):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΤΟΤΕ"
          raise Exception
        pcmd+=xpr(cmd[10:-4],pblock,vargs)+") == B1):"
      elif(line in rword("ΑΛΛΙΩΣ") and ablock):          #ELSE
        if(ifN<0):
          errmsg=("\n> unexpected \'ΑΛΛΙΩΣ\' εκτός δομής επιλογής")
          raise Exception          
        block=True
        nsp-=2
        pcmd="else:"
      elif(line in rword("ΤΕΛΟΣ_ΑΝ") and ablock):    #ENDIF
        ifN-=1
        if(ifN<0):
          errmsg=("\n> unexpected \'ΤΕΛΟΣ_ΑΝ\' εκτός δομής επιλογής")
          raise Exception
        if(ALLblock[-1]!="if"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
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
        pcmd="sw"+str(swN)+"="+xpr(cmd[8:],pblock,vargs)+"#<"+str(nl)+">#\n"+nsp*" " #//
        pcmd+="if(False):\n"+nsp*" "
        pcmd+="  0"
      elif(cmd[:10]==list("ΠΕΡΙΠΤΩΣΗ ") and ("ΑΛΛΙΩΣ" not in line) and ablock):   #CASE
        if(swN<0):
          errmsg="\n> unexpected \'ΠΕΡΙΠΤΩΣΗ\' εκτός δομής επιλογής"
          raise Exception
        block=True
        nsp-=2
        pcmd="elif( ( (sw"+str(swN) #ΠΕΡΙΠΤΩΣΗ ~ elif
        if("<" not in line and "=" not in line and ">" not in line and ",..," not in line):
          pcmd+=" in ("+xpr(cmd[10:],swflag=True)+",)) == B1):"
        elif(",..," in line):
          casepos=line.find(",..,")
          swRa=xpr(cmd[10:casepos],swflag=True)
          swRb=xpr(cmd[casepos+4:],swflag=True)
          pcmd+=" in list(range("+swRa+","+swRb+"+("+swRa+"<="+swRb+")))+list(range("+swRb+","+swRa+"+("+swRa+">"+swRb+")))) == B1) ):"
        else:
          pcmd+=" "+xpr(cmd[10:],swflag=True)+") == B1):"
      elif(line in rword("ΠΕΡΙΠΤΩΣΗ ΑΛΛΙΩΣ") and ablock):           #CASE DEFAULT
        if(swN<0):
          errmsg="\n> unexpected \'ΠΕΡΙΠΤΩΣΗ ΑΛΛΙΩΣ\' εκτός δομής επιλογής"
          raise Exception
        block=True
        nsp-=2
        pcmd="else:"
      elif(line in rword("ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ") and ablock):    #ENDSWITCH
        swN-=1
        if(swN<0):
          errmsg=("\n> unexpected \'ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ\' εκτός δομής επιλογής")
          raise Exception
        if(ALLblock[-1]!="sw"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
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
        pcmd+="while( ("
        if(cmd[-9:]!=list("ΕΠΑΝΑΛΑΒΕ") or cmd[-10:] in letters+["_"]):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ: λείπει η λέξη ΕΠΑΝΑΛΑΒΕ"
          raise Exception
        pcmd+=xpr(cmd[4:-10],pblock,vargs)+") == B1):"
      elif(cmd[:4]==list("ΓΙΑ ") and ablock):           # FOR ΜΕΣΩ WHILE
        whN+=1
        whline.append(str(nl))
        ALLline.append(str(nl))
        ALLblock.append("wh")
        if(" ΑΠΟ " not in line or " ΜΕΧΡΙ " not in line 
           or " ΓΙΑ " in line[4:] or line.count(" ΑΠΟ ")>1 or line.count(" ΜΕΧΡΙ ")>1 or line.count("ΜΕ_ΒΗΜΑ")>1):
          errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ της εντολής ΓΙΑ"
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
          if(" ΜΕ_ΒΗΜΑ " not in line):
            errmsg="\n> ΜΗ ΕΓΚΥΡΗ ΣΥΝΤΑΞΗ της εντολής ΓΙΑ"
            raise Exception
          pcmd="correction"+str(whN)+"=1-2*("+xpr(cmd[pos4:],pblock,vargs)+"<0)#<"+str(nl)+">#\n"+" "*nsp #//
          step=xpr(cmd[pos4:],pblock,vargs)
        else:
          pcmd="correction"+str(whN)+"=1#<"+str(nl)+">#\n"+" "*nsp
          step="1"
        whv.append(xpr(cmd[4:pos1-1],pblock,vargs))
        whstep.append(step)
        vname=whv[-1]
        vnamecl=vname if vname[0]!='_' else vname[1:]
        if(not segment and vnamecl not in vdict[fname].keys() and vname!=fname):
          #vname=vname if vname[0]!='_' else vname[1:]
          errmsg="\n> ΔΕΝ ΕΧΕΙ ΔΗΛΩΘΕΙ Η ΜΕΤΑΒΛΗΤΗ "+vnamecl
          if(fname=="_main_"):
            print("ΤΟ ΠΡΟΓΡΑΜΜΑ ΕΧΕΙ","ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i])
          else:
            print("ΥΠΟΠΡΟΓΡΑΜΜΑ",fname,"ΕΧΕΙ ΜΕΤΑΒΛΗΤΕΣ:",[i for i in vdict[fname].keys() if "." not in i])
          raise Exception
        pcmd+=whv[-1]+"="+xpr(cmd[pos1+4:pos2],pblock,vargs)+"\n"+" "*nsp
        pcmd+="while( ("  #for "
        if("ΜΕ_ΒΗΜΑ" in line):
          pcmd+=xpr(cmd[4:pos1],pblock,vargs)+"*correction"+str(whN)+" <= "+xpr(cmd[pos2+6:pos3],pblock,vargs)+"*correction"+str(whN)+") == B1):"
        else:
          pcmd+=xpr(cmd[4:pos1],pblock,vargs)+"<= "+xpr(cmd[pos2+6:],pblock,vargs)+") == B1):\n"+" "*nsp
      elif(line in rword("ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ") and ablock):                                        #ENDFOR/WHILE
        whN-=1
        if(whN<0):
          errmsg=("\n> unexpected \'ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ\' εκτός δομής επανάληψης")
          raise Exception
        if(ALLblock[-1]!="wh"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
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
          errmsg=("\n> unexpected \'ΜΕΧΡΙΣ_ΟΤΟΥ\' εκτός δομής επανάληψης")
          raise Exception
        if(ALLblock[-1]!="dwh"):
          errmsg="ΑΝΟΙΧΤΗ ΔΟΜΗ "+blockdict2[ALLblock[-1]]+" in line "+ALLline[-1]
          errmsg+=("\n> expected \'"+blockdict[ALLblock.pop(-1)]+"\'")
          raise Exception
        ALLblock.pop(-1)
        dwhline.pop(-1)
        ALLline.pop(-1)
        deblock=True
        pcmd="if( ("+xpr(list("".join(cmd[12:])),pblock,vargs)
        pcmd+=") == B1):#<"+str(nl)+">#\n"+" "*(nsp+2)+"break"  #//
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
        tryblock=True
        exe=True
        pcmd="def main():\n  N1,N0,B1,A1=NUM(1),NUM(0),myB(),myA([1],int)\n"
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
        pcmd+=" "*(nsp+2)+"N1,B1,A1=NUM(),myB(),myA([1],int)\n"
      elif(fname==line[:len(fname)] and ("<--"==line[len(fname):len(fname)+3] 
        or " <--"==line[len(fname):len(fname)+4])):                                       #RETURN
        if(not fblock):
          errmsg="\n> αυτή η σύνταξη επιτρέπεται μόνο μέσα σε ΣΥΝΑΡΤΗΣΕΙΣ"
          raise Exception
        pcmd+="__"+xpr(fname)+xpr(list("<--"))+"assign2("+ftypos+","+xpr(cmd[len(fname)+3:])+")"
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
        pcmd+=" "*(nsp+2)+"N1,B1,A1=NUM(),myB(),myA([1],int)\n"
      elif(line in rword("ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ")):                    #ENDPROCEDURE
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
        nP=0              #number of open left(
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
          errmsg="ΜΗ έγκυρη δήλωση ΜΕΤΑΒΛΗΤΗΣ εκτός δηλωτικού τμήματος ΜΕΤΑΒΛΗΤΩΝ"
        elif(not cblock and ("=" in line)):
          errmsg="ΜΗ έγκυρη δήλωση ΣΤΑΘΕΡΑΣ εκτός δηλωτικού τμήματος ΣΤΑΘΕΡΩΝ"
        raise Exception

      if(pcmd not in ["","\n"]):              # save line ----------------------
        if(pcmd[-1]=="\n"):
          pcmd=pcmd[:-1]
        fout.write(nsp*" "+pcmd+comment+"#<"+str(nl)+">#\n")  #//
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
    # endfor line in file  -----------------------------------------------------
    if(segment):
      tryblock=0
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
    print("-"*75+'\n'+"ΣΥΝΤΑΚΤΙΚΟ ΣΦΑΛΜΑ: "+errmsg.replace("Exception()","\n> μη έγκυρη σύνταξη")+"\n----> "+str(nl)+". "+line)   #str(nl+1)
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
