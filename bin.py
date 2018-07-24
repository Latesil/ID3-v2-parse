#!/bin/python3

import sys

def sys_exit(msg):
    print(msg)
    sys.exit()

if len(sys.argv) > 2:
    sys_exit("Too many arguments")

if len(sys.argv) == 1:
    sys_exit("Need at least one file to open")

tags = {b'TYER': "Year", b'TRCK': 'Track number', 
        b'AENC': 'Info', b'ASPI': 'Info', b'APIC': 'Info', 
        b'COMM': 'Comment', b'COMR': 'Info', b'ENCR': 'Info',
        b'EQUA': 'Info', b'EQU2': 'Info', b'ETCO': 'Info', 
        b'GEOB': 'Info', b'GRID': 'Info', b'IPLS': 'Info', 
        b'TIPL': 'Info', b'LINK': 'Info', b'MCDI': 'Info', 
        b'MLLT': 'Info', b'OWNE': 'Info', b'PRIV': 'Info', 
        b'PCNT': 'Info', b'POPM': 'Info', b'POSS': 'Info', 
        b'RBUF': 'Info', b'RVAD': 'Info', b'RVA2': 'Info', 
        b'RVRB': 'Info', b'SEEK': 'Info', b'SIGN': 'Info', 
        b'SYLT': 'Info', b'SYTC': 'Info', b'TALB':'Album', 
        b'TBPM': 'Track BPM', b'TCOM': 'Info', b'TCON': 'Genre', 
        b'TCOP': 'Info', b'TDAT': 'Info', b'TDRC': 'Recording Time', 
        b'TDEN': 'Info', b'TDLY': 'Info', b'TDRL': 'Info', 
        b'TDTG': 'Info', b'TENC': 'Info', 
        b'TEXT': 'Info', b'TFLT': 'Info', b'TIME': 'Info', 
        b'TIT1': 'Info', b'TIT2': 'Title', 
        b'TIT3': 'Info', b'TKEY': 'Info', b'TLAN': 'Info', 
        b'TLEN': 'Info', b'TMCL': 'Info', b'TMED': 'Info', 
        b'TMOO': 'Info', b'TOAL': 'Info', b'TOFN': 'Info', 
        b'TOLY': 'Info', b'TOPE': 'Info', b'TORY': 'Info', 
        b'TDOR': 'Info', b'TOWN': 'Info', b'TPE1': 'Artist', 
        b'TPE2':'Artist', b'TPE3': 'Artist', b'TPE4': 'Artist', 
        b'TPOS': 'Info', b'TPRO': 'Info', b'TPUB': 'Info', 
        b'TXXX': 'Info', b'TRDA': 'Info', 
        b'TRSN': 'Info', b'TRSO': 'Info', b'TSIZ': 'Info', 
        b'TSOA': 'Info', b'TSOP': 'Info', b'TSOT': 'Info', 
        b'TSRC': 'Info', b'TSSE': 'Info', b'TSST': 'Info', 
        b'UFID': 'Info', b'USER': 'Info', b'USLT': 'Info', 
        b'WCOM': 'Info', b'WCOP': 'Info', b'WOAF': 'Info', 
        b'WOAR': 'Info', b'WOAS': 'Info', b'WORS': 'Info', 
        b'WPAY': 'Info', b'WPUB': 'Info', b'WXXX': 'Info', 
        b'CTPE': 'Info'}

found_tags = {}
def main():
    with open(sys.argv[1], "rb") as binary_file:

        header_size = 10

        binary_file.seek(0, 0)

        begin = binary_file.read(3)

        if begin != b'ID3':
            sys_exit("No tags found")

        version = binary_file.read(2) #two bytes of version of ID3

        binary_file.seek(10, 0)

        start = 10

        data = binary_file.read(1)

        while data != b'':
            if data == b'T':
                binary_file.seek(-1, 1)
                tag = binary_file.read(4)
                size = int.from_bytes(binary_file.read(4), byteorder='big')
                if tag in tags.keys():
                    
                    collect_tag(binary_file, start)
                    start += size + header_size
                    
                    binary_file.seek(start, 0)

            if data == b'C':
                binary_file.seek(-1, 1)
                tag = binary_file.read(4)
                size = int.from_bytes(binary_file.read(4), byteorder='big')
                if tag in tags.keys():
                    
                    collect_tag(binary_file, start)
                    start += size + header_size
                    
                    binary_file.seek(start, 0)
                    

            if data == b'L':
                binary_file.seek(-1, 1)
                if binary_file.read(4) == b'LAME':
                    break

            data = binary_file.read(1)
    parse_tags(found_tags)

def collect_tag(bin, offset):
    bin.seek(offset, 0)
    tag1 = bin.read(4)
    # tag_description = found_tags[tag1]
    size = int.from_bytes(bin.read(4), byteorder='big')
    flag_bytes = bin.read(2)

    # byte = bin.read(1)

    count = 0

    b = b""

    while count != size:
        b += bin.read(1)
        count += 1
        if count > 200:
            break
    
    found_tags[tag1.decode()] = b
    return

def parse_tags(d):
    for key, value in d.items():
        if key[0] == "T":
            if value[0] == 0:
                decoding_text = 'ISO-8859-1'
                offset = 0

            if value[0] == 1 or value[0] == 2:
                if value[1] == 255:
                    if value[2] == 254:
                        decoding_text = 'utf-16-le'
                        offset = 3

                if value[1] == 254:
                    if value[2] == 255:
                        decoding_text = 'utf-16-be'


            if value[0] == 3:
                decoding_text = 'utf-8'
                offset = 3

            description = tags[str.encode(key)]
            # print("{0}: {1}".format(key, value[offset:].decode(decoding_text)))
            print("{0}: {1}".format(description, value[offset:].decode(decoding_text)))

        if key[0] == "C":
            if value[0] == 1: # find language
                b = bytearray()
                for i in range(1,4):
                    b.append(value[i])
                lang = b.decode()

            if value[0] == 0:
                decoding_text = 'ISO-8859-1'
                offset = 0

            if value[0] == 1 or value[0] == 2:
                if value[1] == 255:
                    if value[2] == 254:
                        decoding_text = 'utf-16-le'
                        offset = 3

                if value[1] == 254:
                    if value[2] == 255:
                        decoding_text = 'utf-16-be'
                        offset = 3
                
            if value[6] == 0:
                if value[7] == 0:
                    pass
            description = tags[str.encode(key)]
            print("{0}: {1}".format(description, value[offset * 2:].decode(decoding_text)))

        if key[0] == "W":
            print("{0}: {1}".format(key, value))
    

def find_dec(dict, num=0):

    pass

if __name__ == '__main__':
    main()
