import lib.checkplate as plates

plate = input('Enter Plate: ')
# plates.notifyComputer(plates.verifyNumberPlate(plates.getDataFromNumberPlate(plate)))
print(plates.verifyNumberPlate(plates.getDataFromNumberPlate(plate)))
