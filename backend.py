from tapsdk import TapSDK, TapInputMode
from Finger import Finger

from keyboard import is_pressed
import screen_brightness_control as sbc

tap_instance = []
tap_identifiers = []
fingerList = []

class Interaction:
    tap_status = False
    isActive = False
    current_tapcode = 0
    
    def on_connect(self, identifier, name, fw):
        tap_status = True
        if identifier not in tap_identifiers:
            tap_identifiers.append(identifier)
        print("Connected taps:")
        for identifier in tap_identifiers:
            print(identifier)
    
    def on_disconnect(self, identifier):
        tap_status = False
        print("Tap has disconnected")
        if identifier in tap_identifiers:
            tap_identifiers.remove(identifier)
        for identifier in tap_identifiers:
            print(identifier)
    
    def on_tap_event(self, identifier, tapcode):
        if int(tapcode) == 30:
            if isActive:
                Interaction.selectMode(tapcode)
            else:
                isActive = True
    
    def selectMode(tapcode):
        if tapcode == 2:
            finger = fingerList[0]
            print("Pointer Finger Active")
        elif tapcode == 4:
            finger = fingerList[1]
            print("Middle Finger Active")
        elif tapcode == 8:
            finger = fingerList[2]
            print("Ring Finger Active")
        elif tapcode == 16:
            finger = fingerList[3]
            print("Pinky Finger Active")

def main():
    global tap_instance
    tap_instance = TapSDK()
    tap_interaction = Interaction()
    tap_instance.run()
    tap_instance.register_connection_events(tap_interaction.on_connect)
    tap_instance.register_disconnection_events(tap_interaction.on_disconnect)
    tap_instance.register_tap_events(tap_interaction.on_tap_event)
    tap_instance.set_input_mode(TapInputMode("controller"))
    
    running = True
    while running:
        if (is_pressed('Left')) & Interaction.current_tapcode == 2:
            sbc.set_brightness(sbc.get_brightness - 10)
        elif (is_pressed('Right')) & Interaction.current_tapcode == 2:
            sbc.set_brightness(sbc.get_brightness + 10)
        
        if(is_pressed('BackSpace')):
            running = False
        else:
            pass
        
if __name__ == "__main__":
    main()