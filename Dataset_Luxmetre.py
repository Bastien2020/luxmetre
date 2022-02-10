import serial
import time
from datetime import datetime
import io
import Function_Luxmetre as FL


# Acquisition des mesures d'éclairement

PC_activation = FL.mode_PC_activation()
rge = PC_activation[1]

# Enregistrement dans le fichier data4.csvde 100 mesures d'éclairement avec le format suivant
# [Timestamp, Mesure Eclairement])
file = open("data4.csv","w")
file.write("timestamp"+","+"Lux"+"\n")

# Enregistrement de 100 mesures dans le fichier data4.csv
compteur = 0
while 1:
    print(compteur)
    compteur += 1

    if compteur == 200:
        break

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    # Print the contents of the serial data
    try:
        output = FL.data_collect(rge)
        file.write(str(timestamp) + "," + output + "\n")
    except:
        pass

file.close()
