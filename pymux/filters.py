from prompt_toolkit.filters import Condition


__all__ = [
    "has_prefix",
    "waits_for_confirmation",
    "in_command_mode",
    "waits_for_prompt",
    "in_scroll_buffer",
    "in_scroll_buffer_not_searching",
    "in_scroll_buffer_searching",
]


def has_prefix(pymux):
    """
    When the prefix key (Usual C-b) has been pressed.
    """
    def _():
        return pymux.get_client_state().has_prefix
    return _


def waits_for_confirmation(pymux):
    """
    Waiting for a yes/no key press.
    """
    def _():
        return bool(pymux.get_client_state().confirm_command)
    return _


def in_command_mode(pymux):
    """
    When ':' has been pressed.'
    """
    def _():
        client_state = pymux.get_client_state()
        return client_state.command_mode and not client_state.confirm_command
    return _


def waits_for_prompt(pymux):
    """
    Waiting for input for a "command-prompt" command.
    """
    def _():
        client_state = pymux.get_client_state()
        return bool(client_state.prompt_command) and not client_state.confirm_command
    return _


def _confirm_or_prompt_or_command(pymux):
    "True when we are waiting for a command, prompt or confirmation."
    client_state = pymux.get_client_state()
    if (
        client_state.confirm_text
        or client_state.prompt_command
        or client_state.command_mode
    ):
        return True


def in_scroll_buffer(pymux):
    def _():
        if _confirm_or_prompt_or_command(pymux):
            return False

        pane = pymux.arrangement.get_active_pane()
        return pane.display_scroll_buffer
    return _


def in_scroll_buffer_not_searching(pymux):
    def _():
        if _confirm_or_prompt_or_command(pymux):
            return False

        pane = pymux.arrangement.get_active_pane()
        return pane.display_scroll_buffer and not pane.is_searching
    return _


def in_scroll_buffer_searching(pymux):
    def _():
        if _confirm_or_prompt_or_command(pymux):
            return False

        pane = pymux.arrangement.get_active_pane()
        return pane.display_scroll_buffer and pane.is_searching
    return _
