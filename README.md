# Currículo — Victor Emanuel Maksud Carneiro

Currículo-site no padrão australiano/internacional, feito para o intercâmbio na Gold Coast (QLD).

**Site:** https://curriculo-victor-emanuel-maksud-carneiro.onrender.com
(inglês na raiz, português em `/pt/`)

## O que tem aqui

| Caminho | O que é |
| --- | --- |
| `index.html` | Site em inglês (gerado) |
| `pt/index.html` | Site em português (gerado) |
| `assets/` | CSS e favicon do site |
| `Victor-Maksud-Carneiro-Resume.pdf` | Currículo em PDF, A4, 2 páginas, padrão australiano (gerado) |
| `src/content.py` | **Todo o texto do site** (inglês e português) — edite aqui |
| `src/build.py` | Gera `index.html` e `pt/index.html` a partir do `content.py` |
| `src/resume.html` | Texto e layout do PDF |
| `src/make_pdf.py` | Gera o PDF a partir do `resume.html` |
| `src/fonts/` | Fonte Inter (licença OFL) usada no PDF |
| `design/` | Arquivos do design original feito no Claude (canvas) |
| `docs/pesquisa-curriculo-padrao-australiano.md` | Pesquisa sobre currículo no padrão australiano |
| `versao-2025/` | Versão anterior do currículo (site, PDF e foto) |

## Como atualizar

```bash
# 1. edite os textos do site em src/content.py e os do PDF em src/resume.html
# 2. gere o site
python3 src/build.py
# 3. gere o PDF (precisa de: pip install playwright && playwright install chromium)
python3 src/make_pdf.py
```

Depois é só fazer commit e push: o Render publica o site estático direto da raiz do repositório.

## Campos a preencher

Os trechos entre `[colchetes]` ainda precisam dos seus dados: celular australiano, validade do visto,
mês de disponibilidade, data de início na DIMAK, detalhes das mentorias de IA, instituição do
intercâmbio e nota do IELTS (se tiver).

## Decisões do padrão australiano

- Sem foto, data de nascimento, estado civil, CPF ou endereço completo — só "Gold Coast, QLD".
- Telefone só no PDF, nunca no site público.
- Linha de direito de trabalho: Student visa (subclass 500), até 48 horas por quinzena no período letivo
  e tempo integral nas férias.
- Cursos da Cisco e da Oracle listados como *course certificate* (não como "Certified").
- PDF em coluna única e com texto selecionável, para passar nos sistemas de triagem (ATS).
