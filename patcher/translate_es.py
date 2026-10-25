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
    "24 FPS estáveis e mais leve. Ligue se o jogo não segura 30 FPS.":
        "24 FPS estables y más liviano. Actívalo si el juego no aguanta 30 FPS.",
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
    "CONFIRMA COM ○  (JAPÃO)": "CONFIRMA CON ○  (JAPÓN)",
    "Controle: ": "Control: ",
    "Controles\nXbox 360 · PS3": "Controles\nXbox 360 · PS3",
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
    "GATILHOS ↔ OMBROS": "GATILLOS ↔ HOMBROS",
    "Importar save": "Importar save",
    "Itens (direcional)": "Objetos (cruceta)",
    "Modo desempenho LIGADO: 24 FPS estáveis, 540p no máximo, sem suavização (Chidori!).":
        "Modo rendimiento ACTIVADO: 24 FPS estables, 540p como máximo, sin suavizado (¡Chidori!).",
    "Modo desempenho desligado: o jogo mira 30 FPS na resolução escolhida.":
        "Modo rendimiento desactivado: el juego apunta a 30 FPS en la resolución elegida.",
    "Nenhum controle conectado. Ligue um pelo cabo ou Bluetooth.": "Ningún control conectado. Conecta uno por cable o Bluetooth.",
    "Nenhum save ainda": "Todavía no hay save",
    "Normal · escala simples da imagem para a tela.": "Normal · escalado simple de la imagen a la pantalla.",
    "Não deu para ": "No se pudo ",
    "Não deu para importar o save: ": "No se pudo importar el save: ",
    "Não deu para instalar o driver: ": "No se pudo instalar el driver: ",
    "O jogo fechou com o driver ": "El juego se cerró con el driver ",
    "Off · sem suavização: mais leve, bordas serrilhadas.": "Off · sin suavizado: más liviano, bordes dentados.",
    "PADRÃO  XBOX 360 · PS3": "POR DEFECTO  XBOX 360 · PS3",
    "Painel de FPS": "Panel de FPS",
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
    "mostra FPS, CPU e RAM": "muestra FPS, CPU y RAM",
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
    "tudo liberado; o seu volta": "todo desbloqueado; el tuyo vuelve",
    "⚡ MODO DESEMPENHO": "⚡ MODO RENDIMIENTO",
    "自来也 · O SANNIN LENDÁRIO": "自来也 · EL SANNIN LEGENDARIO",
    "Área do analógico": "Área del analógico",
    "Antisserrilhado": "Antialiasing",
    "Concluir": "Listo",
    "Esticar": "Estirar",
    "Fechar": "Cerrar",
    "Manter": "Mantener",
    "Tamanho": "Tamaño",
    "Tela": "Pantalla",
    "Trocar": "Cambiar",
    "leve": "liviano",
    "Licenças": "Licencias",
    "Licenças de código aberto": "Licencias de código abierto",
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
