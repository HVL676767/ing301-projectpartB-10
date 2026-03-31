from typing import List, Optional, Union

class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit



# TODO: Add your own classes here!

class Building:
    
    def __init__(self):
        self.floor = []
    
    def addFloor(self, floor: "Floor"): 
        self.floor.append(floor)

    def removeFloor(self, floor: "Floor"):
        if floor in self.floor:
            self.floor.remove(floor)

    def __repr__(self):
        return f"Bygg med {len(self.floor)}"

class Floor:
    
    def __init__(self, building: Building, etasje: int):
        self.etasje =  etasje
        self.building = building
        if any(f.etasje == etasje for f in building.floor):
            raise ValueError("Etasje finnes allerede")
        self.room = []
        self.building.addFloor(self)
    
    def __repr__(self):
        return f"Etasje {self.etasje}, building {self.building}, antallRom {len(self.room)}"

    def addRoom(self, room: "Room"):
        self.room.append(room)

    def removeRoom(self, room: "Room"):
        if room in self.room:
            self.room.remove(room)

    def totalAreal(self):
        areal = 0
        for room in self.room:
            areal = areal + room.areal
        return areal

class Room: 

    def __init__(self, floor: Floor, roomName: str,  roomAreal :float, device = None):
        self.floor = floor
        self.room_name = roomName
        self.areal = roomAreal

        if (device is None):
            self.devices = []        
        elif(type(device) == list):
            self.devices = device
        else:
            self.devices = [device]

        self.floor.addRoom(self)


    def changeRoomSize(self, newSize):
        self.areal = newSize

    def changeRoomName(self, newName):
        self.room_name = newName

    def addDevice(self, device : "Device"):
        self.devices.append(device)

    def removeDevice(self, device : "Device"):
        if device in self.devices:
            self.devices.remove(device)

    def __repr__(self):
        return f"Etasje {self.floor.etasje}, romNavn {self.room_name}, areal {self.areal}"
        
        


class Device:

    def __init__(self,id: str, produktegenskap: "Produktegenskap", huskenavn = None):
        self.id = id
        self.room = None
        self.produktegenskap = produktegenskap
        self.huskenavn = huskenavn
        # self.room.addDevice(self)


    def regRoom(self, room):
        if self.room is not None:
            self.room.removeDevice(self)
        self.room = room
        self.room.addDevice(self)

    def changeRoom(self, newRoom : "Room"):
        self.room.removeDevice(self)
        self.room = newRoom
        self.room.addDevice(self)   

    def is_actuator(self):
        return False

    def is_sensor(self):
        return False

    def get_device_type(self):
        return self.produktegenskap.device_type
    

class Produktegenskap:

    def __init__(self, supplier: str, model_name : str, device_type: str):
        self.supplier = supplier
        self.model_name  = model_name 
        self.device_type = device_type

class Actuator(Device):
    
    def __init__(self, id: str, produktegenskap: Produktegenskap, state = False, huskenavn = None):
        super().__init__(id, produktegenskap, huskenavn)
        self.state = state

    def is_actuator(self):
        return True
    def turn_on(self, targetValue = True):
        self.state = targetValue
    def turn_off(self):
        self.state = False
    def is_active(self):
        return bool(self.state)
    
        
class Sensor(Device):

    def __init__(self,  id: str,  produktegenskap: "Produktegenskap", huskenavn = None, measurement = 0):
        super().__init__(id, produktegenskap, huskenavn)
        self.measurements = [measurement]

    def is_sensor(self):
        return True
    
    def addMeasurement(self, measurement: Measurement):
        self.measurements.append(measurement)
    
    def last_measurement(self):
        return self.measurements[len(self.measurements)-1]
    
    def all_measurements(self):
        return self.measurements

class KompleksDevice(Device):

    @staticmethod
    def listTilTupleList(verdi):
        if verdi is None:
            liste = []
        elif type(verdi) == list:
            liste = []
            for enVerdi in verdi:
                if type(enVerdi) == tuple:
                    liste.append(enVerdi)
                else:
                    liste.append(('',enVerdi))
        elif type(verdi) == tuple:
            liste = [verdi]
        else:
            liste = [('', verdi)]
        return liste

    def __init__(self, id:str, produktegenskap:Produktegenskap, measurement: Optional[Measurement] = None, state = None, huskenavn: Optional[str] =None):
        super().__init__(id, produktegenskap, huskenavn)
        self.measurements = self.listTilTupleList(measurement)
        self.state = state
    
    def addMeasurement(self, measurement : Measurement, sensorType : Optional[str]):
        self.measurements.append((sensorType, measurement))

    def is_sensor(self):
        return bool(self.measurements)
    
    def is_actuator(self):
        return bool(self.state)
    
    def turn_on(self, targetValue = True):
        self.state = targetValue
    def turn_off(self):
        self.state = False
    def is_active(self):
        return self.state


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """
    def __init__(self):
        self.building = Building()    

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        for f in self.building.floor:
            if f.etasje == level:
                return f
        floor = Floor(self.building, level)
        return floor


    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(floor, room_name, room_size)
        return room

    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return self.building.floor #TODO Sortere


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        allRoom = []

        for floors in self.building.floor:
            allRoom = allRoom + floors.room

        return allRoom


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        areal = 0

        for floor in self.building.floor:
            areal = areal + floor.totalAreal()

        return areal


    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        device.regRoom(room)
        return device

    
    def get_devices(self):
        returnDevice = []
        for etasje in self.building.floor:
            for room in etasje.room:
                for device in room.devices:
                    returnDevice.append(device)

        return returnDevice

    def get_device_by_id(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        
        returnDevice = None

        for device in self.get_devices():
            if device.id == device_id:
                returnDevice = device
        
        return returnDevice
