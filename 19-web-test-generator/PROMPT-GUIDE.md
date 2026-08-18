# Prompt Guide — Web Test Generator Agent

Panduan cara menggunakan agent ini untuk generate automation testing website secara cepat, akurat, dan profesional.

---

## Quick Start

### Full Professional Pipeline (Recommended)

Prompt ini akan menjalankan semua skill berurutan — dari strategy sampai kode:

```
Generate complete professional test suite untuk https://practicesoftwaretesting.com
Mulai dari:
1. Risk-based test strategy
2. Analisis halaman
3. Test case (positive, negative, edge, security)
4. Automation code (Playwright + pytest)
5. Accessibility test (WCAG 2.1 AA)
6. API intercept & performance test
7. Visual regression test
```

### Quick Functional Tests Only

Kalau cuma butuh functional test cepat:

```
Generate automation test untuk login page di https://practicesoftwaretesting.com/auth/login
Include positive, negative, dan edge case. Pakai POM pattern + Allure.
```

---

## Output — Kemana Hasilnya Disimpan?

Setiap website yang di-generate punya folder sendiri:

```
19-web-test-generator/
├── .kiro/                ← Agent definition (tidak berubah)
├── output/               ← SEMUA hasil generate ada di sini
│   ├── practicesoftwaretesting/     ← website 1
│   │   ├── docs/                    ← test-strategy, analysis, test-cases
│   │   └── automation/              ← full runnable code
│   ├── tokopedia/                   ← website 2
│   │   ├── docs/
│   │   └── automation/
│   └── myapp-staging/               ← website 3
│       ├── docs/
│       └── automation/
├── PROMPT-GUIDE.md
└── README.md
```

**Naming dari URL:**
- `https://practicesoftwaretesting.com` → `output/practicesoftwaretesting/`
- `https://www.tokopedia.com` → `output/tokopedia/`
- `https://staging.myapp.io` → `output/myapp-staging/`

**Custom name:** Tambah `--name` di prompt:
```
Generate test untuk https://myapp.com --name myapp-v2
→ output/myapp-v2/
```

**Folder sudah ada?** Agent akan tanya: overwrite, rename, atau abort.

---

## Contoh Prompt per Skill

### Skill 0 — Test Strategy (Risk-Based)

Gunakan di awal project baru untuk prioritas yang benar:

```
Buat risk-based test strategy untuk https://practicesoftwaretesting.com
Analisis semua fitur, kasih risk score, dan tentukan coverage level per fitur.
Include: quality gates, browser matrix, dan execution schedule.
```

```
Sebagai Senior QE, buat test strategy untuk e-commerce app di https://mystore.com
Business context: 50k daily users, revenue dari checkout flow.
Prioritaskan berdasarkan business impact.
```

```
Evaluate ROI automasi testing untuk website https://myapp.com
Fitur mana yang worth automate vs manual test? Mana yang butuh mock?
```

---

### Skill 1 — Analyze Website

```
Analisis halaman https://practicesoftwaretesting.com/auth/login
Identifikasi: semua element interaktif, form validation rules, user flow, dan selector strategy.
```

```
Scan seluruh website https://practicesoftwaretesting.com
List semua halaman, fitur, dan interaksi yang bisa di-test.
Klasifikasikan per priority (critical/high/medium/low).
```

---

### Skill 2 — Generate Test Cases

```
Generate test case lengkap untuk fitur checkout:
- Critical: complete purchase flow
- Positive: semua payment method, berbagai product
- Negative: invalid card, expired card, insufficient balance, empty fields
- Edge case: concurrent purchase, back button during payment, session timeout
- Security: XSS di address field, SQL injection di coupon code
```

```
Buatkan test case untuk form registration dengan severity dan priority:
- CRITICAL: successful registration
- NORMAL: validation per field (email format, password strength, required fields)
- MINOR: edge case (unicode name, max length, special chars)
Assign TC-ID format TC-REG-001, TC-REG-002, dst.
```

---

### Skill 3 — Generate Automation Code

```
Generate Playwright automation lengkap untuk fitur login dan registration.
Output:
- pages/login_page.py
- pages/register_page.py
- tests/test_login.py (8+ test cases)
- tests/test_registration.py (10+ test cases)
- tests/test_data.py
- Full project skeleton (conftest, pytest.ini, requirements, .env)
```

```
Generate automation test untuk checkout flow end-to-end:
Login → Browse → Add to Cart → Checkout → Payment → Confirmation
Pakai fixture logged_in_page dan parametrize untuk multiple products.
```

---

### Skill 4 — Accessibility Testing

```
Generate accessibility test suite untuk https://practicesoftwaretesting.com
Cover:
- axe-core scan semua halaman kritis (score harus >= 90)
- Keyboard navigation (login form, checkout form)
- ARIA labels pada semua form inputs
- Color contrast check
- Heading hierarchy
- Image alt text
```

```
Buat a11y test khusus untuk flow checkout:
- Form bisa di-navigate full pakai keyboard (Tab, Enter, Escape)
- Error messages di-announce ke screen reader (aria-live)
- Focus management benar setelah submit
```

---

### Skill 5 — API Intercept & Performance

```
Generate API intercept test untuk login flow:
- Verify request payload (email + password ke /users/login)
- Mock 401 response → verify error message di UI
- Mock 500 response → verify graceful error handling
- Mock slow response (5s) → verify loading state muncul
- Mock network offline → verify no crash
```

```
Generate performance test dengan budget:
- Semua halaman load < 3 detik
- API response < 1 detik
- Network requests per page < 30
- Core Web Vitals (LCP < 2.5s, CLS < 0.1)
```

```
Test bagaimana UI handle ketika backend down:
- Products page dengan API return 500
- Cart page dengan network offline
- Checkout dengan payment gateway timeout
Verify: user sees friendly error, no raw stack trace, no data loss.
```

---

### Skill 6 — Visual Regression

```
Generate visual regression test untuk semua halaman kritis:
- Homepage (desktop + tablet + mobile)
- Login page
- Product listing
- Product detail
- Cart
- Checkout
Threshold: 0.1% pixel diff. Include cross-browser comparison.
```

```
Generate component state visual test:
- Button states: default, hover, focus, disabled
- Form field states: empty, filled, error, success
- Alert/notification: info, warning, error, success
- Loading skeleton vs loaded content
```

```
Generate responsive visual test:
- Test di 3 viewport: mobile (375px), tablet (768px), desktop (1366px)
- Verify navigation collapse di mobile
- Verify grid layout change di tablet
- Update baselines setelah redesign: --update-baselines
```

---

## Combo Prompts (Multiple Skills)

### New Project (Full Pipeline)
```
Saya punya website baru di https://myapp.com
Tolong:
1. Buat test strategy (risk assessment + browser matrix)
2. Analisis 5 halaman kritis
3. Generate test case per halaman (total ~50 test cases)
4. Generate automation code lengkap
5. Include accessibility dan visual regression
Output harus production-ready, bisa langsung jalan di CI/CD.
```

### Existing Project Enhancement
```
Saya sudah punya functional test untuk login dan cart.
Tambahkan:
- Accessibility test (axe-core + keyboard)
- API intercept test (mock backend failures)
- Visual regression (baseline screenshots)
- Performance budget test (Web Vitals)
Untuk halaman: login, product listing, cart, checkout.
```

### Pre-Release Check
```
Generate pre-release test checklist:
- Smoke test (5 critical paths, < 5 menit)
- Accessibility score check semua halaman
- Visual regression vs last release baseline
- Performance budget verification
- Cross-browser quick check (Chrome + Firefox + Safari)
```

---

## Tips untuk Hasil Optimal

### 1. Selalu kasih business context
```
❌ "Test website ini"
✅ "Test e-commerce platform ini. Revenue dari checkout. 50k daily users. 
    Prioritas: checkout > login > search > product browse"
```

### 2. Sebutkan constraint/requirement
```
"Generate test dengan constraint:
- Harus jalan di CI/CD (headless, no GPU)
- Max execution time: 30 menit untuk full suite
- Harus support 3 browser (Chrome, Firefox, Safari)
- Accessibility score minimum 90
- No flaky tests (retry max 2x)"
```

### 3. Sebutkan kalau ada limitation
```
"Website ini tidak punya data-test attributes.
Pakai role-based selector dan text content sebagai fallback.
Jangan pakai XPath."
```

### 4. Minta output spesifik
```
"Generate HANYA test file (tanpa project skeleton).
Saya sudah punya conftest.py dan base_page.py.
Tambahkan test_checkout.py dan checkout_page.py saja."
```

---

## Execution Commands Reference

```bash
# === Setup (pertama kali) ===
cd output/practicesoftwaretesting/automation
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install firefox
brew install allure

# === Run Tests (report auto-open di browser) ===
pytest -v              # semua tests + report
pytest -m smoke -v     # 9 critical path + report
pytest -m wave1 -v     # 47 functional + report
pytest -m a11y -v      # 16 accessibility + report

# === Other Markers ===
pytest -m regression -v
pytest -m critical -v
pytest -m negative -v

# === Cross-Browser ===
playwright install chromium webkit
pytest --browser firefox --browser chromium --browser webkit -v

# === Debug (lihat browser) ===
pytest --browser firefox --headed --slowmo=500 -v
pytest tests/test_login.py::TestLogin::test_login_valid_credentials -v --headed

# === Parallel ===
pip install pytest-xdist
pytest -n auto

# === Deactivate venv ===
deactivate
```

### Report
- Otomatis open di browser setelah `pytest` selesai
- Screenshot full-page di setiap step
- Hanya tampil hasil run saat ini (bukan akumulasi)
- Prerequisite: `brew install allure`

---

## Skill 7 — Refactor & Fix

Kalau ada test gagal, gunakan Skill 7:

```
@7-refactor-and-fix.md fix this #Terminal
@7-refactor-and-fix.md --fix-all
@7-refactor-and-fix.md --refactor pages
```

| Mode | Fungsi |
|------|--------|
| `fix this #Terminal` | Kiro baca error dari terminal, fix otomatis |
| `--fix-all` | Agent jalankan pytest sendiri, loop fix sampai 0 failures |
| `--refactor [scope]` | Improve code quality (pages/tests/config/all) |

**Tips kasih error ke agent:**
- Paling gampang: ketik `#Terminal` dan Kiro baca sendiri
- Atau copy-paste bagian `short test summary info` saja
- Atau `--fix-all` biar agent run + fix sendiri

---

## FAQ

**Q: Agent generate terlalu banyak test, saya mau yang essential saja?**
A: Gunakan prompt: "Generate hanya smoke test (5-10 test, critical path saja)."

**Q: Website saya butuh login dulu, bagaimana?**
A: Agent otomatis generate `logged_in_page` fixture. Sertakan credentials di prompt atau akan di-generate dengan placeholder.

**Q: Bisa untuk mobile app (React Native / Flutter)?**
A: Agent ini khusus web. Tapi bisa test mobile web (responsive viewport). Untuk native app, perlu agent berbeda.

**Q: Test flaky, apa yang harus dilakukan?**
A: Baca `.kiro/steering/test-quality-standards.md` — ada section "Flaky Test Prevention" dengan root cause table dan stability checklist.

**Q: Berapa lama waktu generate?**
A: Skill 0-2 (planning): ~2 menit. Skill 3-6 (code): ~5 menit. Total full pipeline: ~7 menit.
