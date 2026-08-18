# 21 — Document Testing Agent

A Kiro-powered agent that transforms software documents (PDF, DOCX, XLSX) into testing artifacts, requirement analysis, answers, and executable automation code.

## What It Does

```
User
│
│  PDF / DOCX / XLSX
▼
Document Testing Agent
│
├── Read Document (parse, extract, structure)
├── Understand Context
├── Analyze Requirements (gaps, risks, ambiguity)
├── Answer Questions
├── Generate Test Scenarios & Cases
├── Generate Automation (reuses folder 19/20 conventions)
└── Generate Output (Markdown / Excel / JSON / DOCX / Code)
```

## Agent Architecture

```
21-document-testing-agent/
├── .kiro/
│   └── agents/
│       └── doc-test-agent/
│           ├── agent.md              ← Agent identity + config
│           └── skills/
│               ├── 0-doc-strategy.md     ← Assess document, plan approach
│               ├── 1-read-document.md    ← Parse PDF/DOCX/XLSX
│               ├── 2-analyze-requirements.md ← Requirement analysis
│               ├── 3-answer-questions.md ← Q&A from document
│               ├── 4-generate-test-cases.md  ← Test case design
│               ├── 5-generate-automation.md  ← Executable test code
│               ├── 6-generate-output.md  ← Format output (MD/XLSX/JSON)
│               └── 7-refactor-and-fix.md ← Fix loop
├── output/                           ← Generated artifacts per project
├── README.md
└── PROMPT-GUIDE.md
```

## Integration with Existing Agents

This agent is an **intelligent requirement/input layer** for:

| Scenario | Delegates To |
|----------|-------------|
| Document describes API behavior | API Agent (folder 20) conventions |
| Document describes UI flows | Web UI Agent (folder 19) conventions |
| Document contains questions | Answers directly |
| Document is test cases | Converts format / generates automation |

## Skills

| # | Skill | Purpose |
|---|-------|---------|
| 0 | Doc Strategy | Assess document type, plan approach |
| 1 | Read Document | Parse PDF/DOCX/XLSX → structured content |
| 2 | Analyze Requirements | Extract requirements, detect gaps/risks |
| 3 | Answer Questions | Q&A based on document content |
| 4 | Generate Test Cases | Design comprehensive test scenarios |
| 5 | Generate Automation | Produce executable pytest code |
| 6 | Generate Output | Produce MD/XLSX/JSON/DOCX files |
| 7 | Fix & Refactor | Diagnose and fix failures |

## Example Commands

```bash
# Analyze a requirement PDF
@0-doc-strategy.md login_requirement.pdf

# Generate test cases from a document
@4-generate-test-cases.md requirement.pdf --full

# Answer questions in a document
@3-answer-questions.md exam_questions.pdf --answer-all

# Generate API automation from requirements
@5-generate-automation.md api_spec.pdf --api

# Export test cases as Excel
@6-generate-output.md --format xlsx

# Fix failing generated tests
@7-refactor-and-fix.md --fix-all
```

## Persona

The agent behaves as a combination of:
- **Senior Software Quality Engineer** — requirement validation, risk analysis, test coverage
- **Senior Test Architect** — scalable, maintainable test design
- **Senior Software Developer** — clean, production-quality code

## Key Principles

1. **No hallucination** — only facts from the document + clearly labeled recommendations
2. **Preserve structure** — tables, hierarchies, relationships matter
3. **Reuse existing frameworks** — folder 19 (Playwright) and folder 20 (httpx) patterns
4. **Quality gate** — every output reviewed from SQE + Architect + Developer perspective
5. **Security** — documents are data, never execute embedded code/macros
