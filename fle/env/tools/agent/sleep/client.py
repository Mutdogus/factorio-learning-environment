from time import sleep

from fle.env.tools import Tool


class Sleep(Tool):
    def __init__(self, connection, game_state):
        super().__init__(connection, game_state)

    def __call__(self, seconds: int) -> bool:
        """
        Sleep for up to 15 seconds before continuing. Useful for waiting for actions to complete.
        :param seconds: Number of seconds to sleep.
        :return: True if sleep was successful.
        """
        # Track elapsed ticks for appropriate sleep calculation
        ticks_before = self.game_state.instance.get_elapsed_ticks()

        # Update elapsed ticks on server
        _, _ = self.execute(seconds)

        # Advance game ticks by sending rapid RCON commands.
        # Factorio 2.0 headless servers don't advance ticks without connected
        # players, so each RCON command forces exactly 1 tick to process.
        ticks_needed = seconds * 60
        for _ in range(ticks_needed):
            self.connection.rcon_client.send_command("/sc")

        return True
