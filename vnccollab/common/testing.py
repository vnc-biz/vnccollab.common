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
        import vnccollab.common
        xmlconfig.file(
            'configure.zcml',
            vnccollab.common,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

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
