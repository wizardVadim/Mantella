from src.localization.translator import tr

def test_tr_inserts_named_parameter():
    result = tr(
        "missing.translation",
        "en",
        "{game}: Path to Game Folder",
        game="Fallout 4",
    )

    assert result == "Fallout 4: Path to Game Folder"

def test_tr_leaves_unknown_parameter_visible():
    result = tr(
        "missing.translation",
        "en",
        "{game}: Path to {folder_type}",
        game="Fallout 4",
    )

    assert result == "Fallout 4: Path to {folder_type}"