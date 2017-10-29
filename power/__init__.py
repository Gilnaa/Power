# coding=utf-8
"""
Provides crossplatform checking of current power source, battery warning level and battery time remaining estimate.
Allows you to add observer for power notifications if platform supports it.

Usage:
    from power import PowerManagement, PowerManagementObserver # Automatically imports platform-specific implementation

    class Observer(PowerManagementObserver):
        def on_power_sources_change(self, power_management):
            print("Power sources did change.")

        def on_time_remaining_change(self, power_management):
            print("Time remaining did change.")

    # class Observer(object):
    #     ...
    # PowerManagementObserver.register(Observer)
"""
from sys import platform
import traceback

from power.common import *
from power.version import VERSION

__version__ = VERSION


try:
    if platform.startswith('darwin'):
        from power.darwin import PowerManagement as PowerManagementPlatform
    elif platform.startswith('freebsd'):
        from power.freebsd import PowerManagement as PowerManagementPlatform
    elif platform.startswith('win32'):
        from power.win32 import PowerManagement as PowerManagementPlatform
    elif platform.startswith('linux'):
        from power.linux import PowerManagement as PowerManagementPlatform
    else:
        raise RuntimeError("{platform} is not supported.".format(platform=platform))

    class PowerManagement(PowerManagementPlatform):
        def __init__(self, *args, **kwargs):
            super(PowerManagement, self).__init__(*args, **kwargs)

            from power.common import PowerManagementNoop
            self._noop = PowerManagementNoop()

        def add_observer(self, observer):
            try:
                return super().add_observer(observer)
            except:
                warnings.warn("{}.add_observer raised:\n{}".format(PowerManagementPlatform.__name__, traceback.format_exc()), category=RuntimeWarning)
                return self._noop.add_observer(observer)

        def remove_observer(self, observer):
            try:
                return super().remove_observer(observer)
            except:
                warnings.warn("{}.remove_observer raised:\n{}".format(PowerManagementPlatform.__name__, traceback.format_exc()), category=RuntimeWarning)
                return self._noop.remove_observer(observer)

        def get_providing_power_source_type(self):
            try:
                return super().get_providing_power_source_type()
            except:
                warnings.warn("{}.get_providing_power_source_type raised:\n{}".format(PowerManagementPlatform.__name__, traceback.format_exc()), category=RuntimeWarning)
                return self._noop.get_providing_power_source_type()

        def get_time_remaining_estimate(self):
            try:
                return super().get_time_remaining_estimate()
            except:
                warnings.warn("{}.get_time_remaining_estimate raised:\n{}".format(PowerManagementPlatform.__name__, traceback.format_exc()), category=RuntimeWarning)
                return self._noop.get_time_remaining_estimate()

        def get_low_battery_warning_level(self):
            try:
                return super().get_low_battery_warning_level()
            except:
                warnings.warn("{}.get_low_battery_warning_level raised:\n{}".format(PowerManagementPlatform.__name__, traceback.format_exc()), category=RuntimeWarning)
                return self._noop.get_low_battery_warning_level()
except (RuntimeError, ImportError) as e:
    import warnings
    warnings.warn("Unable to load PowerManagement for {platform}. No-op PowerManagement class is used: {error}".format(error=str(e), platform=platform))
    from power.common import PowerManagementNoop as PowerManagement
