package com.naruto.port;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

/** Copia el save del juego (STORM3FB.S) al destino que el usuario eligio con "Guardar como". */
public final class SaveExporter {
    private SaveExporter() {}

    /** @return null si salio bien, o un mensaje para mostrar. Siempre cierra {@code out}. */
    public static String copy(File src, OutputStream out) {
        try (InputStream in = new FileInputStream(src); OutputStream o = out) {
            byte[] buf = new byte[64 * 1024];
            for (int n; (n = in.read(buf)) > 0; ) o.write(buf, 0, n);
            return null;
        } catch (IOException e) {
            return "No se pudo exportar el save: " + e.getMessage();
        }
    }
}
