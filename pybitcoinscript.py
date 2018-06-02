"""
Input: int int
Output: int int int
Code:
  1000 OP_ROT OP_DIV
  OP_2DUP OP_SUB
  9 OP_OVER OP_MOD

  OP_DUP 0 OP_NUMEQUAL OP_IF 0 OP_ELSE
  OP_DUP 1 OP_NUMEQUAL OP_IF 7 OP_ELSE
  OP_DUP 2 OP_NUMEQUAL OP_IF 5 OP_ELSE
  OP_DUP 3 OP_NUMEQUAL OP_IF 3 OP_ELSE
  OP_DUP 4 OP_NUMEQUAL OP_IF 1 OP_ELSE
  OP_DUP 5 OP_NUMEQUAL OP_IF 8 OP_ELSE
  OP_DUP 6 OP_NUMEQUAL OP_IF 6 OP_ELSE
  OP_DUP 7 OP_NUMEQUAL OP_IF 4 OP_ELSE
  OP_DUP 8 OP_NUMEQUAL OP_IF 2 OP_ELSE
  OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF

  OP_OVER 0 OP_NUMEQUAL OP_IF 0 OP_ELSE
  OP_OVER 1 OP_NUMEQUAL OP_IF 3 OP_ELSE
  OP_OVER 2 OP_NUMEQUAL OP_IF 2 OP_ELSE
  OP_OVER 3 OP_NUMEQUAL OP_IF 1 OP_ELSE
  OP_OVER 4 OP_NUMEQUAL OP_IF 0 OP_ELSE
  OP_OVER 5 OP_NUMEQUAL OP_IF 3 OP_ELSE
  OP_OVER 6 OP_NUMEQUAL OP_IF 2 OP_ELSE
  OP_OVER 7 OP_NUMEQUAL OP_IF 1 OP_ELSE
  OP_OVER 8 OP_NUMEQUAL OP_IF 0 OP_ELSE
  OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF OP_ENDIF

  OP_2SWAP OP_DROP
  9 OP_SWAP OP_DIV OP_SUB

  OP_DUP OP_DUP OP_ABS OP_NUMEQUAL
  OP_IF
    OP_2OVER OP_DROP
    OP_3DUP OP_SUB OP_SUB

    OP_DUP OP_DUP OP_ABS OP_NUMEQUAL
    OP_IF
      OP_2SWAP
    OP_ELSE
      -1 -1 -1
    OP_ENDIF
  OP_ELSE
    -1 -1 -1
  OP_ENDIF
"""

import re
import sys

inputFormat = []
outputFormat = []
code = []
stack = []
alt = []

def parse():
    global inputFormat, outputFormat, code
    cur = None
    for d in __doc__.split():
        if d=="Input:":
            cur = inputFormat
        elif d=="Output:":
            cur = outputFormat
        elif d=="Code:":
            cur = code
        else:
            if cur == None:
                raise Exception("parse error", d)
            cur += [d]

def int2str(v):
    res = ""
    a = abs(v)
    while a>0:
        res += chr(a&0xff)
        a >>= 8
    if len(res)>0 and ord(res[-1])&0x80:
        res += "\x80" if v<0 else "\x00"
    elif v<0:
        res = res[:-1] + chr(ord(res[-1])|0x80)
    return res

def str2int(s):
    res = 0
    for i in range(len(s)):
        res |= ord(s[i])<<(i*8)
    if len(s)>0 and ord(s[-1])&0x80:
        res = -(res ^ (0x80<<(len(s)*8-8)))
    return res

def str2bool(s):
    return s != "\0"*len(s)

def input():
    global stack
    i = []
    buf = []
    for f in inputFormat:
        while buf==[]:
            buf = raw_input().split()
        if f=="int":
            i += [int2str(int(buf.pop(0), 10))]
        elif f=="str":
            i += [buf.pop(0)]
        else:
            raise Exception("invalid input format", f)
    stack = i[::-1]

def execute():
    global stack, alt

    # get int
    gi = lambda: str2int(stack.pop())
    # get str
    gs = lambda: stack.pop()

    ip = 0
    fexec = []
    while ip<len(code):
        op = code[ip]
        ip += 1
        r = None

        if not all(fexec) and op not in ["OP_IF", "OP_NOTIF", "OP_VERIF", "OP_VERNOTIF", "OP_ELSE", "OP_ENDIF"]:
            continue

        if False: pass

        # push value
        elif op=="OP_0":                    r = 0
        elif op=="OP_FALSE":                r = 0
        elif op=="OP_PUSHDATA1":            raise Exception("not implemented op code", op)
        elif op=="OP_PUSHDATA2":            raise Exception("not implemented op code", op)
        elif op=="OP_PUSHDATA4":            raise Exception("not implemented op code", op)
        elif op=="OP_1NEGATE":              r = -1
        elif op=="OP_RESERVED":             raise Exception("not implemented op code", op)
        elif op=="OP_1":                    r = 1
        elif op=="OP_TRUE":                 r = 1
        elif op=="OP_2":                    r = 2
        elif op=="OP_3":                    r = 3
        elif op=="OP_4":                    r = 4
        elif op=="OP_5":                    r = 5
        elif op=="OP_6":                    r = 6
        elif op=="OP_7":                    r = 7
        elif op=="OP_8":                    r = 8
        elif op=="OP_9":                    r = 9
        elif op=="OP_10":                   r = 10
        elif op=="OP_11":                   r = 11
        elif op=="OP_12":                   r = 12
        elif op=="OP_13":                   r = 13
        elif op=="OP_14":                   r = 14
        elif op=="OP_15":                   r = 15
        elif op=="OP_16":                   r = 16

        # control
        elif op=="OP_NOP":                  pass
        elif op=="OP_VER":                  raise Exception("not implemented op code", op)
        elif op=="OP_IF":                   fexec += [str2bool(stack.pop()) if all(fexec) else False]
        elif op=="OP_NOTIF":                fexec += [not str2bool(stack.pop()) if all(fexec) else False]
        elif op=="OP_VERIF":                raise Exception("not implemented op code", op)
        elif op=="OP_VERNOTIF":             raise Exception("not implemented op code", op)
        elif op=="OP_ELSE":                 fexec += [not fexec.pop()]
        elif op=="OP_ENDIF":                fexec.pop()
        elif op=="OP_VERIFY":               raise Exception("not implemented op code", op)
        elif op=="OP_RETURN":               break

        # stack ops
        elif op=="OP_TOALTSTACK":           alt += [stack.pop()]
        elif op=="OP_FROMALTSTACK":         stack += [alt.pop()]
        elif op=="OP_2DROP":                stack.pop(); stack.pop()
        elif op=="OP_2DUP":                 stack += stack[-2:]
        elif op=="OP_3DUP":                 stack += stack[-3:]
        elif op=="OP_2OVER":                stack += stack[-4:-2]
        elif op=="OP_2ROT":                 stack += [stack.pop(-6), stack.pop(-5)]
        elif op=="OP_2SWAP":                stack += [stack.pop(-4), stack.pop(-3)]
        elif op=="OP_IFDUP":                t = stack.pop(); stack += [t]*(2 if str2bool(t) else 1)
        elif op=="OP_DEPTH":                r = len(stack)
        elif op=="OP_DROP":                 stack.pop()
        elif op=="OP_DUP":                  stack += [stack[-1]]
        elif op=="OP_NIP":                  stack.pop(-2)
        elif op=="OP_OVER":                 stack += [stack[-2]]
        elif op=="OP_PICK":                 stack += [stack[-gi()-1]]
        elif op=="OP_ROLL":                 stack += [stack.pop(-gi()-1)]
        elif op=="OP_ROT":                  stack += [stack.pop(-3)]
        elif op=="OP_SWAP":                 stack += [stack.pop(-2)]
        elif op=="OP_TUCK":                 stack.insert(-2, stack[-1])

        # splice ops
        elif op=="OP_CAT":                  r = gs()+gs()
        elif op=="OP_SUBSTR":               size = gi(); begin = gi(); r = gs()[begin:begin+size]
        elif op=="OP_LEFT":                 size = gi(); r = stack.pop[:size]
        elif op=="OP_RIGHT":                size = gi(); r = stack.pop[-size:] if size>0 else ""
        elif op=="OP_SIZE":                 r = len(stack[-1])

        # bit logic
        elif op=="OP_INVERT":               r = "".join(chr(ord(x)^0xff) for x in gs())
        elif op in ["OP_INVERT", "OP_AND", "OP_OR", "OP_XOR"]:
            A = gs()
            B = gs()
            A += "\0"*max(len(B)-len(A), 0)
            B += "\0"*max(len(A)-len(B), 0)
            r = ""
            for a, b in zip(A, B):
                if op=="OP_AND": r += chr(ord(a) & ord(b))
                if op=="OP_OR": r += chr(ord(a) | ord(b))
                if op=="OP_OR": r += chr(ord(a) ^ ord(b))
        elif op=="OP_EQUAL":                r = gs() == gs()
        elif op=="OP_EQUALVERIFY":
            if not gs() == gs():
                break
        elif op=="OP_RESERVED1":            raise Exception("not implemented op code", op)
        elif op=="OP_RESERVED2":            raise Exception("not implemented op code", op)

        # numeric
        elif op=="OP_1ADD":                 r = gi() + 1
        elif op=="OP_1SUB":                 r = gi() - 1
        elif op=="OP_2MUL":                 r = gi() * 2
        elif op=="OP_2DIV":                 r = gi() / 2
        elif op=="OP_NEGATE":               r = -gi()
        elif op=="OP_ABS":                  r = abs(gi())
        elif op=="OP_NOT":                  r = gi() == 0
        elif op=="OP_0NOTEQUAL":            r = gi() != 0

        elif op=="OP_ADD":                  r = gi() + gi()
        elif op=="OP_SUB":                  r = gi() - gi()
        elif op=="OP_MUL":                  r = gi() * gi()
        elif op=="OP_DIV":                  r = gi() / gi()
        elif op=="OP_MOD":                  r = gi() % gi()
        elif op=="OP_LSHIFT":               r = gi() << gi()
        elif op=="OP_RSHIFT":               r = gi() >> gi()

        elif op=="OP_BOOLAND":              r = gi() != 0 and gi() != 0
        elif op=="OP_BOOLOR":               r = gi() != 0 or gi() != 0
        elif op=="OP_NUMEQUAL":             r = gi() == gi()
        elif op=="OP_NUMEQUALVERIFY":
            if not gi() == gi():
                break
        elif op=="OP_NUMNOTEQUAL":          r = gi() != gi()
        elif op=="OP_LESSTHAN":             r = gi() < gi()
        elif op=="OP_GREATERTHAN":          r = gi() > gi()
        elif op=="OP_LESSTHANOREQUAL":      r = gi() <= gi()
        elif op=="OP_GREATERTHANOREQUAL":   r = gi() >= gi()
        elif op=="OP_MIN":                  r = min(gi(), gi())
        elif op=="OP_MAX":                  r = max(gi(), gi())

        elif op=="OP_WITHIN":               x = gi(); y = gi(); z = gi(); r = y <= z < x

        elif op=="OP_RIPEMD160":            h = hashlib.new("ripemd160"); h.update(gs()); r= h.digest()
        elif op=="OP_SHA1":                 r = hashlib.sha1(gs()).digest()
        elif op=="OP_SHA256":               r = hashlib.sha256(gs()).digest()
        elif op=="OP_HASH160":              h = hashlib.new("ripemd160"); h.update(hashlib.sha256(gs()).digest()); r = h.digest()
        elif op=="OP_HASH256":              r = hashlib.sha256(hashlib.sha256(gs()).digest()).digest()
        elif op=="OP_CODESEPARATOR":        raise Exception("not implemented op code", op)
        elif op=="OP_CHECKSIG":             raise Exception("not implemented op code", op)
        elif op=="OP_CHECKSIGVERIFY":       raise Exception("not implemented op code", op)
        elif op=="OP_CHECKMULTISIG":        raise Exception("not implemented op code", op)
        elif op=="OP_CHECKMULTISIGVERIFY":  raise Exception("not implemented op code", op)

        elif op=="OP_NOP1":                 pass
        elif op=="OP_CHECKLOCKTIMEVERIFY":  raise Exception("not implemented op code", op)
        elif op=="OP_CHECKSEQUENCEVERIFY":  raise Exception("not implemented op code", op)
        elif op=="OP_NOP4":                 pass
        elif op=="OP_NOP5":                 pass
        elif op=="OP_NOP6":                 pass
        elif op=="OP_NOP7":                 pass
        elif op=="OP_NOP8":                 pass
        elif op=="OP_NOP9":                 pass
        elif op=="OP_NOP10":                pass

        elif op=="OP_INVALIDOPCODE":        raise Exception("invalid op code", op)
        elif re.match(r"^([-+]?)0x([0-9a-f]+)$", op, re.IGNORECASE):
            m = re.match(r"^([-+]?)0x([0-9a-f]+)$", op, re.IGNORECASE)
            r = int(m.group(1)+m.group(2), 16)
        elif re.match(r"^[-+]?\d+$", op):
            r = int(op)
        elif op[0]=="'" and op[-1]=="'" or op[0]=='"' and op[-1]=='"':
            r = op[1:-1]
        else:
            r = op

        if isinstance(r, bool):
            r = int(r)
        if isinstance(r, int):
            r = int2str(r)
        if isinstance(r, str):
            stack += [r]

def output():
    global stack
    for f in outputFormat:
        if f=="int":
            print str2int(stack.pop()),
        elif f=="str":
            print stack.pop(),
        else:
            raise Exception("invalid op code", op)
    print

parse()
input()
execute()
output()
# debug
print >>sys.stderr, "stack:", stack
