swara = {1:"S",2:"R",3:"G",4:"M",5:"P",6:"D",7:"N",
         8:"Ṡ",9:"Ṙ",10:"Ġ",11:"Ṁ",12:"Ṗ",13:"Ḋ",14:"Ṇ",
         15:"Ṣ",16:"Ṙ",17:"G̣",18:"Ṃ",19:"P̣",20:"Ḍ",21:"Ṇ"}

def numbering(ls):
  ls = ls.split()
  ct = 0
  doub_ct = 0
  twoD = []
  temp = []
  for i in  ls:

    if i == "│" or i=="|":
        print("|",end = " ")

    elif i == "‖" or i=="||":
      twoD.append(temp)
      temp = []
      print("‖",end = " ")
      doub_ct +=1
      if ct<8:
        ct = 0
        if doub_ct%2 == 0:
          print()
      elif ct==8:
        ct=0
        print()

    elif i in swara.values():
      a = list(swara.keys())[list(swara.values()).index(i)]
      print(a,end = " ")
      ct +=1
      temp.append(a)

    else:
      print(i,end = " ")
      ct+=1
  return twoD

def triplets(malahari):
  skkp = []
  for array in malahari:
    triplets = list()
    for arr in array:
      for i in range(0,len(arr)-2):
        tup = (arr[i],arr[i+1],arr[i+2])
        triplets.append(tup)
    #print(triplets)
    skkp.append(triplets)
  return skkp

def as_swara(kudutha_set):
  final_common_swara = []
  for trip in kudutha_set:
    strip = []
    for num in trip:
      strip.append(swara[num])
    final_common_swara.append(strip)
  return final_common_swara
    
      


def common_swara(skkp):
  first = set(skkp[0])
  temp = set(first)
  for i in skkp[1:]:
    temp = temp.intersection(i)
  return temp

  
