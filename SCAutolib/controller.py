from typing import Union

import yaml
from shutil import rmtree

from SCAutolib import logger, run
from SCAutolib.models import CA
from pathlib import Path


class Controller:
    authselect = None
    sssd_conf = None
    lib_conf: yaml.YAMLObject = None
    local_ca: CA.LocalCA = None
    ipa_ca = None
    users: dict = None

    def __int__(self, config: Union[Path, str], params: []):
        # Parse config file
        with open(config, "r") as file:
            self.lib_conf = yaml.load(file, Loader=yaml.FullLoader)
            assert self.lib_conf, "Data are not loaded correctly."
        self._check_required_fields()
        # Validate values in config

        # Check params

        # Create object for SSSD
        # Create object for Authselect

        # Create required CAs

        # Initialize users (just objects without real creation in the system)
        # Initialize cards along with users
        ...

    def setup_system(self):
        """
        This method would setup whole system for smart card testing.
        """

        # Update SSSD with values for local users
        ...

    def setup_local_ca(self):
        # Create directory structure for CA

        # Generate certificates
        # self.local_ca.create()
        ...

    def setup_ipa_ca(self):
        # Setup IPA client on the system
        # Update values in the self.sssd_conf
        # self.ipa_ca.create()
        ...

    def setup_user(self, username):
        # Add user to the corresponding system
        # Request certificates
        # Add certs to the user
        ...

    def _general_steps_for_virtual_sc(self):
        """
        Prepare the system for virtual smart card
        """
        # TODO: This steps should be done in the Controller
        with open("/usr/lib/systemd/system/pcscd.service", "r+") as f:
            data = f.read().replace("--auto-exit", "")
            f.write(data)

        with open("/usr/share/p11-kit/modules/opensc.module", "r+") as f:
            data = f.read()
            if "disable-in: virt_cacard" not in data:
                f.write("disable-in: virt_cacard\n")
                logger.debug("opensc.module is updated")

        run(['systemctl', 'stop', 'pcscd.service', 'pcscd.socket', 'sssd'])
        rmtree("/var/lib/sss/mc/*", ignore_errors=True)
        rmtree("/var/lib/sss/db/*", ignore_errors=True)
        logger.debug(
            "Directories /var/lib/sss/mc/ and /var/lib/sss/db/ removed")

        run("systemctl daemon-reload")
        run("systemctl restart pcscd sssd")

    def cleanup(self):
        ...

    def _check_required_fields(self):
        """
        Check if all required fields are present in the config file. Warn user
        if some fields are missing.
        """
        result = True
        fields = ("root_passwd", "ca_dir", "ipa_server_root",
                  "ipa_server_hostname", "ipa_client_hostname", "ipa_domain",
                  "ipa_realm", "ipa_server_admin_passwd", "local_user", "ipa_user")
        config_fields = self.lib_conf.keys()
        for f in fields:
            if f not in config_fields:
                logger.warning(f"Field {f} is not present in the config.")
                result = False
        if result:
            logger.info("Configuration file is OK.")
        return result
