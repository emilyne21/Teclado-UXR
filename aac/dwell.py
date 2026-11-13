
class DwellTracker(object):
    def __init__(self, dwell_ms):
        self.dwell_ms = int(dwell_ms)
        self.reset()

    def reset(self):
        self.target = None      # uid de la tecla en la que está el puntero
        self.t_enter = None     # instante (ms) en que entró
        self.fired = False      # ya se activó mientras sigue dentro

    def set_dwell(self, dwell_ms):
        self.dwell_ms = int(dwell_ms)

    def update(self, now_ms, target, valid=True):
        """Actualiza con el objetivo actual. Devuelve 'select' al completar el dwell."""
        if not valid or target is None:
            self.reset()
            return None
        if target != self.target:
            self.target = target
            self.t_enter = now_ms
            self.fired = False
            return None
        if not self.fired and now_ms - self.t_enter >= self.dwell_ms:
            self.fired = True
            return "select"
        return None

    def elapsed(self, now_ms):
        if self.target is None:
            return 0
        return max(0, now_ms - self.t_enter)

    def progress(self, now_ms):
        """0..1 (1 si ya se activó y el puntero no ha salido)."""
        if self.target is None:
            return 0.0
        if self.fired:
            return 1.0
        return min(1.0, self.elapsed(now_ms) / float(self.dwell_ms))
