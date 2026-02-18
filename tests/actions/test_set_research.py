import pytest

from fle.env.game_types import Technology


@pytest.fixture()
def game(configure_game):
    g = configure_game(all_technologies_researched=False)
    # Pre-research automation prerequisites for Factorio 2.0 tech tree
    for tech in ["electronics", "steam-power", "automation-science-pack"]:
        g.instance.rcon_client.send_command(
            f'/c game.forces["player"].technologies["{tech}"].researched = true'
        )
    return g


def test_set_research(game):
    ingredients = game.set_research(Technology.Automation)
    assert ingredients[0].count == 10


def test_fail_to_research_locked_technology(game):
    try:
        game.set_research(Technology.Automation2)
    except Exception:
        assert True
        return
    assert False, "Was able to research locked technology. Expected exception."
