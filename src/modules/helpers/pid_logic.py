import time

class PID:
    def __init__(self, kp, ki, kd, output_limits=(-125, 125)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.proportional = 0
        self.integral = 0
        self.derivative = 0
        self.prev_error = 0
        self.output_limits = output_limits

    def compute(self, setpoint, measurement, dt):
        error = setpoint - measurement
        self.integral += error * dt

        # Anti-windup clamp
        self.integral = self.ki * max(min(self.integral, 100), -100)

        der = (error - self.prev_error) / dt if dt > 0 else 0
        self.derivative = (self.kd * der)
        self.prev_error = error

        self.proportional = (self.kp * error)

        output = self.proportional + self.integral + self.derivative

        # Clamp output
        return max(min(output, self.output_limits[1]), self.output_limits[0])
