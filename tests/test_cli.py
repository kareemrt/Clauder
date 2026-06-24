import xml.etree.ElementTree as ET

from lsystemgarden.cli import main
from lsystemgarden.presets import PRESETS


def test_list_command_runs_and_mentions_every_preset(capsys):
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    for name in PRESETS:
        assert name in out


def test_render_command_writes_valid_svg(tmp_path):
    output = tmp_path / "out.svg"
    assert main(["render", "koch_snowflake", "-o", str(output), "--iterations", "2"]) == 0
    assert output.exists()
    ET.fromstring(output.read_text())


def test_render_command_creates_missing_parent_dirs(tmp_path):
    output = tmp_path / "nested" / "deep" / "out.svg"
    assert main(["render", "binary_tree", "-o", str(output), "--iterations", "1"]) == 0
    assert output.exists()


def test_render_command_honors_color_overrides(tmp_path):
    output = tmp_path / "out.svg"
    main(["render", "koch_snowflake", "-o", str(output), "--iterations", "1", "--start-color", "#112233"])
    assert "#112233" in output.read_text()


def test_render_command_honors_seed_override_for_stochastic_preset(tmp_path):
    out_a = tmp_path / "a.svg"
    out_b = tmp_path / "b.svg"
    main(["render", "wild_bush", "-o", str(out_a), "--seed", "1", "--iterations", "3"])
    main(["render", "wild_bush", "-o", str(out_b), "--seed", "1", "--iterations", "3"])
    assert out_a.read_text() == out_b.read_text()


def test_every_preset_renders_without_error(tmp_path):
    for name in PRESETS:
        output = tmp_path / f"{name}.svg"
        assert main(["render", name, "-o", str(output)]) == 0
        assert output.stat().st_size > 0
