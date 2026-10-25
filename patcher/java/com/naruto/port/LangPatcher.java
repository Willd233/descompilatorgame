package com.naruto.port;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Elige el idioma del texto del juego redirigiendo, en el indice (TOC) de los CPK,
 * las entradas "eng" hacia los datos de otro idioma que ya trae el disco NTSC-U.
 * Solo se reescribe el TOC; la primera vez se guarda una copia del TOC original.
 */
public final class LangPatcher {
    private static final String[] LANGS = {"eng", "spa", "fre"};
    private static final String[] CPKS = {"dataRegion.cpk", "dlc.cpk"};

    private LangPatcher() {}

    /** @return null si salio bien, o un mensaje para mostrar. */
    public static String apply(String gameDir, int lang, File backupDir) {
        if (gameDir == null) return null;
        if (lang < 0 || lang >= LANGS.length) lang = 0;
        try {
            for (String name : CPKS) {
                File cpk = new File(gameDir, "data/disc/" + name);
                if (cpk.isFile()) patch(cpk, LANGS[lang], new File(backupDir, name + ".toc"));
            }
            return null;
        } catch (IllegalStateException e) {
            return e.getMessage();
        } catch (IOException e) {
            return "No se pudo cambiar el idioma: " + e.getMessage();
        }
    }

    private static void patch(File cpk, String lang, File backup) throws IOException {
        try (RandomAccessFile f = new RandomAccessFile(cpk, "rw")) {
            byte[] hdr = new byte[0x800];
            f.readFully(hdr);
            if (hdr[0] != 'C' || hdr[1] != 'P' || hdr[2] != 'K') throw new IllegalStateException(cpk.getName() + " no es un CPK");
            Table info = Table.parse(hdr, 0x10);
            long tocOff = info.longValue(0, "TocOffset");
            int tocLen = (int) (0x10 + info.longValue(0, "TocSize"));

            byte[] current = new byte[tocLen];
            f.seek(tocOff);
            f.readFully(current);

            // TOC original: el respaldo si corresponde a este archivo; si no, el actual (y se respalda).
            byte[] original = readBackup(backup, f.length(), tocLen);
            if (original == null) {
                Table t = Table.parse(current, 0x10);
                if (isRedirected(t)) {
                    throw new IllegalStateException(cpk.getName() + " ya viene modificado: pon el original del juego para poder elegir idioma.");
                }
                original = current;
                writeBackup(backup, f.length(), original);
            }

            byte[] wanted = original.clone();
            if (!lang.equals("eng")) {
                Table t = Table.parse(wanted, 0x10);
                Map<String, Integer> target = t.index(lang);
                for (Map.Entry<String, Integer> e : t.index("eng").entrySet()) {
                    Integer src = target.get(e.getKey());
                    if (src == null) continue;
                    for (String col : new String[] {"FileOffset", "FileSize", "ExtractSize"}) t.copyField(src, e.getValue(), col);
                }
            }
            if (!java.util.Arrays.equals(wanted, current)) {
                f.seek(tocOff);
                f.write(wanted);
                f.getFD().sync();
            }
        }
    }

    private static boolean isRedirected(Table t) {
        Map<String, Integer> eng = t.index("eng");
        for (String l : LANGS) {
            if (l.equals("eng")) continue;
            Map<String, Integer> other = t.index(l);
            int same = 0;
            for (Map.Entry<String, Integer> e : eng.entrySet()) {
                Integer o = other.get(e.getKey());
                if (o != null && t.longValue(o, "FileOffset") == t.longValue(e.getValue(), "FileOffset")) same++;
            }
            if (same > 0 && same >= other.size() / 2) return true;
        }
        return false;
    }

    private static byte[] readBackup(File backup, long cpkLength, int tocLen) throws IOException {
        if (!backup.isFile() || backup.length() != 8 + tocLen) return null;
        byte[] b = new byte[8 + tocLen];
        try (FileInputStream in = new FileInputStream(backup)) {
            int n = 0;
            while (n < b.length) { int r = in.read(b, n, b.length - n); if (r < 0) return null; n += r; }
        }
        if (ByteBuffer.wrap(b).getLong() != cpkLength) return null;  // otro juego/archivo: respaldo obsoleto
        return java.util.Arrays.copyOfRange(b, 8, b.length);
    }

    private static void writeBackup(File backup, long cpkLength, byte[] toc) throws IOException {
        backup.getParentFile().mkdirs();
        try (FileOutputStream out = new FileOutputStream(backup)) {
            out.write(ByteBuffer.allocate(8).putLong(cpkLength).array());
            out.write(toc);
            out.getFD().sync();
        }
    }

    /** Tabla @UTF de CRIWARE (sin cifrar), con acceso a la posicion de cada campo por fila. */
    private static final class Table {
        private static final Pattern LANG = Pattern.compile("(/|_)(eng|spa|fre|ger|ita|rus)(/|[._])");
        final byte[] buf;
        final int body, rowsOff, strOff, rowLen, rows;
        final Map<String, int[]> cols = new HashMap<>();  // nombre -> {offset en fila, tipo}

        private Table(byte[] buf, int at) {
            this.buf = buf;
            ByteBuffer b = ByteBuffer.wrap(buf);
            if (b.getInt(at) != 0x40555446) throw new IllegalStateException("tabla @UTF cifrada o invalida");
            body = at + 8;
            rowsOff = b.getShort(body + 2) & 0xFFFF;
            strOff = b.getInt(body + 4);
            int ncols = b.getShort(body + 16) & 0xFFFF;
            rowLen = b.getShort(body + 18) & 0xFFFF;
            rows = b.getInt(body + 20);
            int o = body + 24, rowPos = 0;
            for (int i = 0; i < ncols; i++) {
                int flags = buf[o] & 0xFF, type = flags & 0x0F, storage = flags & 0xF0;
                String name = str(b.getInt(o + 1));
                o += 5;
                if (storage == 0x30) o += size(type);
                if (storage == 0x50) {
                    cols.put(name, new int[] {rowPos, type});
                    rowPos += size(type);
                }
            }
        }

        static Table parse(byte[] buf, int at) { return new Table(buf, at); }

        static int size(int type) {
            switch (type) {
                case 0: case 1: return 1;
                case 2: case 3: return 2;
                case 6: case 7: case 0xB: return 8;
                default: return 4;
            }
        }

        String str(int off) {
            int s = body + strOff + off, e = s;
            while (buf[e] != 0) e++;
            return new String(buf, s, e - s, StandardCharsets.UTF_8);
        }

        int pos(int row, String col) { return body + rowsOff + row * rowLen + cols.get(col)[0]; }

        long longValue(int row, String col) {
            ByteBuffer b = ByteBuffer.wrap(buf);
            int p = pos(row, col);
            return size(cols.get(col)[1]) == 8 ? b.getLong(p) : b.getInt(p) & 0xFFFFFFFFL;
        }

        void copyField(int from, int to, String col) {
            System.arraycopy(buf, pos(from, col), buf, pos(to, col), size(cols.get(col)[1]));
        }

        /** ruta con el idioma reemplazado por LANG -> fila, solo para filas de ese idioma. */
        Map<String, Integer> index(String lang) {
            Map<String, Integer> m = new HashMap<>();
            ByteBuffer b = ByteBuffer.wrap(buf);
            for (int r = 0; r < rows; r++) {
                String path = str(b.getInt(pos(r, "DirName"))) + "/" + str(b.getInt(pos(r, "FileName")));
                Matcher mt = LANG.matcher(path);
                if (mt.find() && mt.group(2).equals(lang)) m.put(mt.replaceFirst("$1LANG$3"), r);
            }
            return m;
        }
    }
}
