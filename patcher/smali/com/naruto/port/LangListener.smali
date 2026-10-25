.class public final Lcom/naruto/port/LangListener;
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

    iput-object p1, p0, Lcom/naruto/port/LangListener;->a:Lcom/naruto/port/LauncherActivity;

    iput-object p2, p0, Lcom/naruto/port/LangListener;->b:Landroid/widget/LinearLayout;

    return-void
.end method


# virtual methods
.method public final a(I)V
    .locals 3

    iget-object v0, p0, Lcom/naruto/port/LangListener;->a:Lcom/naruto/port/LauncherActivity;

    iget-object v1, v0, Lcom/naruto/port/LauncherActivity;->a:Landroid/content/SharedPreferences;

    invoke-interface {v1}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v1

    const-string v2, "menu_lang"

    invoke-interface {v1, v2, p1}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;

    move-result-object v1

    invoke-interface {v1}, Landroid/content/SharedPreferences$Editor;->apply()V

    iget-object v1, p0, Lcom/naruto/port/LangListener;->b:Landroid/widget/LinearLayout;

    invoke-static {v1}, Lcom/naruto/port/LauncherActivity;->g(Landroid/view/View;)V

    const-string v1, "Se aplica al tocar Jugar. Solo cambia los textos; las voces quedan igual."

    invoke-virtual {v0, v1}, Lcom/naruto/port/LauncherActivity;->j(Ljava/lang/String;)V

    return-void
.end method
