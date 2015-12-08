# BOT-Whatsapp

Aplicación basada en [Yowsup](https://github.com/tgalal/yowsup/blob/master/README.md)
Mini Robot que responde a ciertos comandos enviados por Whatsapps a un numero configurado con Yowsup.

# Funcionalidades

En general el Robot tiene el siguiente funcionamiento:

```
!comando argumento
```

##Comandos
```
!bip numero_tarjeta => Consulta el saldo de una tarjeta !Bip
!sismo => Consulta los ultimos 8 sismo de Chile
!hora => Hora actual en Chile
!version => Muestra la version
!USD valor => Convierte el valor dolar a pesos chilenos (CLP) (Ej. !USD 1)
!UF valor => Convierte el valor UF a pesos chilenos (CLP) (Ej. !UF 1
!chiste = > Recibe un chiste random
```
##Clima

Si se envía la posición de GPS responde con la temperatura actual del lugar según la geolocalizacion

#Deploy

En Distribuciones basadas en Debian:

```
aptitude install python-dev python-pip libjpeg-dev zlib1g-dev libpng12-dev --without-recommends
```

Clonar Repositorio de Yowsup y seguir las instrucciones de para registrar un numero telefónico
```
git clone https://github.com/tgalal/yowsup
python yowsup/yowsup/setup.py install
```
Clonar Repositorio
```
git clone https://github.com/yasserisa/BOT-Whatsapp
```
Setear el archivo config.py basado en el config.py.template

## Ejecucción
```
python run.py
```

## Background

Recomiendo [Supervisor](http://supervisord.org/)
