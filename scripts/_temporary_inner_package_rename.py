"""One-time Django inner settings-package rename."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
assert (root/"dashboard/DjangoProject/settings.py").is_file()
subprocess.check_call(["git","mv","dashboard/DjangoProject","dashboard/web_config"],cwd=root)
changed=[]
for p in root.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.name.startswith("_temporary_") or ".github/workflows" in str(p):
        continue
    if p.suffix.lower() not in (".py",".html",".md",".yaml",".yml",".json",".js",".css",".toml",".sh",".txt"):
        continue
    try:old=p.read_text("utf-8")
    except UnicodeDecodeError:continue
    new=old.replace("DjangoProject","web_config")
    if old!=new:
        p.write_text(new,"utf-8")
        changed.append(str(p.relative_to(root)))
print("INNER_PACKAGE_REFS",changed,flush=True)
subprocess.check_call(["git","add","-A"],cwd=root)
subprocess.check_call(["git","diff","--cached","--check"],cwd=root)
subprocess.check_call(["git","-c","user.name=github-actions[bot]","-c","user.email=41898282+github-actions[bot]@users.noreply.github.com","commit","-m","대시보드 설정 패키지 이름을 기능 중심으로 변경"],cwd=root)
subprocess.check_call(["git","push","origin","HEAD:refactor/public-repository-structure-20261109"],cwd=root)
print("INNER_PACKAGE_RENAME_SUCCESS",flush=True)
