class TruckProblem:
    def __init__(self, f_curr=0, pos=0, f_max=3, n=5, base_fuel_used=0):
        self.f_curr = f_curr
        self.pos = pos
        self.f_max = f_max
        self.n = n
        self.camp_dumps = [0] * n
        self.base_camp_fuel_used = base_fuel_used
        self.base_fuel_log = []
        self.camp_dump_log = []

    def refill(self, amt_of_fuel=1):
        if self.f_curr == self.f_max:
            return 0
        if self.pos == 0:
            self.base_camp_fuel_used += self.f_max - self.f_curr
            self.f_curr = self.f_max
            self.base_fuel_log.append(self.base_camp_fuel_used)
        else:
            if self.camp_dumps[self.pos - 1] == 0:
                return 0
            self.f_curr += amt_of_fuel
            assert self.f_curr <= self.f_max
            self.camp_dumps[self.pos - 1] -= amt_of_fuel
            assert self.camp_dumps[self.pos - 1] >= 0

    def move_one_right(self):
        if self.pos == self.n:
            return 0
        if self.f_curr == 0:
            raise ValueError("Truck is empty")
        self.f_curr -= 1
        self.pos += 1

    def move_one_left(self):
        if self.pos == 0:
            return 0
        if self.f_curr == 0:
            raise ValueError("Truck is empty")
        self.f_curr -= 1
        self.pos -= 1

    def unload(self, amt_of_fuel):
        if self.f_curr == 0:
            return 0
        self.f_curr -= amt_of_fuel
        self.camp_dumps[self.pos - 1] += amt_of_fuel

    def final_trip(self):
        self.refill()
        while self.pos < self.n:
            self.move_one_right()
            self.refill(1)
        print("Units of fuel used from the base camp to reach target camp",
              ":", self.base_camp_fuel_used)

    def store_one_at(self, destination_camp):
        if destination_camp == 1:
            self.refill()
            self.move_one_right()
            self.unload(1)
            self.move_one_left()
            self.camp_dump_log.append(self.camp_dumps)
            return 0
        destination_camp_idx = destination_camp - 1

        for idx in range(destination_camp_idx):
            if self.camp_dumps[destination_camp_idx - idx-1] < 2:
                while self.camp_dumps[destination_camp_idx - idx-1] < 2:
                    self.store_one_at(destination_camp - idx - 1)

        if destination_camp != 1:
            while self.pos < destination_camp:
                self.refill()
                self.move_one_right()
            self.unload(1)
            while self.pos > 0:
                self.move_one_left()
                self.refill()
            self.camp_dump_log.append(self.camp_dumps)


num_camps = int(
    input("Enter the number of fuel camps including the target camp : ")
)
fuel_cap = 3
truck_obj = TruckProblem(0, 0, fuel_cap, num_camps, 0)
store_target = truck_obj.n - truck_obj.f_max
for i in range(store_target):
    truck_obj.store_one_at(store_target-i)
truck_obj.final_trip()
