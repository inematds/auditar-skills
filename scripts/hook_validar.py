#!/usr/bin/env python3
"""Hook PostToolUse do Claude Code: valida a skill quando um SKILL.md é salvo.

Lê o JSON do evento na entrada padrão. Se o arquivo salvo (Write/Edit) se chama
SKILL.md, roda o validate_skill.py na pasta dele. Com erro, sai com código 2 e
manda o resumo para stderr: o Claude Code devolve esse texto ao agente, que
corrige na hora. Sem erro (ou outro arquivo), sai 0 em silêncio.

Exemplo de configuração em docs/receita-inema.md. Só biblioteca padrão.
"""
import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
# Procura o validador: ao lado deste script, na pasta skill-creator-plus deste repo
# ou na skill instalada em ~/.claude/skills.
CANDIDATOS = [
    AQUI / "validate_skill.py",
    AQUI.parent / "skill-creator-plus" / "scripts" / "validate_skill.py",
    Path.home() / ".claude" / "skills" / "skill-creator-plus" / "scripts" / "validate_skill.py",
]
VALIDADOR = next((c for c in CANDIDATOS if c.is_file()), None)


def main():
    try:
        evento = json.load(sys.stdin)
    except ValueError:
        return 0  # entrada estranha: não atrapalha o trabalho
    caminho = (evento.get("tool_input") or {}).get("file_path") or ""
    if Path(caminho).name != "SKILL.md":
        return 0
    pasta = Path(caminho).parent
    if not pasta.is_dir():
        return 0
    if VALIDADOR is None:
        print("hook_validar.py: validate_skill.py não encontrado; veja docs/receita-inema.md", file=sys.stderr)
        return 0  # sem validador, avisa e não bloqueia
    r = subprocess.run([sys.executable, str(VALIDADOR), str(pasta)],
                       capture_output=True, text=True, timeout=60)
    if r.returncode == 1:
        linhas = [l for l in r.stdout.splitlines() if l.startswith("ERROR") or l.startswith("Result:")]
        print(f"validate_skill.py achou erros em {pasta}:", file=sys.stderr)
        print("\n".join(linhas[:20]), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
