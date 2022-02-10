# from board import SCL, SDA
# import busio
#
# from adafruit_pca9685 from PCA9685
def pwn

if __name__ == '__main__':
    # i2c_bus = busio.I2C(SCL, SDA)
    # pca = PCA9685(i2c_bus)
    motor = input("Which motor do you want to use? (Input a number between 0-7): ")
    valueType = input("Would you like to set the RPM or thrust?: ").lower()
    while valueType != "rpm" or valueType != "thrust":
        print("Invalid input! Must input either 'RPM' or 'thrust'")
        valueType = input("Would you like to set the RPM or thrust?: ").lower()
    while True:
        try:
            if valueType == "rpm":
                value = int(input("Enter RPM: "))

            else:
                value = int(input("Enter thrust: "))

        except ValueError:
            print("Provide an integer value...")
            continue




    pca.frequency = 60 #Not really sure what this does
    pca.channels[0].duty_cycle = 0x7FFF #Not really sure what this does