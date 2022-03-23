import lib.checkplate as plates
import lib.alpr as alpr

# plate = input('Plate: ')
# plates.notifyComputer(plates.verifyNumberPlate(plates.getDataFromNumberPlate(plate)))

print(alpr.getPlateFromImage('./images/test2.jpeg'))