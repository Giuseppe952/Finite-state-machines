class LogicGate:

    def __init__(self,n):
        self.name = n
        self.output = None
        self.visited = False

    def getLabel(self):
        return self.name

    def getOutput(self):
        if self.visited:
            return self.output
        
        self.visited = True
        self.output = self.performGateLogic()
        self.visited = False
        return self.output


class BinaryGate(LogicGate):

    def __init__(self,n):
        super(BinaryGate, self).__init__(n)

        self.pinA = None
        self.pinB = None

    def getPinA(self):
        if self.pinA == None:
            return int(input("Enter Pin A input for gate "+self.getLabel()+"-->"))
        else:
            return self.pinA.getFrom().getOutput()

    def getPinB(self):
        if self.pinB == None:
            return int(input("Enter Pin B input for gate "+self.getLabel()+"-->"))
        else:
            return self.pinB.getFrom().getOutput()

    def setNextPin(self,source):
        if self.pinA == None:
            self.pinA = source
        else:
            if self.pinB == None:
                self.pinB = source
            else:
                print("Cannot Connect: NO EMPTY PINS on this gate")


class AndGate(BinaryGate):

    def __init__(self,n):
        BinaryGate.__init__(self,n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 and b==1:
            return 1
        else:
            return 0
        
class NandGate(BinaryGate):

    def __init__(self,n):
        BinaryGate.__init__(self,n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a==1 and b==1:
            return 0
        else:
            return 1

class OrGate(BinaryGate):

    def __init__(self,n):
        BinaryGate.__init__(self,n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a ==1 or b==1:
            return 1
        else:
            return 0
        
class NotOrGate(BinaryGate):

    def __init__(self,n):
        BinaryGate.__init__(self,n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a ==1 or b==1:
            return 0
        else:
            return 1


class XorGate(BinaryGate):

    def __init__(self,n):
        BinaryGate.__init__(self,n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a == b:
            return 0
        else:
            return 1

class XnorGate(BinaryGate):

    def __init__(self,n):
        BinaryGate.__init__(self,n)

    def performGateLogic(self):

        a = self.getPinA()
        b = self.getPinB()
        if a == b:
            return 1
        else:
            return 0

class UnaryGate(LogicGate):

    def __init__(self,n):
        LogicGate.__init__(self,n)

        self.pin = None

    def getPin(self):
        if self.pin == None:
            return int(input("Enter Pin input for gate "+self.getLabel()+"-->"))
        else:
            return self.pin.getFrom().getOutput()

    def setNextPin(self,source):
        if self.pin == None:
            self.pin = source
        else:
            print("Cannot Connect: NO EMPTY PINS on this gate")

class NotGate(UnaryGate):

    def __init__(self,n):
        UnaryGate.__init__(self,n)

    def performGateLogic(self):
        if self.getPin():
            return 0
        else:
            return 1


class Connector:

    def __init__(self, fgate, tgate):
        self.fromgate = fgate
        self.togate = tgate

        tgate.setNextPin(self)

    def getFrom(self):
        return self.fromgate

    def getTo(self):
        return self.togate

class JKFlipflop(BinaryGate):
    def __init__(self, n):
        super().__init__(n)
        self.q = 0
        self.q_next = 0
    def performGateLogic(self):
        return self.q
    def find_q(self):
        j = self.getPinA()
        k = self.getPinB()
        if self.q == 0:
            if j == 1:
                self.q_next = 1
            else:
                self.q_next = 0
        elif self.q == 1:
              if k == 1:
                self.q_next = 0
              else:
                self.q_next = 1
    def clock_tick(self):
        self.q = self.q_next

class Power(UnaryGate):
    def __init__(self, n):
        super().__init__(n)
    def performGateLogic(self):
        return 1

class Switch(UnaryGate):
    def __init__(self, n):
        super().__init__(n)
        self.state = 0
    def set_state(self, value):
        self.state = value
    def getPin(self):
       return self.state
    def performGateLogic(self):
        return self.state


def main():
   flip1 = JKFlipflop("Flip1")
   flip2 = JKFlipflop("Flip2")
   nflip1 = NotGate("N0")
   Connector(flip1, nflip1)
   power = Power("Power")
   switch = Switch("Switch")

   a1 = AndGate("A1")
   a2 = AndGate("A2")
   a3 = AndGate("A3") #Final output
   n1 = NotGate("N1")
   c1 = Connector(switch, a1)
   c2 = Connector(flip2, a1)
   c3 = Connector(switch, n1)
   c4 = Connector(a1, flip1)
   c5 = Connector(n1, flip1)
   c6 = Connector(switch, a2)
   c7 = Connector(nflip1, a2)
   c8 = Connector(a2, flip2)
   c9 = Connector(power, flip2)
   c10 = Connector(nflip1, a3)
   c11 = Connector(flip2, a3)


   while True:
      button_press = int(input("Button Pressed? "))
      switch.set_state(button_press)
      output = a3.getOutput()
      if output == 1:
          print("Pulse")
      else:
          print("No pulse")
      flip1.find_q()
      flip2.find_q()
      flip1.clock_tick()
      flip2.clock_tick()

main()