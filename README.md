# Mejoras para el port nativo de Naruto Storm 3 Full Burst (Android)

Parche **no oficial** para el [port nativo de Naruto Shippuden: Ultimate Ninja Storm 3 Full Burst](https://github.com/Masterllgod/naruto-storm-3-full-burst-port-nativo), creado por **Masterllgod**. Todo el mérito del port (que el juego corra en Android) es suyo. Las mejoras se le propusieron en [este issue](https://github.com/Masterllgod/naruto-storm-3-full-burst-port-nativo/issues/21).

> **Este repositorio no trae el juego ni la app.** Trae un programa que toma la app original (que bajas del repo del autor) y le agrega las mejoras en tu computadora.

## ¿Qué agrega?

| Mejora | Qué vas a ver |
|---|---|
| **App en español** | Todos los menús y avisos de la app, que venían en portugués. |
| **Idioma del juego** | Opción **"Idioma del texto": English · Español · Français**. El juego americano ya traía español, pero la app siempre lo mostraba en inglés. |
| **45 FPS** | El selector **FPS** de la app (20 · 24 · 30) suma la opción **45**. Usa **30** para jugar normal: 45 se ve más fluido, pero el juego va **1.5x más rápido**. |
| **Salir del juego** | Dentro del juego, al tocar el **emblema** (el ícono de Shadow), aparece **"Salir del juego"**. |
| **Ocultar los controles** | **Emblema → "Ocultar controles"** oculta de un toque todos los botones táctiles **y el analógico** (como el ícono de la v0.3.1); **"Mostrar controles"** los devuelve. Deslizar para mover la cámara sigue funcionando. En **Editar botones** también está **"Ocultar todos"** sin selección, o "Ocultar" para uno solo (ahora también el analógico). Lo oculto no responde al toque. |
| **Exportar el save** | En **"Save del juego"**, debajo de **Importar**, el botón **"Exportar"** guarda una copia de tu partida (`STORM3FB.S`) donde elijas: Descargas, Google Drive, etc. Sirve como respaldo o para pasarla a otro celular. |
| **Sin actualización automática** | La app original busca versiones nuevas e intenta instalar la oficial, que tiene otra firma y no se puede instalar encima. Aquí está desactivado: actualiza con este repo. |

Basado en la app original **v0.5.4**.

---

# Guía paso a paso

Vas a necesitar:
- Una **computadora con Windows** (más abajo hay notas para Linux y Mac).
- Tu **celular Android** con el juego ya funcionando en la app original, o al menos con la carpeta del juego copiada.
- Un **cable USB** para conectar el celular a la computadora.
- Unos **30 minutos** la primera vez.

## Paso 1. Respalda tu partida (no te lo saltes)

Para instalar la versión mejorada hay que **desinstalar la app original**, y **Android borra tus partidas al desinstalar**. Primero haz una copia:

1. Conecta el celular a la computadora con el cable USB.
2. En el celular, baja la barra de notificaciones, toca el aviso de USB y elige **"Transferencia de archivos"** (o "MTP").
3. En la computadora, abre el **Explorador de archivos** y entra a tu celular → **Almacenamiento interno** → `Android` → `data` → `com.naruto.storm3`.
4. Copia la carpeta **`files`** completa a tu computadora, por ejemplo al Escritorio, en una carpeta llamada `respaldo-naruto`.
5. Comprueba que dentro de la copia exista un archivo llamado **`STORM3FB.S`** (está dentro de `files\data\content\...`). Esa es tu partida.

> Si no ves la carpeta `com.naruto.storm3`, abre la app original una vez y vuelve a intentarlo. Si nunca jugaste, no hay nada que respaldar y puedes seguir.

## Paso 2. Instala Python y Java en la computadora

El programa que aplica las mejoras necesita **Python** y **Java (JDK)**. Se instalan una sola vez.

**Python:**
1. Entra a https://www.python.org/downloads/ y toca el botón amarillo **"Download Python 3.x"**.
2. Abre el instalador. **Muy importante:** en la primera pantalla marca la casilla **"Add python.exe to PATH"**, y luego toca **"Install Now"**.

**Java (JDK):**
1. Entra a https://adoptium.net/temurin/releases/?os=windows&package=jdk&version=21
2. Descarga el archivo **`.msi`** de la versión **21** para **Windows x64**.
3. Abre el instalador. En la pantalla de opciones, busca **"Set JAVA_HOME variable"** y cámbiala a **"Will be installed on local hard drive"**. Luego sigue con **"Next"** hasta terminar.

**Comprueba que quedaron bien instalados:**
1. Presiona la tecla **Windows**, escribe `cmd` y presiona **Enter**. Se abre una ventana negra (la "terminal").
2. Escribe `python --version` y presiona Enter. Debe responder algo como `Python 3.12.x`.
3. Escribe `javac -version` y presiona Enter. Debe responder algo como `javac 21.0.x`.

> Si alguno dice *"no se reconoce como un comando"*, cierra la ventana negra y abre una nueva (los programas recién instalados no aparecen en ventanas que ya estaban abiertas). Si sigue igual, reinicia la computadora. Ver también [Problemas comunes](#problemas-comunes).

## Paso 3. Descarga la app original

1. Entra a la página de descargas del autor: https://github.com/Masterllgod/naruto-storm-3-full-burst-port-nativo/releases
2. En la versión **v0.5.4**, descarga **`NarutoStorm3FullBurst-PortNativo-v0.5.4-arm64.apk`**.
3. Déjalo en tu carpeta **Descargas**.

> Solo sirve **ese archivo exacto**. El programa lo comprueba solo y te avisa si es otro.

> ⚠️ **Bájalo solo de esa página.** Circulan copias reempaquetadas de la app (por ejemplo `Naruto-Storm-3-FB-v0.5.4.apk`, 22.6 MB) con un **menú de trucos inyectado y código ofuscado** de un tercero. No son del autor y no se puede saber qué más hacen.

## Paso 4. Descarga este repositorio

1. Arriba en esta página, toca el botón verde **"<> Code"** y luego **"Download ZIP"**.
2. Ve a tu carpeta **Descargas**, haz clic derecho sobre `descompilatorgame-main.zip` → **"Extraer todo..."** → **"Extraer"**.
3. Se crea la carpeta `descompilatorgame-main`. Ábrela: deben verse las carpetas `patcher`, `cpk-idioma` y `docs`.

## Paso 5. Crea la app mejorada

1. Dentro de la carpeta `descompilatorgame-main`, haz clic en la **barra de direcciones** del Explorador (arriba, donde dice la ruta), escribe `cmd` y presiona **Enter**. Se abre la ventana negra ya ubicada en esa carpeta.
2. Copia este comando, pégalo en la ventana negra (clic derecho pega) y presiona **Enter**:

   ```
   python patcher\build.py "%USERPROFILE%\Downloads\NarutoStorm3FullBurst-PortNativo-v0.5.4-arm64.apk"
   ```

3. Espera de 1 a 3 minutos. La primera vez descarga unas herramientas (unos 25 MB). Debe verse algo así:

   ```
   1/5 desarmando el APK...
   descargando apktool.jar...
   2/5 aplicando traduccion y funciones nuevas...
   3/5 armando el APK...
   4/5 compilando el selector de idioma...
   descargando r8.jar...
   5/5 firmando...
   descargando uber-apk-signer.jar...
   listo: NarutoStorm3FullBurst-PortNativo-v0.5.4-arm64-mejoras.apk
   ```

4. Cuando diga **`listo`**, en la carpeta `descompilatorgame-main` aparece el archivo **`NarutoStorm3FullBurst-PortNativo-v0.5.4-arm64-mejoras.apk`**. Esa es tu app mejorada.

> Si aparece una línea que empieza con **`ERROR:`**, mira [Problemas comunes](#problemas-comunes).

## Paso 6. Instala la app mejorada en el celular

1. Con el celular conectado por USB (en "Transferencia de archivos"), copia `NarutoStorm3FullBurst-PortNativo-v0.5.4-arm64-mejoras.apk` a la carpeta **Download** del celular. También puedes mandártelo por Google Drive o Telegram.
2. **Desinstala la app original:** en el celular, mantén presionado el ícono de la app → **Desinstalar**. (Ya respaldaste tu partida en el Paso 1.)
   > Si ya tenías instalada una versión anterior **hecha con este repo**, no hace falta desinstalar: la nueva se instala encima y conserva tus partidas.
3. Abre la app **Archivos** (o "Mis archivos") del celular, entra a **Download** y toca el archivo `...-mejoras.apk`.
4. Si Android dice que por seguridad no se permite instalar apps de esa fuente, toca **"Configuración"**, activa **"Permitir de esta fuente"**, vuelve atrás y toca **"Instalar"**.
5. Abre la app. Igual que con la original, elige la carpeta del juego con **ELEGIR CARPETA** y dale permiso de acceso a los archivos.

## Paso 7. Recupera tu partida

1. Copia tu archivo **`STORM3FB.S`** del respaldo (Paso 1) a la carpeta **Download** del celular.
2. En la app, toca **"Importar save"** → **"Elegir archivo"** y elige ese `STORM3FB.S`.
3. Debe aparecer el aviso **"Save importado"**.

> **Para las próximas veces:** con esta versión ya no hace falta conectar el celular a la PC para respaldar. En **"Save del juego" → "Exportar"** guardas la partida donde quieras, y la recuperas con **"Importar"**.

## Paso 8. Elige idioma y FPS, y juega

1. En la pantalla de inicio, en **"Idioma del texto"**, toca **Español** (viene seleccionado por defecto).
2. En **"FPS"**, deja **30** para jugar a velocidad normal.
3. Toca **JUGAR**. Los textos del juego salen en español (las voces no cambian).
4. Para salir: dentro del juego toca el **emblema** → **"Salir del juego"** → **"Salir"**.

> Si al tocar Jugar aparece **"ya viene modificado: pon el original del juego para poder elegir idioma"**, los archivos `dataRegion.cpk` o `dlc.cpk` de tu carpeta del juego no son los originales (alguien ya los cambió). Vuelve a copiar esos dos archivos desde tu copia original del juego, a la carpeta `data/disc` del juego en el celular.

---

## Problemas comunes

| Mensaje o problema | Qué hacer |
|---|---|
| `"python" no se reconoce como un comando` | Reinstala Python marcando **"Add python.exe to PATH"** (Paso 2). Como alternativa, usa `py` en lugar de `python` en el comando del Paso 5. |
| Se abre la **Microsoft Store** al escribir `python` | Python no quedó instalado o no está en el PATH. Repite la instalación del Paso 2. |
| `ERROR: no encuentro 'javac'` | Instalaste solo Java (JRE) o no se configuró `JAVA_HOME`. Instala el **JDK 21 `.msi`** del Paso 2 activando **"Set JAVA_HOME variable"**, cierra la ventana negra y abre una nueva. |
| `ERROR: ese APK no es el v0.5.4 arm64 original` | El archivo no es el correcto, o está incompleto. Descárgalo de nuevo desde el Paso 3, sin renombrarlo ni modificarlo. |
| `ERROR: ... no coincide con el hash esperado` | Una descarga de herramientas salió mal (internet inestable). Ejecuta el mismo comando otra vez. |
| `ERROR: no se pudo descargar` / error de conexión | Revisa tu internet o el antivirus/firewall y vuelve a intentar. |
| En el celular: **"App no instalada"** | Seguramente la app original sigue instalada. Desinstálala (Paso 6.2) y vuelve a instalar. |
| La app se cierra al abrir el juego | Abre la app → **"Enviar log"** y repórtalo en los [issues de este repo](https://github.com/Willd233/descompilatorgame/issues) con el modelo de tu celular. |
| El juego va muy rápido | Elegiste **45 FPS**. Cambia a **30 FPS**. |
| Perdí mi partida | Si hiciste el Paso 1, impórtala con el Paso 7. Si no, Android la borró al desinstalar y no se puede recuperar. |

---

## Linux y macOS

Todo es igual, salvo los Pasos 2, 4 y 5:
- **Paso 2:** instala Python 3.10+ y un JDK 17+. Por ejemplo, en Ubuntu/Debian: `sudo apt install python3 openjdk-21-jdk`; en macOS con Homebrew: `brew install python openjdk@21`.
- **Paso 4:** extrae el ZIP con doble clic.
- **Paso 5:** abre una terminal en la carpeta extraída y ejecuta:
  ```sh
  python3 patcher/build.py ~/Downloads/NarutoStorm3FullBurst-PortNativo-v0.5.4-arm64.apk
  ```

---

## Información técnica

<details>
<summary>Cómo funciona por dentro (para desarrolladores)</summary>

### El parche (`patcher/build.py`)
1. Comprueba el SHA-256 del APK original (`563acc3dc264f156d45d95e8292fb778f70e73c13b5f84b9dda8b0f51aae623f`, v0.5.4 arm64).
2. Descarga apktool 3.0.3, uber-apk-signer 1.3.0 y D8 (R8 8.13.25) desde sus fuentes oficiales y verifica sus hashes.
3. Desarma el APK (`apktool d -r`), traduce los `const-string` PT→ES ([translate_es.py](patcher/translate_es.py)) y aplica los cambios al smali. Cada cambio exige encontrar su fragmento exacto **una sola vez**; si no lo encuentra, se detiene en vez de parchear a ciegas.
4. Reemplaza 4 textos del motor en `libmain.so` por traducciones del **mismo largo en bytes**, para no mover nada en `.rodata`, y quita el filtro de `frame_rate` (ver abajo). Los parches nativos se buscan por contenido, no por dirección.
5. Compila [LangPatcher.java](patcher/java/com/naruto/port/LangPatcher.java) a `classes2.dex` (minSdk 29, multidex nativo), arma el APK y lo firma con la clave de depuración de uber-apk-signer.

### Selector de FPS
El launcher le pasa al motor `frame_rate`, que es el **vblank** de la Xbox 360 emulada. El juego presenta 1 frame cada 2 vblanks: 40 → 20 FPS, 48 → 24 FPS, 60 → 30 FPS, 90 → 45 FPS. La lógica del juego avanza por frame, por eso 45 FPS acelera el juego 1.5x.

El selector del autor (etiquetas `w`, valores `x`, preferencia `menu_fps`) suma la cuarta opción: 45 → 90, y el índice máximo pasa de 2 a 3.

El motor filtraba el valor al leer `naruto.ini`: solo aceptaba **40, 48, 60 o 120**, y cualquier otro valor pasaba a 60. Por eso 90 terminaba en 30 FPS:

```
cmp  w0, #40 ; ccmp w0, #48 ; mov w8, #60
csel w8, w0, w8, eq        ; 40 o 48 pasan, si no -> 60
cmp  w0, #120 ; csel w8, w8, w9, lt   ; >= 120 -> 120
```

El parche cambia ese `csel` por `mov w8, w0`, así que cualquier valor menor a 120 pasa tal cual y el tope de 120 se mantiene.

### Selector de idioma
El disco NTSC-U (`default.xex` v9, SHA-1 `f7ad65e2…`) trae `eng`, `spa` y `fre` en `data/disc/dataRegion.cpk` (770 archivos por idioma) y `dlc.cpk` (39). En consola, el juego elige la carpeta según `XamGetLanguage`; el port siempre reporta inglés.

Al tocar Jugar, `LangPatcher` reescribe **solo el TOC** (tabla `@UTF`) de esos CPK, para que las entradas `eng` apunten a los datos del idioma elegido (`FileOffset`, `FileSize` y `ExtractSize`). Los datos no se tocan. La primera vez guarda el TOC original en `getFilesDir()`, junto con el tamaño del CPK para detectar si cambiaste de archivo. Si encuentra un CPK ya redirigido y no tiene respaldo, se niega a modificarlo.

### Herramienta para PC: `cpk-idioma/cpk_lang.py`
Hace la misma redirección sin el APK. Sirve para cualquier emulador o port que use el disco NTSC-U:
```sh
python cpk-idioma/cpk_lang.py dataRegion.cpk dataRegion_es.cpk --de eng --a spa
python cpk-idioma/cpk_lang.py dlc.cpk dlc_es.cpk --de eng --a spa
```
Si el CPK destino no trae el idioma, se le puede pasar como tercer argumento un CPK de otra región, y los textos se copian al final del archivo.

### Estado
- El APK que genera el script es idéntico byte a byte al que se armó y verificó a mano.
- El selector de idioma se probó en PC con los CPK reales: español, inglés (vuelve exactamente al original) y francés.
- Falta probarlo a fondo en dispositivos.
</details>

---

## Aviso legal

- Este repositorio **no distribuye** la app del autor ni archivos del juego. Necesitas tu propia copia del juego y descargar la app original desde el repo del autor.
- La [licencia MIT](LICENSE) de este repositorio cubre **solo el código propio de este repositorio** (scripts, smali y Java). No cubre el port de Naruto Storm 3 Full Burst ni sus binarios, que pertenecen a su autor, ni el juego, que pertenece a sus titulares.
- Si el autor del port pide retirar este parche, se retira.
