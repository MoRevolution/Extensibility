class Interaction:
    from tapsdk import TapSDK, TapInputMode
    from Finger import Finger

    import keyboard
    import screen_brightness_control as sbc
    # from multiplePages import tapStrapGUI
   
    finger = Finger("Empty", "Put Hotkey Here", 0)
    tap_instance = []
    tap_identifiers = []
    fingerList = [Finger("Pointer", "ctrl", 2), Finger("Middle", "ctrl", 4), Finger("Ring", "ctrl", 8),Finger("Pinky", "ctrl", 16)]
    tap_status = False
    isActive = False
    current_tapcode = 0
    interval = 1
    direction = 0
    
    #Adds the connected Tap Strap to a list of connected taps and sets connection status to true
    def on_connect(self, identifier, name, fw):
        self.tap_status = True
        if identifier not in self.tap_identifiers:
            self.tap_identifiers.append(identifier)
        print("Connected taps:")
        for identifier in self.tap_identifiers:
            print(identifier)
    
    #Removes the connected Tap Strap from a list of connected taps and sets connection status to true
    def on_disconnect(self, identifier):
        self.tap_status = False
        print("Tap has disconnected")
        if identifier in self.tap_identifiers:
            self.tap_identifiers.remove(identifier)
        for identifier in self.tap_identifiers:
            print(identifier)
    
    #Detects a tap and gives the tapcode from the Tap Strap
    def on_tap_event(self, identifier, tapcode):
        # print(identifier, str(tapcode)) # For debugging to see what tapcode is being sent
        self.current_tapcode = tapcode
        self.activeStatus(tapcode)
        self.selectMode(tapcode)
        # self.selectMode(tapcode)

    #Detects mouse movement and gives the x and y coordinates
    def on_mouse_event(self, identifier, dx, dy, isMouse):
        if self.isActive:
            if isMouse:
                #print(str(dx), str(dy)) # For debugging to see what the mouse movement is
                if (int(dx) > 10):
                    self.sbc.set_brightness(75)
                elif (int(dx) < -10):
                    self.sbc.set_brightness(25)
            else:
                pass
                # print("Air: ", str(dx), str(dy))

    #Activates or deactivates the Tap Strap
    def activeStatus(self, tapcode):
        if int(self.current_tapcode) == 30:
            if Interaction.isActive:
                Interaction.isActive = False
                print("Tap is inactive")
            else:
                Interaction.isActive = True
                print("Tap is active")
    
    #Selects the mode of the Tap Strap using the given tapcode
    def selectMode(self, tapcode):
        if self.isActive:
            if int(self.current_tapcode) == 2:
                self.finger = self.fingerList[0]
                print("Pointer Finger Active")
            elif int(self.current_tapcode) == 4:
                self.finger = self.fingerList[1]
                print("Middle Finger Active")
            elif int(self.current_tapcode) == 8:
                self.finger = self.fingerList[2]
                print("Ring Finger Active")
            elif int(self.current_tapcode) == 16:
                self.finger = self.fingerList[3]
                print("Pinky Finger Active")
            elif int(self.current_tapcode) == 14:
                self.activateHotkey(self.finger.getHotKey())
                print("Hotkey Activated")

    #Changes the hotkey assigned to the finger 
    def setHotKey(self, hotkey):
        newKey = self.keyboard.record(until='\\')
        self.finger.changeHotKey(newKey)

    #Activates the hotkey of the current finger
    def activateHotkey(self, hotkey):
        self.keyboard.press_and_release(hotkey)
    
    #Changes the interval of adjustments when using the mouse mode
    def set_interval(self, interval):
        self.interval = interval
    
                

def main():
    global tap_instance
    tap_instance = Interaction.TapSDK()
    tap_interaction = Interaction()
    tap_instance.run()
    tap_instance.register_connection_events(tap_interaction.on_connect)
    tap_instance.register_disconnection_events(tap_interaction.on_disconnect)
    tap_instance.register_tap_events(tap_interaction.on_tap_event)
    tap_instance.register_mouse_events(tap_interaction.on_mouse_event)
    tap_instance.set_input_mode(Interaction.TapInputMode("controller"))
    
    running = True
    while running:
        if(Interaction.keyboard.is_pressed('BackSpace+\\')):
            running = False
        else:
            pass
        
if __name__ == "__main__":
    main()
