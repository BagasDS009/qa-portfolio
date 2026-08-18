# Traceability Matrix — Practice Software Testing (Toolshop)

Maps TC-IDs from `test-cases.md` → test methods → page objects.

## Login

| TC-ID | Test Method | Page Object | Marker |
|-------|-------------|-------------|--------|
| TC-LOGIN-001 | `test_login.py::TestLogin::test_login_valid_credentials` | `LoginPage` | smoke, critical |
| TC-LOGIN-002 | `test_login.py::TestLogin::test_login_admin` | `LoginPage` | regression |
| TC-LOGIN-003 | `test_login.py::TestLogin::test_login_wrong_password` | `LoginPage` | smoke, negative |
| TC-LOGIN-004 | `test_login.py::TestLogin::test_login_unregistered_email` | `LoginPage` | regression, negative |
| TC-LOGIN-005 | `test_login.py::TestLogin::test_login_empty_email` | `LoginPage` | regression, negative |
| TC-LOGIN-006 | `test_login.py::TestLogin::test_login_empty_password` | `LoginPage` | regression, negative |
| TC-LOGIN-007 | `test_login.py::TestLogin::test_login_sql_injection` | `LoginPage` | regression, edge |
| TC-LOGIN-008 | `test_login.py::TestLogin::test_login_xss_attempt` | `LoginPage` | regression, edge |

## Registration

| TC-ID | Test Method | Page Object | Marker |
|-------|-------------|-------------|--------|
| TC-REG-001 | `test_registration.py::TestRegistration::test_registration_valid` | `RegisterPage` | smoke, critical |
| TC-REG-003 | `test_registration.py::TestRegistration::test_registration_min_password` | `RegisterPage` | regression |
| TC-REG-004 | `test_registration.py::TestRegistration::test_registration_duplicate_email` | `RegisterPage` | smoke, negative |
| TC-REG-005 | `test_registration.py::TestRegistration::test_registration_empty_fields` | `RegisterPage` | regression, negative |
| TC-REG-006 | `test_registration.py::TestRegistration::test_registration_invalid_email` | `RegisterPage` | regression, negative |
| TC-REG-007 | `test_registration.py::TestRegistration::test_registration_weak_password` | `RegisterPage` | regression, negative |
| TC-REG-008 | `test_registration.py::TestRegistration::test_registration_short_password` | `RegisterPage` | regression, negative |
| TC-REG-009 | `test_registration.py::TestRegistration::test_registration_unicode_name` | `RegisterPage` | regression, edge |
| TC-REG-011 | `test_registration.py::TestRegistration::test_registration_html_injection` | `RegisterPage` | regression, edge |

## Search & Filter

| TC-ID | Test Method | Page Object | Marker |
|-------|-------------|-------------|--------|
| TC-SEARCH-001 | `test_search.py::TestSearch::test_search_valid_keyword` | `HomePage` | smoke, critical |
| TC-SEARCH-002 | `test_search.py::TestSearch::test_search_partial_keyword` | `HomePage` | regression |
| TC-SEARCH-003 | `test_search.py::TestSearch::test_filter_by_category` | `HomePage` | regression |
| TC-SEARCH-004 | `test_search.py::TestSearch::test_sort_price_ascending` | `HomePage` | regression |
| TC-SEARCH-005 | `test_search.py::TestSearch::test_search_no_results` | `HomePage` | regression, negative |
| TC-SEARCH-006 | `test_search.py::TestSearch::test_search_empty_query` | `HomePage` | regression |
| TC-SEARCH-007 | `test_search.py::TestSearch::test_search_sql_wildcard` | `HomePage` | regression, edge |
| TC-SEARCH-008 | `test_search.py::TestSearch::test_search_special_chars` | `HomePage` | regression, edge |

## Cart

| TC-ID | Test Method | Page Object | Marker |
|-------|-------------|-------------|--------|
| TC-CART-001 | `test_cart.py::TestCart::test_add_to_cart` | `HomePage`, `ProductDetailPage` | smoke, critical |
| TC-CART-002 | `test_cart.py::TestCart::test_add_multiple_products` | `HomePage`, `ProductDetailPage`, `CartPage` | regression |
| TC-CART-003 | `test_cart.py::TestCart::test_update_quantity` | `CartPage` | regression |
| TC-CART-004 | `test_cart.py::TestCart::test_proceed_empty_cart` | `CartPage` | regression, negative |
| TC-CART-005 | `test_cart.py::TestCart::test_quantity_zero` | `CartPage` | regression, negative |
| TC-CART-006 | `test_cart.py::TestCart::test_negative_quantity` | `CartPage` | regression, negative, edge |
| TC-CART-008 | `test_cart.py::TestCart::test_remove_all_items` | `CartPage` | regression, edge |

## Checkout

| TC-ID | Test Method | Page Object | Marker |
|-------|-------------|-------------|--------|
| TC-CHECKOUT-001 | `test_checkout.py::TestCheckout::test_checkout_bank_transfer` | `CheckoutPage` | smoke, critical |
| TC-CHECKOUT-002 | `test_checkout.py::TestCheckout::test_checkout_cash_on_delivery` | `CheckoutPage` | regression |
| TC-CHECKOUT-003 | `test_checkout.py::TestCheckout::test_checkout_different_country` | `CheckoutPage` | regression |
| TC-CHECKOUT-004 | `test_checkout.py::TestCheckout::test_checkout_empty_billing` | `CheckoutPage` | smoke, negative |
| TC-CHECKOUT-005 | `test_checkout.py::TestCheckout::test_checkout_empty_payment` | `CheckoutPage` | regression, negative |
| TC-CHECKOUT-006 | `test_checkout.py::TestCheckout::test_checkout_without_login` | `CheckoutPage`, `LoginPage` | regression, negative |

## Contact

| TC-ID | Test Method | Page Object | Marker |
|-------|-------------|-------------|--------|
| TC-CONTACT-001 | `test_contact.py::TestContact::test_contact_valid_submission` | `ContactPage` | regression |
| TC-CONTACT-002 | `test_contact.py::TestContact::test_contact_all_subjects[*]` | `ContactPage` | regression |
| TC-CONTACT-003 | `test_contact.py::TestContact::test_contact_empty_fields` | `ContactPage` | regression, negative |
| TC-CONTACT-004 | `test_contact.py::TestContact::test_contact_invalid_email` | `ContactPage` | regression, negative |
| TC-CONTACT-005 | `test_contact.py::TestContact::test_contact_short_message` | `ContactPage` | regression, negative |
| TC-CONTACT-006 | `test_contact.py::TestContact::test_contact_xss_message` | `ContactPage` | regression, edge |

---

*Generated by Web Test Generator Agent — Skill 3*
*Date: 2026-08-15*
