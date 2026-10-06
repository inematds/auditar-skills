# Relatório de auditoria de skills (2026-10-06)

- Skills analisadas: **4**
- Erros: **34** · Avisos: **20** · Limpas (sem erro nem aviso): **0**
- Regras que mais falham: `ST5` (28), `ST6` (19), `ST4` (4), `DS3` (1), `DS1` (1), `SC5` (1)

Os IDs das regras estão em `skill-creator-plus/references/audit-checklist.md`. Este relatório cobre só a parte mecânica; as regras de julgamento exigem leitura da skill.

## As 4 piores

| # | Skill | Erros | Avisos | Notas | Regras com erro ou aviso |
|---|---|---|---|---|---|
| 1 | `video-ia` | 16 | 8 | 2 | ST5 ST6 |
| 2 | `media-use` | 13 | 11 | 2 | SC5 ST4 ST5 ST6 |
| 3 | `formato-curso-v2` | 5 | 0 | 5 | DS1 ST5 |
| 4 | `clima` | 0 | 1 | 0 | DS3 |

### 1. video-ia

Pasta: `teste-skills/video-ia`

- **ST5** (erro, 16x)
  - `references/adapters/agnes-keyframes.md` is 147 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/adapters/dreamina-seedance-20.md` is 121 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/adapters/seedance-25-multishot.md` is 204 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/apresentador.md` is 134 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/assets.md` is 141 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - … mais 11
- **ST6** (aviso, 8x)
  - `marcas/_exemplo-oficina-do-bairro.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - `marcas/_modelo.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - `references/adapters/agnes-keyframes.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - `references/adapters/dreamina-seedance-20.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - `references/adapters/seedance-25-multishot.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - … mais 3

### 2. media-use

Pasta: `teste-skills/media-use`

- **ST4** (erro, 4x)
  - `audio/references/captions/authoring.md:7,20` audio/references/transcribe.md is reached only through other reference files (audio/references/captions/authoring.md:7, audio/references/captions/authoring.md:20, audio/references/captions/transcript-handling.md:3, audio/references/captions/transcript-handling.md:60, audio/references/captions/transcript-handling.md:96), never from SKILL.md. Claude may only preview files it reaches that way (for example with head -100). Link it from SKILL.md, or fold its content into the file that needs it.
  - `audio/references/captions/authoring.md:153` audio/references/captions/motion.md is reached only through other reference files (audio/references/captions/authoring.md:153), never from SKILL.md. Claude may only preview files it reaches that way (for example with head -100). Link it from SKILL.md, or fold its content into the file that needs it.
  - `audio/references/transcribe.md:38` audio/references/captions/transcript-handling.md is reached only through other reference files (audio/references/transcribe.md:38, audio/references/captions/authoring.md:7, audio/references/captions/authoring.md:20, audio/references/captions/authoring.md:154), never from SKILL.md. Claude may only preview files it reaches that way (for example with head -100). Link it from SKILL.md, or fold its content into the file that needs it.
  - `audio/references/tts-to-captions.md:21` audio/references/tts.md is reached only through other reference files (audio/references/tts-to-captions.md:21), never from SKILL.md. Claude may only preview files it reaches that way (for example with head -100). Link it from SKILL.md, or fold its content into the file that needs it.
- **ST5** (erro, 8x)
  - `audio/references/captions/authoring.md` is 163 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `audio/references/remove-background.md` is 143 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `audio/references/tts.md` is 243 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/grading.md` is 160 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/media-treatment-recipes.md` is 929 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - … mais 3
- **ST6** (erro, 1x)
  - `SKILL.md:6` link target does not exist: ../hyperframes/references/plugin-installation.md.
- **SC5** (aviso, 1x)
  - `audio/scripts/lyria-recipe.py:55` needs the package 'google' but no install line was found anywhere in the skill. Add 'pip install google' next to the script or code that needs it.
- **ST6** (aviso, 10x)
  - `SKILL.md` 19 bundled file(s) are never mentioned by any file in the skill: audio/scripts/audio.test.mjs, audio/scripts/gemini-pipeline.test.mjs, audio/scripts/wait-bgm.test.mjs, audio/scripts/lib/audio-meta.test.mjs, audio/scripts/lib/bgm.test.mjs, audio/scripts/lib/concurrency.test.mjs, audio/scripts/lib/gemini-auth.test.mjs, audio/scripts/lib/gemini-tts.test.mjs (+11 more). Mention each where it is used, or delete it.
  - `audio/assets/sfx/CREDITS.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - `audio/references/bgm.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - `audio/references/captions/authoring.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - `audio/references/remove-background.md` is never linked from SKILL.md, so Claude has no reason to open it. Link it from SKILL.md with a line on when to read it, or delete it.
  - … mais 5

### 3. formato-curso-v2

Pasta: `teste-skills/formato-curso-v2`

- **DS1** (erro, 1x)
  - `SKILL.md:3` description is 1251 characters; the limit is 1024.
- **ST5** (erro, 4x)
  - `references/CHECKLIST_REVISAO.md` is 527 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/DESIGN-SYSTEM.md` is 483 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/LEARN-LAYER.md` is 618 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.
  - `references/SVG-FUTURISTA.md` is 162 lines with no contents list in its first 50 lines. Add a '## Contents' list at the top so a partial read still shows everything the file covers.

### 4. clima

Pasta: `teste-skills/clima`

- **DS3** (aviso, 1x)
  - `SKILL.md:3` description says what the skill does but not when to use it. Add a "Use when ..." clause with the words people actually type.

## Próximos passos (receita INEMA)

1. Para cada skill acima, peça ao agente o relatório completo (modo AUDIT) antes de editar.
2. Corrija primeiro os erros mecânicos (`ST5` sumário, `ST4` um nível, `DS1` tamanho da descrição).
3. Antes de apagar linha "prescritiva", rode a mesma tarefa com e sem a skill e compare.
4. Regra que tem de valer sempre vira hook. Rode o validador de novo no fim.
