from pxr import Tf
from pxr.Usdviewq.plugin import PluginContainer


class TutorialPluginContainer(PluginContainer):

    def registerPlugins(self, plugRegistry, usdviewApi):

        printer = self.deferredImport(".printer")
        self._printMessage = plugRegistry.registerCommandPlugin(
            "TutorialPluginContainer.printMessage",
            "Print Message",
            printer.printMessage)

    def configureView(self, plugRegistry, plugUIBuilder):

        tutMenu = plugUIBuilder.findOrCreateMenu("Tutorial")
        tutMenu.addItem(self._printMessage)


Tf.Type.Define(TutorialPluginContainer)
