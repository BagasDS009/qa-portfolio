# Prompt Guide — Document Testing Agent

## Quick Reference

### Analyze a Document
```
@0-doc-strategy.md [attach PDF/DOCX/XLSX]
```
→ Assesses document type, plans approach, estimates output.

### Full Requirement Analysis
```
@2-analyze-requirements.md [attach document] --full
```
→ Extracts requirements, business rules, detects gaps, identifies risks.

### Answer Questions
```
@3-answer-questions.md [attach document] --answer-all
```
→ Finds and answers all questions in the document.

### Generate Test Cases
```
@4-generate-test-cases.md [attach document] --full
```
→ Produces positive, negative, boundary, edge, and security test cases.

### Generate Automation (API)
```
@5-generate-automation.md [attach document] --api
```
→ Produces pytest + httpx automation following folder 20 conventions.

### Generate Automation (Web UI)
```
@5-generate-automation.md [attach document] --ui
```
→ Produces Playwright + pytest automation following folder 19 conventions.

### Export as Excel
```
@6-generate-output.md --format xlsx
```
→ Exports test cases or analysis as `.xlsx` file.

### Fix Generated Tests
```
@7-refactor-and-fix.md --fix-all
```
→ Runs tests, diagnoses failures, fixes until green.

---

## Workflow Examples

### Example 1: Requirement PDF → Test Cases → Automation

```
1. @0-doc-strategy.md login_requirement.pdf
2. @2-analyze-requirements.md login_requirement.pdf --full
3. @4-generate-test-cases.md login_requirement.pdf --full
4. @5-generate-automation.md login_requirement.pdf --api
5. @7-refactor-and-fix.md --fix-all
```

### Example 2: Excel Test Cases → Automation Code

```
1. @1-read-document.md test_cases.xlsx
2. @5-generate-automation.md test_cases.xlsx --from-test-cases
3. @7-refactor-and-fix.md --fix-all
```

### Example 3: Document with Questions → Answers

```
1. @3-answer-questions.md exam_document.pdf --answer-all
2. @6-generate-output.md --format md
```

### Example 4: Mixed Document → Full Analysis + Output

```
1. @0-doc-strategy.md sprint_stories.docx
2. @2-analyze-requirements.md sprint_stories.docx --full
3. @4-generate-test-cases.md sprint_stories.docx --full
4. @6-generate-output.md --format xlsx
```

---

## Tips

- Always start with `@0-doc-strategy.md` for unfamiliar documents
- Use `--full` flag for comprehensive analysis
- Use `--api` or `--ui` flag to specify automation type
- The agent will ask for clarification if the document is ambiguous
- Generated automation follows existing folder 19/20 conventions — no new frameworks
- If tests fail, use `@7-refactor-and-fix.md --fix-all` for automatic fix loop
