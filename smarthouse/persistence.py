import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Sensor, Actuator, KompleksDevice, Produktegenskap, Device
from datetime import datetime as dt
from datetime import timedelta as td

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file 
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        # TODO: START here! remove the following stub implementation and implement this function 
        #       by retrieving the data from the database via SQL `SELECT` statements.
        STORED_HOUSE = SmartHouse()
        floors = []
        rooms = []
        devices = {}
        produkt = {}

        res = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY LENGTH(name);")
        table = res.fetchall()
        
        for name in table:
            res = self.conn.execute(f"SELECT * FROM {name[0]}")
            info = res.fetchall()
            if name[0] == 'rooms':
                for room in info:
                    if not any(floor[0] == room[1] for floor in floors): 
                        floor = STORED_HOUSE.register_floor(room[1])
                        oneRoom = STORED_HOUSE.register_room(floor, room[2], room[3])
                        floors.append((room[1], floor))
                        rooms.append((room[0], oneRoom))
                    else:
                        for floor in floors:
                            if floor[0] == room[1]:
                                oneRoom = STORED_HOUSE.register_room(floor[1], room[2], room[3])
                                rooms.append((room[0], oneRoom))

            elif name[0] == 'devices':
                for device in info:
                    res = self.conn.execute("""select m.unit
                        FROM devices d 
                        join measurements m 
                        on d.id = m.device 
                        where d.id = ?""", (device[0],))
                    unit = res.fetchone()
                    produkt[device[5]] = Produktegenskap(device[4],device[5], device[2])
                    if device[3] == 'sensor':
                        devices[device[0]] = (Sensor(device[0], produkt[device[5]]))    
                    elif device[3] == 'actuator':
                        if unit is None:
                            devices[device[0]] = (Actuator(device[0], produkt[device[5]]))
                        else:
                            devices[device[0]] = (KompleksDevice(device[0],produkt[device[5]]))
                    
                    for room in rooms:
                        if room[0] == device[1]:
                            room[1].addDevice(devices[device[0]])
                            break

            elif name[0] == 'measurements':
                for measurment in info:
                    devices[measurment[0]].addMeasurement(Measurement(measurment[1],measurment[2],measurment[3]))
            elif name[0] == 'actuatorState':
                for state in info:
                    if bool(state[1]):
                        devices[state[0]].turn_on()
                    else:
                        devices[state[0]].turn_off()


            
        #TODO FUJSE
        return STORED_HOUSE


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here
        if isinstance(sensor, Device):
            id = sensor.id

        res = self.conn.execute("select value FROM measurements m WHERE device = ? ORDER BY ts DESC LIMIT 1;",(id,))
        reading = res.fetchone()
        if reading:
            verdi = reading[0]
        else:
            verdi = None
        return verdi


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.

        res = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND lower(name) = 'actuator';")
        if res.fetchone() is None:
            self.conn.execute("""
                CREATE TABLE actuatorState(
                    device text not null,
                    state int not null,
                    foreign key (device) references  devices(id)
                    )""")
        res = self.conn.execute("SELECT state FROM actuatorState where device = ?", (actuator.id,))
        state = res.fetchone()
        if state is None:
            self.conn.execute("INSERT INTO actuatorState (device, state) VALUES (?,?)",(actuator.id, actuator.state))
        else:
            self.conn.execute("UPDATE actuatorState set state = ? where device = ?", (actuator.state, actuator.id))
        self.conn.commit()

    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        # TODO: This and the following statistic method are a bit more challenging. Try to desfign the respective 
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.  
        if from_date is not None:
            start_date = dt.strptime(from_date, '%Y-%m-%d').date()
        else:
            res = self.conn.execute("""
                    SELECT MIN(ts)
                    FROM measurements m
                    JOIN devices d ON m.device = d.id
                    JOIN rooms r ON r.id  = d.room 
                    WHERE m.unit like '%C'
                    AND lower(r.name) = ?""", (room.name.lower(),))
            
            resDate = res.fetchone()
            start_date = dt.strptime(resDate[0], '%Y-%m-%d %H:%M:%S').date()
        
        if until_date is not None:
            end_date = dt.strptime(until_date, '%Y-%m-%d').date()
        else:
            res = self.conn.execute("""
                    SELECT MAX(ts)
                    FROM measurements m
                    JOIN devices d ON m.device = d.id
                    JOIN rooms r ON r.id  = d.room 
                    WHERE m.unit like '%C'
                    AND lower(r.name) = ?""", (room.name.lower(),))
            
            resDate = res.fetchone()
            end_date = dt.strptime(resDate[0], '%Y-%m-%d %H:%M:%S').date()

        dateAndValue = dict()
        while start_date <= end_date:
            res = self.conn.execute("""
                SELECT avg(m.value)
                FROM measurements m
                JOIN devices d ON m.device = d.id
                JOIN rooms r ON r.id  = d.room 
                WHERE m.unit like '%C'
                AND lower(r.name) = ?
                AND m.ts like ? """,(room.name.lower(),start_date + '%'))
            dateAndValue[start_date] = res.fetchone()[0]
            start_date += td(days=1)
        return dateAndValue

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        hours = []
        dato = dt.strptime(date, '%Y-%m-%d').date()
        date_whole = dato.strftime('%Y-%m-%d') + '%'
        
        #for i in range(0,24):
         #date_hour = dato.replace(hour=i).strftime('%Y-%m-%d %H') + '%' 
        res = self.conn.execute("""
            SELECT strftime('%H', m.ts) as hour, COUNT(*) as count
            FROM measurements m
            JOIN devices d ON m.device = d.id
            JOIN rooms r ON r.id  = d.room
            WHERE m.unit = '%'
            AND lower(r.name) = lower(?)
            AND m.ts like ?
            AND m.value > (SELECT avg(value)as v
                            FROM measurements m
                            JOIN devices d ON m.device = d.id
                            JOIN rooms r ON r.id  = d.room 
                            WHERE m.unit = '%'
                            AND lower(r.name) = lower(?)
                            AND m.ts like ?)
            GROUP BY strftime('%H', m.ts)
                                """, (room.name, date_whole, room.name, date_whole))
        listValue = res.fetchall()
        for value in listValue:
            if value[1] > 3:
                hours.append(value[0])
            #hours.append(i)

        return NotImplemented

