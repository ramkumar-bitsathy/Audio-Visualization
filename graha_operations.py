def shift(lst,n):
  for i in range(n):
    lst.insert(0,lst.pop())

raga_dict = {'Invalid':'Invalid','SR1G1M1PD1N1': 'Kanakangi', 'SR1G1M1PD1N2': 'Ratnangi', 'SR1G1M1PD1N3': 'Ganamurti', 'SR1G1M1PD2N2': 'Vanaspati', 'SR1G1M1PD2N3': 'Manavati', 'SR1G1M1PD3N3': 'Tanarapi', 'SR1G2M1PD1N1': 'Senavati', 'SR1G2M1PD1N2': 'Hanumatodi', 'SR1G2M1PD1N3': 'Dhenukā', 'SR1G2M1PD2N2': 'Natakapriya', 'SR1G2M1PD2N3': 'Kokilapriya', 'SR1G2M1PD3N3': 'Rupavati', 'SR1G3M1PD1N1': 'Gayakapriya', 'SR1G3M1PD1N2': 'Vakuḷabharaṇam', 'SR1G3M1PD1N3': 'Mayamalavagowla', 'SR1G3M1PD2N2': 'Chakravakam', 'SR1G3M1PD2N3': 'Suryakantam', 'SR1G3M1PD3N3': 'Hatakambari', 'SR2G2M1PD1N1': 'Jhankaradhvani', 'SR2G2M1PD1N2': 'Naṭabhairavi', 'SR2G2M1PD1N3': 'Karavaṇi', 'SR2G2M1PD2N2': 'Kharaharapriya', 'SR2G2M1PD2N3': 'Gourimanohari', 'SR2G2M1PD3N3': 'Varuṇapriya', 'SR2G3M1PD1N1': 'Mararanjani', 'SR2G3M1PD1N2': 'Charukesi', 'SR2G3M1PD1N3': 'Sarasangi', 'SR2G3M1PD2N2': 'Harikambhoji', 'SR2G3M1PD2N3': 'Dhirasankarabharaṇam', 'SR2G3M1PD3N3': 'Naganandini', 'SR3G3M1PD1N1': 'Yagapriya', 'SR3G3M1PD1N2': 'Ragavardhini', 'SR3G3M1PD1N3': 'Gangeyabhusani', 'SR3G3M1PD2N2': 'Vagadhisvari', 'SR3G3M1PD2N3': 'Sulini', 'SR3G3M1PD3N3': 'Chalanata', 'SR1G1M2PD1N1': 'Salagam', 'SR1G1M2PD1N2': 'Jalarnavam', 'SR1G1M2PD1N3': 'Jhalavaraḷi', 'SR1G1M2PD2N2': 'Navanitam', 'SR1G1M2PD2N3': 'Pavani', 'SR1G1M2PD3N3': 'Raghupriya', 'SR1G2M2PD1N1': 'Gavambhodi', 'SR1G2M2PD1N2': 'Bhavapriya', 'SR1G2M2PD1N3': 'Subhapantuvaraḷi', 'SR1G2M2PD2N2': 'Sadvidamargini', 'SR1G2M2PD2N3': 'Suvarnangi', 'SR1G2M2PD3N3': 'Divyamaṇi', 'SR1G3M2PD1N1': 'Dhavalambari', 'SR1G3M2PD1N2': 'Namanarayaṇi', 'SR1G3M2PD1N3': 'Kamavardhini', 'SR1G3M2PD2N2': 'Ramapriya', 'SR1G3M2PD2N3': 'Gamanashrama', 'SR1G3M2PD3N3': 'Visvambari', 'SR2G2M2PD1N1': 'Samalangi', 'SR2G2M2PD1N2': 'Sanmukhapriya', 'SR2G2M2PD1N3': 'Simhendramadhyamam', 'SR2G2M2PD2N2': 'Hemavati', 'SR2G2M2PD2N3': 'Dharmavati', 'SR2G2M2PD3N3': 'Nitimati', 'SR2G3M2PD1N1': 'Kantamaṇi', 'SR2G3M2PD1N2': 'Risabhapriya', 'SR2G3M2PD1N3': 'Latangi', 'SR2G3M2PD2N2': 'Vachaspati', 'SR2G3M2PD2N3': 'Mechakalyani', 'SR2G3M2PD3N3': 'Chitrambari', 'SR3G3M2PD1N1': 'Sucharitra', 'SR3G3M2PD1N2': 'Jyoti svarupini', 'SR3G3M2PD1N3': 'Dhathuvardhani', 'SR3G3M2PD2N2': 'Nasikabhushani', 'SR3G3M2PD2N3': 'Kosalam', 'SR3G3M2PD3N3': 'Rasikapriya'}

def find_raga(lst):
  lst_str = ""
  for i in lst:
    lst_str+=i
  return raga_dict[lst_str]
  

def three_numbered(lst):


  for i in range(len(lst)):
    if i == 0 and lst[i]=='S':
      continue

    if i == 1 and lst[i] == 'G1':
      lst[i] = 'R2'
    elif i == 1 and lst[i] == 'G2':
      lst[i] = 'R3'

    if i == 2 and lst[i] =='R2':
      lst[i] = 'G1'
    elif i == 2 and lst[i] == 'G1':
      lst[i] = 'G2'
    elif i == 2 and lst[i] == 'G2':
      lst[i] = 'G3'

    if i == 3 and (lst[i] == 'M1' or lst[i] == 'M2'):
      continue
    if i == 4 and lst[i] == 'P':
      continue

    if i == 5 and lst[i] == 'N1':
      lst[i] = 'D2'
    elif i == 5 and lst[i] == 'N2':
      lst[i] = 'D3'

    if i == 6 and lst[i] =='D2':
      lst[i] = 'N1'
    elif i == 6 and lst[i] == 'N1':
      lst[i] = 'N2'
    elif i == 6 and lst[i] == 'N2':
      lst[i] = 'N3'

  if 'M1' in lst and 'M2' in lst:
    return [lst,'Invalid']
  if 'M1' not in lst and 'M2' not in lst:
    return [lst,'Invalid']
  if 'R1' not in lst and 'R2' not in lst and 'R3' not in lst:
    return [lst,'Invalid']
  if 'G1' not in lst and 'G2' not in lst and 'G3' not in lst:
    return [lst,'Invalid']
  if 'D1' not in lst and 'D2' not in lst and 'D3' not in lst:
    return [lst,'Invalid']
  if 'N1' not in lst and 'N2' not in lst and 'N3' not in lst:
    return [lst,'Invalid']
  if 'P' not in lst:
    return [lst,'Invalid']
  if 'S' not in lst:
    return [lst,'Invalid']
  
  return lst


    
