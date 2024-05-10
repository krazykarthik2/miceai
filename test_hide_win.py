import ctypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
SW_HIDE = 0

def hide_console_window():
  """Hides the console window of the current process."""
  whnd = kernel32.GetConsoleWindow()
  if whnd != 0:
    kernel32.ShowWindow(whnd, SW_HIDE)

if __name__ == "__main__":
  # Your main program logic here

  # Hide the console window after program initialization
  hide_console_window()

  # Rest of your program code
