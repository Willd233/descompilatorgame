"""Aplica las mejoras sobre el APK original del port de Naruto Storm 3 Full Burst.

No incluye nada del port: toma el APK que el usuario bajo del repo del autor,
lo desarma, aplica los cambios de este repo, lo vuelve a armar y lo firma.

Uso:  python build.py <NarutoStorm3FullBurst-PortNativo-v0.3.1-arm64.apk> [-o salida.apk]
Requiere: JDK 17+ (java y javac en el PATH o en JAVA_HOME).
"""
import argparse, hashlib, os, pathlib, shutil, subprocess, sys, urllib.request, zipfile

import translate_es

HERE = pathlib.Path(__file__).resolve().parent
TOOLS = HERE / ".tools"
BUILD = HERE / "build"

APK_SHA256 = "89fda15b1c4b0b5338ecc31d90655ea7b4f63a4dbcfaa327446b8078f29dc847"  # v0.3.1 arm64

DOWNLOADS = {  # nombre: (url, algoritmo, hash)
    "apktool.jar": ("https://github.com/iBotPeaches/Apktool/releases/download/v3.0.3/apktool_3.0.3.jar",
                    "sha256", "dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423"),
    "uber-apk-signer.jar": ("https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar",
                            "sha256", "e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835"),
    "r8.jar": ("https://dl.google.com/android/maven2/com/android/tools/r8/8.13.25/r8-8.13.25.jar",
               "sha1", "bd7564f5058d382e9c488ed7d3140c13a2c50e86"),
}

LAUNCHER = "smali/com/naruto/port/LauncherActivity.smali"
GAME = "smali/com/naruto/port/NarutoActivity.smali"

# (archivo, fragmento original exacto, reemplazo). Cada fragmento debe aparecer una sola vez.
EDITS = [
    # aplicar el idioma elegido justo antes de lanzar el juego
    (LAUNCHER,
     ".method public final q()V\n    .locals 16\n\n    move-object/from16 v0, p0\n",
     ".method public final q()V\n    .locals 16\n\n    move-object/from16 v0, p0\n\n"
     "    invoke-virtual {v0}, Lcom/naruto/port/LauncherActivity;->applyLanguage()V\n"),
    # filas "FPS del juego" e "Idioma del texto" debajo de Pantalla / Antialiasing / Escala
    (LAUNCHER,
     "    invoke-virtual {v0, v1}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V\n\n    new-instance v1, La/c;\n",
     "    invoke-virtual {v0, v1}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V\n\n"
     "    invoke-virtual {v7, v0}, Lcom/naruto/port/LauncherActivity;->addFpsRow(Landroid/view/ViewGroup;)V\n\n"
     "    invoke-virtual {v7, v0}, Lcom/naruto/port/LauncherActivity;->addLangRow(Landroid/view/ViewGroup;)V\n\n"
     "    new-instance v1, La/c;\n"),
    # frame_rate (vblank) segun el FPS elegido, salvo con el modo rendimiento
    (LAUNCHER,
     '    :cond_6\n    const-string v6, "60"\n\n    :goto_5',
     "    :cond_6\n    iget-object v6, v0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;\n\n"
     "    invoke-static {v6}, Lcom/naruto/port/LauncherActivity;->fpsRate(Landroid/content/SharedPreferences;)Ljava/lang/String;\n\n"
     "    move-result-object v6\n\n    :goto_5"),
    # boton "Salir del juego" en el panel de la tuerca
    (GAME,
     "    iput v2, v0, Landroid/widget/FrameLayout$LayoutParams;->topMargin:I\n\n"
     "    iget-object v2, p0, Lcom/naruto/port/NarutoActivity;->editorPanel:Landroid/widget/LinearLayout;\n",
     "    iput v2, v0, Landroid/widget/FrameLayout$LayoutParams;->topMargin:I\n\n"
     "    invoke-direct {p0}, Lcom/naruto/port/NarutoActivity;->addExitButton()V\n\n"
     "    iget-object v2, p0, Lcom/naruto/port/NarutoActivity;->editorPanel:Landroid/widget/LinearLayout;\n"),
]

# metodos nuevos: archivo destino -> (insertar antes de esta linea, bloque en smali_methods/)
METHODS = {
    LAUNCHER: (".method public final c(Landroid/view/View;FI)V", "LauncherActivity.smali"),
    GAME: (".method private dp(F)I", "NarutoActivity.smali"),
}

# textos del codigo nativo: mismo largo en bytes, para no mover nada en .rodata
NATIVE = {
    "\nCPU jogo %.0f%% (%.0f%% de %ld nucleos)": "\nCPU juego: %.0f%% (%.0f%% de %ld nucl.)",
    "O jogo encontrou um erro e vai fechar.\n\n": "El juego tuvo un error y ahora cierra.\n\n",
    "A pasta do jogo não tem o default.xex:\n": "A esta carpeta le falta el default.xex:\n",
}


def fail(msg):
    sys.exit(f"ERROR: {msg}")


def digest(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def jdk_tool(name):
    home = os.environ.get("JAVA_HOME")
    exe = name + (".exe" if os.name == "nt" else "")
    path = pathlib.Path(home, "bin", exe) if home else shutil.which(name)
    if not path or not pathlib.Path(path).exists():
        fail(f"no encuentro '{name}'. Instala un JDK 17+ o define JAVA_HOME.")
    return str(path)


def tool(name):
    url, algo, expected = DOWNLOADS[name]
    path = TOOLS / name
    if not path.exists():
        TOOLS.mkdir(exist_ok=True)
        print(f"descargando {name}...")
        urllib.request.urlretrieve(url, path)
    if digest(path, algo) != expected:
        path.unlink()
        fail(f"{name} no coincide con el hash esperado; se borro, vuelve a intentar.")
    return str(path)


def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"fallo: {' '.join(cmd[:3])}...\n{r.stdout}\n{r.stderr}")


def patch_smali(app):
    missing = translate_es.apply(app / "smali")
    if missing:
        fail(f"textos que no aparecieron en el APK (otra version?): {sorted(missing)[:3]}")

    for rel, old, new in EDITS:
        f = app / rel
        text = f.read_text(encoding="utf-8")
        if text.count(old) != 1:
            fail(f"el fragmento a parchear aparece {text.count(old)} veces en {rel}")
        f.write_text(text.replace(old, new), encoding="utf-8", newline="\n")

    for rel, (anchor, block) in METHODS.items():
        f = app / rel
        text = f.read_text(encoding="utf-8")
        if text.count(anchor) != 1:
            fail(f"no encuentro '{anchor}' en {rel}")
        code = (HERE / "smali_methods" / block).read_text(encoding="utf-8")
        f.write_text(text.replace(anchor, code + anchor), encoding="utf-8", newline="\n")

    shutil.copytree(HERE / "smali", app / "smali", dirs_exist_ok=True)


def patch_native(app):
    so = app / "lib/arm64-v8a/libmain.so"
    data = bytearray(so.read_bytes())
    for old, new in NATIVE.items():
        o, n = old.encode(), new.encode()
        assert len(o) == len(n), new
        key = o + b"\0"
        if data.count(key) != 1:
            fail(f"texto nativo no encontrado: {old.strip()!r}")
        i = data.index(key)
        data[i:i + len(o)] = n
    so.write_bytes(bytes(data))


def build_lang_dex(java, javac):
    classes, dex = BUILD / "classes", BUILD / "dex"
    for d in (classes, dex):
        d.mkdir(parents=True, exist_ok=True)
    run(javac, "--release", "8", "-nowarn", "-d", str(classes), str(HERE / "java/com/naruto/port/LangPatcher.java"))
    run(java, "-cp", tool("r8.jar"), "com.android.tools.r8.D8", "--release", "--min-api", "29",
        "--output", str(dex), *map(str, classes.rglob("*.class")))
    return dex / "classes.dex"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("apk", help="APK original v0.3.1 arm64 del repo del autor")
    ap.add_argument("-o", "--output", default="NarutoStorm3FullBurst-PortNativo-v0.3.1-arm64-mejoras.apk")
    a = ap.parse_args()

    if digest(a.apk, "sha256") != APK_SHA256:
        fail("ese APK no es el v0.3.1 arm64 original; este parche solo sirve para esa version exacta.")
    java, javac = jdk_tool("java"), jdk_tool("javac")

    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir()
    app = BUILD / "app"
    print("1/5 desarmando el APK...")
    run(java, "-jar", tool("apktool.jar"), "d", "-r", "-f", a.apk, "-o", str(app))
    print("2/5 aplicando traduccion y funciones nuevas...")
    patch_smali(app)
    patch_native(app)
    print("3/5 armando el APK...")
    unsigned = BUILD / "unsigned.apk"
    run(java, "-jar", tool("apktool.jar"), "b", str(app), "-o", str(unsigned))
    print("4/5 compilando el selector de idioma...")
    with zipfile.ZipFile(unsigned, "a", zipfile.ZIP_DEFLATED) as z:
        z.write(build_lang_dex(java, javac), "classes2.dex")
    print("5/5 firmando...")
    signed = BUILD / "signed"
    run(java, "-jar", tool("uber-apk-signer.jar"), "-a", str(unsigned), "-o", str(signed))
    out = next(signed.glob("*.apk"))
    shutil.copyfile(out, a.output)
    print(f"listo: {a.output}")


if __name__ == "__main__":
    main()
