__author__ = 'f.scaduto'

# Slider
import maya.cmds as mc

def main_UI():
    light_control = '*:ltDr001_A_lightOrient_ctrl'

    if not mc.objExists(light_control):
        mc.confirmDialog(title='Alert', message='You dont have the LT rig in the scene', button=['Ok'], defaultButton='Ok')
        pass

    else:
        # Get value of rig light attributes
        lightDirection = mc.getAttr(light_control+".rx")
        frontBack = mc.getAttr(light_control+".Front_Back")
        offsetLight = mc.getAttr(light_control+".Offset_Light")
        shadow = mc.getAttr(light_control+".Shadow")
        shadowsRes = mc.getAttr(light_control+".ShadowsRes")
        intensityValue = mc.getAttr(light_control+".Intensity")
        ambianteValue = mc.getAttr(light_control+".IntensityGlobal")

        # Check if window exist
        if mc.window('ltControlsWin', exists=1):
            mc.deleteUI('ltControlsWin')

        # Create window UI
        light_slider_win = mc.window('ltControlsWin', title='LT Controls Window')
        mc.columnLayout()

        # Create slider Light Direction
        light_direction_slider = mc.floatSliderGrp( label='Light Direction', field=True, minValue=-190.0, maxValue=190.0, precision=3, value=lightDirection )
        # Connect values
        mc.connectControl( light_direction_slider, light_control+".rx" )

        # Create slider Front Back
        light_direction_slider = mc.intSliderGrp( label='Front Back', field=True, minValue=0, maxValue=1, value=frontBack )
        # Connect values
        mc.connectControl( light_direction_slider, light_control+".Front_Back" )

        # Create slider Offset Light
        light_direction_slider = mc.floatSliderGrp( label='Offset Light', field=True, minValue=-100.0, maxValue=100.0, precision=3, value=offsetLight )
        # Connect values
        mc.connectControl( light_direction_slider, light_control+".Offset_Light" )

        # Create slider Activate Shadows
        light_direction_slider = mc.intSliderGrp( label='Activate Shadows', field=True, minValue=0, maxValue=1, value=shadow )
        # Connect values
        mc.connectControl( light_direction_slider, light_control+".Shadow" )

        # Create slider Shadows Resolution
        light_direction_slider = mc.intSliderGrp( label='Shadows Resolution', field=True, minValue=0, maxValue=2, value=shadowsRes )
        # Connect values
        mc.connectControl( light_direction_slider, light_control+".ShadowsRes" )

        # Create slider Directionnal light Intensity
        directionnal_int_slider = mc.floatSliderGrp( label='Directionnal light Intensity', field=True, minValue=0.0, maxValue=5.0, precision=3, value=intensityValue )
        # Connect values
        mc.connectControl( directionnal_int_slider, light_control+".Intensity" )

        # Create slider Ambiante light Intensity
        ambiante_int_slider = mc.floatSliderGrp( label='Ambiante light Intensity', field=True, minValue=0.0, maxValue=5.0, precision=3, value=ambianteValue )
        # Connect values
        mc.connectControl( ambiante_int_slider, light_control+".IntensityGlobal" )

        mc.showWindow( light_slider_win )

