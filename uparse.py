# parse_qsl

from re import compile as re_compile

_percent_pat = re_compile(b'((?:%[A-Fa-f0-9]{2})+)')
_unreserved_chars = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                              b'abcdefghijklmnopqrstuvwxyz'
                              b'0123456789'
                              b'_.-')

def percent_decode(string, encoding = 'utf-8', errors = 'replace'):
    str_bytes = string.encode('utf-8')
    hex_to_byte = lambda match_ret: str(bytearray.fromhex( match_ret.group(0).replace(b'%', b'').decode('utf-8')))
    str_bytes = _percent_pat.sub(hex_to_byte, str_bytes)
    string = str_bytes.decode(encoding, errors)
    return string

def percent_decode_plus(string, encoding = 'utf-8', errors = 'replace'):
    return percent_decode(string.replace('+', '%20'), encoding, errors)

def percent_encode(string, safe = '/', encoding = 'utf-8', errors = 'strict'):
    if not string:
        return string
    string = string.encode(encoding, errors)
    bytes_unchanged = _unreserved_chars.union(
        safe.encode('ascii', 'ignore'))
    process_byte = lambda byte: chr(byte) if byte in bytes_unchanged else '%{:02X}'.format(byte)
    return ''.join((process_byte(b) for b in string))

def percent_encode_plus(string, safe = '', encoding = 'utf-8',  errors = 'strict'):
    safe += ' '
    string = percent_encode(string, safe, encoding, errors)
    return string.replace(' ', '+')



def parse_qsl(qs,keep_blank_values=0,strict_parsing=0):
    pairs = qs.split('&')
    r = []
    for name_value in pairs:
        if not name_value and not strict_parsing: continue
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            if strict_parsing:
                raise ValueError, "bad query field: %r" % (name_value,)
            if keep_blank_values:
                nv.append('')
            else:
                continue
        if len(nv[1]) or keep_blank_values:
            name = percent_decode_plus(nv[0].replace('+', ' '))
            value = percent_decode_plus(nv[1].replace('+', ' '))
            r.append((name,value))
    return r
