import serial
import time
import numpy

#Activation du luxmètre en mode PC

ser = serial.Serial(port="/dev/ttyUSB0",baudrate= 9600,  bytesize=7, timeout=18, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)

def buildMsgString(command):
    STX = chr(0x02)
    ETX = chr(0x03)

    def computeBCC(command):
        if command != None and len(command) > 0:
            c = ord(command[0])
            # print(hex(c)+'\n')
            # for k in range(1, len(command)):
            for k in range(1, len(command)):
                # print(hex( ord(command[k])) +'\n')
                c ^= ord(command[k])
            hx = hex(c)[2:]
            if len(hx) == 1:
                hx = '0' + hx
        return hx

    def checkBCC(str):
        if str[0] != STX:
            print("bad starting character")
            return False  # bad starting character

        msg = ''
        for k in range(1, len(str)):
            # print(hex(ord(str[k])))
            if str[k] == ETX:
                # print("k: ", k)
                msg = str[1:(k + 1)]
                if len(str) >= k + 3:
                    bcc = str[k + 1:k + 3]
                else:
                    print("too short")
                    return False  # too short message
                break
        if msg != '':
            bccTh = computeBCC(msg)
            print("bccTh: ", bccTh)
            return bccTh == bcc  # True if bcc is correct, false otherwise
        else:
            return False  # ETX not found

    res = STX + command + ETX + computeBCC(command + ETX) + chr(0xD) + chr(0xA)
    return res

def error_processing(value_error):
    if value_error =="1":
        print("Error : Receptor head power is switched off")
        exit()
        return False
    elif value_error =="2":
        print("Error : Switch off the T10-A and then switch it back on, and repeat the procedure from the beginning")
        exit()
        return False
    elif value_error =="3":
        print("Error : Switch off the T10-A and then switch it back on, and repeat the procedure from the beginning")
        exit()
        return False
    elif value_error =="5":
        print("Error : Measurement value error, out of range")
        exit()
        return False
    else:
        return True


def mode_PC_activation():
    ser.write(buildMsgString('00541   ').encode('utf-8'))
    ln = ser.readline()
    time.sleep(0.75)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    ser.write(buildMsgString('00100300').encode('utf-8'))
    ln = ser.readline()

    # Identification du Range et de l'activation correcte ou non du mode PC
    rge = ln.decode('utf-8')[7]
    error = ln.decode('utf-8')[6]
    #print("error : "+error)
    if error_processing(error) == True:
        print("Activation mode PC = OK")
        time.sleep(3)
        return True, rge
    else:
        print("Activation mode PC = KO")
        exit()
        return False

def data_collect(rge):
    ser.write(buildMsgString('00100300').encode('utf-8'))
    ln = ser.readline()
    error = ln.decode('utf-8')[6]
    rge1 = ln.decode('utf-8')[7]
    #print(rge)
    if error_processing(error) == True:
        if rge1 != rge:
            print("Measurement out of range, value not taken into account")
            time.sleep(0.5)
            return False
        else :
            data = ln.decode('utf-8')[9:15]
            measure1 = data[1:5]
            exp = data[5] 
            measure2 = int(measure1)*10**(-4+int(exp))
            measure3 = str(measure2)
            return measure3
    else:
        print("Measurement error")
        return False
