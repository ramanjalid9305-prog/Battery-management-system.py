import random
import time
from datetime import datetime

# Battery specifications
BATTERY_CAPACITY_AH = 100.0
MIN_VOLTAGE = 10.5
MAX_VOLTAGE = 14.6
MAX_TEMPERATURE = 45.0
MIN_TEMPERATURE = 0.0

soc = 80.0


def read_battery_sensors():
    """
    Simulate battery sensor readings.

    Replace this function with real sensor readings
    when connecting the system to hardware.
    """

    voltage = random.uniform(11.0, 14.4)
    current = random.uniform(-10.0, 20.0)
    temperature = random.uniform(20.0, 45.0)

    return voltage, current, temperature


def calculate_soc(current, elapsed_seconds):
    """
    Estimate SOC using coulomb counting.

    Positive current = charging
    Negative current = discharging
    """

    global soc

    elapsed_hours = elapsed_seconds / 3600

    # Convert current into Ah
    charge_change = current * elapsed_hours

    # Update SOC
    soc += (charge_change / BATTERY_CAPACITY_AH) * 100

    # Keep SOC between 0 and 100%
    soc = max(0, min(100, soc))

    return soc


def check_battery_status(voltage, temperature, soc):
    """Check battery operating conditions."""

    warnings = []

    if voltage < MIN_VOLTAGE:
        warnings.append("LOW VOLTAGE")

    if voltage > MAX_VOLTAGE:
        warnings.append("HIGH VOLTAGE")

    if temperature > MAX_TEMPERATURE:
        warnings.append("HIGH TEMPERATURE")

    if temperature < MIN_TEMPERATURE:
        warnings.append("LOW TEMPERATURE")

    if soc <= 10:
        warnings.append("LOW SOC")

    if soc >= 95:
        warnings.append("HIGH SOC")

    if warnings:
        return "WARNING: " + ", ".join(warnings)

    return "NORMAL"


def main():
    global soc

    previous_time = time.time()

    print("=" * 60)
    print("             BATTERY MANAGEMENT SYSTEM")
    print("=" * 60)

    try:
        while True:

            voltage, current, temperature = read_battery_sensors()

            current_time = time.time()
            elapsed_seconds = current_time - previous_time
            previous_time = current_time

            battery_soc = calculate_soc(
                current,
                elapsed_seconds
            )

            status = check_battery_status(
                voltage,
                temperature,
                battery_soc
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            print("\n----------------------------------------")
            print(f"Time        : {timestamp}")
            print(f"Voltage     : {voltage:.2f} V")
            print(f"Current     : {current:.2f} A")
            print(f"Temperature : {temperature:.2f} °C")
            print(f"SOC         : {battery_soc:.2f}%")
            print(f"Status      : {status}")
            print("----------------------------------------")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nBattery Management System stopped.")


if __name__ == "__main__":
    main()
