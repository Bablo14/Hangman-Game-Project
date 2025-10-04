# timers.py
# Simple countdown timer helpers using Tk's after().

def start_timer(root, seconds, on_tick, on_timeup):
    # Returns a control dict with remaining time and after_id for cancellation
    ctrl = {"remaining": seconds, "after_id": None}

    def tick():
        # Call on_tick with remaining seconds
        on_tick(max(ctrl["remaining"], 0))
        if ctrl["remaining"] <= 0:
            on_timeup()  # time expired
            return
        ctrl["remaining"] -= 1
        ctrl["after_id"] = root.after(1000, tick)  # schedule next tick in 1s

    if seconds > 0:
        ctrl["after_id"] = root.after(1, tick)  # start almost immediately
    else:
        # No timer configured; still invoke on_tick once for consistency
        on_tick(0)
    return ctrl

def cancel_timer(root, ctrl):
    # Stop the countdown if running
    if ctrl and ctrl.get("after_id") is not None:
        try:
            root.after_cancel(ctrl["after_id"])
        except Exception:
            pass
        ctrl["after_id"] = None
