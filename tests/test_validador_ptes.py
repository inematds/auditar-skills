#!/usr/bin/env python3
"""Teste mínimo das mudanças INEMA no validate_skill.py (PT/ES).

Rodar na raiz do repositório:  python3 tests/test_validador_ptes.py
Só biblioteca padrão. Cria skills temporárias, roda o validador com --json e
confere se as regras DS3, ST5 e CT9 disparam (ou não) como esperado.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

VALIDADOR = Path(__file__).resolve().parent.parent / "skill-creator-plus" / "scripts" / "validate_skill.py"
CORPO_LONGO = "\n".join(f"Linha {i} de referência." for i in range(1, 121))


def rodar(descricao, corpo="Faz a tarefa.\n", ref=None):
    """Monta uma skill mínima e devolve o conjunto (nível, regra) dos achados."""
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp) / "teste-skill"
        pasta.mkdir()
        texto = f'---\nname: teste-skill\ndescription: "{descricao}"\n---\n\n# Teste\n\n{corpo}'
        if ref is not None:
            (pasta / "references").mkdir()
            (pasta / "references" / "guia.md").write_text(ref, encoding="utf-8")
            texto += "\nDetalhes em [references/guia.md](references/guia.md).\n"
        (pasta / "SKILL.md").write_text(texto, encoding="utf-8")
        r = subprocess.run([sys.executable, str(VALIDADOR), str(pasta), "--json"],
                           capture_output=True, text=True)
        dados = json.loads(r.stdout)
        return {(f["level"], f["rule"]) for f in dados["skills"][0]["findings"]}


DESC_PT = "Gera relatórios semanais de vendas a partir da planilha do time. Use quando a pessoa pedir o relatório da semana."


class TestDS3(unittest.TestCase):
    def test_pt_use_quando(self):
        self.assertNotIn(("WARN", "DS3"), rodar(DESC_PT))

    def test_es_usala_cuando(self):
        d = "Genera informes semanales de ventas a partir de la planilla. Úsala cuando el usuario pida el informe."
        self.assertNotIn(("WARN", "DS3"), rodar(d))

    def test_pt_gatilhos(self):
        d = "Gera relatórios semanais de vendas a partir da planilha do time. Gatilhos: relatório da semana, vendas."
        self.assertNotIn(("WARN", "DS3"), rodar(d))

    def test_acione_quando(self):
        d = "Gera relatórios semanais de vendas a partir da planilha do time. Acione também quando pedirem vendas."
        self.assertNotIn(("WARN", "DS3"), rodar(d))

    def test_aciona_sem_quando_continua_avisando(self):
        d = "Aciona o deploy da aplicação no servidor de produção e confere os logs depois de publicar a versão."
        self.assertIn(("WARN", "DS3"), rodar(d))

    def test_sem_pista_continua_avisando(self):
        d = "Gera relatórios semanais de vendas a partir da planilha do time com gráficos e totais por região."
        self.assertIn(("WARN", "DS3"), rodar(d))


class TestST5(unittest.TestCase):
    def test_sumario_pt(self):
        self.assertNotIn(("ERROR", "ST5"), rodar(DESC_PT, ref="# Guia\n\n## Sumário\n\n- Parte 1\n\n" + CORPO_LONGO))

    def test_contenido_es(self):
        self.assertNotIn(("ERROR", "ST5"), rodar(DESC_PT, ref="# Guía\n\n## Contenido\n\n- Parte 1\n\n" + CORPO_LONGO))

    def test_contents_en(self):
        self.assertNotIn(("ERROR", "ST5"), rodar(DESC_PT, ref="# Guide\n\n## Contents\n\n- Part 1\n\n" + CORPO_LONGO))

    def test_sem_sumario_continua_erro(self):
        self.assertIn(("ERROR", "ST5"), rodar(DESC_PT, ref="# Guia\n\n" + CORPO_LONGO))


class TestCT9(unittest.TestCase):
    def test_todo_palavra_pt(self):
        corpo = "Mudar a raiz quebraria TODO o markup, por isso é vetado.\n"
        self.assertNotIn(("ERROR", "CT9"), rodar(DESC_PT, corpo=corpo))

    def test_todo_marcador(self):
        self.assertIn(("ERROR", "CT9"), rodar(DESC_PT, corpo="TODO: escrever o passo 3.\n"))

    def test_fixme(self):
        self.assertIn(("ERROR", "CT9"), rodar(DESC_PT, corpo="FIXME conferir o total.\n"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
