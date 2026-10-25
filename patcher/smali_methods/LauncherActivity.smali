.method public static fpsRate(Landroid/content/SharedPreferences;)Ljava/lang/String;
    .locals 2

    # vblank de la 360 simulada; el juego presenta 1 frame cada 2 vblanks
    const-string v0, "menu_fps"

    const/4 v1, 0x1

    invoke-interface {p0, v0, v1}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result p0

    if-eqz p0, :cond_0

    const/4 v0, 0x2

    if-eq p0, v0, :cond_1

    const-string p0, "60"

    return-object p0

    :cond_0
    const-string p0, "48"

    return-object p0

    :cond_1
    const-string p0, "90"

    return-object p0
.end method

.method public final applyLanguage()V
    .locals 4

    iget-object v0, p0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;

    const-string v1, "gameDirectory"

    const/4 v2, 0x0

    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const-string v2, "menu_lang"

    const/4 v3, 0x1

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result v2

    invoke-virtual {p0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v3

    invoke-static {v1, v2, v3}, Lcom/naruto/port/LangPatcher;->apply(Ljava/lang/String;ILjava/io/File;)Ljava/lang/String;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {p0, v0}, Lcom/naruto/port/LauncherActivity;->j(Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method public final addLangRow(Landroid/view/ViewGroup;)V
    .locals 5

    const-string v0, "English"

    const-string v1, "Español"

    const-string v2, "Français"

    filled-new-array {v0, v1, v2}, [Ljava/lang/String;

    move-result-object v0

    iget-object v1, p0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;

    const-string v2, "menu_lang"

    const/4 v3, 0x1

    invoke-interface {v1, v2, v3}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result v1

    new-instance v2, La/S;

    const/4 v4, 0x0

    invoke-direct {v2, p0, v0, v4, v1}, La/S;-><init>(Lcom/naruto/port/LauncherActivity;[Ljava/lang/String;[Ljava/lang/String;I)V

    invoke-virtual {v2, v3}, La/S;->setCompact(Z)V

    const-string v0, "Idioma del texto"

    invoke-virtual {p0, v0, v2}, Lcom/naruto/port/LauncherActivity;->n(Ljava/lang/String;Landroid/view/View;)Landroid/widget/LinearLayout;

    move-result-object v0

    new-instance v1, Lcom/naruto/port/LangListener;

    invoke-direct {v1, p0, v0}, Lcom/naruto/port/LangListener;-><init>(Lcom/naruto/port/LauncherActivity;Landroid/widget/LinearLayout;)V

    invoke-virtual {v2, v1}, La/S;->setListener(La/Q;)V

    new-array v1, v3, [Landroid/view/View;

    aput-object v0, v1, v4

    invoke-virtual {p0, v1}, Lcom/naruto/port/LauncherActivity;->i([Landroid/view/View;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {p1, v0}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V

    return-void
.end method

.method public final addFpsRow(Landroid/view/ViewGroup;)V
    .locals 5

    const-string v0, "24 FPS"

    const-string v1, "30 FPS"

    const-string v2, "45 FPS"

    filled-new-array {v0, v1, v2}, [Ljava/lang/String;

    move-result-object v0

    iget-object v1, p0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;

    const-string v2, "menu_fps"

    const/4 v3, 0x1

    invoke-interface {v1, v2, v3}, Landroid/content/SharedPreferences;->getInt(Ljava/lang/String;I)I

    move-result v1

    new-instance v2, La/S;

    const/4 v4, 0x0

    invoke-direct {v2, p0, v0, v4, v1}, La/S;-><init>(Lcom/naruto/port/LauncherActivity;[Ljava/lang/String;[Ljava/lang/String;I)V

    invoke-virtual {v2, v3}, La/S;->setCompact(Z)V

    const-string v0, "FPS del juego"

    invoke-virtual {p0, v0, v2}, Lcom/naruto/port/LauncherActivity;->n(Ljava/lang/String;Landroid/view/View;)Landroid/widget/LinearLayout;

    move-result-object v0

    new-instance v1, Lcom/naruto/port/FpsListener;

    invoke-direct {v1, p0, v0}, Lcom/naruto/port/FpsListener;-><init>(Lcom/naruto/port/LauncherActivity;Landroid/widget/LinearLayout;)V

    invoke-virtual {v2, v1}, La/S;->setListener(La/Q;)V

    new-array v1, v3, [Landroid/view/View;

    aput-object v0, v1, v4

    invoke-virtual {p0, v1}, Lcom/naruto/port/LauncherActivity;->i([Landroid/view/View;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {p1, v0}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V

    return-void
.end method

