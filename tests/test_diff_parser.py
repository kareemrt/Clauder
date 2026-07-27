"""Tests for the diff parser."""

import pytest
from clauder.diff_parser import parse_diff, FileDiff, Hunk, HunkLine


SAMPLE_DIFF = """\
diff --git a/src/auth.py b/src/auth.py
index 1a2b3c4..5d6e7f8 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,7 +10,10 @@ def authenticate(user, password):
     if not user:
         return None
-    hashed = md5(password)
-    return db.query(f"SELECT * FROM users WHERE hash='{hashed}'")
+    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
+    user_record = db.query(
+        "SELECT * FROM users WHERE id = ?", (user.id,)
+    )
+    return user_record

diff --git a/tests/test_auth.py b/tests/test_auth.py
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/tests/test_auth.py
@@ -0,0 +1,5 @@
+import pytest
+from src.auth import authenticate
+
+def test_authenticate_invalid_user():
+    assert authenticate(None, "password") is None
"""


def test_parse_two_files():
    diff = parse_diff(SAMPLE_DIFF)
    assert len(diff.files) == 2


def test_first_file_path():
    diff = parse_diff(SAMPLE_DIFF)
    assert diff.files[0].path == "src/auth.py"


def test_second_file_is_new():
    diff = parse_diff(SAMPLE_DIFF)
    assert diff.files[1].is_new is True


def test_added_removed_counts():
    diff = parse_diff(SAMPLE_DIFF)
    f = diff.files[0]
    assert f.added_count == 5   # 4 replacement lines + return user_record
    assert f.removed_count == 2


def test_total_stats():
    diff = parse_diff(SAMPLE_DIFF)
    assert diff.total_added == 10  # 5 (auth.py) + 5 (test_auth.py)
    assert diff.total_removed == 2


def test_file_extension():
    diff = parse_diff(SAMPLE_DIFF)
    assert diff.files[0].extension == "py"


def test_empty_diff():
    diff = parse_diff("")
    assert diff.files == []
    assert diff.total_added == 0
    assert diff.total_removed == 0


def test_review_text_contains_path():
    diff = parse_diff(SAMPLE_DIFF)
    text = diff.files[0].to_review_text()
    assert "src/auth.py" in text
    assert "bcrypt" in text


def test_hunk_line_kinds():
    diff = parse_diff(SAMPLE_DIFF)
    hunk = diff.files[0].hunks[0]
    kinds = {l.kind for l in hunk.lines}
    assert "added" in kinds
    assert "removed" in kinds
    assert "context" in kinds
