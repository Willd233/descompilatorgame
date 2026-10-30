.method public final allOff()Z
    .locals 4

    iget-boolean v0, p0, @CTRL@->analogOff:Z

    if-eqz v0, :cond_2

    iget-object v0, p0, @CTRL@->a:[@BTN_CLS@

    array-length v1, v0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-object v3, v0, v2

    iget-boolean v3, v3, @BTN_CLS@->p:Z

    if-nez v3, :cond_0

    :cond_2
    const/4 v0, 0x0

    return v0

    :cond_0
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_1
    const/4 v0, 0x1

    return v0
.end method

.method public final setAnalogOff(Z)V
    .locals 2

    iput-boolean p1, p0, @CTRL@->analogOff:Z

    iget-object v0, p0, @CTRL@->e:Landroid/content/SharedPreferences;

    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    const-string v1, "analog_hidden"

    invoke-interface {v0, v1, p1}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V

    return-void
.end method

.method public final toggleHide()V
    .locals 5

    # analogico seleccionado: solo el
    iget-boolean v0, p0, @CTRL@->q:Z

    if-eqz v0, :cond_0

    iget-boolean v0, p0, @CTRL@->analogOff:Z

    xor-int/lit8 v0, v0, 0x1

    invoke-virtual {p0, v0}, @CTRL@->setAnalogOff(Z)V

    goto :goto_1

    # un boton seleccionado: igual que el original (solo ese)
    :cond_0
    iget-object v0, p0, @CTRL@->p:@BTN_CLS@

    if-eqz v0, :cond_1

    iget-boolean v0, v0, @BTN_CLS@->p:Z

    xor-int/lit8 v0, v0, 0x1

    invoke-virtual {p0, v0}, @CTRL@->setSelectedOff(Z)V

    return-void

    # sin seleccion: todos
    :cond_1
    invoke-virtual {p0}, @CTRL@->toggleAll()V

    return-void

    :goto_1
    invoke-virtual {p0}, @CTRL@->j()V

    invoke-virtual {p0}, Landroid/view/View;->invalidate()V

    return-void
.end method

# oculta todos (botones y analogico) o, si ya estan todos ocultos, los muestra.
# Lo usan el editor (sin seleccion) y el menu del emblema.
.method public final toggleAll()V
    .locals 5

    invoke-virtual {p0}, @CTRL@->allOff()Z

    move-result v0

    xor-int/lit8 v0, v0, 0x1

    invoke-virtual {p0, v0}, @CTRL@->setAnalogOff(Z)V

    iget-object v1, p0, @CTRL@->a:[@BTN_CLS@

    array-length v2, v1

    const/4 v3, 0x0

    :goto_0
    if-ge v3, v2, :cond_0

    aget-object v4, v1, v3

    iput-boolean v0, v4, @BTN_CLS@->p:Z

    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    :cond_0
    invoke-virtual {p0}, @CTRL@->p()V

    invoke-virtual {p0}, @CTRL@->j()V

    invoke-virtual {p0}, Landroid/view/View;->invalidate()V

    return-void
.end method

