from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
import pandas as pd
import numpy as np
import keyboard

tap_instance = []
tap_identifiers = []

modes = ["text", "controller", "controller_text", "raw"]


# For connection notification
def on_connect(identifier, name, fw):
    print("Tap has connected")
    print(identifier + " Tap: " + str(name), " FW Version: ", fw)
    if identifier not in tap_identifiers:
        tap_identifiers.append(identifier)
    print("Connected taps:")
    for identifier in tap_identifiers:
        print(identifier)

# For disconnection notification
def on_disconnect(identifier):
    print("Tap has disconnected")
    if identifier in tap_identifiers:
        tap_identifiers.remove(identifier)
    for identifier in tap_identifiers:
        print(identifier)

# For mouse data
def on_mouse_event(identifier, dx: int, dy: int, isMouse):
    if isMouse:
        print("X-coor"+str(dx), "Y-coor"+str(dy)) 
        # with open("hello.txt", "w") as my_file:
        #     my_file.write(str(dx), str(dy))
        # return ("X-coor"+str(dx), "Y-coor"+str(dy)) 
        
    else:
        pass
        # print("Air: ", str(dx), str(dy))

#For adding
def add_top_column(df: pd.DataFrame, top_col: str, inplace=False):
    if not inplace:
        df = df.copy()
    
    df.columns = pd.MultiIndex.from_product([[top_col], df.columns])
    return df


def main():    
    global tap_instance
    tap_instance = TapSDK()
    tap_instance.run()
    tap_instance.register_connection_events(on_connect)
    tap_instance.register_disconnection_events(on_disconnect)
    tap_instance.register_mouse_events(on_mouse_event)
    tap_instance.set_input_mode(TapInputMode(modes[1])) 
    
    trial = True 
    while trial:
        if(keyboard.is_pressed("q")):
            trial = False
            print("You have chosen to end this trial.")
        else: 
            pass

if __name__ == "__main__":
    main() 