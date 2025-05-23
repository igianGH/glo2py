# ΒΙΒΛΙΟΘΗΚΕΣ #
import random as r
import math as m
import numpy as np
import __ as _
import sys
import traceback
from copy import deepcopy as cdc


def main():
  Ne,N1,N0,B1,A1=NUM(2),NUM(1),NUM(0),myB(),myA([1],int)
  try:#<2>#
    α==α
  except NameError:
    try:#<2>#
      α = 27 #<2>#
    except Exception as e:
      raise RuntimeError(str(e)+"\n#<2>#")
  try:#<2>#
    α = assign2(α,( 27 ))#<2>#
  except Exception as e:
    raise RuntimeError(str(e)+"\n#<2>#")#<2>#
  try:#<3>#
    β==β
  except NameError:
    try:#<3>#
      β = -N0-27 #<3>#
    except Exception as e:
      raise RuntimeError(str(e)+"\n#<3>#")
  try:#<3>#
    β = assign2(β,( -N0-27 ))#<3>#
  except Exception as e:
    raise RuntimeError(str(e)+"\n#<3>#")#<3>#
  try:#<4>#
    γ==γ
  except NameError:
    try:#<4>#
      γ = -N0-1 #<4>#
    except Exception as e:
      raise RuntimeError(str(e)+"\n#<4>#")
  try:#<4>#
    γ = assign2(γ,( -N0-1 ))#<4>#
  except Exception as e:
    raise RuntimeError(str(e)+"\n#<4>#")#<4>#
  try:#<5>#
    δ==δ
  except NameError:
    try:#<5>#
      δ = (β^N1^2 )-N0- 4*N1*α*N1*γ #<5>#
    except Exception as e:
      raise RuntimeError(str(e)+"\n#<5>#")
  try:#<5>#
    δ = assign2(δ,( (β^N1^2 )-N0- 4*N1*α*N1*γ ))#<5>#
  except Exception as e:
    raise RuntimeError(str(e)+"\n#<5>#")#<5>#
  try:#<7>#
    ε==ε
  except NameError:
    try:#<7>#
      ε = (α^N1^2)+N0+β #<7>#
    except Exception as e:
      raise RuntimeError(str(e)+"\n#<7>#")
  try:#<7>#
    ε = assign2(ε,( (α^N1^2)+N0+β ))#<7>#
  except Exception as e:
    raise RuntimeError(str(e)+"\n#<7>#")#<7>#
  _.eprint(ε)#<9>#

  try:
    delete()
  except:
    pass

def delete():
  global α,β,γ,δ,ε
  del α,β,γ,δ,ε
################################################################################

class NUM:
  def __init__(self,value):
    self.value=value
  def __rmatmul__(self,x): #x..NUM
    if(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    else:
      return NUM(x)
  def __lt__(self,x): #NUM<x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("δεν ορίζεται το '<' στις ΛΟΓΙΚΕΣ τιμές")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(type(x)==type(self.value) or {type(x),type(self.value)}=={int,float} ):
      return self.value<x
    elif(hasattr(x,'value')):
      return NUM(self.value<x.value)
    else:
      raise SyntaxError("πράξη μεταξύ ΑΣΥΜΒΑΤΩΝ αντικειμένων")
  def __gt__(self,x): #NUM>x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("δεν ορίζεται το '>' στις ΛΟΓΙΚΕΣ τιμές")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(type(x)==type(self.value) or {type(x),type(self.value)}=={int,float} ):
      return self.value>x
    elif(hasattr(x,'value')):
      return NUM(self.value>x.value)
    else:
      raise SyntaxError("πράξη μεταξύ ΑΣΥΜΒΑΤΩΝ αντικειμένων")
  def __le__(self,x): #NUM<=x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("δεν ορίζεται το '<=' στις ΛΟΓΙΚΕΣ τιμές")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif( type(x)==type(self.value) or {type(x),type(self.value)}=={int,float} ):
      return self.value<=x
    elif(hasattr(x,'value')):
      return NUM(self.value<=x.value)
    else:
      raise SyntaxError("πράξη μεταξύ ΑΣΥΜΒΑΤΩΝ αντικειμένων: "+str(self.value)+", "+str(x))
  def __ge__(self,x): #NUM>=x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("δεν ορίζεται το '>=' στις ΛΟΓΙΚΕΣ τιμές")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(type(x)==type(self.value) or {type(x),type(self.value)}=={int,float} ):
      return self.value>=x
    elif(hasattr(x,'value')):
      return NUM(self.value>=x.value)
    else:
      raise SyntaxError("πράξη μεταξύ ΑΣΥΜΒΑΤΩΝ αντικειμένων")
  def __eq__(self,x): #NUM==x
    if(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(type(x)==type(self.value) or {type(x),type(self.value)}=={int,float} ):
      return self.value==x
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")#return NUM(self.value==x.value)
    else:
      raise SyntaxError("πράξη μεταξύ ΑΣΥΜΒΑΤΩΝ αντικειμένων")
  def __mul__(self,x):  #NUM*x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής * στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")
    return self.value*x
  def __rmul__(self,x): #x*NUM
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής * στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return NUM(x)
  def __add__(self,x):  #NUM0+x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής + στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")
    return self.value+x
  def __radd__(self,x): #x+NUM0 <-----------------------------------------------
    #if(type(x)==bool or hasattr(x,'Bvalue')):
      #raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    #elif(type(x)==str):
      #raise SyntaxError("δεν ορίζεται ο τελεστής + στους ΧΑΡΑΚΤΗΡΕΣ")
    if(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return NUM(x)
  def __sub__(self,x):  #NUM0-x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής - στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")
    return self+(-x)
  def __neg__(self):  #-NUM0
    return 0-self
  def __rsub__(self,x): #x-NUM0
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής - στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")
    return NUM(x)
  def __truediv__(self,x):  #NUM1/x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής / στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")
    return self.value/x
  def __rtruediv__(self,x): #x/NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής / στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")
    return NUM(x)
  def __floordiv__(self,x):  #NUM1//x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str or type(x)==float):
      raise SyntaxError("δεν ορίζεται ο τελεστής DIV στους "+("ΧΑΡΑΚΤΗΡΕΣ" if type(x)==str else "ΠΡΑΓΜΑΤΙΚΟΥΣ"))
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(hasattr(x,'value')):
      raise SyntaxError("unexpected NwN")
    return self.value//x
  def __rfloordiv__(self,x): #x//NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str or type(x)==float):
      raise SyntaxError("δεν ορίζεται ο τελεστής DIV στους "+("ΧΑΡΑΚΤΗΡΕΣ" if type(x)==str else "ΠΡΑΓΜΑΤΙΚΟΥΣ"))
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return NUM(x)
  def __mod__(self,x):  #NUM1%x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str or type(x)==float):
      raise SyntaxError("δεν ορίζεται ο τελεστής MOD στους "+("ΧΑΡΑΚΤΗΡΕΣ" if type(x)==str else "ΠΡΑΓΜΑΤΙΚΟΥΣ"))
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return self.value%x
  def __rmod__(self,x): #x%NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str or type(x)==float):
      raise SyntaxError("δεν ορίζεται ο τελεστής MOD στους "+("ΧΑΡΑΚΤΗΡΕΣ" if type(x)==str else "ΠΡΑΓΜΑΤΙΚΟΥΣ"))
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return NUM(x)
  def __pow__(self,x):  #NUM1**x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής ^ στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return NUM(x)
  def __rpow__(self,x): #x**NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής ^ στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return x**self.value
  def __xor__(self,x):  #NUM1**x
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής ^ στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return self.value**x
  def __rxor__(self,x): #x**NUM1
    if(type(x)==bool or hasattr(x,'Bvalue')):
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
    elif(type(x)==str):
      raise SyntaxError("δεν ορίζεται ο τελεστής ^ στους ΧΑΡΑΚΤΗΡΕΣ")
    elif(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    return NUM(x)
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
        raise RuntimeError("> κάποια μεταβλητή δεν έχει λάβει τιμή")
      print("["+str(self.ΤΙΜΗ[0]),end=", ")
      for i in self.ΤΙΜΗ[1:-1]:
        if( hasattr(i,'typos') ):
          print("")
          raise RuntimeError("> κάποια μεταβλητή δεν έχει λάβει τιμή")
        print(i,end=", ")
      if( hasattr(self.ΤΙΜΗ[-1],'typos') ):
        print("")
        raise RuntimeError("> κάποια μεταβλητή δεν έχει λάβει τιμή")
      print(str(self.ΤΙΜΗ[-1])+"]")
      return "-"*75+"\nWarning: το ~ δεν επιτρέπεται στη ΓΛΩΣΣΑ\n"
    n=0
    for l in self.ΤΙΜΗ:
      n+=1
      print(str(n)+".",l)
    return "-"*75+"\nWarning: το ~ δεν επιτρέπεται στη ΓΛΩΣΣΑ\n"
class myB:
  def __init__(self,value=True):
    self.Bvalue=value
  def __matmul__(self,x): #B1@x
    if(hasattr(x,'ΤΙΜΗ')):
      raise SyntaxError("δεν ορίζεται πράξη απευθείας σε ΠΙΝΑΚΕΣ")
    elif(type(x)==bool):
      return x #myB(x)
    else:
      raise SyntaxError("μη έγκυρη ΛΟΓΙΚΗ έκφραση")
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
def assign2(y,x,segment=False,nl=1,decl=False):
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
    return x if not decl else True
  #elif(tt[1]=="ΠΡΑΓΜΑΤΙΚΗ" and tt[2]=="ΑΚΕΡΑΙΑ"):
    #return float(x) if not decl else True
  raise RuntimeError("> Δεν επιτρέπεται εκχώρηση τιμής τύπου "+tt[2]+" σε μεταβλητή τύπου "+tt[1])
