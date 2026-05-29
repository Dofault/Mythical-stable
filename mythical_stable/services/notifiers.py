


class ScrollNotifier:
    def notify(self, message: str):
        print(f"📜 [SCROLL] {message}")

class MirrorNotifier:
    def notify(self, message: str):
        with open("mirror_log.txt", "a") as file:
            file.write(f"🪞 [MIRROR] {message}\n")

class SilentNotifier:
    def notify(self, message: str) -> None:
        pass  # delivers nothing

class SilentLogger:
    def unknown1(self):
        ...

class ConsoleMissionLogger:
    def unknown2(self):
        ...
