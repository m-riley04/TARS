import time

class PID:
    def __init__(self, kp, ki, kd, output_limits=(-125, 125)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0
        self.output_limits = output_limits

    def compute(self, setpoint, measurement, dt):
        error = setpoint - measurement
        self.integral += error * dt

        # Anti-windup clamp
        self.integral = max(min(self.integral, 100), -100)

        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        # Clamp output
        return max(min(output, self.output_limits[1]), self.output_limits[0])
