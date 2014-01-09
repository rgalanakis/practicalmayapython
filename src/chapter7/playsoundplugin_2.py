from maya import OpenMayaMPx, OpenMaya
import playsound

wav_flag_short = '-w' #(1)
wav_flag_long = '-wavname'

WAVS = { #(2)
    'gobble': playsound.GOBBLE,
    'roar': playsound.GORILLA,
}

class SoundPlayer(OpenMayaMPx.MPxCommand):
    def doIt(self, args):
        parser = OpenMaya.MArgParser(self.syntax(), args) #(3)
        key = 'gobble' #(4)
        if parser.isFlagSet(wav_flag_short):
            key = parser.flagArgumentString(wav_flag_short, 0)
        playsound.play_sound(WAVS[key]) #(5)

def create_syntax(): #(6)
    syn = OpenMaya.MSyntax()
    syn.addFlag(
        wav_flag_short, wav_flag_long, OpenMaya.MSyntax.kString)
    return syn

def create_plugin():
    return OpenMayaMPx.asMPxPtr(SoundPlayer())

plugin_name = 'playSound'

def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(
        mobject, 'Marcus Reynir', '0.01')

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.registerCommand(
        plugin_name, create_plugin, create_syntax) #(7)

def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.deregisterCommand(plugin_name)
