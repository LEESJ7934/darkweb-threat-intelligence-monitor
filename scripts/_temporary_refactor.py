"""One-time safe cleanup of the public-facing repository layout."""
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.check_output(["git",*args],cwd=root).decode().strip()

targets=[
"DjangoProject/mongoDbConnect/static/assets/demo/chart-area-demo.js",
"DjangoProject/mongoDbConnect/static/assets/demo/chart-bar-demo.js",
"DjangoProject/mongoDbConnect/static/assets/demo/chart-pie-demo.js",
"DjangoProject/mongoDbConnect/static/assets/demo/datatables-demo.js",
"DjangoProject/mongoDbConnect/static/assets/img/error-404-monochrome.svg",
"DjangoProject/mongoDbConnect/static/css/styles.css",
"DjangoProject/mongoDbConnect/static/js/datatables-simple-demo.js",
"DjangoProject/mongoDbConnect/static/js/scripts.js",
]
all_paths=git("ls-files").splitlines()
assert all(t in all_paths for t in targets), "unexpected missing cleanup candidate"
protected={"scripts/_temporary_refactor.py",".github/workflows/_temporary_refactor.yml"}
for target in targets:
    name=Path(target).name
    uses=[]
    for source in all_paths:
        if source in targets or source in protected:
            continue
        try:
            text=(root/source).read_text("utf-8")
        except (UnicodeError, OSError):
            continue
        if name in text:
            uses.append(source)
    print("ASSET",target,"REFERENCES",uses,flush=True)
    if uses:
        raise SystemExit("Asset may be in use: "+target)
for t in targets:
    subprocess.check_call(["git","rm",t],cwd=root)
subprocess.check_call(["git","mv","DjangoProject","dashboard"],cwd=root)

changed=[]
for p in root.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.name=="_temporary_refactor.py":
        continue
    if p.suffix.lower() not in {".py",".html",".css",".js",".json",".md",".txt",".yml",".yaml",".toml",".sh",".env",".example"} and p.name not in {"Dockerfile",".gitignore",".gitattributes"}:
        continue
    try:
        old=p.read_text("utf-8")
    except (UnicodeError,OSError):
        continue
    new=old.replace("DjangoProject/","dashboard/").replace("DjangoProject\\","dashboard\\")
    if new!=old:
        p.write_text(new,"utf-8")
        changed.append(str(p.relative_to(root)))
print("PATH_REFERENCES_UPDATED",changed,flush=True)
(root/"AGENTS.md").write_text("""# 개발 및 문서 관리 기준

## 커밋 메시지
- 앞으로의 커밋 제목은 한글 평문으로 기능과 변경 대상을 구체적으로 설명한다.
- 제목에는 정리 수정 기능 같은 분류 접두어나 콜론 따옴표 괄호 이모지 장식 문자를 넣지 않는다.
- 예시 웹 대시보드 경로 개선 및 사용하지 않는 자산 제거
- 기존 커밋 이력은 강제 재작성하지 않는다.

## 저장소 파일
- 파일과 폴더는 목적을 설명하는 이름을 사용한다.
- 실제 운영 기록이나 증적 및 테스트를 단순 미참조만으로 삭제하지 않는다.
- ISMS-P 모의진단 자료와 당시 기준 및 미완료 상태를 보존한다.
- 삭제나 이름 변경 전 코드 템플릿 CI Docker 및 문서 링크의 참조를 검사한다.
- 개인정보 자격증명 유출 원문과 실제 비밀값을 저장소에 추가하지 않는다.
""",encoding="utf-8")
subprocess.check_call(["git","add","-A"],cwd=root)
subprocess.check_call(["git","diff","--cached","--check"],cwd=root)
subprocess.check_call(["git","-c","user.email=41898282+github-actions[bot]@users.noreply.github.com","-c","user.name=github-actions[bot]","commit","-m","웹 대시보드 경로 개선 및 미사용 예제 자산 제거"],cwd=root)
subprocess.check_call(["git","push","origin","HEAD:refactor/public-repository-structure-20261109"],cwd=root)
print("REFACTOR_SUCCESS",flush=True)
