from machine import Pin
import onewire, ds18x20, time

pins = {
    15: "First",
    16: "Second",
    17: "Third",
}

measurement_period_ms = 750
sample_frequency_seconds = 2

fahrenheit: bool = False

sensors = {}

# Initialize each sensor on its own pin
for pin_num, name in pins.items():
    pin = Pin(pin_num)
    ow = onewire.OneWire(pin)
    ds = ds18x20.DS18X20(ow)

    roms = ds.scan()
    if not roms:
        raise RuntimeError(f"No sensor found on GPIO {pin_num}")

    # Use the first rom since only one sensor is connected per pin
    sensors[name] = {
        "ds": ds,
        "rom": roms[0]
    }

print("Initialized sensors:", sensors.keys())

while True:
    temps = {}

    # Conversions
    for s in sensors.values():
        s["ds"].convert_temp()

    time.sleep_ms(measurement_period_ms)

    # Read temperatures, overwrite dict key with latest value
    for name, s in sensors.items():
        temp = s["ds"].read_temp(s["rom"])
        if fahrenheit:
            temp = temp * (9 / 5) + 32
        temps[name] = temp

    print(temps)
    time.sleep(sample_frequency_seconds)

