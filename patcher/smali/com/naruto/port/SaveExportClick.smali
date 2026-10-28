.class public final Lcom/naruto/port/SaveExportClick;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Landroid/view/View$OnClickListener;


# instance fields
.field private final a:Lcom/naruto/port/LauncherActivity;


# direct methods
.method public constructor <init>(Lcom/naruto/port/LauncherActivity;)V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/naruto/port/SaveExportClick;->a:Lcom/naruto/port/LauncherActivity;

    return-void
.end method


# virtual methods
.method public final onClick(Landroid/view/View;)V
    .locals 0

    iget-object p1, p0, Lcom/naruto/port/SaveExportClick;->a:Lcom/naruto/port/LauncherActivity;

    invoke-virtual {p1}, Lcom/naruto/port/LauncherActivity;->startSaveExport()V

    return-void
.end method
