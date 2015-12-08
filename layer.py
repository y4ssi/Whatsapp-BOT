# -*- coding: utf-8 -*-
import re
import requests
import datetime
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_media.protocolentities import *
import config

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
        if True:
            if messageProtocolEntity.getType() == 'media':
                if messageProtocolEntity.getMediaType() == "location":
                    # Log
                    file = open("/var/log/yowsup/log.txt", "a")
                    file.write(messageProtocolEntity.getFrom() + " " + messageProtocolEntity.getLatitude() + ":" + messageProtocolEntity.getLongitude() + "\n")
                    file.close()
                    receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(),
                                                            messageProtocolEntity.getFrom(),
                                                            'read',
                                                            messageProtocolEntity.getParticipant())
                    # Temperatura
                    lat = messageProtocolEntity.getLatitude()
                    lon = messageProtocolEntity.getLongitude()
                    respuesta = requests.get(("http://api.openweathermap.org"
                                              "/data/2.5/weather?lat=%s&lon=%s&"
                                              "APPID=" + config.weather + "&"
                                              "units=metric") % (lat, lon))
                    respuesta = str(respuesta.json()["main"]["temp"])

                    outgoingMessageProtocolEntity = TextMessageProtocolEntity("Hay "+respuesta+"ºC donde te encuentras" ,
                                                                              to = messageProtocolEntity.getFrom())
                    self.toLower(receipt)
                    self.toLower(outgoingMessageProtocolEntity)

            else:
                receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(),
                                                        messageProtocolEntity.getFrom(),
                                                        'read',
                                                        messageProtocolEntity.getParticipant())
                # Log
                file = open("/var/log/yowsup/log.txt", "a")
                file.write(messageProtocolEntity.getFrom() + " " + messageProtocolEntity.getBody() + "\n")
                file.close()
                # Robot
                mensaje = messageProtocolEntity.getBody()
                mensaje_lista = mensaje.split()
                # Saldo BIP
                if mensaje_lista[0] == "!bip":
                    try:
                        int(str(mensaje_lista[1]))
                        respuesta = requests.get(("http://saldobip.yasserisa.com"
                                                  "/v1/tarjetas/%s/saldo")
                                                 % (mensaje_lista[1]))
                        respuesta = respuesta.text
                    except:
                        respuesta = "Ingrese número de tarjeta"
                # Sismo
                elif mensaje == "!sismo":
                    respuesta = requests.get("http://sismo.yasserisa.com/v1/sismos")
                    respuesta = respuesta.text
                # Info
                elif mensaje == "!version":
                    respuesta = {"Creado por": "Yasser Isa",
                                 "Version": "Beta V0.1"}
                    respuesta = str(respuesta)
                elif mensaje == "!hora":
                    respuesta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " UTC-3"
                # Algún mensaje
                elif mensaje == "Hola":
                    respuesta = "Hola +" + messageProtocolEntity.getFrom(False)
                # Dolar a CLP
                elif mensaje_lista[0] == "!USD":
                    respuesta = requests.get(("https://www.google.com/finance/"
                                              "converter?a=%s&from=USD&to=CLP")
                                             % (mensaje_lista[1]))
                    resultado = re.findall('<span class=bld>(.*?)</span>',
                                           respuesta.text, re.DOTALL)
                    respuesta = resultado[0]
                # UF a CLP
                elif mensaje_lista[0] == "!UF":
                    respuesta = requests.get(("https://www.google.com/finance/"
                                              "converter?a=%s&from=CLF&to=CLP")
                                             % (mensaje_lista[1]))
                    resultado = re.findall('<span class=bld>(.*?)</span>',
                                           respuesta.text, re.DOTALL)
                    respuesta = resultado[0]
                # Chiste
                elif mensaje == "!chiste":
                    respuesta = requests.get("http://www.chistescortos.eu/random")
                    respuesta = str(re.findall(('class="oldlink">(.*?)</a>'), respuesta.text, re.DOTALL)[0].replace("<br />", "\n").strip('\n'))
                    respuesta = unicode(respuesta)
                # Respuesta Genérica
                else:
                    respuesta = "Podrias expresarte mejor"
                outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                    respuesta,
                    to=messageProtocolEntity.getFrom())
                self.toLower(receipt)
                self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(),
                                        "receipt",
                                        entity.getType(), entity.getFrom())
        self.toLower(ack)


