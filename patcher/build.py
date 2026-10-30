"""Aplica las mejoras sobre el APK original del port de Naruto Storm 3 Full Burst.

No incluye nada del port: toma el APK que el usuario bajo del repo del autor,
lo desarma, aplica los cambios de este repo, lo vuelve a armar y lo firma.

Uso:  python build.py <NarutoStorm3FullBurst-PortNativo-v0.4.7-arm64.apk> [-o salida.apk]
Requiere: JDK 17+ (java y javac en el PATH o en JAVA_HOME).
"""
import argparse, hashlib, os, pathlib, re, shutil, struct, subprocess, sys, urllib.request, zipfile

import translate_es

HERE = pathlib.Path(__file__).resolve().parent
TOOLS = HERE / ".tools"
BUILD = HERE / "build"

VERSION = "v0.6.10"
APK_SHA256 = "74d6973ffe3c1a32d9ec1edb341aa1427b8086850fe3df17b902e3816e6c7f08"  # v0.6.10 arm64

# El APK viene ofuscado y los nombres cortos cambian entre versiones. Nuestro smali usa estos
# marcadores; verify_refs() comprueba al armar que cada metodo/campo del autor que usamos exista.
NAMES = {
    "@CTRL@": "La/f0;",        # capa de controles tactiles (tiene setSelectedOff)
    "@BTN_CLS@": "La/c0;",     # un boton tactil (flag de oculto en p)
    "@EDIT_IF@": "La/d0;",     # interfaz que avisa al editor: a(String;FZZ)V
    "@EMB_MENU@": "La/Y;",     # arma el PopupMenu del emblema
    "@EMB_CLICK@": "La/X;",    # onMenuItemClick de ese menu
    "@SEL@": "La/W;",          # selector segmentado del menu (setCompact)
    "@SEL_LIS@": "La/V;",      # su interfaz de listener
    "@FPS_LIS@": "La/r;",      # listener de los selectores (caso "menu_fps")
    "@CTRL_ACC@": "access$1700",  # NarutoActivity -> capa de controles
    "@TOAST@": "k",            # LauncherActivity: aviso k(String)V
    "@PULSE@": "h",            # LauncherActivity: animacion h(View)V
    "@WRAP@": "j",             # LauncherActivity: fila j(View[])
    "@ROW@": "q",              # LauncherActivity: fila de selector q(String, View)
    "@BTN@": "g",              # LauncherActivity: boton g(String, int, int)
    "@DP@": "b",               # LauncherActivity: dp -> px
}


def subst(text):
    for k, v in NAMES.items():
        text = text.replace(k, v)
    left = re.findall(r"@[A-Z_]+@", text)
    if left:
        fail(f"marcadores sin definir en NAMES: {sorted(set(left))}")
    return text

DOWNLOADS = {  # nombre: (url, algoritmo, hash)
    "apktool.jar": ("https://github.com/iBotPeaches/Apktool/releases/download/v3.0.3/apktool_3.0.3.jar",
                    "sha256", "dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423"),
    "uber-apk-signer.jar": ("https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar",
                            "sha256", "e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835"),
    "r8.jar": ("https://dl.google.com/android/maven2/com/android/tools/r8/8.13.25/r8-8.13.25.jar",
               "sha1", "bd7564f5058d382e9c488ed7d3140c13a2c50e86"),
}

LAUNCHER = "Lcom/naruto/port/LauncherActivity;"
GAME = "Lcom/naruto/port/NarutoActivity;"
CONTROLLER_MAP = "Lcom/naruto/port/ControllerMapActivity;"  # pantalla MAPEAR
CONTROLS = "@CTRL@"        # capa de controles tactiles (botones en a:[@BTN_CLS@], seleccionado en p)
FPS_LISTENER = "@FPS_LIS@"     # listener de los selectores del menu (caso FPS)
EMBLEM_MENU = "@EMB_MENU@"      # arma el menu del emblema del Shadow (dentro del juego)
EMBLEM_CLICK = "@EMB_CLICK@"     # atiende los toques de ese menu

# (clase, fragmento original exacto, reemplazo). Cada fragmento debe aparecer una sola vez.
EDITS = [
    # FPS: agregar 45 al selector del autor (etiquetas w y valores frame_rate x)
    (LAUNCHER,
     '    const-string v0, "30"\n\n    const-string v1, "20"\n\n    const-string v2, "24"\n\n'
     "    filled-new-array {v1, v2, v0}, [Ljava/lang/String;",
     '    const-string v0, "30"\n\n    const-string v1, "20"\n\n    const-string v2, "24"\n\n'
     '    const-string v3, "45"\n\n    filled-new-array {v1, v2, v0, v3}, [Ljava/lang/String;'),
    (LAUNCHER,
     '    const-string v0, "60"\n\n    const-string v1, "40"\n\n    const-string v2, "48"\n\n'
     "    filled-new-array {v1, v2, v0}, [Ljava/lang/String;",
     '    const-string v0, "60"\n\n    const-string v1, "40"\n\n    const-string v2, "48"\n\n'
     '    const-string v3, "90"\n\n    filled-new-array {v1, v2, v0, v3}, [Ljava/lang/String;'),
    # el indice de FPS se limitaba a 2 (tres opciones) en el menu y al lanzar el juego
    (LAUNCHER,
     "    move-result v5\n\n    invoke-static {v11, v5}, Ljava/lang/Math;->min(II)I",
     "    move-result v5\n\n    const/4 v6, 0x3\n\n    invoke-static {v6, v5}, Ljava/lang/Math;->min(II)I"),
    # al lanzar: v13 (valor por defecto) se reutiliza; v3 (las preferencias) se pisa con 0 justo despues
    (LAUNCHER,
     "    move-result v2\n\n    invoke-static {v13, v2}, Ljava/lang/Math;->min(II)I",
     "    move-result v2\n\n    const/4 v3, 0x3\n\n    invoke-static {v3, v2}, Ljava/lang/Math;->min(II)I"),
    # efecto de particulas del selector de FPS: 4 opciones en vez de 3
    (FPS_LISTENER,
     '    const-string v2, "menu_fps"\n\n'
     "    invoke-interface {v1, v2, p1}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;\n\n"
     "    move-result-object v1\n\n    invoke-interface {v1}, Landroid/content/SharedPreferences$Editor;->apply()V\n\n"
     "    int-to-float v1, p1\n\n    const/high16 v2, 0x3f000000    # 0.5f\n\n    add-float/2addr v1, v2\n\n    const/4 v2, 0x3",
     '    const-string v2, "menu_fps"\n\n'
     "    invoke-interface {v1, v2, p1}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;\n\n"
     "    move-result-object v1\n\n    invoke-interface {v1}, Landroid/content/SharedPreferences$Editor;->apply()V\n\n"
     "    int-to-float v1, p1\n\n    const/high16 v2, 0x3f000000    # 0.5f\n\n    add-float/2addr v1, v2\n\n    const/4 v2, 0x4"),
    # fila "Idioma del texto" debajo de Resolucion / FPS
    (LAUNCHER,
     "    :cond_b\n    invoke-virtual {v8, v1}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V\n",
     "    :cond_b\n    invoke-virtual {v8, v1}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V\n\n"
     "    invoke-virtual {v7, v8}, Lcom/naruto/port/LauncherActivity;->addLangRow(Landroid/view/ViewGroup;)V\n"),
    # el interruptor PT-BR del autor queda oculto: el portugues es una opcion de nuestro selector
    (LAUNCHER,
     "    invoke-virtual {v7, v2, v4, v1}, Lcom/naruto/port/LauncherActivity;->p(Ljava/lang/String;Ljava/lang/String;La/c;)Landroid/widget/LinearLayout;\n\n"
     "    move-result-object v2\n",
     "    invoke-virtual {v7, v2, v4, v1}, Lcom/naruto/port/LauncherActivity;->p(Ljava/lang/String;Ljava/lang/String;La/c;)Landroid/widget/LinearLayout;\n\n"
     "    move-result-object v2\n\n    const/16 v4, 0x8\n\n    invoke-virtual {v2, v4}, Landroid/view/View;->setVisibility(I)V\n"),
    # aplicar el idioma justo antes de lanzar el juego (aca la actividad esta en v1)
    (LAUNCHER,
     ".method public final t()V\n    .locals 22\n\n    move-object/from16 v1, p0\n",
     ".method public final t()V\n    .locals 22\n\n    move-object/from16 v1, p0\n\n"
     "    invoke-virtual {v1}, Lcom/naruto/port/LauncherActivity;->applyLanguage()V\n"),
    # sin actualizacion automatica: instalaria el APK oficial, que tiene otra firma
    (LAUNCHER,
     '    const-string v0, "update check"\n\n'
     "    invoke-direct {v1, v4, v0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V\n\n"
     "    invoke-virtual {v1}, Ljava/lang/Thread;->start()V\n",
     '    const-string v0, "update check"\n\n'
     "    invoke-direct {v1, v4, v0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V\n"),
    # menu del emblema (el autor usa los ids 1-6): "Ocultar/Mostrar controles" (id 7) y "Salir del juego" (id 8),
    # al final. v1 = 0 (grupo); v3 = el emblema (una View)
    (EMBLEM_MENU,
     '    const-string v0, "Ocultar a Shadow"\n\n'
     "    invoke-interface {p1, v1, p2, v7, v0}, Landroid/view/Menu;->add(IIILjava/lang/CharSequence;)Landroid/view/MenuItem;\n\n"
     "    new-instance p1, @EMB_CLICK@\n",
     '    const-string v0, "Ocultar a Shadow"\n\n'
     "    invoke-interface {p1, v1, p2, v7, v0}, Landroid/view/Menu;->add(IIILjava/lang/CharSequence;)Landroid/view/MenuItem;\n\n"
     "    invoke-virtual {v3}, Landroid/view/View;->getContext()Landroid/content/Context;\n\n"
     "    move-result-object p2\n\n    check-cast p2, Lcom/naruto/port/NarutoActivity;\n\n"
     "    invoke-static {p2}, Lcom/naruto/port/NarutoActivity;->@CTRL_ACC@(Lcom/naruto/port/NarutoActivity;)@CTRL@\n\n"
     "    move-result-object p2\n\n    if-eqz p2, :cond_hide_item_end\n\n"
     "    invoke-virtual {p2}, @CTRL@->allOff()Z\n\n    move-result p2\n\n"
     "    invoke-virtual {p0}, Landroid/widget/PopupMenu;->getMenu()Landroid/view/Menu;\n\n"
     "    move-result-object p1\n\n    if-eqz p2, :cond_hide_item_label\n\n"
     '    const-string v0, "Mostrar controles"\n\n    goto :goto_hide_item\n\n'
     '    :cond_hide_item_label\n    const-string v0, "Ocultar controles"\n\n'
     "    :goto_hide_item\n    const/4 p2, 0x7\n\n"
     "    invoke-interface {p1, v1, p2, p2, v0}, Landroid/view/Menu;->add(IIILjava/lang/CharSequence;)Landroid/view/MenuItem;\n\n"
     "    :cond_hide_item_end\n"
     "    invoke-virtual {p0}, Landroid/widget/PopupMenu;->getMenu()Landroid/view/Menu;\n\n"
     "    move-result-object p1\n\n    const/16 p2, 0x8\n\n"
     '    const-string v0, "Salir del juego"\n\n'
     "    invoke-interface {p1, v1, p2, p2, v0}, Landroid/view/Menu;->add(IIILjava/lang/CharSequence;)Landroid/view/MenuItem;\n\n"
     "    new-instance p1, @EMB_CLICK@\n"),
    # v0 = id tocado, v1 = 1 (lo que se retorna); v4/v5 se vuelven a cargar antes del codigo original.
    # Ambas opciones terminan en :goto_4 como las del autor (devuelve la transparencia al emblema).
    (EMBLEM_CLICK,
     "    const/4 v4, 0x4\n\n    const/4 v5, 0x0\n\n    if-eq v0, v2, :cond_5\n",
     "    const/4 v4, 0x7\n\n    if-ne v0, v4, :cond_hide_no\n\n"
     "    invoke-virtual {p0}, Landroid/view/View;->getContext()Landroid/content/Context;\n\n"
     "    move-result-object v4\n\n    check-cast v4, Lcom/naruto/port/NarutoActivity;\n\n"
     "    invoke-static {v4}, Lcom/naruto/port/NarutoActivity;->@CTRL_ACC@(Lcom/naruto/port/NarutoActivity;)@CTRL@\n\n"
     "    move-result-object v4\n\n    if-eqz v4, :goto_4\n\n"
     "    invoke-virtual {v4}, @CTRL@->toggleAll()V\n\n    goto :goto_4\n\n"
     "    :cond_hide_no\n    const/16 v4, 0x8\n\n    if-ne v0, v4, :cond_exit_no\n\n"
     "    invoke-virtual {p0}, Landroid/view/View;->getContext()Landroid/content/Context;\n\n"
     "    move-result-object v4\n\n    check-cast v4, Landroid/app/Activity;\n\n"
     "    new-instance v5, Lcom/naruto/port/ExitHelper;\n\n"
     "    invoke-direct {v5, v4}, Lcom/naruto/port/ExitHelper;-><init>(Landroid/app/Activity;)V\n\n"
     "    invoke-virtual {v5, p0}, Lcom/naruto/port/ExitHelper;->onClick(Landroid/view/View;)V\n\n"
     "    goto :goto_4\n\n"
     "    :cond_exit_no\n    const/4 v4, 0x4\n\n    const/4 v5, 0x0\n\n    if-eq v0, v2, :cond_5\n"),
    # MAPEAR solo reconoce los codigos estandar (BUTTON_A, L1, DPAD...). Los controles genericos
    # mandan otros (BUTTON_1..16, C, Z) y se ignoraban en silencio: ahora se avisa cual llego.
    # v0 = viene de un control, v2 = boton reconocido o null. Si avisamos, v2 queda null y el
    # flujo original sigue igual (no lo reconoce y se lo pasa a Android).
    (CONTROLLER_MAP,
     "    :goto_1\n    if-eqz v0, :cond_6\n\n    if-eqz v2, :cond_6\n",
     "    :goto_1\n    if-eqz v0, :cond_diag_end\n\n    if-nez v2, :cond_diag_end\n\n"
     "    invoke-virtual {p1}, Landroid/view/KeyEvent;->getAction()I\n\n    move-result v3\n\n"
     "    if-nez v3, :cond_diag_end\n\n"
     "    invoke-virtual {p1}, Landroid/view/KeyEvent;->getKeyCode()I\n\n    move-result v3\n\n"
     # teclas del telefono: atras, volumen, encendido, silencio
     "    const/4 v2, 0x4\n\n    if-eq v3, v2, :cond_diag_skip\n\n"
     "    const/16 v2, 0x18\n\n    if-eq v3, v2, :cond_diag_skip\n\n"
     "    const/16 v2, 0x19\n\n    if-eq v3, v2, :cond_diag_skip\n\n"
     "    const/16 v2, 0x1a\n\n    if-eq v3, v2, :cond_diag_skip\n\n"
     "    const/16 v2, 0xa4\n\n    if-eq v3, v2, :cond_diag_skip\n\n"
     "    new-instance v2, Ljava/lang/StringBuilder;\n\n"
     '    const-string v0, "Bot\\u00f3n no reconocido por MAPEAR: "\n\n'
     "    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V\n\n"
     "    invoke-static {v3}, Landroid/view/KeyEvent;->keyCodeToString(I)Ljava/lang/String;\n\n"
     "    move-result-object v0\n\n"
     "    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n\n"
     '    const-string v0, " (c\\u00f3digo "\n\n'
     "    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n\n"
     "    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;\n\n"
     '    const-string v0, ")"\n\n'
     "    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n\n"
     "    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;\n\n"
     "    move-result-object v2\n\n    const/4 v0, 0x1\n\n"
     "    invoke-static {p0, v2, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;\n\n"
     "    move-result-object v2\n\n    invoke-virtual {v2}, Landroid/widget/Toast;->show()V\n\n"
     "    :cond_diag_skip\n    const/4 v0, 0x0\n\n    const/4 v2, 0x0\n\n"
     "    :cond_diag_end\n    if-eqz v0, :cond_6\n\n    if-eqz v2, :cond_6\n"),
    # boton "Exportar" debajo de "Importar" en la fila del save
    (LAUNCHER,
     "    invoke-virtual {v1, v3, v4}, Landroid/view/ViewGroup;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V\n\n"
     '    const-string v4, "Save del juego"\n',
     "    invoke-virtual {v7, v1, v3, v4, v5}, Lcom/naruto/port/LauncherActivity;->addSaveButtons("
     "Landroid/widget/LinearLayout;Landroid/widget/TextView;Landroid/widget/LinearLayout$LayoutParams;I)V\n\n"
     '    const-string v4, "Save del juego"\n'),
    # el resultado de "Guardar como" (codigo 0x4e53) lo atiende handleSaveExport
    (LAUNCHER,
     ".method public final onActivityResult(IILandroid/content/Intent;)V\n    .locals 2\n\n"
     "    invoke-super {p0, p1, p2, p3}, Landroid/app/Activity;->onActivityResult(IILandroid/content/Intent;)V\n",
     ".method public final onActivityResult(IILandroid/content/Intent;)V\n    .locals 2\n\n"
     "    invoke-super {p0, p1, p2, p3}, Landroid/app/Activity;->onActivityResult(IILandroid/content/Intent;)V\n\n"
     "    invoke-virtual {p0, p1, p2, p3}, Lcom/naruto/port/LauncherActivity;->handleSaveExport(IILandroid/content/Intent;)Z\n\n"
     "    move-result v0\n\n    if-eqz v0, :cond_not_export\n\n    return-void\n\n    :cond_not_export\n"),
    # analogico ocultable: estado propio, guardado en las preferencias de los controles
    (CONTROLS,
     ".field public final a:[@BTN_CLS@\n",
     ".field public analogOff:Z\n\n.field public final a:[@BTN_CLS@\n"),
    (CONTROLS,
     "    iput-object v1, v0, @CTRL@->e:Landroid/content/SharedPreferences;\n\n"
     "    invoke-virtual/range {p0 .. p0}, @CTRL@->i()V\n",
     "    iput-object v1, v0, @CTRL@->e:Landroid/content/SharedPreferences;\n\n"
     "    invoke-virtual/range {p0 .. p0}, @CTRL@->i()V\n\n"
     '    const-string v2, "analog_hidden"\n\n    const/4 v3, 0x0\n\n'
     "    invoke-interface {v1, v2, v3}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z\n\n"
     "    move-result v2\n\n    iput-boolean v2, v0, @CTRL@->analogOff:Z\n"),
    # con el analogico seleccionado en el editor, "Ocultar/Mostrar" ahora aplica a el
    (CONTROLS,
     '    const-string v0, "Anal\\u00f3gico"\n\n    iget p0, p0, @CTRL@->h:F\n\n'
     "    invoke-interface {v1, v0, p0, v2, v2}, @EDIT_IF@->a(Ljava/lang/String;FZZ)V\n",
     '    const-string v0, "Anal\\u00f3gico"\n\n    iget-boolean v2, p0, @CTRL@->analogOff:Z\n\n'
     "    const/4 v3, 0x1\n\n    iget p0, p0, @CTRL@->h:F\n\n"
     "    invoke-interface {v1, v0, p0, v2, v3}, @EDIT_IF@->a(Ljava/lang/String;FZZ)V\n"),
    # oculto: no se dibuja el joystick...
    (CONTROLS,
     "    :goto_3\n    invoke-virtual/range {p0 .. p1}, @CTRL@->g(Landroid/graphics/Canvas;)V\n",
     "    :goto_3\n    iget-boolean v2, v0, @CTRL@->analogOff:Z\n\n    if-nez v2, :cond_analog_hidden\n\n"
     "    invoke-virtual/range {p0 .. p1}, @CTRL@->g(Landroid/graphics/Canvas;)V\n\n    :cond_analog_hidden\n"),
    # ...y un toque en su zona no lo toma (queda como zona vacia)
    (CONTROLS,
     "    :cond_18\n    iget v13, v0, @CTRL@->k:F\n",
     "    :cond_18\n    iget-boolean v13, v0, @CTRL@->analogOff:Z\n\n    if-nez v13, :cond_19\n\n"
     "    iget v13, v0, @CTRL@->k:F\n"),
    # editor de botones: "Ocultar" sin seleccion oculta/muestra todos (antes quedaba desactivado)
    (GAME,
     "    iget-object p1, p0, Lcom/naruto/port/NarutoActivity;->controls:@CTRL@\n\n"
     "    iget-boolean p0, p0, Lcom/naruto/port/NarutoActivity;->selectionOff:Z\n\n"
     "    xor-int/lit8 p0, p0, 0x1\n\n    invoke-virtual {p1, p0}, @CTRL@->setSelectedOff(Z)V\n",
     "    iget-object p1, p0, Lcom/naruto/port/NarutoActivity;->controls:@CTRL@\n\n"
     "    invoke-virtual {p1}, @CTRL@->toggleHide()V\n"),
    (GAME,
     ".method private updateEditorPanel(Ljava/lang/String;FZZ)V\n    .locals 3\n",
     ".method private updateEditorPanel(Ljava/lang/String;FZZ)V\n    .locals 5\n\n"
     "    move-object v3, p0\n\n    move-object v4, p1\n"),
    (GAME,
     "    invoke-virtual {p0, p1}, Landroid/view/View;->setAlpha(F)V\n\n    return-void\n.end method",
     "    invoke-virtual {p0, p1}, Landroid/view/View;->setAlpha(F)V\n\n"
     "    if-nez v4, :cond_hide_end\n\n"
     "    iget-object v1, v3, Lcom/naruto/port/NarutoActivity;->controls:@CTRL@\n\n"
     "    if-eqz v1, :cond_hide_end\n\n"
     "    iget-object v0, v3, Lcom/naruto/port/NarutoActivity;->hideButton:Landroid/widget/TextView;\n\n"
     "    const/4 v2, 0x1\n\n    invoke-virtual {v0, v2}, Landroid/widget/TextView;->setEnabled(Z)V\n\n"
     "    const/high16 v2, 0x3f800000    # 1.0f\n\n    invoke-virtual {v0, v2}, Landroid/view/View;->setAlpha(F)V\n\n"
     "    invoke-virtual {v1}, @CTRL@->allOff()Z\n\n    move-result v1\n\n"
     "    if-eqz v1, :cond_hide_all\n\n"
     '    const-string v1, "Mostrar todos"\n\n    goto :goto_hide_text\n\n'
     "    :cond_hide_all\n"
     '    const-string v1, "Ocultar todos"\n\n'
     "    :goto_hide_text\n"
     "    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V\n\n"
     "    :cond_hide_end\n    return-void\n.end method"),
]

# metodos nuevos: clase -> (insertar antes de esta linea, bloque en smali_methods/)
METHODS = {
    LAUNCHER: (".method public final c(Landroid/view/View;FI)V", "LauncherActivity.smali"),
    CONTROLS: (".method public setSelectedOff(Z)V", "Controls.smali"),
}

# textos del codigo nativo: mismo largo en bytes, para no mover nada en .rodata
NATIVE = {
    "\nCPU jogo %.0f%% (%.0f%% de %ld nucleos)": "\nCPU juego: %.0f%% (%.0f%% de %ld nucl.)",
    "O jogo encontrou um erro e vai fechar.\n\n": "El juego tuvo un error y ahora cierra.\n\n",
    "A pasta do jogo não tem o default.xex:\n": "A esta carpeta le falta el default.xex:\n",
    "Este celular nao e suportado: a GPU nao tem o que o renderizador precisa.\n\nVolte ao menu e toque em ENVIAR LOG PARA O SHADOW.":
        "Este celular no es compatible: a su GPU le falta lo que necesita el renderizador.\n\nVuelve al menu y toca ENVIAR LOG A SHADOW.",
}

# El motor solo aceptaba frame_rate 40, 48, 60 o 120 (cualquier otro valor -> 60).
# Se cambia el `csel` del filtro por `mov w8, w0` para que pase 90 (45 FPS); 120 sigue siendo el tope.
FRAME_RATE_FILTER = [0x7100A01F, 0x52800608, 0x52800F09, 0x7A481004, 0x52800788, 0x1A880008, 0x7101E01F, 0x1A89B108]
FRAME_RATE_FIX = (5, 0x2A0003E8)  # (posicion en la secuencia, instruccion nueva)


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
        try:
            urllib.request.urlretrieve(url, path)
        except OSError as e:
            path.unlink(missing_ok=True)
            fail(f"no se pudo descargar {name} ({e}). Revisa tu internet y vuelve a intentar.")
    if digest(path, algo) != expected:
        path.unlink()
        fail(f"{name} no coincide con el hash esperado; se borro, vuelve a intentar.")
    return str(path)


def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"fallo: {' '.join(cmd[:3])}...\n{r.stdout}\n{r.stderr}")


def class_files(app):
    """descriptor de clase -> archivo .smali (el nombre del archivo cambia segun el sistema de archivos)."""
    files = {}
    for f in (app / "smali").rglob("*.smali"):
        with open(f, encoding="utf-8") as fh:
            files[fh.readline().split()[-1]] = f
    return files


def patch_smali(app):
    missing = translate_es.apply(app / "smali")
    if missing:
        fail(f"textos que no aparecieron en el APK (otra version?): {sorted(missing)[:3]}")

    files = class_files(app)
    ours = []  # todo el codigo que agregamos, para verify_refs
    for cls, old, new in EDITS:
        cls, old, new = subst(cls), subst(old), subst(new)
        f = files[cls]
        text = f.read_text(encoding="utf-8")
        if text.count(old) != 1:
            fail(f"el fragmento a parchear aparece {text.count(old)} veces en {cls}: {old.strip().splitlines()[0]!r}")
        f.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
        ours.append(new)

    for cls, (anchor, block) in METHODS.items():
        cls = subst(cls)
        f = files[cls]
        text = f.read_text(encoding="utf-8")
        if text.count(anchor) != 1:
            fail(f"no encuentro '{anchor}' en {cls}")
        code = subst((HERE / "smali_methods" / block).read_text(encoding="utf-8"))
        f.write_text(text.replace(anchor, code + anchor), encoding="utf-8", newline="\n")
        ours.append(code)

    for src in (HERE / "smali").rglob("*.smali"):
        dst = app / "smali" / src.relative_to(HERE / "smali")
        dst.parent.mkdir(parents=True, exist_ok=True)
        code = subst(src.read_text(encoding="utf-8"))
        dst.write_text(code, encoding="utf-8", newline="\n")
        ours.append(code)

    verify_refs(app, ours)


def verify_refs(app, ours):
    """Cada clase, metodo y campo del autor que usa nuestro codigo tiene que existir en esta version.
    Sin esto, un nombre cambiado compila igual y la app se cierra recien en el celular."""
    files = class_files(app)
    defs = {}
    for cls, f in files.items():
        if cls.startswith(("Lcom/naruto/port/", "La/")):
            defs[cls] = set(re.findall(r"^\.(?:method|field) .*? ([\w$<>]+(?:\(.*?\)\S+|:\S+))", f.read_text(encoding="utf-8"), re.M))
    # nuestras clases Java van aparte en classes2.dex
    java = {"L" + p.relative_to(HERE / "java").with_suffix("").as_posix() + ";" for p in (HERE / "java").rglob("*.java")}
    bad = set()
    for code in ours:
        for cls in re.findall(r"(L(?:com/naruto/port|a)/[\w$/]+;)", code):
            if cls not in defs and cls not in java:
                bad.add(f"clase {cls}")
        for cls, member in re.findall(r"(L(?:com/naruto/port|a)/[\w$/]+;)->([\w$<>]+(?:\([^)]*\)\S+|:[^\s,}]+))", code):
            if cls in defs and member not in defs[cls]:
                bad.add(f"{cls}->{member}")
    if bad:
        fail("el codigo del parche usa cosas que no existen en esta version del APK:\n  " + "\n  ".join(sorted(bad)))


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

    seq = struct.pack(f"<{len(FRAME_RATE_FILTER)}I", *FRAME_RATE_FILTER)
    if data.count(seq) != 1:
        fail("no encuentro el filtro de frame_rate en libmain.so")
    pos, insn = FRAME_RATE_FIX
    struct.pack_into("<I", data, data.index(seq) + 4 * pos, insn)
    so.write_bytes(bytes(data))


def build_java_dex(java, javac):
    """Compila el codigo Java propio (idioma, exportar save) a un dex aparte."""
    classes, dex = BUILD / "classes", BUILD / "dex"
    for d in (classes, dex):
        d.mkdir(parents=True, exist_ok=True)
    run(javac, "--release", "8", "-nowarn", "-d", str(classes), *map(str, (HERE / "java").rglob("*.java")))
    run(java, "-cp", tool("r8.jar"), "com.android.tools.r8.D8", "--release", "--min-api", "29",
        "--output", str(dex), *map(str, classes.rglob("*.class")))
    return dex / "classes.dex"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("apk", help=f"APK original {VERSION} arm64 del repo del autor")
    ap.add_argument("-o", "--output", default=f"NarutoStorm3FullBurst-PortNativo-{VERSION}-arm64-mejoras.apk")
    a = ap.parse_args()

    if digest(a.apk, "sha256") != APK_SHA256:
        fail(f"ese APK no es el {VERSION} arm64 original; este parche solo sirve para esa version exacta.")
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
    print("4/5 compilando el codigo Java (idioma y save)...")
    with zipfile.ZipFile(unsigned, "a", zipfile.ZIP_DEFLATED) as z:
        z.write(build_java_dex(java, javac), "classes2.dex")
    print("5/5 firmando...")
    signed = BUILD / "signed"
    run(java, "-jar", tool("uber-apk-signer.jar"), "-a", str(unsigned), "-o", str(signed))
    out = next(signed.glob("*.apk"))
    shutil.copyfile(out, a.output)
    print(f"listo: {a.output}")


if __name__ == "__main__":
    main()
