# Link to Stack Overflow forum with this example: https://stackoverflow.com/a/19586836/18101072
class Observable:
    def subscribe(self,callback):
        self.callback = callback

    def fire(self):
        self.callback()

class CallBackStuff:
    storedInput = None # Class member to store the input
    def doCallback(self):
        self.storedInput = input("Please enter Y or N?")

def main():
    s = CallBackStuff()
    o = Observable()
    o.subscribe(s.doCallback)
    o.fire()
    print (s.storedInput) # Print stored input from call-back object


if __name__ == '__main__':
    main()