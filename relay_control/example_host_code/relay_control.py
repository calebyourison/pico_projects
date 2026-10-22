import serial
import time


class RelayController:
    def __init__(self, port="/dev/ttyACM0"):
        self.ser = serial.Serial(
            port=port,
            baudrate=115200,
            timeout=2,
            write_timeout=2
        )

        # Wait USB connection.
        time.sleep(1)

        # Ignore startup messages.
        self.ser.reset_input_buffer()

    def command(self, cmd):
        """Send a command to the Pico and return its response."""
        self.ser.write((cmd + "\n").encode("ascii"))
        self.ser.flush()

        response = self.ser.readline().decode(
            "ascii", errors="replace"
        ).strip()

        if not response:
            raise TimeoutError(f"No response from Pico: {cmd}")

        if response.startswith("ERR"):
            raise RuntimeError(response)

        return response

    def on(self, relay):
        return self.command(f"RELAY {relay} ON")

    def off(self, relay):
        return self.command(f"RELAY {relay} OFF")

    def toggle(self, relay):
        return self.command(f"TOGGLE {relay}")

    def all_on(self):
        return self.command("ALL ON")

    def all_off(self):
        return self.command("ALL OFF")

    def status(self):
        return self.command("STATUS")

    def close(self):
        self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

relay_module = RelayController()

relay_module.all_on()
time.sleep(1)
relay_module.all_off()

relay_module.on(1)
time.sleep(1)
relay_module.off(1)