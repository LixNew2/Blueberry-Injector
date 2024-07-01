import psutil, keyboard, time, ctypes
from colorama import Fore, Style

print(f"""{Fore.LIGHTGREEN_EX}
██████╗ ██╗     ██╗   ██╗███████╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗    ██╗███╗   ██╗     ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝    ██║████╗  ██║     ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██║     ██║   ██║█████╗  ██████╔╝█████╗  ██████╔╝██████╔╝ ╚████╔╝     ██║██╔██╗ ██║     ██║█████╗  ██║        ██║   ██║   ██║██████╔╝
██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗██╔══██╗  ╚██╔╝      ██║██║╚██╗██║██   ██║██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
██████╔╝███████╗╚██████╔╝███████╗██████╔╝███████╗██║  ██║██║  ██║   ██║       ██║██║ ╚████║╚█████╔╝███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═╝╚═╝  ╚═══╝ ╚════╝ ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   v1.0 
                                                                        by LixNew                                             
{Style.RESET_ALL}
                                                            | Welcome to Blueberry DLL Injector ! |\n
{Fore.LIGHTBLUE_EX}
| Down arrow to scroll process 
| Top arrow to turn back
| Right arrow to select a process
{Style.RESET_ALL} 
""")

existing_process = []
added_process = []
current_process = 0

BLUEBERRY_INJECTOR_DLL = ctypes.WinDLL("./BlueberryInjector.dll")
BLUEBERRY_INJECTOR_DLL.InjectDLL.argtypes = [ctypes.c_char_p, ctypes.c_int]
BLUEBERRY_INJECTOR_DLL.restype = ctypes.c_int

def process():
    for process in psutil.process_iter():
        try:
            if process.name() != "":
                if process.name() not in added_process:
                    added_process.append(process.name())
                    existing_process.append([process.name(), process.pid])
        except:
            pass

def get_PID():
    for process in psutil.process_iter():
        if process.name() == existing_process[current_process][0]:
            return process.pid
    return 0

def inject_dll(dll_path):
    pid = get_PID()
    try:
        BLUEBERRY_INJECTOR_DLL.InjectDLL(dll_path.encode(), pid)
        print("DLL successfully injected !" + Style.RESET_ALL)
    except:
        print("Error during DLL injection !" + Style.RESET_ALL)
        return


while True:
    print(Fore.MAGENTA + "\nUpdate process..."  + Style.RESET_ALL, end="\r")
    process()
    print("\033[K" + "Found process : \n" + Fore.LIGHTGREEN_EX + "-> " + Style.RESET_ALL + existing_process[current_process][0], end="\r")
    while True:
        if keyboard.is_pressed("down"):
            if current_process+1 > len(existing_process)-1:
                current_process = 0
            else:
                current_process += 1
            print("\033[K" + Fore.LIGHTGREEN_EX + "-> " + Style.RESET_ALL + existing_process[current_process][0], end="\r")

        if keyboard.is_pressed("up"):
            if current_process-1 < 0:
                current_process = len(existing_process)-1
            else:
                current_process -= 1
            print("\033[K" +  Fore.LIGHTGREEN_EX + "-> " + Style.RESET_ALL + existing_process[current_process][0], end="\r")

        if keyboard.is_pressed("right"):
            print("\n\nSelected process : " + Fore.YELLOW + existing_process[current_process][0] + Style.RESET_ALL)
            break
        
        time.sleep(0.1)

    dll_path = input("DLL path : " + Fore.YELLOW)
    input(Fore.RED + "\nPress ENTER to inject the DLL !")
    inject_dll(dll_path.replace('"', ""))
    answer = input(Fore.LIGHTGREEN_EX + "\nInject another DLL ? (y / n)" + Style.RESET_ALL)
    if answer.lower() == "n":
        break
    current_process = 0

