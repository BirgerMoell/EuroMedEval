from euromedeval.registry import get_dataset_config, list_dataset_configs


def test_registry_lists_known_configs() -> None:
    configs = list_dataset_configs()
    names = {config.name for config in configs}
    assert "smdt-sv" in names
    assert "lek-pl" in names


def test_registry_filters_by_language() -> None:
    configs = list_dataset_configs(language="sv")
    assert configs
    assert all(config.language == "sv" for config in configs)


def test_get_dataset_config() -> None:
    config = get_dataset_config("smdt-sv")
    assert config.country == "SE"

