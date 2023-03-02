
def values_set_check(*args):
    for arg in args:
        if arg is None:
            print("All values must be set. Canceling operation")
            print("")
            exit()


def continue_prompt(prompt: str):
    prompt = input(prompt + "  (Y/n):  ")
    if not prompt == "y" and not prompt == "Y":
        print("")
        print("Canceling operation")
        print("")
        exit()
    print("")

def exit_with(prompt: str):
    print("")
    print(prompt)
    print("")
    exit()
