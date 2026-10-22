from machine import Pin, WDT
import sys
import select
import time

# Relay 2, Relay 3, Relay 3, Relay 4
RELAY_PINS = (2, 3, 4, 5)

# True for active-low relay modules, set to false if needed
ACTIVE_LOW = True

# All relays off by default
relay_states = [False, False, False, False]

def electrical_level(on:bool) -> int:
    return (0 if on else 1) if ACTIVE_LOW else (1 if on else 0)

# Generate Pins and set relays to off
relays = []

for pin_number in RELAY_PINS:
    pin = Pin(
        pin_number,
        Pin.OUT,
        value=electrical_level(False)
    )
    relays.append(pin)


def set_relay(number:int, on:bool):
    if number < 1 or number > 4:
        raise ValueError("Relay number must be 1-4")

    index = number - 1
    relays[index].value(electrical_level(on))
    relay_states[index] = on


def set_all(on:bool):
    for number in range(1, 5):
        set_relay(number, on)


def get_status():
    states = []

    for number, on in enumerate(relay_states, start=1):
        state = "ON" if on else "OFF"
        states.append("R%d=%s" % (number, state))

    return "OK " + " ".join(states)


def handle_command(command):
    parts = command.strip().upper().split()

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

            set_relay(number, parts[2] == "ON")
            print(get_status())

        elif len(parts) == 2 and parts[0] == "TOGGLE":
            number = int(parts[1])

            if number < 1 or number > 4:
                raise ValueError("Relay number must be 1-4")

            set_relay(number, not relay_states[number - 1])
            print(get_status())

        else:
            print("ERR Unknown command")

    except ValueError as e:
        print("ERR", e)


# Check for input
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

print("PICO-RELAY READY")
print("Commands: RELAY n ON/OFF, ALL ON/OFF, TOGGLE n, STATUS")

# Start watchdog
watchdog = WDT(timeout=8000)

buffer = ""

while True:
    try:
        # Wait briefly for input
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

        # Watchdog
        watchdog.feed()

    except Exception as error:
        print("ERR", error)
        time.sleep_ms(100)

