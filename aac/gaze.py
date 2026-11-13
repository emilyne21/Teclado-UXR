import os
import socket
import subprocess
import sys
import time


def now_ms():
    return time.monotonic() * 1000.0


def parse_packet(data):
    """Devuelve (ts_us, x, y) o None si el paquete no es válido."""
    try:
        text = data.decode("ascii", "ignore").strip()
        parts = text.split(",")
        if len(parts) != 3:
            return None
        ts = int(parts[0])
        x = float(parts[1])
        y = float(parts[2])
        if x != x or y != y:        # NaN
            return None
        return ts, x, y
    except (ValueError, UnicodeError):
        return None


class GazeReceiver(object):
    def __init__(self, ip="127.0.0.1", port=5005, src_w=1920, src_h=1200,
                 stale_ms=150, zero_invalid=True, clock=now_ms):
        self.ip, self.port = ip, int(port)
        self.src_w, self.src_h = float(src_w), float(src_h)
        self.stale_ms = float(stale_ms)
        self.zero_invalid = zero_invalid
        self.clock = clock
        self.sock = None
        self.last_x = None
        self.last_y = None
        self.last_rx_ms = None      # instante de la última muestra recibida (válida o no)
        self.last_valid = False     # la última muestra era válida
        self.packets = 0
        self.bad_packets = 0
        self.started_ms = None

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.setblocking(False)
        self.sock = s
        self.started_ms = self.clock()

    def close(self):
        if self.sock is not None:
            try:
                self.sock.close()
            finally:
                self.sock = None

    def feed(self, data, rx_ms=None):
        """Procesa un paquete (también lo usan las pruebas)."""
        rx = self.clock() if rx_ms is None else rx_ms
        parsed = parse_packet(data)
        if parsed is None:
            self.bad_packets += 1
            return False
        _, x, y = parsed
        self.packets += 1
        self.last_rx_ms = rx
        if self.zero_invalid and x == 0 and y == 0:
            self.last_valid = False
            return True
        self.last_x, self.last_y = x, y
        self.last_valid = True
        return True

    def poll(self):
        """Vacía el socket; devuelve cuántos paquetes llegaron."""
        n = 0
        if self.sock is None:
            return n
        while True:
            try:
                data, _ = self.sock.recvfrom(256)
            except (BlockingIOError, InterruptedError):
                break
            except OSError:
                break
            self.feed(data)
            n += 1
        return n

    def sample(self, now=None):
        """(x, y) en píxeles de la pantalla de origen, o None si no hay mirada válida y fresca."""
        now = self.clock() if now is None else now
        if not self.last_valid or self.last_rx_ms is None:
            return None
        if now - self.last_rx_ms > self.stale_ms:
            return None
        return self.last_x, self.last_y

    def to_window(self, xy, size):
        """Escala de la pantalla de origen a la ventana (sin recortar: fuera = fuera)."""
        return xy[0] * size[0] / self.src_w, xy[1] * size[1] / self.src_h

    def silent_for_ms(self, now=None):
        """Tiempo sin recibir ningún paquete (para avisar de 'sin señal')."""
        now = self.clock() if now is None else now
        ref = self.last_rx_ms if self.last_rx_ms is not None else self.started_ms
        return float("inf") if ref is None else now - ref


def resolve_bridge(tobii_cfg, base_dir):
    """Busca gaze_server.exe: ruta de config y las carpetas superiores (por si sdk_bridge está al lado)."""
    exe = tobii_cfg.get("bridge_executable", "")
    for prefix in ("", "..", os.path.join("..", "..")):
        root = os.path.normpath(os.path.join(base_dir, prefix))
        p = exe if os.path.isabs(exe) else os.path.join(root, exe)
        if os.path.isfile(p):
            cwd = tobii_cfg.get("bridge_cwd") or ""
            cwd = cwd if os.path.isabs(cwd) else os.path.join(root, cwd)
            if not os.path.isdir(cwd):
                cwd = os.path.dirname(p)
            return p, cwd
    return None, None


def launch_bridge(tobii_cfg, base_dir, log_path):
    """Arranca gaze_server.exe. Devuelve el Popen o None (y el motivo)."""
    exe, cwd = resolve_bridge(tobii_cfg, base_dir)
    if exe is None:
        return None, ("No encuentro %s. Copia la carpeta sdk_bridge junto a esta carpeta, "
                      "cambia bridge_executable en config.json o inicia gaze_server.exe a mano." %
                      tobii_cfg.get("bridge_executable"))
    out = open(log_path, "ab")
    kw = {}
    if sys.platform.startswith("win"):
        kw["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.Popen([exe], cwd=cwd, stdout=out, stderr=subprocess.STDOUT, **kw)
    return proc, "gaze_server.exe iniciado (pid %d)" % proc.pid
