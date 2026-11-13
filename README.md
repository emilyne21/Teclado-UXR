# Teclado de pictogramas (comunicación aumentativa y alternativa)

Tablero de comunicación con pictogramas, pensado para usarse **sin clic**: la selección se hace
manteniendo el ratón o la mirada (Tobii) sobre una tecla durante un tiempo (*dwell*).

## Qué hay en el tablero

- **Franja superior**: la frase que se va construyendo (hasta 12 pictogramas) y tres botones:
  HABLAR (dice la frase en voz alta), BORRAR (quita el último) y LIMPIAR (vacía la frase).
- **Rejilla central**: los pictogramas de la página actual (5 columnas; las celdas se agrandan
  cuando la página tiene pocas figuras).
- **Columna derecha**: las páginas.

| Página | Contenido |
|---|---|
| NECESIDADES | el tablero original: yo, quiero, comer, beber, ir al baño, dormir, duchar, oír música, ver la tele, pasear, jugar, hablar, leer, ordenador, videojuegos |
| PERSONAS | yo, tú, mamá, papá, hermanos, abuelo, abuela, amigo, profe, médico, niño, niña, bebé |
| ACCIONES | ir, venir, ver, escuchar, dar, abrir, cerrar, esperar, parar, escribir, dibujar, cantar, bailar, correr, lavar las manos, vestirse, sentarse, abrazar… |
| COMIDA | manzana, plátano, uvas, naranja, pan, queso, huevo, pollo, pescado, pasta, sopa, pizza, galleta, helado, zanahoria, tarta, patatas fritas, yogur |
| BEBIDA | agua, leche, zumo, refresco, té, café, colacao, batido |
| EMOCIONES | feliz, reír, triste, enfadado, miedo, sorpresa, cansado, aburrido, cariño, enfermo, tranquilo, nervioso, vergüenza |
| LUGARES | casa, colegio, parque, supermercado, hospital, playa, piscina, cocina, habitación, salón, coche, autobús, baño |
| RESPUESTAS | sí, no, hola, adiós, gracias, por favor, perdón, más, acabado, no sé, bien, mal, ayuda, otra vez |
| SALUD | me duele, cabeza, tripa, garganta, fiebre, medicina, tos, frío, calor, hambre, sed, me he hecho daño |

Ejemplo: mirar **YO → QUIERO → BEBER** y luego **HABLAR** dice «Yo quiero beber.»

Hay imágenes de todas las páginas en `previews/` (y `previews/todos_los_pictogramas.png`).

## Instalación (Windows, CMD)

Con doble clic en `crear_entorno.bat`, o a mano desde la carpeta del proyecto:

```cmd
py -3.9 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Sólo necesita `pygame==2.5.2`. La voz usa las voces de Windows y no requiere nada más.

## Ejecutar

| Archivo | Qué hace |
|---|---|
| `iniciar_mouse.bat` | entrada con el ratón (ventana 1440×900) |
| `iniciar_tobii.bat` | entrada con Tobii, a pantalla completa |
| `vista_previa.bat` | guarda las imágenes en `previews/` |

O por línea de comandos:

```cmd
.venv\Scripts\python.exe main.py --input mouse
.venv\Scripts\python.exe main.py --input tobii --fullscreen
.venv\Scripts\python.exe main.py --input mouse --start comida --participant P03 --session 2 --dwell 1000
.venv\Scripts\python.exe main.py --input mouse --no-speech
```

Opciones: `--config --input --start --participant --session --dwell --fullscreen --windowed --no-speech --preview`.

## Selección por permanencia

- Se activa al mantener el puntero/mirada sobre la tecla `dwell_time_ms` (por defecto **800 ms**,
  más largo que los 500 ms del teclado de letras porque aquí hay que buscar la figura con la vista;
  se cambia en `config.json`, con `--dwell` o con `+` / `-` durante la sesión).
- Sin clic. Mientras se mantiene, la tecla se resalta y una barra muestra el progreso; al
  activarse se pone verde y parpadea.
- No se repite: para volver a elegir la misma tecla hay que salir y volver a entrar.
- Una muestra inválida (sin mirada, `0,0`, o más vieja de 150 ms) reinicia el progreso.
- Hay una pequeña tolerancia (`hysteresis_px`, 14 px) para no perder la tecla si la mirada
  tiembla en el borde.

## Controles del operador

| Tecla | Acción |
|---|---|
| `ENTER` | decir la frase |
| `RETROCESO` / `SUPR` | borrar el último / vaciar la frase |
| `+` / `-` | dwell ±100 ms (200–3000) |
| `1`–`9` | ir a una página |
| `F2` | panel del operador (modo, dwell, posición, estado del Tobii, archivo de registro) |
| `F3` | dibujar un círculo rojo donde está el puntero o la mirada |
| `ESC` | salir |

## Tobii

Misma conexión que el teclado A/B: `gaze_server.exe` envía por UDP a `127.0.0.1:5005` líneas
`TIMESTAMP_US,X_PX,Y_PX` (`0,0` = sin mirada). Al elegir `--input tobii` la aplicación abre el
puerto y, si `tobii.launch_bridge` es `true`, arranca `gaze_server.exe`.

1. Esta carpeta es independiente: **copia la carpeta `sdk_bridge` del proyecto A/B dentro de ésta**
   (o déjala al lado: también se busca en la carpeta superior). Si hay otra ruta, cámbiala en
   `tobii.bridge_executable` y `tobii.bridge_cwd`.
2. Calibra el Tobii con su software.
3. Ejecuta `iniciar_tobii.bat` (pantalla completa, para que la mirada coincida con la ventana).
4. Con `F2` se ve cuántos paquetes llegan y si la mirada es válida; `F3` pinta el punto de mirada.

Si no llegan datos aparece el aviso rojo «SIN SEÑAL DEL TOBII» y se anota `no_signal` en el log.
**No hay respaldo silencioso al ratón.** La mirada fuera de la pantalla no selecciona nada (no se
recorta a los bordes).

`tobii.source_screen_width_px` / `source_screen_height_px` son el tamaño de la pantalla en la que
se mide la mirada; se usan para escalar a la ventana. En `config.json` están en 1920×1200; el
README del teclado A/B menciona 1080 de alto, así que conviene comprobar cuál es el real
(un valor incorrecto desplaza la mirada en vertical).

## Voz

- **Windows**: voz de Windows (SAPI) en español, la primera instalada con idioma `es*`. Funciona
  mediante un PowerShell que queda abierto para que no haya retardo en cada palabra.
- macOS: `say`. Linux: `espeak-ng`, `espeak` o `spd-say` si están instalados.
- `speech.speak_on_select`: dice cada pictograma al elegirlo (útil para confirmar). Con `false`
  sólo habla al pulsar HABLAR.
- `speech.enabled: false` o `--no-speech` para quitar la voz. Si no hay voz disponible, el tablero
  sigue funcionando en silencio (el panel `F2` muestra `voz: none`).

## Registro de la sesión

En `logs/` se crean, por sesión, archivos `.log` con formato CSV:

```text
<participante>_S<sesión>_<fecha>_events.log      t_ms,event,page,target,detail
<participante>_S<sesión>_<fecha>_selections.log  t_ms,seq,page,kind,target,label,dwell_ms,sentence_len,sentence
<participante>_S<sesión>_<fecha>_samples.log     t_ms,x_px,y_px,valid,target
<participante>_S<sesión>_<fecha>_config.json     configuración usada
```

- `selections`: una fila por cada tecla activada (pictograma, página, HABLAR, BORRAR…), con el
  tiempo real de permanencia y la frase en ese momento. `page` es la página en la que estaba la
  tecla.
- `events`: `session_start`, `speak`, `category`, `delete`, `clear`, `dwell_change`, `overlay`,
  `bridge`, `no_signal`, `session_end`.
- `samples`: posición del puntero/mirada cada fotograma (`valid=0` si no había muestra válida o
  estaba fuera de la ventana). Se desactiva con `"log_samples": false`.
- Con Tobii también queda `bridge_output.log` (salida de `gaze_server.exe`).

## Cambiar o añadir pictogramas

- **Qué página muestra qué**: `aac/pages.py`. Basta con poner el id del pictograma en la lista
  `items` (una figura puede estar en varias páginas). Si una página tiene más de 20, se reparte en
  varias con botones ANTERIOR/SIGUIENTE.
- **Dibujos propios**: guarda un PNG (de preferencia cuadrado y con fondo transparente) en
  `assets/pictograms/` con el nombre del id (`comer.png`, `bano.png`…) y se usa en lugar del
  dibujo incluido. Los ids están en `picto/set_*.py`.
- **Dibujar uno nuevo**: añadir una función con `@icon("id", "ETIQUETA", "texto que dice la voz")`
  en `picto/set_*.py` (ver `picto/draw.py` para las primitivas) y ponerlo en `aac/pages.py`.
- Si usas pictogramas de **ARASAAC** (https://arasaac.org): licencia CC BY-NC-SA; hay que citar
  autoría (Gobierno de Aragón, autor Sergio Palao), no usarlos con fines comerciales y compartir
  con la misma licencia.

## Estructura

```text
main.py               línea de comandos
config.json           configuración
aac/                  app.py (ventana y bucle), board.py (distribución y acciones), pages.py (contenido),
                      dwell.py, gaze.py (UDP Tobii), speech.py, logger.py, preview.py, config.py
picto/                dibujo de los pictogramas (draw.py + set_*.py)
assets/pictograms/    PNG propios opcionales
tests/                pruebas
previews/             imágenes de cada página
logs/                 registros (se crea sola)
```

