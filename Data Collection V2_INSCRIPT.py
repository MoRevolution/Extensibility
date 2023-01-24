# %% [markdown]
# ### Import Libraries

# %%
from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
import pandas as pd
import numpy as np
import keyboard
import time


tap_instance = []
tap_identifiers = []
x_array = np.array([])
y_array = np.array([])  

modes = ["text", "controller", "controller_text", "raw"]

# %% [markdown]
# ### Functions

# %%
class Functionality:
    current_x = None
    current_y = None
    
    # For connection notification
    def pis(self):
        print("Hello world!")
        
    def on_connect(self, identifier, name, fw):
        print("Tap has connected")
        print(identifier + " Tap: " + str(name), " FW Version: ", fw)
        if identifier not in tap_identifiers:
            tap_identifiers.append(identifier)
        print("Connected taps:")
        for identifier in tap_identifiers:
            print(identifier)

    # For disconnection notification
    def on_disconnect(self, identifier):
        print("Tap has disconnected")
        if identifier in tap_identifiers:
            tap_identifiers.remove(identifier)
        for identifier in tap_identifiers:
            print(identifier)

    # For mouse data
    def on_mouse_event(self, identifier, dx: int, dy: int, isMouse):
        if isMouse:
            self.current_x = dx 
            self.current_y = dy
            print(str(dx), str(dy))

            # time.sleep(5) # Sleep for 3 seconds
            # return ("X-coor"+str(dx), "Y-coor"+str(dy)) 
        else:
            pass
            # print("Air: ", str(dx), str(dy))

    #For adding
    def add_top_column(self, df: pd.DataFrame, top_col: str, inplace=False):
        if not inplace:
            df = df.copy()
        
        df.columns = pd.MultiIndex.from_product([[top_col], df.columns])
        return df




# %% [markdown]
# ### Main 

# %%
def main():
    trial_df = pd.DataFrame()
    count = 0
    start = input(f"Type 'St' to start running")

    while start == "St":
        trial = input(f"Type 'ST' to start running this trial")
        x_array = np.array([])
        y_array = np.array([])
        while trial == "ST":
            print("We are on trial" + str(count))

            # instantiate a Tap object and start registering events
            global tap_instance
            tap_instance = TapSDK()
            tap_instance.run()
            tap_instance.register_connection_events(on_connect)
            tap_instance.register_disconnection_events(on_disconnect)
            tap_instance.register_mouse_events(on_mouse_event)
            
            #append each position change value to the array 
            x_array = np.append(x_array,[dx])
            y_array = np.append(x_array,[dy])   
            print(str(dx), str(dy)) 

            #use 1 or 3 for controller or raw data mode respectively in list modes
            tap_instance.set_input_mode(TapInputMode(modes[1])) 

            # Command to end the recording of one trail within a case
            if(keyboard.is_pressed("q")):
                trail = "END"
                print("You have chosen to end this trial.")
            else: 
                pass

        #Add this trial to the trial_df dataframe
        trial_column = pd.DataFrame([[x_array, y_array]], columns=['x', 'y'])
        trial_column = add_top_column(trial_column, "Trial_" + str(count))
        trial_df= pd.concat([trial_df, trial_column])

        print(f"Trial {count} just ended, starting next trial. ")
        count += count
        print(f"Trial {count} is next")

        # Command to end the recording of trials within this database
        if (keyboard.is_pressed('p')): 
            start = "End"
            print("You have chosen to end this iteration of trials. Saving data...")
        else: 
            pass

    trial_df.to_csv(input("Type in the name for this csv file"), index=False)

if __name__ == "__main__":
    main()

# %% [markdown]
# ### Trial and Error

# %%
def main():  
    x_array = np.array([])
    y_array = np.array([])  
    global tap_instance
    tap_instance = TapSDK()
    fun = Functionality()
    tap_instance.run()
    # tap_instance.register_connection_events(on_connect)
    # tap_instance.register_disconnection_events(on_disconnect)
    tap_instance.register_mouse_events(fun.on_mouse_event)
    tap_instance.set_input_mode(TapInputMode(modes[1]))   

    tap_instance.get_data_mouse()
    print(fun.current_x)
    print(fun.current_y)

    # x_array = np.append(x_array,[array[0]])
    # y_array = np.append(x_array,[array[1]])   
    trial = True 
    while trial:
        if(keyboard.is_pressed("q")):
            trial = False
            # with open("hello.txt", "a") as my_file:
            #     my_file.write(str(x_array[0]))
            #     my_file.write(str(y_array[0]))
            print("You have chosen to end this trial.")
            tap_instance.send_vibration_sequence(sequence=[1000,300,200])
        else: 
            pass
main()

# %%
x_array.size

# %%
mouse_data = (1,2)
trial_df = pd.DataFrame()

x_array = np.array([mouse_data[0]])
y_array = np.array([mouse_data[1]])


first_row = pd.DataFrame([[mouse_data[0], mouse_data[1]]], columns=['x', 'y'])
trial_df= pd.concat([trial_df, first_row])
trial_df = add_top_column(trial_df, 'Trial_'+ str(1))

trial_df
# new_row = pd.Series({'x': 3, 'y': 4})
# pd.concat([trial_df, new_row.to_frame().T], ignore_index=True)

# %%
big_df = pd.DataFrame()
orig_df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
orig_df = add_top_column(orig_df, "new column")
big_df = pd.concat([big_df,orig_df], axis=1)
big_df

# new_df3 = add_top_column(orig_df, "new column3")
# print(pd.concat([new_df, new_df2, new_df3], axis=1))

# orig_df.columns

# %%
# new_df2 = add_top_column(orig_df, "new column2")
new_df2 = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
new_df2 = add_top_column(new_df2, "new column1")
big_df = pd.concat([big_df,new_df2], axis=1)
big_df


# %%
big_df = pd.DataFrame([])
new_df3 = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
new_df3 = add_top_column(new_df3, "new column3")
big_df = pd.concat([big_df,new_df3], axis=1)
big_df




