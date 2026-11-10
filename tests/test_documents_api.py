def test_project_imports():
    from backend.main import app
    assert app.title == "IT Troubleshooting Assistant"
