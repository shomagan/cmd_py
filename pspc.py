import time
def main():
    x = 0x01
    all_range = []
    qual = 0
    for i in range(256):
        if x & 0x80:
            uno = 1
        else:
            uno = 0
        if x & 0x40:
            dos = 1
        else:
            dos = 0
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
        print(uno,dos,tres,quatro,cinko,start)
        time.sleep(0.01)
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
if __name__ == "__main__":
    main()