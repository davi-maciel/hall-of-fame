# Hall da Fama — Brasil nas Olimpíadas Científicas Internacionais

Dataset + site estático sobre todos os estudantes que representaram o Brasil em
olimpíadas científicas internacionais — quem participou, quando, com que resultado,
e as fontes que comprovam cada edição.

**11 olimpíadas até agora** (IMO, IChO, IOI, IOAA, IPhO, EuPhO, OIbF, NBPhO, IJSO,
OII/CIIC, EGOI) · ~780 estudantes · ~1.170 participações.

## Estrutura

- Uma pasta por olimpíada: `data/raw/<id>.json` (registros canônicos) →
  `src/data/graph.json` (estudantes + arestas de coparticipação), com
  `data/corroboration.json` listando as fontes verificadas de cada edição.
- `site/` — a interface (tabela, páginas de estudante com trajetória, equipe e
  fontes). Estático, sem dependências.

## Rodar o site

```bash
python3 site/scripts/build_people.py    # consolida identidades (termina com o identity gate)
python3 site/scripts/build_sources.py   # agrega as fontes por edição
python3 -m http.server 8741 -d site     # http://localhost:8741/
```

## Princípios dos dados

- Cada edição tem fontes verificáveis (URL + classe de proveniência + conteúdo
  conferido); resultados nunca são estimados.
- Identidades são unificadas entre olimpíadas com revisão humana
  (`site/scripts/aliases.json` / `distinct.json`); o build falha se houver
  candidatos a duplicata não resolvidos.
- Eventos futuros não entram: resultados só após a edição acontecer.
