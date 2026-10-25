.class public final Lcom/naruto/port/FpsListener;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements La/Q;


# instance fields
.field private final a:Lcom/naruto/port/LauncherActivity;

.field private final b:Landroid/widget/LinearLayout;


# direct methods
.method public constructor <init>(Lcom/naruto/port/LauncherActivity;Landroid/widget/LinearLayout;)V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/naruto/port/FpsListener;->a:Lcom/naruto/port/LauncherActivity;

    iput-object p2, p0, Lcom/naruto/port/FpsListener;->b:Landroid/widget/LinearLayout;

    return-void
.end method


# virtual methods
.method public final a(I)V
    .locals 3

    iget-object v0, p0, Lcom/naruto/port/FpsListener;->a:Lcom/naruto/port/LauncherActivity;

    iget-object v1, v0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;

    invoke-interface {v1}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v1

    const-string v2, "menu_fps"

    invoke-interface {v1, v2, p1}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;

    move-result-object v1

    invoke-interface {v1}, Landroid/content/SharedPreferences$Editor;->apply()V

    iget-object v1, p0, Lcom/naruto/port/FpsListener;->b:Landroid/widget/LinearLayout;

    invoke-static {v1}, Lcom/naruto/port/LauncherActivity;->g(Landroid/view/View;)V

    if-eqz p1, :cond_0

    const/4 v1, 0x2

    if-eq p1, v1, :cond_1

    const-string v1, "30 FPS · velocidad normal del juego (recomendado)."

    goto :goto_0

    :cond_0
    const-string v1, "24 FPS · más liviano, el juego va un poco más lento."

    goto :goto_0

    :cond_1
    const-string v1, "45 FPS · más fluido pero el juego va 1.5x más rápido. El modo rendimiento lo fuerza a 24."

    :goto_0
    invoke-virtual {v0, v1}, Lcom/naruto/port/LauncherActivity;->j(Ljava/lang/String;)V

    return-void
.end method
