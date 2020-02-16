# Python Decoders

This project is a combination of using the Paho MQTT client to subscribe to 
an MQTT broker where each message may need decoding (or parsing) to produce a more readable version for subsequent
processing. The decoded version of the message may be published back into an MQTT broker so other clients can
use the same method to subscribe to those (or the main python process can simply process the message directly).

Decoders can be added *dynamically*, i.e. the main process does not need to be stopped for additional decoders 
to be added. This is to support a typical IoT environment where new sensor types are added to the network 
with a data format not compatible with existing decoders for that network.

In part we are compensating for limitations in the TTN (The Things Network) decoder support, where a destination
'application' is limited to a single Javascript 'decode' function which becomes unwieldy when multiple sensor types are
to be supported.

## Install

```
git clone https://github.com/ijl20/python_decoders
cd python_decoders
pip -m venv venv
pip install -r requirements.txt
```

## Typical use case

When LoraWAN sensor data arrives that the TTN network server (The Things Network), TTN will package the sensor data
into a JsonObject, with the actual data bytes base64-encoded in a `payload_raw` property. `python_decoders` will
subscribe to these messages, pass the full message to each decoder in the 'decoders' directory, and *one* decoder will
interpret the `payload_raw` property and return a new JsonObject with the data from that property transformed into
more easily usable (and readable) Json properties.
