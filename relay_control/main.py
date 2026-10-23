from machine import Pin, WDT
import sys
import select
import time

# Relays corresponding to GPIO pins
relay_one = 2
relay_two = 3
relay_three = 4
relay_four = 5

# Relay mapping number: gpio pin
relay_pairs = {1:relay_one, 2:relay_two, 3:relay_three, 4:relay_four}

valid_relays = sorted(relay_pairs.keys())

# Set to false if the given relay module is active high
active_low = True

def electrical_level(on:bool):
    """Return 0/1 pin value when on/off determined by active low/high"""
    return (0 if on else 1) if active_low else (1 if on else 0)


class Relay:
    """Relay interface for a given address assigned to a Pin"""
    def __init__(self, control:Pin, state:bool=False):
        self.control = control
        self.state = state

    def change_state(self, on:bool):
        """Toggle a relay on or off based on input"""
        self.control.value(electrical_level(on))
        self.state = on


# Mapping relay number: Pin instance
relays:dict[int, Relay] = {}

# Generate the Relays
for relay_number, gpio_pin in relay_pairs.items():
    pin = Pin(
        gpio_pin,
        Pin.OUT,
        value=electrical_level(False)
    )

    r = Relay(control=pin)

    relays[relay_number] = r


def valid_relay(number:int) -> Relay:
    """Return a valid relay or raise an exception"""
    if number not in valid_relays:
        raise ValueError(f"Relay number must be one of {valid_relays}")

    relay = relays.get(number)

    if isinstance(relay, Relay):
        return relay

    else:
        raise TypeError(f"Expected valid Relay, found {type(relay)}")


def set_relay(number:int, on:bool):
    """Toggle a relay on or off"""
    relay = valid_relay(number)

    relay.change_state(on)


def set_all(on:bool) -> None:
    """Toggle all relays on or off"""
    for number in valid_relays:
        set_relay(number, on)

def get_status() -> str:
    """Return the status for all relays as a printable string"""
    states = []
    for number in valid_relays:
        relay = valid_relay(number)
        current_relay_state = "ON" if relay.state else "OFF"
        current_relay_status = f"{number}: {current_relay_state}"
        states.append(current_relay_status)

    return "OK Relays-> " + " ".join(states)


def handle_command(command:str):
    """Interpret string command and execute the appropriate action"""

    parts:list[str] = command.strip().upper().split()

    if not parts:
        return

    try:
        if parts == ["STATUS"]:
            print(get_status())

        elif parts == ["ALL", "ON"]:
            set_all(True)
            print(get_status())

        elif parts == ["ALL", "OFF"]:
            set_all(False)
            print(get_status())

        elif len(parts) == 3 and parts[0] == "RELAY":
            number = int(parts[1])

            if parts[2] not in ("ON", "OFF"):
                print("ERR Expected ON or OFF")
                return

            # Will return either a True/False value
            on_or_off = parts[2] == "ON"
            set_relay(number, on_or_off)
            print(get_status())

        elif len(parts) == 2 and parts[0] == "TOGGLE":
            number = int(parts[1])

            # Ensure the
            relay = valid_relay(number)

            current_relay_state = relay.state

            # Flip to the opposite state
            set_relay(number, not current_relay_state)
            print(get_status())

        else:
            print("ERR Unknown command")

    except ValueError as error:
        print("ERR", error)


# Check for available USB input without blocking
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

print("PICO-RELAY READY")
print("Commands: RELAY n ON/OFF, ALL ON/OFF, TOGGLE n, STATUS")

# Start watchdog only after initialization is complete
watchdog = WDT(timeout=8000)

buffer = ""

while True:
    try:
        # Wait briefly for input; do not block indefinitely
        events = poller.poll(100)

        if events:
            char = sys.stdin.read(1)

            if char:
                if char in ("\r", "\n"):
                    if buffer:
                        handle_command(buffer)
                        buffer = ""
                elif len(buffer) < 100:
                    buffer += char
                else:
                    print("ERR Command too long")
                    buffer = ""

        # Feed the watchdog on every iteration
        watchdog.feed()

    except Exception as e:
        print("ERR", e)
        time.sleep_ms(100)

