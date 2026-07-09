"""
Generates Markdown reports from analyzed git data.
"""
from collections import defaultdict
from datetime import datetime
from pathlib import Path


COMMIT_TYPE_EMOJI = {
    "feature":  "✨",
    "fix":      "🐛",
    "docs":     "📝",
    "test":     "🧪",
    "refactor": "♻️",
    "chore":    "🔧",
    "style":    "🎨",
    "perf":     "⚡",
    "merge":    "🔀",
    "other":    "📦",
}


def generate_markdown_report(
    repo_name: str,
    commits: list,
    file_stats: dict,
    contributors: dict,
    monthly: dict,
    summary: dict,
    output_path: str = "CODEPULSE_REPORT.md",
) -> str:
    lines = []

    # Title
    lines.append(f"# 💓 CodePulse Report — `{repo_name}`")
    lines.append(f"\n> Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC\n")

    # Summary stats
    lines.append("## 📊 Summary\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| 📊 Total Commits | **{summary.get('total_commits', 0):,}** |")
    lines.append(f"| 👥 Contributors | **{summary.get('contributors', 0)}** |")
    lines.append(f"| 📁 Files Changed | **{summary.get('files_changed', 0):,}** |")
    lines.append(f"| ➕ Lines Added | **+{summary.get('insertions', 0):,}** |")
    lines.append(f"| ➖ Lines Removed | **-{summary.get('deletions', 0):,}** |")
    lines.append(f"| 📅 Active Days | **{summary.get('active_days', 0)}** |")
    lines.append(f"| ⏳ Repo Age | **{summary.get('age', '?')}** |")
    lines.append(f"| 🔥 Most Active Day | **{summary.get('most_active_day', '?')}** |")

    # Commit type breakdown
    lines.append("\n## 🏷️ Commit Types\n")
    type_counts: dict = defaultdict(int)
    for c in commits:
        type_counts[c.commit_type] += 1
    total = len(commits) or 1

    lines.append("| Type | Count | Share |")
    lines.append("|------|-------|-------|")
    for ctype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        icon = COMMIT_TYPE_EMOJI.get(ctype, "📦")
        pct = count / total * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        lines.append(f"| {icon} `{ctype}` | **{count}** | `{bar}` {pct:.1f}% |")

    # Monthly activity
    lines.append("\n## 📅 Monthly Activity\n")
    lines.append("| Month | Commits | Trend |")
    lines.append("|-------|---------|-------|")
    mx = max(monthly.values()) if monthly else 1
    for month, count in sorted(monthly.items())[-24:]:
        bar_len = int(count / mx * 20)
        bar = "█" * bar_len
        lines.append(f"| `{month}` | **{count}** | `{bar}` |")

    # Top contributors
    lines.append("\n## 👥 Top Contributors\n")
    lines.append("| # | Author | Commits | +Added | -Removed | Files |")
    lines.append("|---|--------|---------|--------|----------|-------|")
    sorted_contributors = sorted(
        contributors.items(), key=lambda x: x[1]["commits"], reverse=True
    )[:10]
    medals = ["🥇", "🥈", "🥉"]
    for i, (author, stats) in enumerate(sorted_contributors):
        medal = medals[i] if i < 3 else str(i + 1)
        lines.append(
            f"| {medal} | **{author}** | {stats['commits']:,} | "
            f"+{stats['insertions']:,} | -{stats['deletions']:,} | {len(stats['files']):,} |"
        )

    # Top churned files (hotspots)
    lines.append("\n## 🔥 Hotspot Files (Most Changed)\n")
    lines.append("> High churn = higher risk area. Consider adding tests!\n")
    top_files = sorted(file_stats.values(), key=lambda f: f.commits, reverse=True)[:15]
    lines.append("| File | Commits | Churn | Authors |")
    lines.append("|------|---------|-------|---------|")
    for fs in top_files:
        risk = "🔴" if fs.churn > 1000 else "🟡" if fs.churn > 300 else "🟢"
        lines.append(
            f"| `{fs.path}` | {fs.commits} | {risk} {fs.churn:,} | {len(fs.authors)} |"
        )

    # Language breakdown
    lines.append("\n## 🌐 Language Breakdown (by churn)\n")
    ext_churn: dict = defaultdict(int)
    for fs in file_stats.values():
        ext_churn[fs.ext] += fs.churn
    sorted_ext = sorted(ext_churn.items(), key=lambda x: x[1], reverse=True)[:15]
    total_churn = sum(v for _, v in sorted_ext) or 1

    lines.append("| Extension | Churn | Share |")
    lines.append("|-----------|-------|-------|")
    for ext, churn in sorted_ext:
        pct = churn / total_churn * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        lines.append(f"| `.{ext}` | {churn:,} | `{bar}` {pct:.1f}% |")

    # Recent commits
    lines.append("\n## 📜 Recent Commits\n")
    recent = sorted(commits, key=lambda c: c.date, reverse=True)[:20]
    lines.append("| Date | Author | Type | Message |")
    lines.append("|------|--------|------|---------|")
    for c in recent:
        icon = COMMIT_TYPE_EMOJI.get(c.commit_type, "📦")
        msg = c.message[:60] + ("…" if len(c.message) > 60 else "")
        lines.append(
            f"| `{c.date.strftime('%Y-%m-%d')}` | {c.author} | {icon} `{c.commit_type}` | {msg} |"
        )

    lines.append("\n---")
    lines.append(f"\n*Generated by [CodePulse](https://github.com/kareemrt/clauder) — Git Repository Health Visualizer*")

    content = "\n".join(lines)
    Path(output_path).write_text(content, encoding="utf-8")
    return content
