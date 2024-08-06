import uuid
from datetime import datetime


# creating DB schemas in class format

class Vehicle:
    def __init__(self, license_plate, size, reserved=False):
        self.license_plate = license_plate
        self.size = size
        self.reserved = reserved
        self.arrival_time = datetime.now()


class ParkingSpot:

    def __init__(self, spot_id, size, zone):
        self.vehicle = None
        self.is_occupied = False
        self.spot_id = spot_id
        self.size = size
        self.zone = zone

    def assign_vehicle(self, vehicle):
        self.is_occupied = True
        self.vehicle = vehicle

    def remove_vehicle(self):
        self.is_occupied = False
        self.vehicle = None


class Reservation:
    def __init__(self, reservation_id, vehicle, spot, start_time, end_time):
        self.reservation_id = reservation_id
        self.vehicle = vehicle
        self.spot = spot
        self.start_time = start_time
        self.end_time = end_time
        self.is_active = True


class Payment:
    def __init__(self, rate_per_hour):
        self.rate_per_hour = rate_per_hour
        self.invoice = None

    def calculate_fee(self, duration_hours, zone):
        rate = self.rate_per_hour
        if zone == 'VIP':
            rate *= 1.5
        elif zone == 'Handicap':
            rate *= 0.5
        return duration_hours * rate


class ParkingLot:
    def __init__(self, spots):
        self.spots = spots
        self.vehicles = {}
        self.reservations = {}
        self.payment_system = Payment(rate_per_hour=5)

    def check_in(self, vehicle, reservations):
        reservation = self.check_reservation_for_vehicle(vehicle, reservations)
        if reservation:
            if reservation.is_active:
                spot = reservation.spot
            else:
                return False
        else:
            spot = self.find_available_spot(vehicle)

        if spot:
            spot.assign_vehicle(vehicle)
            self.vehicles[vehicle.license_plate] = spot
            return True
        return False

    def check_out(self, license_plate):
        spot = self.vehicles.pop(license_plate, None)
        if spot:
            duration = (datetime.now() - spot.vehicle.arrival_time).total_seconds() / 3600
            fee = self.payment_system.calculate_fee(duration, spot.zone)
            spot.remove_vehicle()
            return fee
        return None

    def check_reservation_for_vehicle(self, vehicle,  reservations):
        for reservation in reservations.values():
            if reservation.vehicle == vehicle:
                return reservation
        return None

    def find_available_spot(self, vehicle):
        for spot in self.spots:
            if not spot.is_occupied and self.can_fit(
                    vehicle.size, spot.size) and (vehicle.reserved or spot.zone != 'VIP'):
                return spot
        return None

    def can_fit(self, vehicle_size, spot_size):
        size_priority = {'small': 1, 'medium': 2, 'large': 3}
        return size_priority[vehicle_size] <= size_priority[spot_size]

    def reserve_spot(self, vehicle, start_time, end_time):
        spot = self.find_available_spot(vehicle)
        if spot:
            reservation_id = self.generate_id()
            reservation = Reservation(reservation_id, vehicle, spot, start_time, end_time)
            self.reservations[reservation_id] = reservation
            return reservation_id
        return None

    def generate_id(self):
        return uuid.uuid4()

    def get_available_spots(self):
        return len([spot for spot in self.spots if not spot.is_occupied])

    def get_zone_availability(self, zone):
        return len([spot for spot in self.spots if not spot.is_occupied and spot.zone == zone])
