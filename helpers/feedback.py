import sys
import time
import utility_controller as uc


def exit_with_message(message: str, timeout_seconds=2):
    """
    Convenience function to abort a script with a message
    visible to the user for a duration of an optional timeout.
    :param timeout_seconds:
    :param message:
    :return:
    """
    print(message)
    uc.print_message(message)
    time.sleep(timeout_seconds)
    sys.exit(1)

