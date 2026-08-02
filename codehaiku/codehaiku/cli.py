"""CodeHaiku CLI — poetry distilled from code."""

import sys
from pathlib import Path

import click
from rich.console import Console

from .parser import parse_file, parse_source_string, LANGUAGE_MAP
from .composer import compose_multiple
from .display import (
    print_banner,
    print_haiku_gallery,
    print_word_cloud,
    print_stats,
    print_error,
    print_info,
    console,
)

SUPPORTED_EXTENSIONS = set(LANGUAGE_MAP.keys())


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option("1.0.0", prog_name="codehaiku")
def cli(ctx):
    """CodeHaiku — distill poetry from source code.

    Transform your code into haiku poetry by extracting meaningful words
    from identifiers, comments, and strings, then composing them into
    valid 5-7-5 syllable haiku.
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        click.echo(ctx.get_help())


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-n", "--count", default=3, show_default=True,
              help="Number of haikus to generate.")
@click.option("--syllables", is_flag=True,
              help="Show syllable counts per line.")
@click.option("--stats", "show_stats", is_flag=True,
              help="Show extraction statistics.")
@click.option("--words", "show_words", is_flag=True,
              help="Show word origin table for each haiku.")
@click.option("--seed", default=42, show_default=True,
              help="Random seed for reproducibility.")
@click.option("--recursive", "-r", is_flag=True,
              help="Recursively process directories.")
def read(path, count, syllables, show_stats, show_words, seed, recursive):
    """Generate haiku(s) from a source code file or directory."""
    p = Path(path)

    if p.is_file():
        _process_file(p, count, syllables, show_stats, show_words, seed)
    elif p.is_dir():
        files = []
        if recursive:
            for ext in SUPPORTED_EXTENSIONS:
                files.extend(p.rglob(f"*{ext}"))
        else:
            for ext in SUPPORTED_EXTENSIONS:
                files.extend(p.glob(f"*{ext}"))

        if not files:
            print_error(f"No supported source files found in {path}")
            print_info(f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
            sys.exit(1)

        files = sorted(set(files))[:10]  # Cap at 10 files for sanity
        print_info(f"Processing {len(files)} file(s)...")

        for f in files:
            _process_file(f, count=1, show_syllables=syllables,
                          show_stats=False, show_words=show_words, seed=seed)
    else:
        print_error(f"Path not recognized: {path}")
        sys.exit(1)


@cli.command()
@click.option("-n", "--count", default=3, show_default=True,
              help="Number of haikus to generate.")
@click.option("--syllables", is_flag=True,
              help="Show syllable counts per line.")
@click.option("--lang", default="python", show_default=True,
              help="Language hint for the input code.")
@click.option("--seed", default=42, show_default=True,
              help="Random seed for reproducibility.")
def pipe(count, syllables, lang, seed):
    """Generate haiku from code piped via stdin.

    Example:

        cat main.py | codehaiku pipe

        echo "def transform_darkness(): pass" | codehaiku pipe --lang python
    """
    if sys.stdin.isatty():
        print_error("No input detected. Pipe source code to stdin.")
        print_info("Example: cat main.py | codehaiku pipe")
        sys.exit(1)

    source = sys.stdin.read()
    if not source.strip():
        print_error("Empty input received.")
        sys.exit(1)

    result = parse_source_string(source, language=lang)
    haikus = compose_multiple(result, count=count, base_seed=seed)

    print_banner()
    print_haiku_gallery(haikus, file_path="<stdin>", show_syllables=syllables)

    if not haikus:
        print_error("Could not compose haikus. Try providing more code.")
        sys.exit(1)


@cli.command()
@click.argument("words", nargs=-1, required=True)
@click.option("--seed", default=42, show_default=True,
              help="Random seed for reproducibility.")
@click.option("-n", "--count", default=1, show_default=True,
              help="Number of haikus to generate.")
def freestyle(words, seed, count):
    """Generate haiku from a list of words.

    Example:

        codehaiku freestyle river memory ancient wandering silence light

    Words are treated as code identifiers and composed into haiku.
    """
    # Build a fake parse result from the given words
    from .parser import ParseResult, WordEntry
    from .syllables import count_syllables

    result = ParseResult(language='freestyle')
    result.words = [
        WordEntry(word=w.lower(), source='identifier', frequency=1)
        for w in words
        if len(w) >= 2
    ]

    if len(result.words) < 3:
        print_error("Please provide at least 3 words.")
        sys.exit(1)

    haikus = compose_multiple(result, count=count, base_seed=seed)

    print_banner()
    if haikus:
        print_haiku_gallery(haikus, file_path="freestyle", show_syllables=True)
    else:
        print_error("Could not form valid haiku from given words.")
        print_info("Try adding more varied words with different syllable counts.")
        sys.exit(1)


def _process_file(path: Path, count: int, show_syllables: bool,
                  show_stats: bool, show_words: bool, seed: int):
    """Process a single file and print its haiku(s)."""
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        print_error(f"Unsupported file type: {ext}")
        return

    result = parse_file(str(path))

    if len(result.words) < 5:
        print_error(f"Not enough words in {path.name} to compose a haiku.")
        return

    haikus = compose_multiple(result, count=count, base_seed=seed)

    print_haiku_gallery(haikus, file_path=str(path), show_syllables=show_syllables)

    if show_stats:
        print_stats(
            file_path=str(path),
            line_count=result.line_count,
            haiku_count=len(haikus),
            identifier_count=result.identifier_count,
            comment_count=result.comment_count,
        )

    if show_words and haikus:
        for haiku in haikus:
            print_word_cloud(haiku)
            console.print()


def main():
    cli()
