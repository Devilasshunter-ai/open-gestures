import subprocess
from actions.base import BaseAction
from actions.system import system

class PauseMedia(BaseAction):
    name = "Pause Media"
    description = "Pause system media"
    id = "pause_media"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
            try:
                subprocess.Popen(
                    ["playerctl", "play"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys=="win":
            #code here
            print("hi")
        elif sys=="mac":
            #code here
            print("hie")
