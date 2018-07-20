import sys

def sys_exit(msg):
    print(msg)
    sys.exit()

if len(sys.argv) > 2:
    sys_exit("Too many arguments")

if len(sys.argv) == 1:
    sys_exit("Need at least one file to open")

tags = [b'TYER', b'TRCK', b'AENC', b'ASPI', b'APIC', b'COMM', b'COMR', b'ENCR',
        b'EQUA', b'EQU2', b'ETCO', b'GEOB', b'GRID', b'IPLS', b'TIPL', b'LINK',
        b'MCDI', b'MLLT', b'OWNE', b'PRIV', b'PCNT', b'POPM', b'POSS', b'RBUF', 
        b'RVAD', b'RVA2', b'RVRB', b'SEEK', b'SIGN', b'SYLT', b'SYTC', b'TALB', 
        b'TBPM', b'TCOM', b'TCON', b'TCOP', b'TDAT', b'TDRC', b'TDEN', b'TDLY', 
        b'TDRC', b'TDRL', b'TDTG', b'TENC', b'TEXT', b'TFLT', b'TIME', b'TDRC', 
        b'TIT1', b'TIT2', b'TIT3', b'TKEY', b'TLAN', b'TLEN', b'TMCL', b'TMED', 
        b'TMOO', b'TOAL', b'TOFN', b'TOLY', b'TOPE', b'TORY', b'TDOR', b'TOWN', 
        b'TPE1', b'TPE2', b'TPE3', b'TPE4', b'TPOS', b'TPRO', b'TPUB', b'TXXX', 
        b'TRDA', b'TDRC', b'TRSN', b'TRSO', b'TSIZ', b'TSOA', b'TSOP', b'TSOT', 
        b'TSRC', b'TSSE', b'TSST', b'UFID', b'USER', b'USLT', b'WCOM', b'WCOP', 
        b'WOAF', b'WOAR', b'WOAS', b'WORS', b'WPAY', b'WPUB', b'WXXX', b'CTPE']

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
                if tag in tags:
                    
                    collect_tag(binary_file, start)
                    start += size + header_size
                    
                    binary_file.seek(start, 0)

            if data == b'C':
                binary_file.seek(-1, 1)
                tag = binary_file.read(4)
                size = int.from_bytes(binary_file.read(4), byteorder='big')
                if tag in tags:
                    
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
    size = int.from_bytes(bin.read(4), byteorder='big')
    flag_bytes = bin.read(2)

    # byte = bin.read(1)

    count = 0

    b = b""

    while count != size:
        b += bin.read(1)
        count += 1
    
    found_tags[tag1.decode()] = b
    return

def parse_tags(d):
    for key, value in d.items():
        if key[0] == "T":
            if value[0] == 0:
                decoding_text = 'ISO-8859-1'
                offset = 0

            if value[0] == 1:
                if value[1] == 255:
                    if value[2] == 254:
                        decoding_text = 'utf-16-le'
                        offset = 3

                if value[1] == 254:
                    if value[2] == 255:
                        decoding_text = 'utf-16-be'
                        offset = 3
            
            if value[0] == 2:
                if value[1] == 255:
                    if value[2] == 254:
                        decoding_text = 'utf-16-le'
                        offset = 3

                if value[1] == 254:
                    if value[2] == 255:
                        decoding_text = 'utf-16-be'
                        offset = 3


            if value[0] == 3:
                decoding_text = 'utf-8'
                offset = 3

            print("{0}: {1}".format(key, value[offset:].decode(decoding_text)))

        if key[0] == "C":
            if value[0] == 1: # find language
                b = bytearray()
                for i in range(1,4):
                    b.append(value[i])
                lang = b.decode()

            if value[0] == 0:
                decoding_text = 'ISO-8859-1'
                offset = 0

            if value[0] == 1:
                if value[1] == 255:
                    if value[2] == 254:
                        decoding_text = 'utf-16-le'
                        offset = 3

                if value[1] == 254:
                    if value[2] == 255:
                        decoding_text = 'utf-16-be'
                        offset = 3
            
            if value[0] == 2:
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
            
            print("{0}: {1}".format(key, value[offset * 2:].decode(decoding_text)))

        if key[0] == "W":
            print("{0}: {1}".format(key, value))
    

def find_dec(dict, num=0):

    pass

if __name__ == '__main__':
    main()