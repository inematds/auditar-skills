#!/usr/bin/env python3
"""Gera um relatório Markdown a partir do JSON do validate_skill.py.

Receita INEMA, passo 2-3: ordenar as skills pela quantidade de erros e avisos,
pegar as N piores e listar o que falha em cada uma, agrupado por regra.

Uso:
  python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills --json > val.json
  python3 scripts/relatorio.py val.json --top 5 > relatorio.md
  # ou direto por pipe:
  python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills --json | python3 scripts/relatorio.py - --top 5

Só biblioteca padrão (Python 3.8+). Não altera nenhuma skill: só lê o JSON.
Códigos de saída: 0 ok, 2 entrada inválida.
"""
import argparse
import datetime
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ORDEM_NIVEL = {"ERROR": 0, "WARN": 1, "NOTE": 2}
ROTULO = {"ERROR": "erro", "WARN": "aviso", "NOTE": "nota"}


def carregar(origem):
    texto = sys.stdin.read() if origem == "-" else Path(origem).read_text(encoding="utf-8")
    dados = json.loads(texto)
    # --all devolve {"skills": [...], "totals": {...}}; uma skill só devolve o objeto da skill
    if isinstance(dados, dict) and "skills" in dados:
        return dados["skills"]
    if isinstance(dados, dict) and "findings" in dados:
        return [dados]
    raise ValueError("JSON não parece saída do validate_skill.py --json")


def nome_da(skill):
    return skill.get("name") or Path(skill.get("path", "?")).name


def chave_pior(skill):
    c = skill.get("counts", {})
    return (-c.get("error", 0), -c.get("warn", 0), -c.get("note", 0), nome_da(skill))


def linha_local(f):
    linhas = f.get("lines") or []
    arq = f.get("file") or ""
    return f"{arq}:{','.join(str(n) for n in linhas)}" if linhas else arq


def montar(skills, top, com_notas):
    hoje = datetime.date.today().isoformat()
    total_e = sum(s.get("counts", {}).get("error", 0) for s in skills)
    total_w = sum(s.get("counts", {}).get("warn", 0) for s in skills)
    limpas = sum(1 for s in skills if not s.get("counts", {}).get("error") and not s.get("counts", {}).get("warn"))
    regras = Counter()
    for s in skills:
        for f in s.get("findings", []):
            if f.get("level") in ("ERROR", "WARN"):
                regras[f.get("rule", "?")] += 1

    piores = sorted(skills, key=chave_pior)[:top]
    out = []
    out.append(f"# Relatório de auditoria de skills ({hoje})\n")
    out.append(f"- Skills analisadas: **{len(skills)}**")
    out.append(f"- Erros: **{total_e}** · Avisos: **{total_w}** · Limpas (sem erro nem aviso): **{limpas}**")
    if regras:
        mais = ", ".join(f"`{r}` ({n})" for r, n in regras.most_common(8))
        out.append(f"- Regras que mais falham: {mais}")
    out.append("")
    out.append("Os IDs das regras estão em `skill-creator-plus/references/audit-checklist.md`. "
               "Este relatório cobre só a parte mecânica; as regras de julgamento exigem leitura da skill.\n")

    out.append(f"## As {len(piores)} piores\n")
    out.append("| # | Skill | Erros | Avisos | Notas | Regras com erro ou aviso |")
    out.append("|---|---|---|---|---|---|")
    for i, s in enumerate(piores, 1):
        c = s.get("counts", {})
        rs = sorted({f.get("rule") for f in s.get("findings", []) if f.get("level") in ("ERROR", "WARN")})
        out.append(f"| {i} | `{nome_da(s)}` | {c.get('error', 0)} | {c.get('warn', 0)} | {c.get('note', 0)} | {' '.join(rs)} |")
    out.append("")

    for i, s in enumerate(piores, 1):
        out.append(f"### {i}. {nome_da(s)}\n")
        out.append(f"Pasta: `{s.get('path', '?')}`\n")
        por_regra = defaultdict(list)
        for f in s.get("findings", []):
            if f.get("level") == "NOTE" and not com_notas:
                continue
            por_regra[(ORDEM_NIVEL.get(f.get("level"), 9), f.get("rule", "?"))].append(f)
        if not por_regra:
            out.append("Nada a corrigir na parte mecânica.\n")
            continue
        for (_, regra), achados in sorted(por_regra.items()):
            nivel = ROTULO.get(achados[0].get("level"), "?")
            out.append(f"- **{regra}** ({nivel}, {len(achados)}x)")
            for f in achados[:5]:
                msg = f.get("message", "")
                arq = f.get("file") or ""
                if arq and msg.startswith(arq + " "):
                    msg = msg[len(arq) + 1:]  # a mensagem já começa pelo arquivo
                out.append(f"  - `{linha_local(f)}` {msg}")
            if len(achados) > 5:
                out.append(f"  - … mais {len(achados) - 5}")
        out.append("")

    out.append("## Próximos passos (receita INEMA)\n")
    out.append("1. Para cada skill acima, peça ao agente o relatório completo (modo AUDIT) antes de editar.")
    out.append("2. Corrija primeiro os erros mecânicos (`ST5` sumário, `ST4` um nível, `DS1` tamanho da descrição).")
    out.append("3. Antes de apagar linha \"prescritiva\", rode a mesma tarefa com e sem a skill e compare.")
    out.append("4. Regra que tem de valer sempre vira hook. Rode o validador de novo no fim.")
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(description="Relatório Markdown a partir do validate_skill.py --json.")
    p.add_argument("json", help="arquivo JSON do validador, ou - para ler da entrada padrão")
    p.add_argument("--top", type=int, default=5, help="quantas piores skills detalhar (padrão 5)")
    p.add_argument("--notas", action="store_true", help="incluir as notas (NOTE) no detalhe")
    a = p.parse_args()
    try:
        skills = carregar(a.json)
    except (OSError, ValueError) as e:
        print(f"relatorio.py: {e}", file=sys.stderr)
        return 2
    sys.stdout.write(montar(skills, max(1, a.top), a.notas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
