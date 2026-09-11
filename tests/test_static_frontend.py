from pathlib import Path


def test_activity_cards_render_a_participants_list_section():
    js = Path("src/static/app.js").read_text()

    assert "participants-list" in js
    assert "details.participants" in js


def test_backend_supports_unregister_via_delete_endpoint():
    py = Path("src/app.py").read_text()

    assert "@app.delete" in py
    assert "activity[\"participants\"].remove(email)" in py


def test_signup_success_refreshes_activity_cards_without_reload():
    js = Path("src/static/app.js").read_text()

    signup_branch = js[js.find("signupForm.addEventListener") : js.find("// Initialize app")]

    assert "fetchActivities();" in signup_branch
