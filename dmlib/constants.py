###########################################################################
# Copyright (c) 2011-2014 Unixmedia S.r.l. <info@unixmedia.it>
# Copyright (c) 2011-2014 Franco (nextime) Lanza <franco@unixmedia.it>
#
# Domotika System Controller Daemon "domotikad"  [http://trac.unixmedia.it]
#
# This file is part of domotikad.
#
# domotikad is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#=at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

UDP_IKA_PORT=12080
UDP_IKA_VERSION=1
IKAP_STARTBYTE=0xa5

IKAP_BROADCAST="\0\0\0\0"

# Encoding types
IKAP_ENC_CLEAR=0x00
IKAP_ENC_XTEA=0x01
IKAP_ENC_XTEA_CBC=0x02
IKAP_ENC_XXTEA=0x03
IKAP_ENC_ARCFOUR=0x04
IKAP_ENC_AES128=0x05
IKAP_ENC_AES256=0x06

# Message Type
IKAP_MSG_NULL=0x00
IKAP_MSG_REQUEST=0x01
IKAP_MSG_ACTION=0x02
IKAP_MSG_ACK=0x03
IKAP_MSG_NOTIFY=0x04
IKAP_MSG_NOTIFYCONF=0x05
IKAP_MSG_REQUESTCONF=0x06
IKAP_MSG_SETCONF=0x07
IKAP_MSG_DEBUG=0xff

# Context
IKAP_CTX_NULL=0x0000
IKAP_CTX_LIGHT=0x0001
IKAP_CTX_SOCKET=0x0002
IKAP_CTX_BLIND=0x0003
IKAP_CTX_SENSOR=0x0004
IKAP_CTX_DOOR=0x0005
IKAP_CTX_WINDOW=0x0006
IKAP_CTX_VALVE=0x0007
IKAP_CTX_STATUS=0x0008
IKAP_CTX_SCENARY=0x0009
IKAP_CTX_ALARM=0x000a
IKAP_CTX_CITOPHONE=0x000b
IKAP_CTX_GENERIC_SWITCH=0x000c
IKAP_CTX_TERMOSTAT=0x000d
IKAP_CTX_GATE=0x000e
IKAP_CTX_AUDIO=0x000f
IKAP_CTX_VIDEO=0x0010
IKAP_CTX_PHONE=0x0011
IKAP_CTX_TV=0x0012
IKAP_CTX_IRRIGATION=0x0013
IKAP_CTX_TIMER=0x0014
IKAP_CTX_INTERNET=0x0015
IKAP_CTX_MESSAGE=0x0016
IKAP_CTX_RFID=0x0017
IKAP_CTX_PUMP=0x0018
IKAP_CTX_MOTOR=0x0019
IKAP_CTX_TENT=0x01a
IKAP_CTX_RTC=0x0020
IKAP_CTX_SEQUENCE=0x0021
IKAP_CTX_SYSTEM=0xfffe
IKAP_CTX_USER=0xffff

SECTIONS={
   IKAP_CTX_NULL: "none",
   IKAP_CTX_LIGHT: "light",
   IKAP_CTX_SOCKET: "socket",
   IKAP_CTX_BLIND: "blind",
   IKAP_CTX_SENSOR: "sensor",
   IKAP_CTX_DOOR: "door",
   IKAP_CTX_WINDOW: "finestra",
   IKAP_CTX_VALVE: "valvle",
   IKAP_CTX_STATUS: "stato",
   IKAP_CTX_SCENARY: "scenario",
   IKAP_CTX_ALARM: "allarme",
   IKAP_CTX_CITOPHONE: "citofono",
   IKAP_CTX_GENERIC_SWITCH: "accensione",
   IKAP_CTX_TERMOSTAT: "clima",
   IKAP_CTX_GATE: "cancello",
   IKAP_CTX_AUDIO: "audio",
   IKAP_CTX_VIDEO: "video",
   IKAP_CTX_PHONE: "telefonia",
   IKAP_CTX_TV: "tv",
   IKAP_CTX_IRRIGATION: "irrigazione",
   IKAP_CTX_TIMER: "timer",
   IKAP_CTX_INTERNET: "network",
   IKAP_CTX_MESSAGE: "messaggio",
   IKAP_CTX_RFID: "rfid",
   IKAP_CTX_PUMP: "pompa",
   IKAP_CTX_MOTOR: "motore",
   IKAP_CTX_TENT: "tenda",
   IKAP_CTX_RTC: "dataora",
   IKAP_CTX_SEQUENCE: "sequenza",
   IKAP_CTX_SYSTEM: "sistema",
   IKAP_CTX_USER: "user"
}

#Actions
IKAP_ACT_NULL=0x00
IKAP_ACT_ON=0x01
IKAP_ACT_OFF=0x02
IKAP_ACT_CHANGE=0x03
IKAP_ACT_OPEN=0x04
IKAP_ACT_CLOSE=0x05
IKAP_ACT_UP=0x06
IKAP_ACT_DOWN=0x07
IKAP_ACT_STOP=0x08
IKAP_ACT_START=0x09
IKAP_ACT_STOPTIMERED=0x0a
IKAP_ACT_STARTTIMERED=0x0b
IKAP_ACT_BLOCKUNBLOCK=0x0c
IKAP_ACT_BLOCK=0x0d
IKAP_ACT_UNBLOCK=0x0e
IKAP_ACT_HI=0x0f
IKAP_ACT_LOW=0x10
IKAP_ACT_EQUAL=0x11
IKAP_ACT_EXPIRED=0x12
IKAP_ACT_TIMEDOUT=0x13
IKAP_ACT_CHANGED=0x14
IKAP_ACT_SWITCHEDON=0x15
IKAP_ACT_SWITCHEDOFF=0x16
IKAP_ACT_CALL=0x17
IKAP_ACT_ANSWER=0x18
IKAP_ACT_RING=0x19
IKAP_ACT_PLAY=0x1a
IKAP_ACT_PAUSE=0x1b
IKAP_ACT_PAUSE_CLOSING=0x1c
IKAP_ACT_PAUSE_OPENING=0x1d
IKAP_ACT_NEXT=0x1e
IKAP_ACT_CLOSING=0x1f
IKAP_ACT_OPENING=0x20
IKAP_ACT_ASK=0x21
IKAP_ACT_BOARD=0xfd
IKAP_ACT_DEBUG=0xff

DM_OUTPUT_TYPE_NULL=0x00
DM_OUTPUT_TYPE_ONOFF=0x01
DM_OUTPUT_TYPE_IMPULSO=0x02
DM_OUTPUT_TYPE_TEMPORIZZATA=0x03
DM_OUTPUT_TYPE_INTERMITTENTE=0x04
DM_OUTPUT_TYPE_INTERMITTENTE_TEMPORIZZATA=0x05
DM_OUTPUT_TYPE_SIGNALING=0x06
DM_OUTPUT_TYPE_PWM=0x07
DM_OUTPUT_TYPE_DIMMER=0x08
DM_OUTPUT_TYPE_2_RELAY_EXCLUSIVE=0xf0
DM_OUTPUT_TYPE_2_RELAY_INCLUSIVE_ON=0xf1
DM_OUTPUT_TYPE_2_RELAY_INCLUSIVE_OFF=0xf2
DM_OUTPUT_TYPE_2_RELAY_ALTERNATE_SEQ=0xf3
DM_OUTPUT_TYPE_OPEN_CLOSE_2_RELAYS=0xf4
DM_OUTPUT_TYPE_RGB=0xfa
DM_OUTPUT_TYPE_SEQUENZA=0xff

RELAY_ACT={
         0: "OPEN",
         1: "CLOSE",
         2: "CHANGE"
      }

SEQUENCE_TYPE_NULL=0x00
SEQUENCE_TYPE_CONTINUE=0x01
SEQUENCE_TYPE_RANDOM=0x02
SEQUENCE_TYPE_CYCLE=0x03
SEQUENCE_TYPE_CONTINUE_RANDOM=0x04
SEQUENCE_TYPE_CYCLE_RANDOM=0x05

VIDEO_TYPE_NULL=0x00
VIDEO_TYPE_IPCAM=0x01

# BYTE ORDER!
MOTION_STATUS_START=0x01
MOTION_STATUS_UPDATE=0x02
MOTION_STATUS_STOP=0x04
MOTION_STATUS_ALL=0xff

MOTION_TYPE_MOTION=0x01

DM_INPUT_TYPE_DIGITAL=0xff
DM_INPUT_TYPE_ANALOG=0x00

DM_ARGTYPE_NULL=0x00
DM_ARGTYPE_RGB_TRANSITION=0x01
DM_ARGTYPE_PRESET=0x02
DM_ARGTYPE_DIMMER=0x03

DM_DIGITAL_INPUT_TYPE_NULL=0x00
DM_DIGITAL_INPUT_TYPE_SINGLECLICK=0x01
DM_DIGITAL_INPUT_TYPE_LONG=0x02
DM_DIGITAL_INPUT_TYPE_CHANGE=0x03
DM_DIGITAL_INPUT_TYPE_CONTINUOS_OPEN=0x04
DM_DIGITAL_INPUT_TYPE_CONTINUOS_CLOSE=0x05
DM_DIGITAL_INPUT_TYPE_PULSE_OPEN=0x90
DM_DIGITAL_INPUT_TYPE_PULSE_OPEN_COUNT=0x91
DM_DIGITAL_INPUT_TYPE_PULSE_CLOSE=0x92
DM_DIGITAL_INPUT_TYPE_PULSE_CLOSE_COUNT=0x93
DM_DIGITAL_INPUT_TYPE_PULSE_CHANGE=0x94
DM_DIGITAL_INPUT_TYPE_PULSE_CHANGE_COUNT=0x95
DM_DIGITAL_INPUT_TYPE_DOUBLECLICK=0xa0
DM_DIGITAL_INPUT_TYPE_SINGLE_AND_LONG=0xa1
DM_DIGITAL_INPUT_TYPE_CLICK_AND_CONTINUOS_CLOSE=0xa2
DM_DIGITAL_INPUT_TYPE_OPENCLOSE=0xa3
DM_DIGITAL_INPUT_TYPE_CONTINUOS_OPENCLOSE=0xa4
DM_DIGITAL_INPUT_TYPE_SEQUENCE2=0xb0
DM_DIGITAL_INPUT_TYPE_SEQUENCE2STEP=0xb1
DM_DIGITAL_INPUT_TYPE_PULSE_OPEN_DOUBLE=0xc0
DM_DIGITAL_INPUT_TYPE_PULSE_CLOSE_DOUBLE=0xc1
DM_DIGITAL_INPUT_TYPE_PULSE_CHANGE_DOUBLE=0xc2
DM_DIGITAL_INPUT_TYPE_TRIPLE=0xd0
DM_DIGITAL_INPUT_TYPE_SEQUENCE3=0xe0

DM_ANALOG_INPUT_TYPE_NULL=0x00
DM_ANALOG_INPUT_TYPE_GENERIC=0x01
DM_ANALOG_INPUT_TYPE_TEMPERATURE=0x02
DM_ANALOG_INPUT_TYPE_HUMIDITY=0x03
DM_ANALOG_INPUT_TYPE_CURRENT=0x04
DM_ANALOG_INPUT_TYPE_WIND=0x05
DM_ANALOG_INPUT_TYPE_SPEED=0x06
DM_ANALOG_INPUT_TYPE_PRESSURE=0x07
DM_ANALOG_INPUT_TYPE_FLUX=0x08
DM_ANALOG_INPUT_TYPE_LIGHT=0x09
DM_ANALOG_INPUT_TYPE_LEVEL=0x0a


BOARD_MODULE_NONE=0x00
BOARD_MODULE_97j60=0x01
BOARD_MODULE_67j60M=0x02
BOARD_MODULE_67j60S=0x03
BOARD_MODULE_67j60_Wifi=0x04
BOARD_MODULE_97j60_Wifi=0x05
BOARD_MODULE_2620=0x06
BOARD_MODULE_2685=0x07

BOARD_WORKER_12R12I_v1=0x0001
BOARD_WORKER_12R12I_v3=0x0002
BOARD_WORKER_RFID=0x0003
BOARD_WORKER_DIMMER=0x0004
BOARD_WORKER_SENSORS=0x0005
BOARD_WORKER_GW=0x0006
BOARD_WORKER_RGBLED=0x0007
BOARD_WORKER_DMSNT84=0x0008
BOARD_WORKER_RGBLED4=0x0009

FWTYPE_IRRIGAZIONE=0x01
FWTYPE_RELAYMASTER=0x02
FWTYPE_CANCELLI=0x03
FWTYPE_1TO1=0x04
FWTYPE_ALARM=0x05
FWTYPE_LIGHT=0x06
FWTYPE_TAPPARELLE=0x07
FWTYPE_DMLED=0x08
FWTYPE_DMLED4=0x09
FWTYPE_DMDIM=0x0a
FWTYPE_RELAYMASTERANA=0x0b
FWTYPE_TESTDMR3=0xff

