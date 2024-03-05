notes = [
 'S1','S2',
 'R1','R2','R3','R4',
 'G1','G2','G3','G4',
 'M1','M2','M3','M4','P1','P2',
 'D1','D2','D3','D4',
 'N1','N2','N3','N4'
 ]

inp = input().split()
print(f"Input: {inp}")
ix = [notes.index(i) for i in inp]

while notes[0]!= inp[0]:
    notes.insert(0,notes.pop())
print(notes)
res = []
for i in ix:
    res.append(notes[i])
print(res)