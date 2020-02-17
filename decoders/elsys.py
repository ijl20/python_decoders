#
# Elsys sensor decoder
#
# Instantiate with:
#    decoder = Elsys(expand, decoded_property)
#    where:
#        expand = [True] | False:  decoder returns expanded original message with "payload_decoded" property.
#        decoded_property = <string> ["payload_decoded"]: contains property name to contain decoded message
#
# Implements:
#    test(message, params): returns true|false whether this decoder will handle message
#    decode(message, params): returns Python dictionary of decoded message, or raises DecodeError

import base64
import simplejson as json

class Decoder(object):
    def __init__(self,expand=True,
                 decoded_property="payload_decoded"):
        print("Elsys init()")

        self.expand = expand
        self.decoded_property = decoded_property

        self.TYPE_TEMP         = 0x01 #temp 2 bytes -3276.8°C -->3276.7°C
        self.TYPE_RH           = 0x02 #Humidity 1 byte  0-100%
        self.TYPE_ACC          = 0x03 #acceleration 3 bytes X,Y,Z -128 --> 127 +/-63=1G
        self.TYPE_LIGHT        = 0x04 #Light 2 bytes 0-->65535 Lux
        self.TYPE_MOTION       = 0x05 #No of motion 1 byte  0-255
        self.TYPE_CO2          = 0x06 #Co2 2 bytes 0-65535 ppm
        self.TYPE_VDD          = 0x07 #VDD 2byte 0-65535mV
        self.TYPE_ANALOG1      = 0x08 #VDD 2byte 0-65535mV
        self.TYPE_GPS          = 0x09 #3bytes lat 3bytes long binary
        self.TYPE_PULSE1       = 0x0A #2bytes relative pulse count
        self.TYPE_PULSE1_ABS   = 0x0B #4bytes no 0->0xFFFFFFFF
        self.TYPE_EXT_TEMP1    = 0x0C #2bytes -3276.5C-->3276.5C
        self.TYPE_EXT_DIGITAL  = 0x0D #1bytes value 1 or 0
        self.TYPE_EXT_DISTANCE = 0x0E     #2bytes distance in mm
        self.TYPE_ACC_MOTION   = 0x0F     #1byte number of vibration/motion
        self.TYPE_IR_TEMP      = 0x10     #2bytes internal temp 2bytes external temp -3276.5C-->3276.5C
        self.TYPE_OCCUPANCY    = 0x11     #1byte data
        self.TYPE_WATERLEAK    = 0x12     #1byte data 0-255
        self.TYPE_GRIDEYE      = 0x13     #65byte temperature data 1byte ref+64byte external temp
        self.TYPE_PRESSURE     = 0x14     #4byte pressure data (hPa)
        self.TYPE_SOUND        = 0x15     #2byte sound data (peak/avg)
        self.TYPE_PULSE2       = 0x16     #2bytes 0-->0xFFFF
        self.TYPE_PULSE2_ABS   = 0x17     #4bytes no 0->0xFFFFFFFF
        self.TYPE_ANALOG2      = 0x18     #2bytes voltage in mV
        self.TYPE_EXT_TEMP2    = 0x19     #2bytes -3276.5C-->3276.5C
        self.TYPE_EXT_DIGITAL2 = 0x1A     # 1bytes value 1 or 0
        self.TYPE_EXT_ANALOG_UV= 0x1B     # 4 bytes signed int (uV)
        self.TYPE_DEBUG        = 0x3D     # 4bytes debug

        return

    def test(self, message, params=None):
        print("Elsys test() {}".format(message))

        return True

    def decode(self, message, params=None):
        print("Elsys decode() {}".format(message))

        inc_msg=str(message,'utf-8')

        print("Elsys decode str {}".format(inc_msg))

        msg_json=json.loads(inc_msg)

        #printf(msg_json)

        print("\nDECODED:\n")

        rawb64 = msg_json["payload_raw"]

        print("rawb64 {}".format(rawb64))

        decoded = self.DecodeElsysPayload(self.b64toBytes(rawb64))

        print(rawb64)
        print(decoded)

        dev_id=msg_json["dev_id"]

        print("dev_id={}".format(dev_id))

        time=msg_json["metadata"]["time"]

        #printf(time)

        print("\nFINITO:\n")

        return_message = { self.decoded_property: decoded}

        return return_message

    def bin8dec(self, bin):
        num=bin&0xFF;
        if (0x80 & num):
            num = - (0x0100 - num);
        return num

    def bin16dec(self, bin):
        num=bin&0xFFFF;
        if (0x8000 & num):
            num = - (0x010000 - num);
        return num

    def hexToBytes(self, hex):
        bytes = []
        for c in range(0,len(hex),2):
            bytes.append(int(hex[c: c+2],16))
        return bytes

    def b64ToHex(self, b64):
        return base64.b64decode(b64).hex()

    def b64toBytes(self,b64):
        print("b64toBytes")
        return base64.b64decode(b64)

    def DecodeElsysPayload(self,data):
        obj = {}
        obj["device"]="elsys"
        print("data ",data," len ",len(data))
        i = 0
        while(i<len(data)):
            #Temperature
            if data[i] == self.TYPE_TEMP:
                temp=(data[i+1]<<8)|(data[i+2])
                temp=self.bin16dec(temp)
                obj["temperature"]=temp/10
                i=i+2

            #Humidity
            elif data[i] == self.TYPE_RH:
                rh=(data[i+1])
                obj["humidity"]=rh
                i+=1

            #Acceleration
            elif data[i] == self.TYPE_ACC:
                obj["x"]=self.bin8dec(data[i+1])
                obj["y"]=self.bin8dec(data[i+2])
                obj["z"]=self.bin8dec(data[i+3])
                i+=3

            #Light
            elif data[i] == self.TYPE_LIGHT:
                obj["light"]=(data[i+1]<<8)|(data[i+2])
                i+=2

            #Motion sensor(PIR)
            elif data[i] == self.TYPE_MOTION:
                obj["motion"]=(data[i+1])
                i+=1

            #CO2
            elif data[i] == self.TYPE_CO2:
                obj["co2"]=(data[i+1]<<8)|(data[i+2])
                i+=2

            #Battery level
            elif data[i] == self.TYPE_VDD:
                obj["vdd"]=(data[i+1]<<8)|(data[i+2])
                i+=2

            #Analog input 1
            elif data[i] == self.TYPE_ANALOG1:
                obj["analog1"]=(data[i+1]<<8)|(data[i+2])
                i+=2

            #gps
            elif data[i] ==  self.TYPE_GPS:
                obj["lat"]=(data[i+1]<<16)|(data[i+2]<<8)|(data[i+3])
                obj["lng"]=(data[i+4]<<16)|(data[i+5]<<8)|(data[i+6])
                i+=6

            #Pulse input 1
            elif data[i] == self.TYPE_PULSE1:
                obj["pulse1"]=(data[i+1]<<8)|(data[i+2])
                i+=2

            #Pulse input 1 absolute value
            elif data[i] ==  self.TYPE_PULSE1_ABS:
                pulseAbs=(data[i+1]<<24)|(data[i+2]<<16)|(data[i+3]<<8)|(data[i+4])
                obj["pulseAbs"]=pulseAbs
                i+=4

            #External temp
            elif data[i] ==self.TYPE_EXT_TEMP1:
                temp=(data[i+1]<<8)|(data[i+2])
                temp=bin16dec(temp)
                obj["externalTemperature"]=temp/10
                i+=2

            #Digital input
            elif data[i] == self.TYPE_EXT_DIGITAL:
                obj["digital"]=(data[i+1])
                i+=1

            #Distance sensor input
            elif data[i] == self.TYPE_EXT_DISTANCE:
                obj["distance"]=(data[i+1]<<8)|(data[i+2])
                obj["JBJB"]="my debug here"
                i+=2

            #Acc motion
            elif data[i] == self.TYPE_ACC_MOTION:
                obj["accMotion"]=(data[i+1])
                i+=1

            #IR temperature
            elif data[i] == self.TYPE_IR_TEMP:
                iTemp=(data[i+1]<<8)|(data[i+2])
                iTemp=self.bin16dec(iTemp)
                eTemp=(data[i+3]<<8)|(data[i+4])
                eTemp=self.bin16dec(eTemp)
                obj["irInternalTemperature"]=iTemp/10
                obj["irExternalTemperature"]=eTemp/10
                i+=4

            #Body occupancy
            elif data[i] == self.TYPE_OCCUPANCY:
                obj["occupancy"]=(data[i+1])
                i+=1

            #Water leak
            elif data[i] == self.TYPE_WATERLEAK:
                obj["waterleak"]=(data[i+1])
                i+=1

            #Grideye data
            elif data[i] == self.TYPE_GRIDEYE:
                obj["grideye"]="8x8 missing"
                i+=65

            #External Pressure
            elif data[i] == self.TYPE_PRESSURE:
                temp=(data[i+1]<<24)|(data[i+2]<<16)|(data[i+3]<<8)|(data[i+4])
                obj["pressure"]=temp/1000
                i+=4

            #Sound
            elif data[i] == self.TYPE_SOUND:
                obj["soundPeak"]=data[i+1]
                obj["soundAvg"]=data[i+2]
                i+=2

            #Pulse 2
            elif data[i] == self.TYPE_PULSE2:
                obj["pulse2"]=(data[i+1]<<8)|(data[i+2])
                i+=2

            #Pulse input 2 absolute value
            elif data[i] == self.TYPE_PULSE2_ABS:
                obj["pulseAbs2"]=(data[i+1]<<24)|(data[i+2]<<16)|(data[i+3]<<8)|(data[i+4])
                i+=4

            #Analog input 2
            elif data[i] ==  self.TYPE_ANALOG2:
                obj["analog2"]=(data[i+1]<<8)|(data[i+2])
                i+=2

            #External temp 2
            elif data[i] == self.TYPE_EXT_TEMP2:
                temp=(data[i+1]<<8)|(data[i+2])
                temp=self.bin16dec(temp)
                obj["externalTemperature2"]=temp/10
                i+=2

            #Digital input 2
            elif data[i] ==  self.TYPE_EXT_DIGITAL2:
                obj["digital2"]=(data[i+1])
                i+=1

            #Load cell analog uV
            elif data[i] == self.TYPE_EXT_ANALOG_UV:
                obj["analogUv"] = (data[i + 1] << 24) | (data[i + 2] << 16) | (data[i + 3] << 8) | (data[i + 4])
                i += 4

            else:
                #print("something is wrong with data")
                i=len(data)

            i+=1

        return obj

