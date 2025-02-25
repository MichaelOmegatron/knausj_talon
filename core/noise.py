"""
Map noises (like pop) to actions so they can have contextually differing behavior
"""

from talon import Module, actions, cron, noise

mod = Module()
hiss_cron = None


@mod.action_class
class Actions:
    def noise_trigger_pop():
        """
        Called when the user makes a 'pop' noise. Listen to
        https://noise.talonvoice.com/static/previews/pop.mp3 for an
        example.
        """

    def noise_trigger_hiss(active: bool):
        """
        Called when the user makes a 'hiss' noise. Listen to
        https://noise.talonvoice.com/static/previews/hiss.mp3 for an
        example.
        """


def noise_trigger_hiss_debounce(active: bool):
    """Since the hiss noise triggers while you're talking we need to debounce it"""
    global hiss_cron
    if active:
        # MG Had to manually change debounce from 100ms for less sensitive pick-up. Also note the debounce only delays the active block of noise_trigger_hiss. It immediately registers the innactive block.
        hiss_cron = cron.after("300ms", lambda: actions.user.noise_trigger_hiss(active))
    else:
        cron.cancel(hiss_cron)
        actions.user.noise_trigger_hiss(active)


noise.register("pop", lambda _: actions.user.noise_trigger_pop())
noise.register("hiss", noise_trigger_hiss_debounce)
