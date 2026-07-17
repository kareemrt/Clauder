"""Demo script showing Clauder's review capabilities without a real git repo."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from clauder.reviewer import ReviewResult, Issue
from clauder.formatter import render_terminal
from rich.console import Console

# Simulated review result to show off the UI without needing an API key
demo_result = ReviewResult(
    summary=(
        "This diff adds a user authentication endpoint. The implementation works "
        "but contains a critical SQL injection vulnerability and stores passwords "
        "in plaintext — both must be fixed before merging."
    ),
    score=42,
    highlights=[
        "Good use of try/except for error handling",
        "Clear separation of the login and register routes",
    ],
    issues=[
        Issue(
            category="security",
            severity="critical",
            title="SQL Injection via string interpolation",
            description="User input is interpolated directly into an SQL query string, allowing an attacker to manipulate the query.",
            file="auth/db.py",
            line="47",
            suggestion="Use parameterized queries: cursor.execute('SELECT * FROM users WHERE email = ?', (email,))",
        ),
        Issue(
            category="security",
            severity="critical",
            title="Plaintext password storage",
            description="Passwords are stored as raw strings in the database with no hashing applied.",
            file="auth/models.py",
            line="23",
            suggestion="Use bcrypt or argon2: password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())",
        ),
        Issue(
            category="bugs",
            severity="high",
            title="Token expiry not validated",
            description="JWT tokens are decoded but the 'exp' claim is never checked, so expired tokens are accepted.",
            file="auth/middleware.py",
            line="61-68",
            suggestion="Add: if payload['exp'] < time.time(): raise TokenExpiredError()",
        ),
        Issue(
            category="performance",
            severity="medium",
            title="N+1 query in user lookup",
            description="Each login check fires an additional SELECT for the user's roles, causing N+1 queries.",
            file="auth/views.py",
            line="89",
            suggestion="Use a JOIN: SELECT u.*, r.name FROM users u JOIN roles r ON u.role_id = r.id",
        ),
        Issue(
            category="style",
            severity="low",
            title="Magic number for token TTL",
            description="Token TTL is hardcoded as 86400 without explanation.",
            file="auth/tokens.py",
            line="12",
            suggestion="Define TOKEN_TTL_SECONDS = 24 * 60 * 60  # 24 hours",
        ),
        Issue(
            category="docs",
            severity="info",
            title="Missing docstrings on public functions",
            description="The authenticate() and generate_token() functions lack docstrings.",
            file="auth/utils.py",
            line="",
            suggestion="Add Google-style docstrings describing parameters and return values.",
        ),
    ],
    raw_diff_lines=312,
)

console = Console()
render_terminal(demo_result, console)
