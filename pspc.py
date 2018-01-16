import time
def main():
    dies_y_seis_bit()

def ocho_bit():
    x = 0x01
    all_range = []
    qual = 0
    for i in range(256):
        if x & 0x80:
            uno = 1
        else:
            uno = 0
        if x & 0x20:
            tres = 1
        else:
            tres = 0
        if x & 0x10:
            quatro = 1
        else:
            quatro = 0
        if x & 0x08:
            cinko = 1
        else:
            cinko = 0

        start = uno ^ tres ^ quatro ^ cinko
        print(uno,tres,quatro,cinko,start)
        x = x<<1
        x = x&0xff
        if start:
            x = x | 0x01
        else:
            x = x & 0xfe
        if x in all_range:
            print('retype')
        else:
            all_range.append(x)
            qual+=1
        print(bin(x))
    print('number',qual)


def dies_y_seis_bit():
    '''algortim for 16 bit 65535 randomize testing use line reg shifting'''
    x = 0x0001
    all_range = []
    qual = 0
    for i in range(65536):
        if x & 0x8000:
            uno = 1
        else:
            uno = 0
        if x & 0x2000:
            tres = 1
        else:
            tres = 0
        if x & 0x1000:
            quatro = 1
        else:
            quatro = 0
        if x & 0x0400:
            seis = 1
        else:
            seis = 0
        start = uno ^ tres ^ quatro ^ seis
        print(uno,tres,quatro,seis,start)
        x = x<<1
        x = x&0xffff
        if start:
            x = x | 0x0001
        else:
            x = x & 0xfffe
        if x in all_range:
            print('retype')
        else:
            all_range.append(x)
            qual+=1
        print(bin(x))
    print('number',qual)
    
if __name__ == "__main__":
    main()