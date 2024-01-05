import re
from typing import Optional

import psutil


def get_process(
    program, scriptname, required_args: set[str]
) -> Optional[psutil.Process]:
    # Find processes which contain the program or script name.
    matching_processes = []
    for process in psutil.process_iter():
        try:
            p = process.name()
            if program in p or scriptname in p:
                matching_processes.append(process)
        except psutil.NoSuchProcess:
            continue
    # If matching processes were found, check for correct arguments.
    if len(matching_processes) != 0:
        mismatch_found = False
        for process in matching_processes:
            try:
                args = process.cmdline()[1:]
                for required_arg in required_args:
                    matching_args = [
                        arg
                        for arg in args
                        if re.match(required_arg, arg, flags=re.IGNORECASE) is not None
                    ]
                    # Skip this process because it does not have a matching required argument.
                    if len(matching_args) == 0:
                        break
                else:
                    # If this process has not been skipped, it matches all arguments.
                    return process
                mismatch_found = True
            except psutil.AccessDenied:
                print(f"Access denied when trying to look at cmdline of {process}!")
            except psutil.NoSuchProcess:
                # process died whilst we were looking at it, so pretend we found none, it will get handles another time
                pass
        if mismatch_found:
            # If we didn't return yet it means all matching programs were skipped.
            raise WrongProcessArgs(
                f"{program} is not running with required arguments: {required_args}!"
            )
    # No matching processes.
    return None


def is_process_running(
    program, scriptname, required_args: set[str]
) -> tuple[bool, Optional[psutil.Process]]:
    process = get_process(program, scriptname, required_args)
    return process is not None, process


class WrongProcessArgs(UserWarning):
    pass
