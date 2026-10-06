# Receita INEMA: auditar as suas skills

Cinco passos para auditar uma biblioteca de skills (Claude Code ou Codex) sem gastar uma tarde inteira.
Medir antes de reescrever: o validador diz o que falha e onde; você decide o que corrigir.

Nunca audite todas de uma vez. A doc da Anthropic recomenda testar a fundo só as skills de que você depende;
fora delas o custo não compensa.

## Conteúdo

1. [Rodar o validador em todas](#1-rodar-o-validador-em-todas)
2. [Pegar as 5 piores](#2-pegar-as-5-piores)
3. [Relatório antes de editar](#3-relatório-antes-de-editar)
4. [Teste com e sem a skill](#4-teste-com-e-sem-a-skill)
5. [Hook que valida ao salvar o SKILL.md](#5-hook-que-valida-ao-salvar-o-skillmd)

Pré-requisito: Python 3.8+ (só biblioteca padrão, nada para instalar). Rode os comandos na pasta deste repositório.

## 1. Rodar o validador em todas

```bash
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills      # Claude Code
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.agents/skills      # Codex
```

Sai uma tabela: uma linha por skill, com erros, avisos, notas e os IDs das regras violadas.
Código de saída `0` = nenhum erro, `1` = há erros, `2` = não conseguiu rodar.
Os IDs (FM, DS, ST, CT, WF, SC, NM, HK, TS, LB) estão explicados em [references/audit-checklist.md](../skill-creator-plus/references/audit-checklist.md).

O validador só lê. Não altera nenhuma skill.

Neste espelho o validador entende skills em português e espanhol ("Use quando…", "## Sumário", a palavra "TODO"
sem dois-pontos). É a única mudança no código original; detalhes na seção "Mudança INEMA no validador" do README.

## 2. Pegar as 5 piores

```bash
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills --json > val.json
python3 scripts/relatorio.py val.json --top 5 > relatorio.md
```

`scripts/relatorio.py` (deste espelho INEMA) ordena por erros, depois avisos, e detalha as N piores agrupando
os achados por regra. Também lê da entrada padrão:

```bash
python3 skill-creator-plus/scripts/validate_skill.py --all ~/.claude/skills --json | python3 scripts/relatorio.py - --top 5
```

Use `--notas` para incluir as notas (NOTE). Exemplo real, gerado sobre cópias de 4 skills do INEMA:
[examples/relatorio-inema.md](../examples/relatorio-inema.md).

Critério alternativo: em vez das 5 com mais erros, as 5 que você mais usa. Skill de terceiro (HyperFrames,
Remotion etc.) só se reporta ao autor; corrija as suas.

## 3. Relatório antes de editar

Com a skill `skill-creator-plus` instalada (ver README), peça em linguagem normal:

> Audite a skill formato-curso-v2 contra as regras da Anthropic. Só o relatório, não edite nada.

O modo AUDIT lê a skill inteira, marca cada regra (passa, falha, n/a) com arquivo e linha e propõe a correção.
Nada muda até você escolher quais aplicar. As correções mecânicas costumam ser as primeiras:

| Regra | O que é | Correção típica |
|---|---|---|
| ST5 | Referência com mais de 100 linhas sem sumário | `## Contents` no topo do arquivo |
| ST4 | Arquivo só alcançado por outro arquivo | Linkar direto do SKILL.md |
| DS1 | Descrição acima de 1.024 caracteres | Cortar; detalhe vai para o corpo |
| DS3 | Descrição sem "quando usar" | Acrescentar "Use quando…" com as palavras que a pessoa digita |
| ST6 | Arquivo órfão ou link morto | Linkar com uma linha de quando ler, ou apagar |

## 4. Teste com e sem a skill

Os modelos 5.5 costumam ir melhor com menos instrução, mas só uma execução comparada prova que uma linha é peso morto.
Antes de apagar trechos "prescritivos demais":

1. Liste as linhas candidatas e por que cada uma pode ser dispensável.
2. Copie a skill para uma pasta de teste e remova as candidatas **na cópia** (a original não muda).
3. Rode as mesmas 3 tarefas reais nas duas versões, cada uma numa sessão nova, no modelo que vai usar a skill.
4. Mantenha a remoção só onde a versão enxuta fez igual ou melhor. Volte qualquer linha cuja falta mudou o resultado.
5. Anote a evidência: qual tarefa, qual modelo, o que mudou.

Um jeito simples de montar as duas versões sem mexer na sua pasta global é usar skills de projeto:

```bash
mkdir -p /tmp/teste-com/.claude/skills /tmp/teste-sem/.claude/skills
cp -r ~/.claude/skills/minha-skill /tmp/teste-com/.claude/skills/
cp -r ~/.claude/skills/minha-skill /tmp/teste-sem/.claude/skills/   # depois apague as linhas candidatas nesta cópia
```

Abra o Claude Code em cada pasta e rode a mesma tarefa. Para a parte "sem skill nenhuma" (baseline),
o método completo está em [references/testing.md](../skill-creator-plus/references/testing.md).

## 5. Hook que valida ao salvar o SKILL.md

Regra que tem de valer sempre não fica só no texto: vira hook, que o Claude Code roda sozinho.
Este repositório traz `scripts/hook_validar.py`: quando o agente salva um arquivo chamado `SKILL.md`
(ferramentas Write ou Edit), ele roda o validador na pasta da skill. Se houver erro, sai com código 2 e
o Claude Code devolve a lista de erros ao agente, que corrige na mesma hora.

**Exemplo — não vem instalado.** Para usar, acrescente ao seu `~/.claude/settings.json` (ou ao
`.claude/settings.json` de um projeto), trocando `~/auditar-skills` pela pasta onde você clonou este repositório:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/auditar-skills/scripts/hook_validar.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Teste antes de ligar, simulando o evento:

```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"'"$HOME"'/.claude/skills/minha-skill/SKILL.md"}}' \
  | python3 scripts/hook_validar.py; echo "código: $?"
```

Código `0` = sem erro (ou não era um SKILL.md); `2` = erros, listados na saída de erro.

Alternativa: o hook também pode morar no frontmatter da própria skill (`hooks:`), e aí só fica ativo
depois que a skill é usada na sessão. A regra HK1 do validador aponta onde isso vale a pena.

---

Baseado em [robonuggets/skill-creator-plus](https://github.com/robonuggets/skill-creator-plus) (MIT, RoboNuggets).
Receita, `relatorio.py` e `hook_validar.py`: INEMA.CLUB.
