from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class VnccollabcommonLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.js.jqueryui
        xmlconfig.file(
            'configure.zcml',
            collective.js.jqueryui,
            context=configurationContext
        )
        import vnccollab.common
        xmlconfig.file(
            'configure.zcml',
            vnccollab.common,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'vnccollab.common:default')

VNCCOLLAB_COMMON_FIXTURE = VnccollabcommonLayer()
VNCCOLLAB_COMMON_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VNCCOLLAB_COMMON_FIXTURE,),
    name="VnccollabcommonLayer:Integration"
)
VNCCOLLAB_COMMON_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VNCCOLLAB_COMMON_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VnccollabcommonLayer:Functional"
)
