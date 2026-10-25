"""Redirige los archivos de un idioma a otro dentro de un CPK de CRIWARE (Naruto Storm 3).

El juego sigue pidiendo `eng`, pero el indice apunta a los datos `spa`.
Si el CPK destino no trae `spa`, los datos se copian desde otro CPK (ej. el europeo) al final.

Uso: python cpk_lang.py <destino.cpk> <salida.cpk> [fuente.cpk] [--de eng] [--a spa]
"""
import argparse, re, shutil, struct

TYPES = {0: ">B", 1: ">b", 2: ">H", 3: ">h", 4: ">I", 5: ">i", 6: ">Q", 7: ">q", 8: ">f", 0xA: ">I", 0xB: ">II"}


def utf_rows(buf, base):
    """Lee una tabla @UTF sin cifrar. Devuelve filas con valores y la posicion absoluta de cada campo por fila."""
    assert buf[:4] == b"@UTF", "tabla @UTF cifrada o invalida"
    b = buf[8:8 + struct.unpack_from(">I", buf, 4)[0]]
    _, rows_off, str_off, _, _, ncols, rowlen, nrows = struct.unpack_from(">HHIIIHHI", b, 0)
    s = lambda o: b[str_off + o:b.index(b"\0", str_off + o)].decode("utf-8", "replace")
    cols, o = [], 24
    for _ in range(ncols):
        fl, name = b[o], struct.unpack_from(">I", b, o + 1)[0]
        o += 5
        const = None
        if fl & 0xF0 == 0x30:
            const = struct.unpack_from(TYPES[fl & 0xF], b, o)
            o += struct.calcsize(TYPES[fl & 0xF])
        cols.append((s(name), fl & 0xF0, fl & 0xF, const))
    rows = []
    for r in range(nrows):
        o, vals, pos = rows_off + r * rowlen, {}, {}
        for name, st, t, const in cols:
            if st == 0x50:
                v = struct.unpack_from(TYPES[t], b, o)
                vals[name] = s(v[0]) if t == 0xA else v[0]
                pos[name] = (base + 8 + o, TYPES[t])
                o += struct.calcsize(TYPES[t])
            elif st == 0x30:
                vals[name] = s(const[0]) if t == 0xA else const[0]
        rows.append((vals, pos))
    return rows


def read_cpk(path):
    with open(path, "rb") as f:
        hdr = f.read(0x800)
        assert hdr[:4] == b"CPK ", f"{path} no es un CPK"
        info, info_pos = utf_rows(hdr[0x10:], 0x10)[0]
        f.seek(info["TocOffset"] + 0x10)
        toc = utf_rows(f.read(info["TocSize"]), info["TocOffset"] + 0x10)
    return info, info_pos, toc


def lang_key(vals, lang):
    path = f"{vals['DirName']}/{vals['FileName']}"
    pat = rf"(/|_){lang}(/|[._])"
    return re.sub(pat, r"\1LANG\2", path) if re.search(pat, path) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("destino"); ap.add_argument("salida"); ap.add_argument("fuente", nargs="?")
    ap.add_argument("--de", default="eng"); ap.add_argument("--a", default="spa")
    a = ap.parse_args()

    info, info_pos, toc = read_cpk(a.destino)
    src_lang = {lang_key(v, a.a): v for v, _ in toc if lang_key(v, a.a)}
    ext, fbase = {}, 0
    if a.fuente:
        finfo, _, ftoc = read_cpk(a.fuente)
        fbase = finfo["TocOffset"]
        ext = {lang_key(v, a.a): v for v, _ in ftoc if lang_key(v, a.a)}
    print(f"destino: {len(toc)} archivos, '{a.a}' propios: {len(src_lang)}, '{a.a}' en fuente: {len(ext)}")

    shutil.copyfile(a.destino, a.salida)
    align, base = info["Align"], info["TocOffset"]
    same = copied = missing = 0
    with open(a.salida, "r+b") as out, (open(a.fuente, "rb") if a.fuente else open(a.destino, "rb")) as fsrc:
        end = out.seek(0, 2)
        for vals, pos in toc:
            k = lang_key(vals, a.de)
            if not k:
                continue
            if k in src_lang:
                new = src_lang[k]; same += 1
                off, size, xsize = new["FileOffset"], new["FileSize"], new["ExtractSize"]
            elif k in ext:
                new = ext[k]
                fsrc.seek(new["FileOffset"] + fbase)
                data = fsrc.read(new["FileSize"])
                end = (end + align - 1) // align * align
                out.seek(end); out.write(data)
                off, size, xsize = end - base, new["FileSize"], new["ExtractSize"]
                end += len(data); copied += 1
            else:
                missing += 1
                continue
            for name, v in (("FileOffset", off), ("FileSize", size), ("ExtractSize", xsize)):
                p, fmt = pos[name]
                out.seek(p); out.write(struct.pack(fmt, v))
        if copied:
            out.truncate(end)
            p, fmt = info_pos["ContentSize"]
            out.seek(p); out.write(struct.pack(fmt, end - info["ContentOffset"]))
    print(f"redirigidos dentro del CPK: {same}, copiados desde fuente: {copied}, sin equivalente (quedan en {a.de}): {missing}")


if __name__ == "__main__":
    main()
