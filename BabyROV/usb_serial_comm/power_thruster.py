
class Thruster():
    LEFT = True
    RIGHT = False
    ON = True
    OFF = False

    def __init__(self, which_thruster):
        self.thruster = which_thruster

    def set_thruster(self, power=False):
        '''Sets the on/off state of the specified which_thruster to the specified value

        :param bool which_thruster: specifies which which_thruster to adjust 
                            (True for left, False for right)
        :param bool power:    specifies whether the which_thruster should be set to on or off

        :returns: True if the which_thruster was successfully set to the specified state

        '''

        if self.thruster is self.LEFT and power is self.ON:
            return True  # TODO
        elif self.thruster is self.LEFT and power is self.OFF:
            return True  # TODO
        elif self.thruster is self.RIGHT and power is self.ON:
            return True # TODO
        elif self.thruster is self.RIGHT and power is self.OFF:
            return True # TODO
        else:
            return False
        