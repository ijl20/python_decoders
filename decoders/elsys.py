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

class Decoder(object):
    def __init__(self,expand=True,
                 decoded_property="payload_decoded"):
        print("Elsys init()")

        self.expand = expand
        self.decoded_property = decoded_property

        return

    def test(self, message, params=None):
        print("Elsys test() {}".format(message))

        return True

    def decode(self, message, params=None):
        print("Elsys decode() {}".format(message))
        return_message = { self.decoded_property: { "foo": "bah" }}
        return return_message

