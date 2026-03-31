from smarthouse.domain import SmartHouse, Aktuator, Sensor, KopleksDevice, Produktegenskap, Measurement

DEMO_HOUSE = SmartHouse()

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")

guestRoom1 = DEMO_HOUSE.register_room(ground_floor,8, "Guest Room")
bathRoom1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom 1")
livingRoom = DEMO_HOUSE.register_room(ground_floor, 39.75, "LivingRoom / Kitchen")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")

second_floor = DEMO_HOUSE.register_floor(2)
hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
guestRoom2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest Room 2")
masterBedroom = DEMO_HOUSE.register_room(second_floor, 17, "Master Bedroom")
dressingRoom = DEMO_HOUSE.register_room(second_floor, 4, "Dressing Room")
guestRoom3 = DEMO_HOUSE.register_room(second_floor, 10, "Guest Room 3")
office = DEMO_HOUSE.register_room(second_floor,11.75,"Office")
bathroom2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")

smartLook = DEMO_HOUSE.register_device(entrance, Aktuator("4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", Produktegenskap("MythicalTech","Guardian Lock 7000","Smart Lock")))
co2Sensor = DEMO_HOUSE.register_device(livingRoom, Sensor("8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e",Produktegenskap("ElysianTech","Smoke Warden 1000","CO2 sensor")))
co2Sensor.addMeasurment(Measurement("2026-03-15T12:00:00+01:00",1098,'ppm'))
stromMaaler = DEMO_HOUSE.register_device(entrance, Sensor("a2f8690f-2b3a-43cd-90b8-9deea98b42a7",Produktegenskap("MysticEnergy Innovations","Volt Watch Elite","Electricity Meter")))
stromMaaler.addMeasurment(Measurement("2026-03-15T12:00:00+01:00", 98, 'W'))
heatPump = DEMO_HOUSE.register_device(livingRoom, Aktuator("5e13cabc-5c58-4bb3-82a2-3039e4480a6d",Produktegenskap("ElysianTech","Thermo Smart 6000","Heat Pump")))
motrionSensor = DEMO_HOUSE.register_device(livingRoom, Sensor("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5",Produktegenskap("NebulaGuard Innovations","MoveZ Detect 69","Motion Sensor")))
motrionSensor.addMeasurment(Measurement("2026-03-15T12:00:00+01:00", True, 'bevegelse'))
fuktSensor = DEMO_HOUSE.register_device(bathRoom1, Sensor("3d87e5c0-8716-4b0b-9c67-087eaaed7b45",Produktegenskap("AetherCorp","Aqua Alert 800","Humidity Sensor")))
fuktSensor.addMeasurment(Measurement("2026-03-15T12:00:00+01:00",42,'%'))
oven1 = DEMO_HOUSE.register_device(guestRoom1,Aktuator("8d4e4c98-21a9-4d1e-bf18-523285ad90f6",Produktegenskap("AetherCorp","Pheonix HEAT 333","Smart Oven")))
garageDoor = DEMO_HOUSE.register_device(garage,Aktuator("9a54c1ec-0cb5-45a7-b20d-2a7349f1b132",Produktegenskap("MythicalTech","Guardian Lock 9000","Automatic Garage Door")))
oven2 = DEMO_HOUSE.register_device(masterBedroom,Aktuator("c1e8fa9c-4b8d-487a-a1a5-2b148ee9d2d1",Produktegenskap("IgnisTech Solutions","Ember Heat 3000","Smart Oven")))
tempSensor = DEMO_HOUSE.register_device(masterBedroom,Sensor("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e",Produktegenskap("AetherCorp","SmartTemp 42","Temperature Sensor")))
tempSensor.addMeasurment(Measurement("2026-03-15T12:00:00+01:00", 21.2, '°C'))
airQual = DEMO_HOUSE.register_device(guestRoom3,Sensor("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c",Produktegenskap("CelestialSense Technologies","AeroGuard Pro","Air Quality Sensor")))
airQual.addMeasurment(Measurement("2026-03-15T12:00:00+01:00", 9, 'PM2'))
plug = DEMO_HOUSE.register_device(office,Aktuator("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79",Produktegenskap("MysticEnergy Innovations","FlowState X","Smart Plug")))
dehumidi = DEMO_HOUSE.register_device(bathroom2,Aktuator("9e5b8274-4e77-4e4e-80d2-b40d648ea02a",Produktegenskap("ArcaneTech Solutions","Volt Watch Elite","Dehumidifier")))
bulb = DEMO_HOUSE.register_device(guestRoom2,Aktuator("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28",Produktegenskap("Elysian Tech","Lumina Glow 4000","Light Bulp")))


# TODO: continue registering the remaining floor, rooms and devices

