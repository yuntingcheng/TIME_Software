"""
run.py:
User Interface for interacting with K-Mirror.
"""

import sys
import string
from kmirror_device import Device

def main():
    """
    Main function of User Interface.
    """

    # Instantiate list of option shortcuts, which is just the alphabet
    option = list(string.ascii_lowercase)
    # Print welcome message
    print "----------------------------------------"
    print "Welcome to the K-Mirror Control System"
    print "----------------------------------------"

    # Initialize K-Mirror instance
    print "Initializing..."
    device = Device()
    if type(device.state).__name__ == 'Home':
        print "Inititialization complete."
        print ""
    else:
        # Error out if K-Mirror couldn't be initialized
        print "Error: Could not initialize."
        sys.exit(1)

    # Infinite loop for sending events
    while True:

        # Print current state
        print "Current State: {} \n".format(type(device.state).__name__)

        # Print list of all actions
        print "List of actions:"
        events = device.events()
        index = 0
        for i in list(events):
            print "{}) {}".format(option[index], i)
            index += 1
        print ""

        # Ask for desired action
        action = raw_input("Enter the letter for the desired action or 'end' to exit: ")
        print ""

        # Do desired action
        if action == 'end':
            return
        elif action in option:
            event = option.index(action)
            if event < len(events):
                device.on_event(events[event])
                if device.state.auto_next_event is not None:
                    device.on_event(device.state.auto_next_event)
            else:
                print "Error: Invalide action inputted!\n"
        else:
            # Print error if invalid action was entered
            print "Error: Invalid action inputted!"

if __name__ == "__main__":
    main()
