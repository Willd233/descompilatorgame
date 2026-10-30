.method public final applyLanguage()V
    .locals 6

    iget-object v0, p0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;

    const-string v1, "gameDirectory"

    const/4 v2, 0x0

    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const-string v2, "menu_lang"

    const/4 v3, 0x1

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result v2

    # 3 = Portugues: lo resuelve el motor del autor (idioma de consola, preferencia menu_ptbr) y
    # los CPK quedan originales. Los demas idiomas los resuelve el indice de los CPK.
    const/4 v3, 0x3

    if-ne v2, v3, :cond_not_pt

    const/4 v3, 0x1

    goto :goto_pt

    :cond_not_pt
    const/4 v3, 0x0

    :goto_pt
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v4

    const-string v5, "menu_ptbr"

    invoke-interface {v4, v5, v3}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;

    move-result-object v4

    invoke-interface {v4}, Landroid/content/SharedPreferences$Editor;->apply()V

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v3

    invoke-static {v1, v2, v3}, Lcom/naruto/port/LangPatcher;->apply(Ljava/lang/String;ILjava/io/File;)Ljava/lang/String;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {p0, v0}, Lcom/naruto/port/LauncherActivity;->@TOAST@(Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method public final addLangRow(Landroid/view/ViewGroup;)V
    .locals 5

    const-string v0, "English"

    const-string v1, "Español"

    const-string v2, "Français"

    const-string v3, "Português"

    filled-new-array {v0, v1, v2, v3}, [Ljava/lang/String;

    move-result-object v0

    iget-object v1, p0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;

    const-string v2, "menu_lang"

    const/4 v3, 0x1

    invoke-interface {v1, v2, v3}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result v1

    new-instance v2, @SEL@

    const/4 v4, 0x0

    invoke-direct {v2, p0, v0, v4, v1}, @SEL@-><init>(Lcom/naruto/port/LauncherActivity;[Ljava/lang/String;[Ljava/lang/String;I)V

    invoke-virtual {v2, v3}, @SEL@->setCompact(Z)V

    const-string v0, "Idioma del texto"

    invoke-virtual {p0, v0, v2}, Lcom/naruto/port/LauncherActivity;->@ROW@(Ljava/lang/String;Landroid/view/View;)Landroid/widget/LinearLayout;

    move-result-object v0

    new-instance v1, Lcom/naruto/port/LangListener;

    invoke-direct {v1, p0, v0}, Lcom/naruto/port/LangListener;-><init>(Lcom/naruto/port/LauncherActivity;Landroid/widget/LinearLayout;)V

    invoke-virtual {v2, v1}, @SEL@->setListener(@SEL_LIS@)V

    new-array v1, v3, [Landroid/view/View;

    aput-object v0, v1, v4

    invoke-virtual {p0, v1}, Lcom/naruto/port/LauncherActivity;->@WRAP@([Landroid/view/View;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {p1, v0}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V

    return-void
.end method

.method public final addSaveButtons(Landroid/widget/LinearLayout;Landroid/widget/TextView;Landroid/widget/LinearLayout$LayoutParams;I)V
    .locals 5

    # columna con "Importar" (el original) y "Exportar" debajo, mismo estilo y ancho
    new-instance v0, Landroid/widget/LinearLayout;

    invoke-direct {v0, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setOrientation(I)V

    invoke-virtual {v0, p2, p3}, Landroid/view/ViewGroup;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    const-string v1, "Exportar"

    const v2, -0xa193c

    invoke-virtual {p0, v1, v2, p4}, Lcom/naruto/port/LauncherActivity;->@BTN@(Ljava/lang/String;II)Landroid/widget/TextView;

    move-result-object v1

    invoke-virtual {p2}, Landroid/widget/TextView;->getTextSize()F

    move-result v2

    const/4 v3, 0x0

    invoke-virtual {v1, v3, v2}, Landroid/widget/TextView;->setTextSize(IF)V

    new-instance v2, Landroid/widget/LinearLayout$LayoutParams;

    invoke-direct {v2, p3}, Landroid/widget/LinearLayout$LayoutParams;-><init>(Landroid/widget/LinearLayout$LayoutParams;)V

    const/high16 v3, 0x40c00000    # 6.0f

    invoke-virtual {p0, v3}, Lcom/naruto/port/LauncherActivity;->@DP@(F)I

    move-result v3

    iput v3, v2, Landroid/view/ViewGroup$MarginLayoutParams;->topMargin:I

    invoke-virtual {v0, v1, v2}, Landroid/view/ViewGroup;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    new-instance v2, Lcom/naruto/port/SaveExportClick;

    invoke-direct {v2, p0}, Lcom/naruto/port/SaveExportClick;-><init>(Lcom/naruto/port/LauncherActivity;)V

    invoke-virtual {v1, v2}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    new-instance v2, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v3, -0x2

    invoke-direct {v2, v3, v3}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    invoke-virtual {p1, v0, v2}, Landroid/view/ViewGroup;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    return-void
.end method

.method public final startSaveExport()V
    .locals 3

    invoke-static {p0}, La/l;->d(Landroid/content/Context;)Ljava/io/File;

    move-result-object v0

    if-nez v0, :cond_0

    const-string v0, "Todav\u00eda no hay save para exportar."

    invoke-virtual {p0, v0}, Lcom/naruto/port/LauncherActivity;->@TOAST@(Ljava/lang/String;)V

    return-void

    # "Guardar como" de Android: el usuario elige carpeta y nombre
    :cond_0
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.CREATE_DOCUMENT"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    const-string v1, "android.intent.category.OPENABLE"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    const-string v1, "application/octet-stream"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    const-string v1, "android.intent.extra.TITLE"

    const-string v2, "STORM3FB.S"

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    const v1, 0x4e53

    :try_start_0
    invoke-virtual {p0, v0, v1}, Landroid/app/Activity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end_0
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    const-string v0, "No hay una app para guardar archivos en este celular."

    invoke-virtual {p0, v0}, Lcom/naruto/port/LauncherActivity;->@TOAST@(Ljava/lang/String;)V

    return-void
.end method

.method public final handleSaveExport(IILandroid/content/Intent;)Z
    .locals 4

    const v0, 0x4e53

    if-eq p1, v0, :cond_0

    const/4 v0, 0x0

    return v0

    :cond_0
    const/4 v0, -0x1

    if-ne p2, v0, :cond_done

    if-eqz p3, :cond_done

    invoke-virtual {p3}, Landroid/content/Intent;->getData()Landroid/net/Uri;

    move-result-object v0

    if-eqz v0, :cond_done

    invoke-static {p0}, La/l;->d(Landroid/content/Context;)Ljava/io/File;

    move-result-object v1

    if-nez v1, :cond_1

    const-string v0, "Todav\u00eda no hay save para exportar."

    goto :goto_msg

    :cond_1
    :try_start_0
    invoke-virtual {p0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v2

    const-string v3, "wt"

    invoke-virtual {v2, v0, v3}, Landroid/content/ContentResolver;->openOutputStream(Landroid/net/Uri;Ljava/lang/String;)Ljava/io/OutputStream;

    move-result-object v2
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    if-nez v2, :cond_2

    const-string v0, "No se pudo abrir el destino."

    goto :goto_msg

    :cond_2
    invoke-static {v1, v2}, Lcom/naruto/port/SaveExporter;->copy(Ljava/io/File;Ljava/io/OutputStream;)Ljava/lang/String;

    move-result-object v0

    if-nez v0, :goto_msg

    const-string v0, "Save exportado: STORM3FB.S"

    goto :goto_msg

    :catch_0
    move-exception v0

    const-string v0, "No se pudo abrir el destino."

    :goto_msg
    invoke-virtual {p0, v0}, Lcom/naruto/port/LauncherActivity;->@TOAST@(Ljava/lang/String;)V

    :cond_done
    const/4 v0, 0x1

    return v0
.end method

