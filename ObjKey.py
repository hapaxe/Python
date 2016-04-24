import maya.cmds as mc


def object_select(nbr):
    if nbr == 1:
        global selObj1
        selObj1 = mc.ls(sl=True)
        print(selObj1)
    else:
        global selObj2
        selObj2 = mc.ls(sl=True)
        print(selObj2)


# define first frame
def button_frame_a(*args):
    global firstFrame
    firstFrame = mc.currentTime(q=True)
    print(firstFrame)


# define last frame
def button_frame_b(*args):
    global endFrame
    endFrame = mc.currentTime(q=True)
    print(endFrame)


# define how to copy animation
def copy_frames(*args):
    first = int(firstFrame)
    end = int(endFrame) + 1
    print(first)
    print(end)

    mc.select(selObj2)

    for i in range(first, end):
        mc.currentTime(i)
        trans = mc.xform(selObj1, q=True, t=True)
        rot = mc.xform(selObj1, q=True, ro=True)
        scale = mc.xform(selObj1, q=True, s=True)

        mc.xform(selObj2, t=trans)
        mc.xform(selObj2, ro=rot)
        mc.xform(selObj2, s=scale)
        mc.select(selObj2)
        mc.setKeyframe(selObj2)


# UI creation
def ui():
        window = mc.window(title="copyFrames", iconName='Short Name', widthHeight=(250, 150))
        mc.rowColumnLayout(numberOfColumns=1, columnAlign=(1, 'right'), ca=(2, 'both', 0), cw=(2, 200))
        
        obj1 = mc.button('obj 1', label='To copy object', command=('object_select(1)'))
        obj2 = mc.button('obj 2', label='New object', command=('object_select(2)'))
        
        mc.button('KeyA', label='Key Frame 1', command=('button_frame_a()'))
        mc.button('KeyB', label='Key Frame 2', command=('button_frame_b()'))

        mc.rowColumnLayout( numberOfColumns=1 )
        
        copyKey = mc.button('copy', label='Copy Animation', command=('copy_frames()'))
        mc.button(label='Close', command=('mc.deleteUI(\"' + window + '\", window=True)'))

        mc.showWindow( window )
        return True
     
firstFrame = 0
endFrame = 0

inst = ui()
