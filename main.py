import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Teclado de pictogramas con selección por permanencia")
    p.add_argument("--config", default=os.path.join(BASE_DIR, "config.json"), help="ruta de config.json")
    p.add_argument("--input", choices=["mouse", "tobii"], help="entrada: ratón o Tobii (UDP)")
    p.add_argument("--start", help="página inicial (necesidades, personas, acciones, comida, bebida, "
                                   "emociones, lugares, respuestas, salud)")
    p.add_argument("--participant", help="identificador del participante")
    p.add_argument("--session", type=int, help="número de sesión")
    p.add_argument("--dwell", type=int, help="tiempo de permanencia en ms (por defecto el de config.json)")
    p.add_argument("--fullscreen", action="store_true", help="pantalla completa (recomendado con Tobii)")
    p.add_argument("--windowed", action="store_true", help="forzar ventana")
    p.add_argument("--no-speech", action="store_true", help="sin voz")
    p.add_argument("--preview", nargs="?", const="previews", metavar="CARPETA",
                   help="guardar imágenes PNG de cada página y salir")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        import pygame      # noqa: F401
    except ModuleNotFoundError:
        print("Falta pygame. Ejecuta: python -m pip install -r requirements.txt")
        return 1
    from aac.config import load_config
    cfg = load_config(args.config)
    if args.input:
        cfg["input_mode"] = args.input
    if args.participant:
        cfg["participant_id"] = args.participant
    if args.session is not None:
        cfg["sessionID"] = args.session
    if args.dwell:
        cfg["dwell_time_ms"] = args.dwell
    if args.fullscreen:
        cfg["fullscreen"] = True
    if args.windowed:
        cfg["fullscreen"] = False
    if args.no_speech:
        cfg["speech"]["enabled"] = False

    if args.preview:
        from aac.preview import make_previews
        out = args.preview if os.path.isabs(args.preview) else os.path.join(BASE_DIR, args.preview)
        files = make_previews(cfg, BASE_DIR, out)
        print("Se guardaron %d imágenes en %s" % (len(files), out))
        return 0

    from aac.app import App
    App(cfg, BASE_DIR, start=args.start).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
