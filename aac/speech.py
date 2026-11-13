import base64
import shutil
import subprocess
import sys

_PS_SCRIPT = r"""
$ErrorActionPreference = 'SilentlyContinue'
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.Rate = {rate}
$s.Volume = {volume}
$v = $s.GetInstalledVoices() | Where-Object {{ $_.Enabled -and $_.VoiceInfo.Culture.Name -like '{lang}*' }} | Select-Object -First 1
if ($v) {{ $s.SelectVoice($v.VoiceInfo.Name) }}
while (($line = [Console]::In.ReadLine()) -ne $null) {{
  if ($line.Length -eq 0) {{ continue }}
  $text = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($line))
  $s.SpeakAsyncCancelAll()
  [void]$s.SpeakAsync($text)
}}
"""


class Speaker(object):
    def __init__(self, enabled=True, language="es", rate=0, volume=100, backend=None):
        self.enabled = bool(enabled)
        self.language = language
        self.rate = int(max(-10, min(10, rate)))
        self.volume = int(max(0, min(100, volume)))
        self.history = []           # lo último que se pidió decir (útil en pruebas)
        self.backend = None         # 'sapi' | 'say' | 'espeak' | 'none'
        self._proc = None
        self._cmd = None
        if not self.enabled:
            self.backend = "none"
            return
        self.backend = backend or self._detect()
        if self.backend == "sapi":
            self._start_sapi()

    # -------------------------------------------------------------- detección
    def _detect(self):
        if sys.platform.startswith("win"):
            return "sapi" if shutil.which("powershell") else "none"
        if sys.platform == "darwin":
            return "say" if shutil.which("say") else "none"
        for name in ("espeak-ng", "espeak", "spd-say"):
            if shutil.which(name):
                self._cmd = name
                return "espeak"
        return "none"

    def _start_sapi(self):
        script = _PS_SCRIPT.format(rate=self.rate, volume=self.volume, lang=self.language)
        enc = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            self._proc = subprocess.Popen(
                ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                 "-EncodedCommand", enc],
                stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=flags)
        except Exception:
            self._proc = None
            self.backend = "none"

    # ------------------------------------------------------------------- voz
    def say(self, text):
        text = (text or "").strip()
        if not text:
            return False
        self.history.append(text)
        del self.history[:-50]
        if not self.enabled or self.backend in (None, "none"):
            return False
        try:
            if self.backend == "sapi" and self._proc is not None:
                line = base64.b64encode(text.encode("utf-8")) + b"\n"
                self._proc.stdin.write(line)
                self._proc.stdin.flush()
                return True
            if self.backend == "say":
                self._spawn(["say", "-v", "Monica" if self.language == "es" else "Samantha", text])
                return True
            if self.backend == "espeak":
                if self._cmd == "spd-say":
                    self._spawn(["spd-say", "-l", self.language, text])
                else:
                    self._spawn([self._cmd, "-v", self.language, text])
                return True
        except Exception:
            return False
        return False

    def _spawn(self, cmd):
        if self._proc is not None and self._proc.poll() is None and self.backend != "sapi":
            try:
                self._proc.terminate()
            except Exception:
                pass
        self._proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def close(self):
        p, self._proc = self._proc, None
        if p is None:
            return
        try:
            if p.stdin:
                p.stdin.close()
            p.terminate()
        except Exception:
            pass
