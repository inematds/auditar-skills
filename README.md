# Auditar Skills

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![Auditar Skills](guia/assets/banner.jpg)](https://inematds.github.io/auditar-skills/guia/)

> Baseado em [robonuggets/skill-creator-plus](https://github.com/robonuggets/skill-creator-plus) (MIT, RoboNuggets). Todo o crédito do validador, das 46 regras e da skill à RoboNuggets. O INEMA acrescentou a receita, dois scripts e o guia PT/EN/ES.

## O que é

Auditar Skills é um kit aberto para conferir as skills do seu agente, as pastas com um arquivo SKILL.md que o Claude Code e o Codex usam para fazer uma tarefa sempre do mesmo jeito. Ele traz o skill-creator-plus, uma skill da RoboNuggets que confere cada skill contra 46 regras da Anthropic, e uma receita do INEMA em cinco passos: rodar o validador, pegar as cinco piores, gerar um relatório, testar com e sem a skill e ligar um hook. Serve para quem já tem várias skills e não sabe quais estão quebradas. Precisa só de Python 3.8 ou mais novo, e nenhuma skill muda sem você aprovar.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/auditar-skills/guia/**

## Comece em três comandos

```bash
git clone https://github.com/inematds/auditar-skills ~/auditar-skills
cd ~/auditar-skills
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills    # Codex: ~/.agents/skills
```

Sai uma tabela com uma linha por skill: erros, avisos, notas e os IDs das regras violadas. O validador só lê; não altera nada.

Para pegar as cinco piores num relatório Markdown:

```bash
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills --json \
  | python3 scripts/relatorio.py - --top 5 > relatorio.md
```

## A receita INEMA

1. **Validador em todas** as skills da pasta.
2. **As 5 piores** (ou as 5 que você mais usa) com `scripts/relatorio.py`.
3. **Relatório antes de editar:** instale a skill e peça o modo AUDIT; nada muda até você escolher.
4. **Teste com e sem** a skill antes de apagar linha "prescritiva demais".
5. **Hook** que roda o validador toda vez que um `SKILL.md` é salvo (`scripts/hook_validar.py`, exemplo de `settings.json`; não vem instalado).

Passo a passo completo, com os comandos e o exemplo de hook: [docs/receita-inema.md](docs/receita-inema.md).
Exemplo real de relatório, sobre cópias de quatro skills do INEMA: [examples/relatorio-inema.md](examples/relatorio-inema.md).

## Instalar a skill

A pasta `skill-creator-plus/` é a skill original, com uma única mudança INEMA no validador (ver abaixo). Copie para a sua pasta de skills:

```bash
cp -r ~/auditar-skills/skill-creator-plus ~/.claude/skills/    # Claude Code
cp -r ~/auditar-skills/skill-creator-plus ~/.agents/skills/    # Codex
```

Depois, numa sessão nova, peça em linguagem normal. Três modos:

| Modo | Peça algo como | Você recebe |
|---|---|---|
| AUDIT | "Audite a minha skill de deploy contra as regras da Anthropic." | Relatório: uma linha por regra, falhas primeiro, correções em ordem. Nada é editado até você escolher. |
| NEW | "Transforme isso numa skill; escrevemos notas de versão assim toda sexta." | Prompts de teste primeiro, depois uma pasta de skill que passa no validador. |
| REFINE | "A skill de relatório sempre esquece o filtro de data. Conserte." | A regra reescrita em torno do motivo, geralmente mais curta. |

A skill passa no próprio validador: 0 erros, 1 aviso (a imagem do README original não é citada no SKILL.md).

## Mudança INEMA no validador

O `validate_skill.py` original só reconhece inglês e dava alarme falso em skills escritas em português ou espanhol. O espelho INEMA muda três expressões regulares, nada mais (marcadas com `# Mudança INEMA` no código):

| Regra | Original | No espelho INEMA |
|---|---|---|
| DS3 (quando usar) | só "Use when…", "whenever", "triggers on"… | aceita também "Use quando…", "quando usar", "sempre que", "Gatilhos", "acione quando", "Úsala cuando…", "cuando el usuario", "disparadores" |
| ST5 (sumário) | só o título "Contents" / "Table of contents" | aceita também "Sumário", "Índice", "Conteúdo", "Contenido", "Tabla de contenido(s)" |
| CT9 (TODO) | qualquer "TODO" em caixa alta | "TODO" só com `:` ou `(` depois (ou no fim da linha); "quebraria TODO o markup" deixa de contar. FIXME continua valendo sempre |

Efeito medido nas 123 skills de `~/.claude/skills` (6/10/2026): DS3 caiu de 75 para 38 avisos, CT9 de 10 para 2 erros, ST5 de 248 para 246. Teste mínimo: `python3 tests/test_validador_ptes.py` (13 casos, inclusive os que devem continuar falhando).

## O que tem dentro

```text
skill-creator-plus/            a skill original da RoboNuggets (MIT); só o validador mudou
  SKILL.md                     regras, os três modos e links para o resto
  references/                  checklist das 46 regras, guia de escrita, testes
  scripts/validate_skill.py    o validador (Python 3.8+, só biblioteca padrão)
  scripts/init_skill.py        cria uma skill nova que já passa no validador
  examples/                    skill quebrada de exemplo, saída do validador e relatório
  README.md                    o README original, em inglês
scripts/relatorio.py           INEMA: relatório Markdown das N piores a partir do --json
scripts/hook_validar.py        INEMA: hook PostToolUse que valida ao salvar um SKILL.md
docs/receita-inema.md          INEMA: a receita em cinco passos
examples/relatorio-inema.md    INEMA: relatório real de quatro skills
tests/test_validador_ptes.py   INEMA: teste das mudanças PT/ES no validador
guia/                          guia PT, EN e ES (GitHub Pages)
```

As 46 regras, com a fonte de cada uma na documentação da Anthropic, estão no [README original](skill-creator-plus/README.md#the-rules) e em [skill-creator-plus/references/audit-checklist.md](skill-creator-plus/references/audit-checklist.md) (em inglês).

## Créditos e licença

Baseado em [robonuggets/skill-creator-plus](https://github.com/robonuggets/skill-creator-plus) (MIT, RoboNuggets), feito por [RoboNuggets](https://www.skool.com/robonuggets). Os nomes dos modos de falha usados nas auditorias vêm do "writing-great-skills" de Matt Pocock. Sem vínculo com a Anthropic. Licença MIT, ver [LICENSE](LICENSE) (o texto original da RoboNuggets, mantido). Receita, scripts `relatorio.py` e `hook_validar.py` e guia PT/EN/ES: [INEMA.CLUB](https://inema.club).
