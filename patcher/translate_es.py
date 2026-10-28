import sys, re, pathlib

ES = {
    "\nDriver: ": "\nDriver: ",
    "  •  toque para trocar": "  •  toca para cambiar",
    " (toque para trocar)": " (toca para cambiar)",
    " KB) é bem diferente do save atual (": " KB) es muy distinto del save actual (",
    " arquivo": " archivo",
    " arquivos": " archivos",
    " o save 100%: ": " el save 100%: ",
    ")\nResolução: ": ")\nResolución: ",
    "+ Importar driver (.zip do AdrenoTools)": "+ Importar driver (.zip de AdrenoTools)",
    ", antisserrilhado: ": ", antialiasing: ",
    "1080p · nítido: 720p com FXAA+ e FSR para a tela do celular, mais pesado (Sharingan).":
        "1080p · nítido: 720p con FXAA+ y FSR para la pantalla del celular, más pesado (Sharingan).",
    "16:9 · a imagem original, com barras nas laterais.": "16:9 · la imagen original, con barras a los lados.",
    "360p · +FPS: poucos pixels, o jogo roda muito mais leve (folhas ao vento).":
        "360p · +FPS: pocos píxeles, el juego corre mucho más liviano (hojas al viento).",
    "540p · leve: bom equilíbrio para celulares médios (shurikens voando).":
        "540p · liviano: buen equilibrio para celulares de gama media (shurikens volando).",
    "720p · padrão: a imagem original do jogo (Rasengan).": "720p · por defecto: la imagen original del juego (Rasengan).",
    "APERTE O BOTÃO…": "PRESIONA EL BOTÓN…",
    "Ainda não tem log: abra o jogo uma vez e tente de novo.": "Aún no hay log: abre el juego una vez e inténtalo de nuevo.",
    "Analógico": "Analógico",
    "Aparelho: ": "Dispositivo: ",
    "Aperte agora, no controle, o botão que vai fazer \"": "Presiona ahora, en el control, el botón que hará \"",
    "Arraste os botões. Os cantos do retângulo mudam a área do analógico.":
        "Arrastra los botones. Las esquinas del rectángulo cambian el área del analógico.",
    "Atalho de corrida": "Atajo de carrera",
    "Atalho 奥": "Atajo 奥",
    "Atalho 術": "Atajo 術",
    "Ataque (B)": "Ataque (B)",
    "Atenção: o pacote é do título %08X, não do Storm 3 Full Burst (%08X).":
        "Atención: el paquete es del título %08X, no del Storm 3 Full Burst (%08X).",
    "Atenção: o tamanho (": "Atención: el tamaño (",
    "CAS · realça contraste e detalhes.": "CAS · realza contraste y detalles.",
    "Controle: ": "Control: ",
    "Defesa (RT)": "Defensa (RT)",
    "Driver da GPU": "Driver de la GPU",
    "ESCOLHER PASTA": "ELEGIR CARPETA",
    "Editar controles  ✥": "Editar controles  ✥",
    "Ele pode não ser compatível com este celular. Voltar para o driver do sistema?":
        "Puede que no sea compatible con este celular. ¿Volver al driver del sistema?",
    "Enviar log": "Enviar log",
    "Escala na tela": "Escala en pantalla",
    "Escolha a pasta que contém o default.xex do jogo.": "Elige la carpeta que contiene el default.xex del juego.",
    "Escolha o save do Storm 3 Full Burst:\n\n• o pacote copiado do Xbox 360 (arquivo STORM3FB.S, também do Horizon/Velocity);\n• o STORM3FB.S do Xenia (content/.../4E4D085C/00000001/);\n• ou um .zip com um deles.\n\nO save atual é copiado antes para a pasta save-backups.":
        "Elige el save del Storm 3 Full Burst:\n\n• el paquete copiado del Xbox 360 (archivo STORM3FB.S, también de Horizon/Velocity);\n• el STORM3FB.S de Xenia (content/.../4E4D085C/00000001/);\n• o un .zip con alguno de ellos.\n\nAntes se copia el save actual a la carpeta save-backups.",
    "Escolher arquivo": "Elegir archivo",
    "Esticar · a imagem preenche a tela inteira.": "Estirar · la imagen llena toda la pantalla.",
    "FSR · reescala com mais nitidez (pesa mais).": "FSR · reescala con más nitidez (pesa más).",
    "FXAA · suaviza as bordas por quase nada de custo.": "FXAA · suaviza los bordes casi sin costo.",
    "FXAA+ · bordas melhores, um pouco mais pesado.": "FXAA+ · mejores bordes, un poco más pesado.",
    "Ferramentas (X)": "Herramientas (X)",
    "Importar save": "Importar save",
    "Itens (direcional)": "Objetos (cruceta)",
    "Nenhum controle conectado. Ligue um pelo cabo ou Bluetooth.": "Ningún control conectado. Conecta uno por cable o Bluetooth.",
    "Nenhum save ainda": "Todavía no hay save",
    "Normal · escala simples da imagem para a tela.": "Normal · escalado simple de la imagen a la pantalla.",
    "Não deu para ": "No se pudo ",
    "Não deu para importar o save: ": "No se pudo importar el save: ",
    "Não deu para instalar o driver: ": "No se pudo instalar el driver: ",
    "O jogo fechou com o driver ": "El juego se cerró con el driver ",
    "Off · sem suavização: mais leve, bordas serrilhadas.": "Off · sin suavizado: más liviano, bordes dentados.",
    "Painel de FPS desligado.": "Panel de FPS desactivado.",
    "Painel de FPS ligado: mostra FPS, CPU e RAM durante o jogo.": "Panel de FPS activado: muestra FPS, CPU y RAM durante el juego.",
    "Pausa (Start)": "Pausa (Start)",
    "Pulo (A)": "Salto (A)",
    "Remover driver": "Quitar driver",
    "Remover um driver": "Quitar un driver",
    "Resolução": "Resolución",
    "Restaurar padrão": "Restaurar por defecto",
    "Save 100% desligado. Seu save anterior voltou.": "Save 100% desactivado. Tu save anterior volvió.",
    "Save 100% ligado. Seu save anterior ficou guardado e volta quando você desligar.":
        "Save 100% activado. Tu save anterior quedó guardado y vuelve cuando lo desactives.",
    "Save atual: ": "Save actual: ",
    "Save do jogo": "Save del juego",
    "Save importado: ": "Save importado: ",
    "Selecionado: ": "Seleccionado: ",
    "Sem default.xex em ": "No hay default.xex en ",
    "Sistema (padrão do celular)": "Sistema (por defecto del celular)",
    "Substituição (LT)": "Sustitución (LT)",
    "Suporte (LB)": "Soporte (LB)",
    "Suporte (RB)": "Soporte (RB)",
    "Toque em ESCOLHER PASTA e permita o acesso aos arquivos.": "Toca ELEGIR CARPETA y permite el acceso a los archivos.",
    "Toque numa ação e aperte o botão do controle que vai fazer isso.": "Toca una acción y presiona el botón del control que la hará.",
    "Toque numa opção: cada uma faz um jutsu. ⚠ FXAA+, FSR e CAS pesam; se o FPS cair, use Off e Normal.":
        "Toca una opción: cada una hace un jutsu. ⚠ FXAA+, FSR y CAS pesan; si bajan los FPS, usa Off y Normal.",
    "Transparência dos controles": "Transparencia de los controles",
    "Voltar para o sistema": "Volver al sistema",
    "arquivo de save (": "archivo de save (",
    "arquivo grande demais para um save": "archivo demasiado grande para un save",
    "do .zip (": "del .zip (",
    "não deu para abrir o arquivo": "no se pudo abrir el archivo",
    "não deu para criar ": "no se pudo crear ",
    "não foi possível criar a pasta do driver": "no se pudo crear la carpeta del driver",
    "não foi possível instalar o driver": "no se pudo instalar el driver",
    "o .zip não tem o STORM3FB.S nem um pacote de save do Xbox 360": "el .zip no tiene el STORM3FB.S ni un paquete de save de Xbox 360",
    "o .zip não é um driver do AdrenoTools (falta o meta.json ou o .so)": "el .zip no es un driver de AdrenoTools (falta el meta.json o el .so)",
    "o arquivo está vazio": "el archivo está vacío",
    "o pacote do Xbox 360 está vazio": "el paquete de Xbox 360 está vacío",
    "pacote do Xbox 360": "paquete de Xbox 360",
    "pacote do Xbox 360 cortado ou inválido": "paquete de Xbox 360 cortado o inválido",
    "padrão": "por defecto",
    "tamanho inválido no pacote: ": "tamaño inválido en el paquete: ",
    "自来也 · O SANNIN LENDÁRIO": "自来也 · EL SANNIN LEGENDARIO",
    "Área do analógico": "Área del analógico",
    "Antisserrilhado": "Antialiasing",
    "Concluir": "Listo",
    "Esticar": "Estirar",
    "Fechar": "Cerrar",
    "Manter": "Mantener",
    "Tela": "Pantalla",
    "Trocar": "Cambiar",
    "leve": "liviano",
    "Licenças": "Licencias",
    "Licenças de código aberto": "Licencias de código abierto",
    # v0.4.x: shadowZero, brillo, controles nuevos y actualizador
    "Limite de ": "Límite de ",
    " FPS, fixo (20 e 24 deixam o aparelho folgado e estável; 30 é o padrão do jogo).":
        " FPS, fijo (20 y 24 alivian el celular; 30 es la velocidad normal; 45 acelera el juego 1.5x).",
    " O jogo pode abrir, mas com falhas de imagem ou travando.":
        " El juego puede abrir, pero con fallas de imagen o trabándose.",
    ") não tem os recursos de Vulkan que ele precisa. O jogo usa o Xenia.":
        ") no tiene las funciones de Vulkan que necesita. El juego usa Xenia.",
    ") não tem: ": ") no tiene: ",
    ". Seus saves e configurações continuam.\n\n": ". Tus saves y tu configuración se mantienen.\n\n",
    "1080p · nítido: 1920x1080 por dentro (2,25 vezes os pixels do 720p), bem mais pesado (Sharingan).":
        "1080p · nítido: 1920x1080 internos (2,25 veces los píxeles de 720p), mucho más pesado (Sharingan).",
    "2K · 2560x1440 por dentro (4 vezes os pixels do 720p): só para GPU forte.":
        "2K · 2560x1440 internos (4 veces los píxeles de 720p): solo para GPU potente.",
    "2K · neste aparelho o jogo usa o Xenia: fica em 720p com FXAA+ e FSR.":
        "2K · en este celular el juego usa Xenia: queda en 720p con FXAA+ y FSR.",
    "360p · +FPS: o jogo desenha 640x360 por dentro, bem mais leve para a GPU (folhas ao vento).":
        "360p · +FPS: el juego dibuja 640x360 internos, mucho más liviano para la GPU (hojas al viento).",
    "480p · leve: 853x480 por dentro, bom equilíbrio (shurikens voando).":
        "480p · liviano: 853x480 internos, buen equilibrio (shurikens volando).",
    "4K · 3840x2160 por dentro (9 vezes os pixels do 720p): pesadíssimo, só para testar.":
        "4K · 3840x2160 internos (9 veces los píxeles de 720p): pesadísimo, solo para probar.",
    "4K · neste aparelho o jogo usa o Xenia: fica em 720p com FXAA+ e FSR.":
        "4K · en este celular el juego usa Xenia: queda en 720p con FXAA+ y FSR.",
    "720p · padrão: a resolução original do jogo (Rasengan).":
        "720p · por defecto: la resolución original del juego (Rasengan).",
    ": clareia os tons médios, sem estourar o branco nem o preto.":
        ": aclara los tonos medios, sin quemar el blanco ni el negro.",
    "APOIO": "APOYO",
    "AVANÇO": "AVANCE",
    "Agora não": "Ahora no",
    "Atualizar": "Actualizar",
    "Atualização disponível: v": "Actualización disponible: v",
    "Aviso sobre a GPU": "Aviso sobre la GPU",
    "Aviso: sua GPU (": "Aviso: tu GPU (",
    "Baixando a v": "Descargando la v",
    "Baixando…": "Descargando…",
    "Brilho": "Brillo",
    "Brilho ": "Brillo ",
    "Brilho Normal: igual ao jogo original (mais escuro).": "Brillo Normal: igual al juego original (más oscuro).",
    "Criado por SHADOWll  ·  YouTube": "Creado por SHADOWll  ·  YouTube",
    "DEFESA": "DEFENSA",
    "Depois": "Después",
    "Desempenho": "Rendimiento",
    "Despertar (analógico direito para o lado)": "Despertar (analógico derecho hacia un lado)",
    "Editar botões": "Editar botones",
    "Este celular não roda o shadowZero: a GPU (": "Este celular no puede usar shadowZero: la GPU (",
    "FERRAMENTA": "HERRAMIENTA",
    "FPS, CPU e RAM": "FPS, CPU y RAM",
    "JOGAR": "JUGAR",
    "Menu (Back)": "Menú (Back)",
    "Modo desempenho LIGADO: 480p no máximo, sem sombras e sem suavização (Chidori!).":
        "Modo rendimiento ACTIVADO: 480p como máximo, sin sombras y sin suavizado (¡Chidori!).",
    "Modo desempenho desligado: resolução e efeitos como escolhidos.":
        "Modo rendimiento desactivado: resolución y efectos como los elegiste.",
    "Não consegui abrir o YouTube": "No se pudo abrir YouTube",
    "Não consegui ligar o Save 100%: ": "No se pudo activar el Save 100%: ",
    "Não deu para abrir o instalador: ": "No se pudo abrir el instalador: ",
    "Não deu para baixar a atualização: ": "No se pudo descargar la actualización: ",
    "PULO": "SALTO",
    "Painel FPS": "Panel FPS",
    "Para instalar a atualização, o Android pede para permitir que este app instale apps. Ative a opção na próxima tela e volte.":
        "Para instalar la actualización, Android pide permitir que esta app instale apps. Activa la opción en la siguiente pantalla y vuelve.",
    "Permitir a instalação": "Permitir la instalación",
    "Pular esta": "Saltar esta",
    "SUBSTITUIÇÃO": "SUSTITUCIÓN",
    "Só controle: os botões somem quando um controle é plugado.":
        "Solo control: los botones desaparecen al conectar un control.",
    "Tamanho de todos os botões (toque num botão para mudar só ele)":
        "Tamaño de todos los botones (toca un botón para cambiar solo ese)",
    "Tamanho: ": "Tamaño: ",
    "Toque + controle": "Táctil + control",
    "Toque + controle: os botões ficam na tela com o controle plugado.":
        "Táctil + control: los botones quedan en pantalla con el control conectado.",
    "VOLTAR": "VOLVER",
    "Você tem a v": "Tienes la v",
    "alvo de cor 16 bits float (brilho)": "destino de color de 16 bits float (brillo)",
    "geometry shader (partes da imagem podem sumir)": "geometry shader (partes de la imagen pueden desaparecer)",
    "o arquivo veio incompleto": "el archivo llegó incompleto",
    "profundidade com stencil": "profundidad con stencil",
    "shadowZero indisponível": "shadowZero no disponible",
    "tudo liberado": "todo desbloqueado",
    # v0.5.x: 900p, dos controles y modo rendimiento solo sin sombras
    "900p · fino: 1600x900 por dentro (1,56 vez os pixels do 720p), quase o 1080p com folga na GPU (chakra).":
        "900p · fino: 1600x900 internos (1,56 veces los píxeles de 720p), casi como 1080p con holgura en la GPU (chakra).",
    "900p · neste aparelho o jogo usa o Xenia: fica em 720p.": "900p · en este celular el juego usa Xenia: queda en 720p.",
    "CONTROLE 1": "CONTROL 1",
    "CONTROLE 2": "CONTROL 2",
    "sem sombras": "sin sombras",
}

LIT = re.compile(r'(const-string(?:/jumbo)? [vp]\d+, )"((?:[^"\\]|\\.)*)"')

def dec(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})|\\(.)',
                  lambda m: chr(int(m[1], 16)) if m[1] else {"n": "\n", "t": "\t", "r": "\r"}.get(m[2], m[2]), s)

def enc(s):
    out = []
    for c in s:
        if c == "\\": out.append("\\\\")
        elif c == '"': out.append('\\"')
        elif c == "\n": out.append("\\n")
        elif ord(c) < 0x20 or ord(c) > 0x7e: out.append(f"\\u{ord(c):04x}")
        else: out.append(c)
    return "".join(out)

def apply(smali_dir):
    """Traduce los const-string PT->ES en todos los .smali. Devuelve las claves sin uso."""
    used = set()

    def sub(m):
        s = dec(m[2])
        if s in ES:
            used.add(s)
            return f'{m[1]}"{enc(ES[s])}"'
        return m[0]

    for f in pathlib.Path(smali_dir).rglob("*.smali"):
        t = f.read_text(encoding="utf-8")
        n = LIT.sub(sub, t)
        if n != t:
            f.write_text(n, encoding="utf-8", newline="\n")
    return set(ES) - used


if __name__ == "__main__":
    missing = apply(sys.argv[1])
    print(f"traducidos {len(ES) - len(missing)}/{len(ES)}")
