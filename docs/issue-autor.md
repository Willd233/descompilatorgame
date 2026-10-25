**Título:** Sugestões: seletor de idioma (o disco NTSC-U já tem espanhol e francês), seletor de FPS, botão de sair e tradução para espanhol

Olá! Antes de tudo, parabéns pelo port, está incrível.

Fiz algumas melhorias para uso pessoal e queria oferecê-las a você, e também pedir permissão para publicá-las.

### 1. O jogo já tem espanhol e francês
O disco NTSC-U (o `default.xex` v9 que o port exige) traz **inglês, espanhol e francês** completos em `data/disc/dataRegion.cpk` (770 arquivos por idioma) e `dlc.cpk` (39). No console, o jogo escolhe a pasta pelo idioma do sistema (`XamGetLanguage`); no port, ele sempre mostra inglês.

Para trocar sem mexer no código nativo, reescrevo só o índice (TOC) dos CPK: as entradas `eng` passam a apontar para os dados `spa` ou `fre`. Os dados do jogo não são alterados, e o TOC original fica guardado para poder voltar ao inglês. No launcher, isso virou um seletor **English · Español · Français** aplicado ao tocar em Jogar.

Se preferir fazer direto no runtime, basta o `XamGetLanguage` retornar o idioma escolhido (inglês = 1, espanhol = 5, francês = 4).

### 2. Seletor de FPS (24 / 30 / 45)
Com o mesmo estilo da "Escala na tela". Usa a chave `frame_rate` que o launcher já passa (vblank 48 / 60 / 90). O 45 deixa o jogo 1,5x mais rápido, porque a lógica está presa aos frames, por isso o aviso diz isso.

### 3. Botão "Sair do jogo" no menu da engrenagem
Com confirmação. Também apaga o `gpu_driver_testing`, para o launcher não confundir a saída voluntária com um crash do driver.

### 4. Tradução do launcher para espanhol
Os ~117 textos do launcher e as 3 mensagens do motor. Posso te mandar a tabela PT→ES pronta.

### Pedido
O port não tem licença, então não quero publicar nada sem a sua autorização. Você aceitaria:
- **(a)** integrar alguma dessas melhorias no port oficial? Posso te passar tudo (a tabela de tradução, o código do seletor de idioma em Java e a lógica dos CPK);
- **(b)** que eu publique um repositório com um **patch** que se aplica ao APK que o usuário baixa daqui, sem redistribuir o seu APK e com os créditos para você;
- **(c)** ou que eu publique o APK modificado, com créditos e link para este repo?

Se não quiser nenhuma das opções, sem problema: fica só para uso pessoal.

Obrigado!
