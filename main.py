
import importlib


def load_decoder(decoder_name):
    return importlib.import_module('decoders.'+decoder_name)

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("csn/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Rcvd: {} {} ".format(msg.topic,str(msg.payload)))

    for decoder in decoders:
        if decoder.test(msg.payload):
            decoded = decoder.decode(msg.payload)
            print("Decoded: {}".format(decoded))
            break


if __name__ == '__main__':
    plugin1 = load_decoder('plugin1')
    plugin1.main()

    elsys = load_decoder('elsys')

    decoders = [ elsys.Decoder() ]

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('csn-node-test','csn-node-test')
    client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
    client.loop_forever()

