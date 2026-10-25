.method private addExitButton()V
    .locals 4

    new-instance v0, Lcom/naruto/port/ExitHelper;

    invoke-direct {v0, p0}, Lcom/naruto/port/ExitHelper;-><init>(Landroid/app/Activity;)V

    const-string v1, "Salir del juego"

    invoke-direct {p0, v1, v0}, Lcom/naruto/port/NarutoActivity;->editorButton(Ljava/lang/String;Landroid/view/View$OnClickListener;)Landroid/widget/TextView;

    move-result-object v0

    const v1, -0xbbbc

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setTextColor(I)V

    const/16 v1, 0x11

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setGravity(I)V

    new-instance v1, Landroid/widget/LinearLayout$LayoutParams;

    const/4 v2, -0x1

    const/4 v3, -0x2

    invoke-direct {v1, v2, v3}, Landroid/widget/LinearLayout$LayoutParams;-><init>(II)V

    const/high16 v2, 0x41000000    # 8.0f

    invoke-direct {p0, v2}, Lcom/naruto/port/NarutoActivity;->dp(F)I

    move-result v2

    iput v2, v1, Landroid/view/ViewGroup$MarginLayoutParams;->topMargin:I

    iget-object v2, p0, Lcom/naruto/port/NarutoActivity;->editorPanel:Landroid/widget/LinearLayout;

    invoke-virtual {v2, v0, v1}, Landroid/view/ViewGroup;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    return-void
.end method

