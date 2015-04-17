class PID:
    def __init__(self, P, I, D, Derivator=0, Integrator=0, Integrator_max=4, Integrator_min=-4):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min

        self.targetTemp = 0
        self.error=0.0

    def update(self, currentTemp, targetTemp):
        """
        Calculate PID output value for given reference input and feedback
        """
        self.targetTemp = targetTemp
        self.error = targetTemp - currentTemp

        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        if self.Integrator > self.Integrator_max:
        	self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
        	self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki

        output = self.P_value + self.I_value + self.D_value

        return(output)

    def setPoint(self,targetTemp):
        """
        Initilize the setpoint of PID
        """
        self.targetTemp = targetTemp
        self.Integrator=0
        self.Derivator=0

    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp=P

    def setKi(self,I):
        self.Ki=I

    def setKd(self,D):
        self.Kd=D

    def getPoint(self):
        return self.targetTemp

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator

    def update_p(self, p):
        self.Kp = p

    def update_i(self, i):
        self.Ki = i

    def update_d(self, d):
        self.Kd = d
