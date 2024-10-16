import psutil
import win32con
import win32gui


def find_window(title):
    """Find window handles based on the window title

    Args:
        title (str): Window title.
    Returns:
        list if found, None otherwise.
    """

    def enum_callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == title:
            result.append(hwnd)

    windows = []
    win32gui.EnumWindows(enum_callback, windows)
    return windows[0] if windows else None


def check_window(window_title):
    """Check that the game is running by window title.

    Note:
        Do not include the `self` parameter in the ``Args`` section.
    Returns:
        True if game is running, False if not.
    """

    hwnd = find_window(window_title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 确保窗口不是最小化状态
        win32gui.SetForegroundWindow(hwnd)
        return True
    else:
        return False


def is_process_running(process_name):
    """
    Check if there is any running process that contains the given name string.

    :param process_name: Name of the process to be searched.
    :return: True if the process is running, otherwise False.
    """
    # Iterate over all running processes
    for proc in psutil.process_iter(['name']):
        try:
            # Check if process name contains the given name string
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


if __name__ == "__main__":
    # Example usage:
    processName = "HYP.exe"  # Replace with the name of the process you want to check
    if is_process_running(processName):
        print(f"The process {processName} is running.")
    else:
        print(f"The process {processName} is not running.")