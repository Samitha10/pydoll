from __future__ import annotations

import logging
import platform
from typing import TYPE_CHECKING, Optional

from pydoll.browser.chromium.base import Browser
from pydoll.browser.managers import ChromiumOptionsManager
from pydoll.exceptions import UnsupportedOS
from pydoll.utils import validate_browser_paths

if TYPE_CHECKING:
    from pydoll.browser.options import Options

logger = logging.getLogger(__name__)


class Brave(Browser):
    """Brave browser implementation for CDP automation."""

    def __init__(
        self,
        options: Optional[Options] = None,
        connection_port: Optional[int] = None,
    ):
        """
        Initialize Brave browser instance.

        Args:
            options: Brave configuration options (default if None).
            connection_port: CDP WebSocket port (random if None).
        """
        options_manager = ChromiumOptionsManager(options)
        super().__init__(options_manager, connection_port)

    @staticmethod
    def _get_default_binary_location():
        """
        Get default Brave executable path based on OS.

        Returns:
            Path to Brave executable.

        Raises:
            UnsupportedOS: If OS is not supported.
            ValueError: If executable not found at default location.
        """
        os_name = platform.system()
        logger.debug(f'Resolving default Edge binary for OS: {os_name}')

        browser_paths = {
            'Windows': [
                (
                    r'C:\Program Files\BraveSoftware\Brave-Browser\Application'
                    r'\brave.exe'
                ),
                (
                    r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application'
                    r'\brave.exe'
                ),
            ],
            'Linux': [
                '/usr/bin/brave-browser',
            ],
            'Darwin': [
                ('/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'),
            ],
        }

        browser_path = browser_paths.get(os_name)

        if not browser_path:
            logger.error(f'Unsupported OS: {os_name}')
            raise UnsupportedOS()

        path = validate_browser_paths(browser_path)
        logger.debug(f'Using Brave binary: {path}')
        return path
