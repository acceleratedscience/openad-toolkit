import os
import sys
import threading
import subprocess
from openad.helpers.output import output_error, output_text, output_success

DEMO_PROCESS = None


def launch_model_service_demo():
    """
    Spin up the model service demo in a subprocess.
    """

    global DEMO_PROCESS
    log_subprocess = False  # Set to true for debugging subprocess

    python_executable = sys.executable
    service_path = os.path.join(os.path.dirname(__file__), "model_service_demo.py")
    command = [python_executable, service_path]

    try:
        DEMO_PROCESS = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout for combined logging
            text=True,  # Decode output as text (Python 3.6+)
            bufsize=1,  # Line-buffered output
        )

        # Log the output of the subprocess
        if log_subprocess:

            def log_output():
                for line in iter(DEMO_PROCESS.stdout.readline, ""):
                    print(f"DEMO SERVICE: {line.strip()}")
                DEMO_PROCESS.stdout.close()

            # Start the logging thread
            log_thread = threading.Thread(target=log_output, daemon=True)
            log_thread.start()

        # Success message
        msg = [
            "<success>Demo model service started at <yellow>http://localhost:8034</yellow></success>\n",
            "Next up, run:",
            "<cmd>catalog model service from remote 'http://localhost:8034' as demo_service</cmd>",
            "",
            "To test the service:",
            "<cmd>demo_service ?</cmd>",
            "<cmd>demo_service get molecule property num_atoms for CC</cmd>",
            "<cmd>service_demo get molecule property num_atoms for NCCc1c[nH]c2ccc(O)cc12</cmd>",
        ]
        return output_text("\n".join(msg), edge=True, pad=1)
    except Exception as e:  # pylint: disable=broad-except
        return output_error(f"Failed to start model service demo: {e}")


def terminate_model_service_demo():
    """
    Terminate the model service demo.
    """
    global DEMO_PROCESS
    if DEMO_PROCESS:
        try:
            DEMO_PROCESS.terminate()
            DEMO_PROCESS.wait()  # Wait for the process to terminate
            output_success("Demo model service terminated")
        except Exception as err1:  # pylint: disable=broad-except
            try:
                DEMO_PROCESS.kill()  # Force kill if terminate fails
                output_success("Demo model service killed")
            except Exception as err2:  # pylint: disable=broad-except
                output_error(["Failed to terminate model service demo", err1, err2])
        finally:
            DEMO_PROCESS = None
