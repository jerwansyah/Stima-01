#!/usr/bin/env python3
# cryptarithmetic.py
# 13519116 Jeane Mikha Erwansyah

from datetime import datetime

l1 = list()             # list operand dan hasil (huruf)
l2 = list()             # list operand dan hasil (angka)
allcrypt = list()       # list of list soal
solution = dict()       # dictionary dengan key huruf dan value angka
key = list()            # list key solution (huruf)
firstletters = list()   # list huruf-huruf pertama

def replacechar(string,setofchar):
    # Fungsi mengembalikan string dengan setofchar yang sudah dihapus.
    string.upper()
    for char in setofchar:
        string = string.replace(char,'')
    return string

def parsefile():
    # Prosedur membaca file test.txt.
    # Hasil disimpan di list global allcrypt.
    # contoh hasil: [['NUMBER', 'NUMBER', 'PUZZLE'], ... ]
    global allcrypt
    ltemp = list()
    ltemp2 = list()
    f = open('../test/test.txt', 'r')
    for line in f:
        if line != '\n':
            temp = (replacechar(line.rstrip(),['+',' '])).upper()
            allcrypt.append(temp)
    f.close()
    
    i = 0
    # Membuat list soal cryptarithmetic
    # yang berupa list operand dan hasil.
    # Membuang char '-' yang berulang
    while i < len(allcrypt):
        if allcrypt[i].find('-') == -1:
            ltemp.append(allcrypt[i])
        else:
            ltemp.append(allcrypt[i+1])
            ltemp2.append(list(ltemp))
            ltemp.clear()
            i += 1
        i += 1

    allcrypt.clear()
    allcrypt = ltemp2

def checkuniqueletters():
    # Fungsi mengecek jumlah huruf unik.
    # Fungsi menghasilkan nilai boolean
    # True apabila jumlah huruf unik kurang dari 10
    # dan False apabila lebih dari 10.
    global solution, key
    solution.clear()
    key.clear()
    for word in reversed(l1):
        for letter in range(len(word)):
            solution[word[letter]] = 9
            if len(solution) > 10:
                return False
    key = list(solution)
    return True

def permutations(numlist, l1, remainder):
    # Generator rekursif menghasilkan permutasi
    if (remainder == 0):
        yield tuple(l1)

    for i in range(10):
        l2 = l1 + numlist[i]
        if len(l2) == len(set(l2)):
            # Benar jika semua huruf/angka unik
            yield from permutations(numlist, l2, remainder - 1)

def listoffirstletters():
    # Prosedur membuat list huruf-huruf pertama.
    for keyindex in range(len(solution)):
        for element in range(len(l1)):
            if key[keyindex] == l1[element][0] and key[keyindex] not in firstletters:
                firstletters.append(key[keyindex]) # key[keyindex] = key yang berupa huruf

def possible(sol):
    # Fungsi mengecek kemungkinan solusi permutasi.
    # Fungsi menghasilkan nilai boolean
    # True bila solusi permutasi mungkin
    # False jika tidak.
    for keyindex in range(len(solution)):
        if key[keyindex] in firstletters and sol[keyindex] == '0':
            return False
    return True

def substitute(l1):
    # Fungsi menghasilkan list string bilangan yang telah
    # diganti dari huruf.
    lsub = list()
    for element in l1:
        for word, letter in solution.items():
            element = element.replace(word, str(letter))
        lsub.append(element)
    return lsub

def solve():
    # Menyelesaikan cryptarithmetic.
    # Jika tidak berhasil nilai -1 dihasilkan
    global solution, key, cases, firstletters, start, l2
    cases = 0
    firstletters.clear()
    start = datetime.now()
    listoffirstletters()            # membuat list huruf-huruf pertama
    for sol in permutations(list('1023456789'),"",len(solution)):
        lefthand = 0
        righthand = 0
        if possible(sol):
            index = 0
            for i in sol:                       # mapping solusi ke dictionary
                solution[key[index]] = i
                index += 1
            l2 = substitute(l1)
            righthand = int(l2[len(l2)-1])
            for operand in range(len(l2)-1):    # menghitung operand
                lefthand += int(l2[operand])
            cases += 1
            if lefthand == righthand:
                return

def transform(l1,l2):
    # Fungsi menghasilkan list list pasangan operand dan hasil
    l3 = list()
    l4 = list()
    for i in range(len(l1)):
        l3.append(l1[i])
        l3.append(l2[i])
        l4.append(list(l3[i*2:(i*2+2)]))
    return l4

def printsolution():
    # Prosedur mencetak solusi
    data = transform(l1,l2)
    width =  max(len(word) for row in data for word in row) + 6
    i = 0
    for row in data:
        if i == len(data)-1:
            print('    ' + (width-4)* '-' + ' +  ' + (width-4)* '-' + ' +')
            print(''.join(word.rjust(width) for word in row))
        else:
            print(''.join(word.rjust(width) for word in row))
        i += 1

    end = datetime.now()
    print('Jumlah uji kasus: ' + str(cases) + ' kasus')
    print(f'Waktu eksekusi  : {end - start}')

if __name__ == '__main__':
    parsefile()
    for q in range(len(allcrypt)):
        l1.clear()
        l1 = allcrypt[q]
        print('\n=>> Soal nomor ' + str(q+1))
        if checkuniqueletters():
            solve()
            lefthand = 0
            for i in range(len(l2)-1):
                lefthand += int(l2[i])
            if lefthand == int(l2[len(l2)-1]):
                printsolution()
            else:
                print('Tidak ada solusi.')
        else:
            print('Tidak ada solusi karena huruf unik lebih dari 10.')
