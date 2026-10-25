# Mejoras para el port nativo de Naruto Storm 3 Full Burst (Android)

Parche **no oficial** para el [port nativo de Naruto Shippuden: Ultimate Ninja Storm 3 Full Burst](https://github.com/Masterllgod/naruto-storm-3-full-burst-port-nativo), creado por **Masterllgod**. Todo el mérito del port (recompilación, motor y gráficos) es suyo.

Este repo **no incluye el APK ni archivos del juego**. Contiene solo un script que toma el APK original, que bajas del repo del autor, y le aplica las mejoras.

## Mejoras

| Mejora | Detalle |
|---|---|
| App en español | Todos los menús y avisos de la app traducidos del portugués (117 textos + 3 mensajes del motor). |
| Idioma del texto del juego | Selector **English · Español · Français**. El disco NTSC-U ya trae los tres idiomas; el port siempre mostraba inglés. |
| FPS del juego | Selector **24 · 30 · 45 FPS**. 30 es la velocidad normal; 45 se ve más fluido pero el juego va 1.5x más rápido (la lógica está atada a los frames). |
| Salir del juego | Botón "Salir del juego" en el menú de la tuerca, con confirmación. |

## Requisitos

- El APK original **v0.3.1 arm64** del repo del autor:
  `SHA-256 89fda15b1c4b0b5338ecc31d90655ea7b4f63a4dbcfaa327446b8078f29dc847`
- Python 3.10+
- JDK 17+ (`java` y `javac` en el PATH, o `JAVA_HOME` definido)

El script descarga apktool 3.0.3, uber-apk-signer 1.3.0 y D8 (R8 8.13.25) desde sus fuentes oficiales y verifica sus hashes.

## Uso

```sh
python patcher/build.py NarutoStorm3FullBurst-PortNativo-v0.3.1-arm64.apk
```

Genera `NarutoStorm3FullBurst-PortNativo-v0.3.1-arm64-mejoras.apk`.

**Al instalar:** el APK queda firmado con otra clave, así que Android no lo instala encima del original. Respalda tus saves y la configuración, desinstala el original e instala el nuevo.

## Idioma del texto: cómo funciona

El juego pide sus textos en la carpeta `eng` dentro de `data/disc/dataRegion.cpk` y `dlc.cpk`. Al tocar **Jugar**, la app reescribe solo el índice de esos CPK (unos KB al inicio) para que las entradas `eng` apunten a los datos `spa` o `fre`. Los datos del juego no se modifican, y la primera vez se guarda el índice original en la memoria privada de la app, así que siempre se puede volver al inglés.

- Usa los **CPK originales** de tu copia NTSC-U. Si ya están modificados, la app avisa y no toca nada.
- Solo cambian los textos y subtítulos; las voces quedan igual.

### Herramienta independiente: `cpk-idioma/cpk_lang.py`

Hace lo mismo desde la PC, sin el APK. Sirve para cualquier emulador o port que use el disco NTSC-U:

```sh
python cpk-idioma/cpk_lang.py dataRegion.cpk dataRegion_es.cpk --de eng --a spa
python cpk-idioma/cpk_lang.py dlc.cpk dlc_es.cpk --de eng --a spa
```

Si el CPK destino no trae el idioma, se le puede pasar un CPK de otra región como tercer argumento para copiar esos textos.

## Estado

- El APK que genera el script es idéntico, byte a byte, al que se armó y verificó a mano.
- El selector de idioma se probó en PC con los CPK reales: español, inglés (vuelve exactamente al original) y francés.
- **Falta probarlo a fondo en dispositivos.** Si algo falla, abre un issue con el modelo del celular y el log ("Enviar log").

## Aviso legal

- No se distribuye el port ni el juego. Necesitas tu propio APK original y tu propia copia del juego.
- La licencia MIT de este repo cubre solo el código propio de este repo.
- Si el autor del port pide retirar este parche, se retira.
