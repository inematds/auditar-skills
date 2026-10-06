# Auditar Skills

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![Auditar Skills](guia/assets/banner-es.jpg)](https://inematds.github.io/auditar-skills/guia/es/)

> Basado en [robonuggets/skill-creator-plus](https://github.com/robonuggets/skill-creator-plus) (MIT, RoboNuggets). Todo el crédito del validador, de las 46 reglas y de la skill es de RoboNuggets. INEMA agregó la receta, dos scripts y la guía PT/EN/ES.

## Qué es

Auditar Skills es un kit abierto para revisar las skills de tu agente, las carpetas con un archivo SKILL.md que Claude Code y Codex usan para hacer una tarea siempre de la misma manera. Incluye skill-creator-plus, una skill de RoboNuggets que revisa cada skill contra 46 reglas de Anthropic, y una receta de INEMA en cinco pasos: correr el validador, tomar las cinco peores, generar un informe, probar con y sin la skill y activar un hook. Sirve para quien ya tiene varias skills y no sabe cuáles están rotas. Solo necesita Python 3.8 o más reciente, y ninguna skill cambia sin tu aprobación.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/auditar-skills/guia/es/**

## Empieza con tres comandos

```bash
git clone https://github.com/inematds/auditar-skills ~/auditar-skills
cd ~/auditar-skills
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills    # Codex: ~/.agents/skills
```

Sale una tabla con una línea por skill: errores, avisos, notas y los IDs de las reglas incumplidas. El validador solo lee; no modifica nada.

Para tomar las cinco peores en un informe Markdown:

```bash
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills --json \
  | python3 scripts/relatorio.py - --top 5 > relatorio.md
```

## La receta INEMA

1. **Validador en todas** las skills de la carpeta.
2. **Las 5 peores** (o las 5 que más usas) con `scripts/relatorio.py`.
3. **Informe antes de editar:** instala la skill y pide el modo AUDIT; nada cambia hasta que elijas.
4. **Prueba con y sin** la skill antes de borrar una línea "demasiado prescriptiva".
5. **Hook** que corre el validador cada vez que se guarda un `SKILL.md` (`scripts/hook_validar.py`, ejemplo de `settings.json`; no viene instalado).

Paso a paso completo, con los comandos y el ejemplo de hook: [docs/receita-inema.md](docs/receita-inema.md) (en portugués).
Ejemplo real de informe, sobre copias de cuatro skills de INEMA: [examples/relatorio-inema.md](examples/relatorio-inema.md) (en portugués).

## Instalar la skill

La carpeta `skill-creator-plus/` es la skill original, con un único cambio INEMA en el validador (ver abajo). Cópiala a tu carpeta de skills:

```bash
cp -r ~/auditar-skills/skill-creator-plus ~/.claude/skills/    # Claude Code
cp -r ~/auditar-skills/skill-creator-plus ~/.agents/skills/    # Codex
```

Después, en una sesión nueva, pídelo con palabras normales. Tres modos:

| Modo | Pide algo como | Recibes |
|---|---|---|
| AUDIT | "Audita mi skill de deploy contra las reglas de Anthropic." | Informe: una línea por regla, fallas primero, correcciones en orden. Nada se edita hasta que elijas. |
| NEW | "Convierte esto en una skill; escribimos notas de versión así cada viernes." | Primero prompts de prueba, después una carpeta de skill que pasa el validador. |
| REFINE | "La skill de informes siempre olvida el filtro de fecha. Corrígela." | La regla reescrita en torno al motivo, normalmente más corta. |

La skill pasa su propio validador: 0 errores, 1 aviso (la imagen del README original no se menciona en el SKILL.md).

## Cambio INEMA en el validador

El `validate_skill.py` original solo reconoce inglés y daba falsas alarmas en skills escritas en portugués o español. El espejo INEMA cambia tres expresiones regulares, nada más (marcadas con `# Mudança INEMA` en el código):

| Regla | Original | En el espejo INEMA |
|---|---|---|
| DS3 (cuándo usar) | solo "Use when…", "whenever", "triggers on"… | acepta también "Use quando…", "quando usar", "sempre que", "Gatilhos", "acione quando", "Úsala cuando…", "cuando el usuario", "disparadores" |
| ST5 (índice) | solo el título "Contents" / "Table of contents" | acepta también "Sumário", "Índice", "Conteúdo", "Contenido", "Tabla de contenido(s)" |
| CT9 (TODO) | cualquier "TODO" en mayúsculas | "TODO" solo con `:` o `(` después (o al final de la línea); la palabra portuguesa "TODO" ("todo") deja de contar. FIXME cuenta siempre |

Efecto medido en las 123 skills de `~/.claude/skills` (6/10/2026): DS3 bajó de 75 a 38 avisos, CT9 de 10 a 2 errores, ST5 de 248 a 246. Prueba mínima: `python3 tests/test_validador_ptes.py` (13 casos, incluidos los que deben seguir fallando).

## Qué hay dentro

```text
skill-creator-plus/            la skill original de RoboNuggets (MIT); solo cambió el validador
  SKILL.md                     reglas, los tres modos y enlaces al resto
  references/                  checklist de las 46 reglas, guía de escritura, pruebas
  scripts/validate_skill.py    el validador (Python 3.8+, solo biblioteca estándar)
  scripts/init_skill.py        crea una skill nueva que ya pasa el validador
  examples/                    skill rota de ejemplo, salida del validador e informe
  README.md                    el README original, en inglés
scripts/relatorio.py           INEMA: informe Markdown de las N peores a partir del --json
scripts/hook_validar.py        INEMA: hook PostToolUse que valida al guardar un SKILL.md
docs/receita-inema.md          INEMA: la receta en cinco pasos (en portugués)
examples/relatorio-inema.md    INEMA: informe real de cuatro skills (en portugués)
tests/test_validador_ptes.py   INEMA: prueba de los cambios PT/ES del validador
guia/                          guía PT, EN y ES (GitHub Pages)
```

Las 46 reglas, con la fuente de cada una en la documentación de Anthropic, están en el [README original](skill-creator-plus/README.md#the-rules) y en [skill-creator-plus/references/audit-checklist.md](skill-creator-plus/references/audit-checklist.md) (en inglés).

## Créditos y licencia

Basado en [robonuggets/skill-creator-plus](https://github.com/robonuggets/skill-creator-plus) (MIT, RoboNuggets), hecho por [RoboNuggets](https://www.skool.com/robonuggets). Los nombres de los modos de falla usados en las auditorías vienen de "writing-great-skills" de Matt Pocock. Sin vínculo con Anthropic. Licencia MIT, ver [LICENSE](LICENSE) (el texto original de RoboNuggets, conservado). Receta, scripts `relatorio.py` y `hook_validar.py` y guía PT/EN/ES: [INEMA.CLUB](https://inema.club).
