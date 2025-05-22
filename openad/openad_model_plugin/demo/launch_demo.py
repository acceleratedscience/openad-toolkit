"""
Launch and shutdown of the model service demo.
See model_service_demo.py for more info and the actual demo service.
"""

import os
import sys
import threading
import subprocess
from openad.helpers.general import confirm_prompt
from openad.helpers.output import output_error, output_text, output_success, output_warning

DEMO_PROCESS = None


def launch_model_service_demo(restart=False, debug=False):
    """
    Spin up the model service demo in a subprocess.
    """

    global DEMO_PROCESS

    # Process already running
    if DEMO_PROCESS:
        # Try restart
        if restart or debug:
            success = terminate_model_service_demo()
            if not success:
                return

        # Remind instructions
        else:
            return _print_success(new=False)

    # Make sure openad_service_utils are installed
    utils_installed = _verify_utils_installed()
    if not utils_installed:
        return

    service_path = os.path.join(os.path.dirname(__file__), "model_service_demo.py")
    command = [sys.executable, service_path]

    try:
        DEMO_PROCESS = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout for combined logging
            text=True,  # Decode output as text (Python 3.6+)
            bufsize=1,  # Line-buffered output
        )

        # Log the subprocess' stdout
        if debug:

            def log_output():
                for line in iter(DEMO_PROCESS.stdout.readline, ""):
                    print(f"DEMO SERVICE: {line.strip()}")
                DEMO_PROCESS.stdout.close()

            # Start the logging thread
            log_thread = threading.Thread(target=log_output, daemon=True)
            log_thread.start()

        # Success message
        return _print_success()
    except Exception as e:  # pylint: disable=broad-except
        return output_error(f"Failed to start model service demo: {e}")


def _verify_utils_installed():
    """
    Make sure openad_service_utils are installed.
    """
    try:
        from openad_service_utils import start_server

        return True
    except ImportError:
        msg = (
            "Install openad_service_utils to use the demo model service:\n"
            "<cmd>pip install git+https://github.com/acceleratedscience/openad_service_utils.git@0.3.1</cmd>"
        )
        output_warning(msg, return_val=False)
        return False


def _print_success(new=True):
    """
    Success message & instructions.
    """
    main_msg = (
        (
            "<success>Demo model service started at <yellow>http://localhost:8034</yellow></success>\n"
            f"<soft>PID: {DEMO_PROCESS.pid}</soft>"
        )
        if new
        else (
            "<yellow>Demo model service already running at <reset>http://localhost:8034</reset></yellow>\n"
            f"<soft>PID: {DEMO_PROCESS.pid} / To restart the demo service, run <cmd>model service demo restart</cmd></soft>"
        )
    )

    msg = [
        main_msg,
        "",
        "Next up, run:",
        "<cmd>catalog model service from remote 'http://localhost:8034' as demo_service</cmd>",
        "",
        "To test the service:",
        "<cmd>demo_service ?</cmd>",
        "<cmd>demo_service get molecule property num_atoms for CC</cmd>",
        "<cmd>demo_service get molecule property num_atoms for NCCc1c[nH]c2ccc(O)cc12</cmd>",
    ]
    return output_text("\n".join(msg), edge=True, pad=1)


def terminate_model_service_demo():
    """
    Terminate the model service demo.
    """
    global DEMO_PROCESS
    if DEMO_PROCESS is None:
        return True

    if DEMO_PROCESS:
        try:
            DEMO_PROCESS.terminate()
            DEMO_PROCESS.wait(timeout=1)
            output_success(f"Demo model service terminated - PID: {DEMO_PROCESS.pid}", return_val=False)
            DEMO_PROCESS = None
            return True
        except Exception as err1:  # pylint: disable=broad-except
            try:
                # Force kill if terminate fails
                DEMO_PROCESS.kill()
                DEMO_PROCESS.wait(timeout=5)
                output_success(f"Demo model service killed - PID: {DEMO_PROCESS.pid}", return_val=False)
                DEMO_PROCESS = None
                return True
            except Exception as err2:  # pylint: disable=broad-except
                output_error(
                    [f"Failed to terminate model service demo with PID: {DEMO_PROCESS.pid}", err1, err2],
                    return_val=False,
                )
                return False
