import maya.cmds as cmds

def objectSelect(nbr):
    if nbr == 1 :
        global selObj1
        selObj1 = cmds.ls(sl=True)
        print(selObj1)
    else :
        global selObj2
        selObj2 = cmds.ls(sl=True)
        print(selObj2)

#define first frame
def BouttonFrA(*args):
    global firstFrame
    firstFrame = cmds.currentTime( q=True )
    print(firstFrame)

#define last frame
def BouttonFrB(*args):
    global endFrame
    endFrame = cmds.currentTime( q=True )
    print(endFrame)

#define how to copy animation
def copyFrames(*args):
    first = int(firstFrame)
    end = int(endFrame) + 1
    print(first)
    print(end)

    cmds.select(selObj2)

    for i in range (first,end) :
        cmds.currentTime(i)
        trans = cmds.xform(selObj1, q=True, t=True)
        rot = cmds.xform(selObj1, q=True, ro=True)
        scale = cmds.xform(selObj1, q=True, s=True)

        cmds.xform(selObj2, t = trans)
        cmds.xform(selObj2, ro = rot)
        cmds.xform(selObj2, s = scale)
        cmds.select(selObj2)
        cmds.setKeyframe(selObj2)


#UI creation
def UI():
        
    
        window = cmds.window( title="copyFrames", iconName='Short Name', widthHeight=(250, 150) )
        cmds.rowColumnLayout( numberOfColumns=1, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=(2, 200) )
        
        obj1 = cmds.button( 'obj 1' , label='To copy object' , command=('objectSelect(1)') )
        obj2 = cmds.button( 'obj 2' , label='New object' , command=('objectSelect(2)') )
        
        cmds.button( 'KeyA' , label='Key Frame 1' , command=('BouttonFrA()') )
        cmds.button( 'KeyB' , label='Key Frame 2' , command=('BouttonFrB()') )
        
        cmds.rowColumnLayout( numberOfColumns=1 )
        
        copyKey = cmds.button( 'copy' , label='Copy Animation' , command=('copyFrames()') )
        cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )

        cmds.showWindow( window )
     
firstFrame = 0
endFrame = 0

inst = UI()
