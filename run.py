# -*- coding: utf-8 -*-
from yowsup.layers.axolotl import YowAxolotlLayer
from layer import EchoLayer
from yowsup.layers.auth import YowCryptLayer, YowAuthenticationProtocolLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.stanzaregulator import YowStanzaRegulator
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup import env
#
from yowsup.layers.protocol_media import YowMediaProtocolLayer
import config

# replace with your phone and password
CREDENTIALS = (config.numero, config.password)

if __name__ == "__main__":
    layers = (
            EchoLayer,
            (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer),#, YowMediaProtocolLayer),
            YowAxolotlLayer,
            YowCoderLayer,
            YowCryptLayer,
            YowStanzaRegulator,
            YowNetworkLayer
        )
    stack = YowStack(layers)
    # setting credentials
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)
    # whatsapp server address
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    # info about us as WhatsApp client
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())
    # sending the connect signal
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    # this is the program mainloop
    stack.loop()

