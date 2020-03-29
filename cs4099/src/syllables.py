def syllableSplitter(word):
    syl = lambda w:len(''.join(c if c in"[aeiouy]"for c in(w[:-1]if 'e'==w[-1]else e)).split())

    correct = total = 0
    
    for i in range(1, 7):
        correct = sum(syl(word) == i)
        total = 1