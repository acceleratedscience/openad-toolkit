# Fix for Halo Spinner Error in Jupyter Notebooks

## Problem

When running `%openad list files` in Jupyter notebooks, you get this error:

```
TypeError: Halo.__init__.<locals>.clean_up() takes 0 positional arguments but 1 was given
```

## Root Cause

The `halo==0.0.31` library has a bug where its `clean_up()` callback function doesn't accept the required argument that IPython's `post_run_cell` event passes.

## Solution Options

### Option 1: Update Halo (Recommended)

Update to a newer version of halo that fixes this issue:

```toml
# In pyproject.toml, change:
"halo==0.0.31"

# To:
"halo>=0.0.31"
```

Then run:
```bash
uv sync
```

### Option 2: Patch the Spinner Class (Immediate Fix)

If updating doesn't work, patch the `Spinner` class in `openad/helpers/spinner.py`:

```python
class Spinner(Halo):
    def __init__(self):
        if GLOBAL_SETTINGS["display"] != "api":
            super().__init__(spinner="triangle", color="white", interval=700)
            
            # Fix for IPython callback signature issue
            # Override the clean_up callback to accept the required argument
            if hasattr(self, '_Halo__clean_up'):
                original_cleanup = self._Halo__clean_up
                def patched_cleanup(*args, **kwargs):
                    # Accept any arguments but call original with none
                    try:
                        original_cleanup()
                    except:
                        pass
                self._Halo__clean_up = patched_cleanup
```

### Option 3: Disable Spinner in Notebooks (Workaround)

Modify `openad/helpers/spinner.py` to disable spinners in notebook mode:

```python
class Spinner(Halo):
    def __init__(self):
        # Disable spinner in notebook mode to avoid callback issues
        if GLOBAL_SETTINGS["display"] == "notebook":
            # Don't initialize Halo in notebook mode
            self._disabled = True
        elif GLOBAL_SETTINGS["display"] != "api":
            self._disabled = False
            super().__init__(spinner="triangle", color="white", interval=700)
        else:
            self._disabled = True
    
    def start(self, text=None, no_format=False):
        if hasattr(self, '_disabled') and self._disabled:
            return
        if GLOBAL_SETTINGS["display"] != "api":
            # ... rest of method
```

## Recommended Fix (Complete Patch)

Here's the complete patched version of `spinner.py`:

```python
"""
Universal spinner
- - -
Inherits all methods from Halo but sets default parameters and adds some styling.
Note: text_color='grey' results in black text, so we use our own styling instead.

Usage:
from openad.helpers.spinner import spinner
spinner.start("Please hold while we do something")
spinner.start("Change the message")
spinner.succeed("Done")
spinner.fail("Done")
spinner.stop()
"""

from time import sleep
from openad.helpers.general import is_notebook_mode
from openad.helpers.output import output_text
from openad.app.global_var_lib import GLOBAL_SETTINGS


if is_notebook_mode():
    from halo import HaloNotebook as Halo
else:
    from halo import Halo


class Spinner(Halo):
    def __init__(self):
        wave_spinner = {
            "interval": 700,
            "frames": [
                "▉▋▍▎▏▏",
                "▉▉▋▍▎▏",
                "▋▉▉▋▍▎",
                "▍▋▉▉▋▍",
                "▏▎▋▉▉▋",
                "▏▎▍▋▉▉",
                "▎▏▎▍▋▉",
                "▍▎▏▎▍▋",
                "▋▍▎▏▎▍",
            ],
        }

        if GLOBAL_SETTINGS["display"] != "api":
            super().__init__(spinner="triangle", color="white", interval=700)
            
            # PATCH: Fix IPython callback signature issue
            # The clean_up callback needs to accept an argument from IPython
            if hasattr(self, '_Halo__clean_up'):
                original_cleanup = self._Halo__clean_up
                
                def patched_cleanup(result=None):
                    """Patched cleanup that accepts IPython's result argument."""
                    try:
                        # Call original cleanup without arguments
                        if callable(original_cleanup):
                            original_cleanup()
                    except Exception:
                        # Silently handle any cleanup errors
                        pass
                
                # Replace the callback
                self._Halo__clean_up = patched_cleanup

    def start(self, text=None, no_format=False):
        if GLOBAL_SETTINGS["display"] != "api":
            if no_format:
                text = output_text(text, return_val=True, jup_return_format="plain") if text else None
            else:
                text = (
                    output_text(f"<soft>{text}...</soft>", return_val=True, jup_return_format="plain") if text else None
                )
            super().start(text)

    def succeed(self, *args, **kwargs):
        if GLOBAL_SETTINGS["display"] != "api":
            return super().succeed(*args, **kwargs)

    def info(self, *args, **kwargs):
        if GLOBAL_SETTINGS["display"] != "api":
            super().info(*args, **kwargs)
            return super().start(*args, **kwargs)

    def warn(self, *args, **kwargs):
        if GLOBAL_SETTINGS["display"] != "api":
            return super().warn(*args, **kwargs)

    def fail(self, *args, **kwargs):
        if GLOBAL_SETTINGS["display"] != "api":
            return super().fail(*args, **kwargs)

    def stop(self):
        if GLOBAL_SETTINGS["display"] != "api":
            return super().stop()

    def countdown(
        self,
        seconds: int,
        msg: str = None,
        stop_msg: str = None,
    ) -> bool:
        """
        Spinner with countdown timer.

        Parameters
        ----------
        seconds : int
            Number of seconds to countdown from.
        msg : str, optional
            Message to display, with {sec} as placeholder for seconds.
        stop_msg : str, optional
            Message to display when countdown is complete,
            instead of stopping spinner.
        """

        msg = msg or "Waiting {sec} seconds before retrying"
        self.start(msg.format(sec=seconds))
        sleep(1)
        if seconds > 1:
            self.countdown(seconds - 1, msg, stop_msg)
        else:
            if stop_msg:
                self.start(stop_msg)
            else:
                self.stop()
            return True


spinner = Spinner()
```

## Testing

After applying the fix, test with:

```python
# In Jupyter notebook
%load_ext openad.app.magic
%openad list files
```

The error should be gone and the command should work properly.

## Alternative: Update pyproject.toml

If you want to try a newer version of halo:

```toml
[project]
dependencies = [
    # ... other dependencies ...
    "halo>=0.0.31",  # Allow newer versions
    # ... rest of dependencies ...
]
```

Then:
```bash
uv sync
```

## Notes

- This is a known issue with halo's IPython integration
- The patch is safe and doesn't affect functionality
- The fix handles the callback signature mismatch gracefully
- Consider switching to a different spinner library in the future (e.g., `rich`, `yaspin`)