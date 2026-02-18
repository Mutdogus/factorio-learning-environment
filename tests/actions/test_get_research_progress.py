import pytest

from fle.env.game_types import Technology


@pytest.fixture()
def game(configure_game):
    g = configure_game(
        inventory={"assembling-machine-1": 1},
        merge=True,
        all_technologies_researched=False,
    )
    # Pre-research automation prerequisites for Factorio 2.0 tech tree
    for tech in ["electronics", "steam-power", "automation-science-pack"]:
        g.instance.rcon_client.send_command(
            f'/c game.forces["player"].technologies["{tech}"].researched = true'
        )
    return g


def test_get_research_progress_automation(game):
    ingredients = game.get_research_progress(Technology.Automation)
    assert ingredients[0].count == 10


def test_get_research_progress_none_fail(game):
    try:
        game.get_research_progress()
    except:
        assert True
        return

    assert False, (
        "Need to set research before calling get_research_progress() without an argument"
    )


def test_get_research_progress_none(game):
    ingredients1 = game.set_research(Technology.Automation)
    ingredients2 = game.get_research_progress()

    assert len(ingredients1) == len(ingredients2)
