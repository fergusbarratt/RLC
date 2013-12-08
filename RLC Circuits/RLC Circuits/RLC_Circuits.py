import math
def frange(x, y, jump):
  while x < y:
    yield x
    x += jump
def scexp(num, exp):
    if exp == "m":
        exp = -3
    elif exp == "mu":
        exp = -6
    elif exp == "n":
        exp = -9
    elif exp == "p":
        exp = -12
    elif exp == "K":
        exp = 3
    elif exp == "M":
        exp = 6
    elif exp == "G":
        exp = 9
    elif exp == "T":
        exp = 12
    return num*10**exp
def is_within(updown, testnum, num):
    if testnum>(num-updown) and testnum<(num+updown):
        return True
    else:
        return False
class DivError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class RLC():
    def __init__(self, R, L, C, f=0, V=0, angle_type = "radians", angular_freq_given = False, rms_given = True):
        if not angular_freq_given:
            self.f = 2*math.pi*f
        else:
            self.f = f
        if not rms_given:
            self.V = V*(1/math.sqrt(2))
        else:
            self.V = V
        self.L = L
        self.C = C
        self.R = R
        if f and V:
            self.power_init(angle_type)
    def power_init(self, angle_type = "radians"):
        try:
            self.imXc = -1/(self.f*self.C)
            self.imXl = self.f*self.L
            self.total_impedance =  math.sqrt(self.R**2+(self.imXc+self.imXl)**2)
            reals = self.R
            ims = self.imXc+self.imXl
            self.I = self.V/self.total_impedance
            self.power_factor = math.cos(math.atan(ims/reals))
            self.I_lags_V = math.degrees(math.acos(self.power_factor)) if angle_type == "degrees" else math.acos(self.power_factor)
            self.rmspower = self.I*self.V*self.power_factor
        except ZeroDivisionError:
            raise(DivError)
            print "f not yet initialised"
    def resonant_frequency(self, angular = True):
        if angular == True:
            return (1/math.sqrt(self.L*self.C))/(2*math.pi)
        else:
            return 1/math.sqrt(self.L*self.C)
    def voltage_across(self, comp):
        if comp == "Array" or "array":
            return {"R":self.I*self.R, "L":self.I*self.imXl, "C":self.I*self.imXc}
        if comp == "R" or comp == "r":
            return self.I*self.R
        if comp == "C" or comp == "c":
            return self.I*self.imXc
        if comp == "L" or comp == "l":
            return self.I*self.imXl
    def f_such_that_phase(self, phase, angle_type = "degrees", prec = 1):
        for i in range(1, 10000):
            self.f = i
            #initialise the power variables for each value of f
            self.power_init("degrees")
            if not i%50:
                print self.I_lags_V
            #if phase in interval 2 either side of I_lags_V
            if is_within(2, self.I_lags_V, phase):
                return self.f
            if i == 9999:
                print i, self.f
                print self.I_lags_V, phase
                break
        return "fail"

        
a = RLC(50, scexp(30, -3), scexp(60, -6), 60, 120)
b = RLC(40, scexp(20, "m"), scexp(60, "mu"))

