"""Kleiner Client fuer den PSXRecomp-TCP-Debugserver (Port 4370).

Voraussetzung: Spiel aus build-debugtools starten, z.B.
  BreathOfFire3.exe --no-launcher --disc "<cue>" --debug-port 4370

Beispiele:
  python tools/psx_debug.py ping
  python tools/psx_debug.py read 0x80010000 32
  python tools/psx_debug.py write 0x800A1234 0x63
  python tools/psx_debug.py shot C:/Temp/bild.png
  python tools/psx_debug.py snap vorher        # RAM (2 MB) in Datei sichern
  python tools/psx_debug.py snap nachher
  python tools/psx_debug.py diff vorher nachher   # geaenderte Adressen
"""
import json, socket, sys

HOST, PORT = "127.0.0.1", 4370
RAM_BASE = 0x80000000
RAM_SIZE = 0x200000


def call(cmd, **kw):
    kw["cmd"] = cmd
    with socket.create_connection((HOST, PORT), timeout=10) as s:
        s.sendall((json.dumps(kw) + "\n").encode())
        buf = b""
        while not buf.endswith(b"\n"):
            chunk = s.recv(1 << 20)
            if not chunk:
                break
            buf += chunk
    return json.loads(buf)


def read_ram(addr, length):
    r = call("read_ram", addr="0x%08X" % addr, len=length)
    if not r.get("ok"):
        raise RuntimeError(r)
    return bytes.fromhex(r["hex"])


def main(a):
    if not a:
        print(__doc__); return
    c = a[0]
    if c == "ping":
        print(call("ping"))
    elif c == "read":
        addr, n = int(a[1], 0), int(a[2], 0)
        d = read_ram(addr, n)
        for i in range(0, len(d), 16):
            row = d[i:i + 16]
            print("%08X  %-47s" % (addr + i, " ".join("%02x" % b for b in row)))
    elif c == "write":
        print(call("write_ram", addr="0x%08X" % int(a[1], 0), val="0x%02X" % int(a[2], 0)))
    elif c == "shot":
        print(call("screenshot_file", path=a[1]))
    elif c == "snap":
        open(a[1] + ".ram", "wb").write(read_ram(RAM_BASE, RAM_SIZE))
        print("gespeichert:", a[1] + ".ram")
    elif c == "diff":
        x = open(a[1] + ".ram", "rb").read()
        y = open(a[2] + ".ram", "rb").read()
        n = 0
        for i, (p, q) in enumerate(zip(x, y)):
            if p != q:
                print("%08X: %02x -> %02x" % (RAM_BASE + i, p, q))
                n += 1
                if n >= 400:
                    print("... (abgeschnitten)"); break
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
