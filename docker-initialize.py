#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import os
import warnings

warnings.simplefilter("always", DeprecationWarning)


class Environment(object):
    """ Configure container via environment variables
    """

    def __init__(
        self,
        env=os.environ,
        zope_conf="/plone/instance/parts/instance/etc/zope.conf",
        custom_conf="/plone/instance/custom.cfg",
    ):
        self.env = env
        self.zope_conf = zope_conf
        self.custom_conf = custom_conf

    def buildout(self):
        """ Buildout from environment variables
        """
        # Already configured
        if os.path.exists(self.custom_conf):
            return

        eggs = self.env.get("PLONE_ADDONS", self.env.get("ADDONS", "")).strip().split()
        if not eggs:
            eggs = self.env.get("BUILDOUT_EGGS", "").strip().split()
            if eggs:
                warnings.warn(
                    "BUILDOUT_EGGS is deprecated. Please use "
                    "PLONE_ADDONS instead !!!",
                    DeprecationWarning,
                )

        zcml = self.env.get("PLONE_ZCML", self.env.get("ZCML", "")).strip().split()
        if not zcml:
            zcml = self.env.get("BUILDOUT_ZCML", "").strip().split()
            if zcml:
                warnings.warn(
                    "BUILDOUT_ZCML is deprecated. Please use " "PLONE_ZCML instead !!!",
                    DeprecationWarning,
                )

        develop = (
            self.env.get("PLONE_DEVELOP", self.env.get("DEVELOP", "")).strip().split()
        )
        if not develop:
            develop = self.env.get("BUILDOUT_DEVELOP", "").strip().split()
            if develop:
                warnings.warn(
                    "BUILDOUT_DEVELOP is deprecated. Please use "
                    "PLONE_DEVELOP instead !!!",
                    DeprecationWarning,
                )

        if not (eggs or zcml or develop):
            return

        buildout = BUILDOUT_TEMPLATE.format(
            eggs="\n\t".join(eggs), zcml="\n\t".join(zcml), develop="\n\t".join(develop)
        )

        with open(self.custom_conf, "w") as cfile:
            cfile.write(buildout)

    def setup(self, **kwargs):
        self.buildout()
        self.zeoclient()
        self.zeopack()
        self.zeoserver()

    __call__ = setup


BUILDOUT_TEMPLATE = """
[buildout]
extends = develop.cfg
develop += {develop}
eggs += {eggs}
zcml += {zcml}
"""


def initialize():
    """ Configure Plone instance as ZEO Client
    """
    environment = Environment()
    environment.setup()


if __name__ == "__main__":
    initialize()
