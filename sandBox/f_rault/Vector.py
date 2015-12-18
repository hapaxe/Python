import maya.cmds as mc

#######################################################################
class Vector():
    def __init__(self, x=0, y=0, z=0, A= None, B= None):
        if A and mc.objExists(A):
            if mc.nodeType( A ) in ['transform', 'joint']:
                posA= mc.xform( A, q=True, ws=True, t=True )
                x, y, z = posA[0], posA[1], posA[2]
        if A and B and mc.objExists(B):
            if mc.nodeType( B ) in ['transform', 'joint']:
                posB= mc.xform( B, q=True, ws=True, t=True )
                x, y, z = posB[0] - x, posB[1] - y, posB[2] - z
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        '''printable'''
        return str([self.x, self.y, self.z])

    def __repr__(self):
        ''' evaluatable '''
        return str([self.x, self.y, self.z])

    def value(self):
        ''' return list '''
        return [self.x, self.y, self.z]

    def var_type( self, b):
        ''' get the input type '''
        if type(b).__name__ == 'instance':
            if b.__class__.__name__ is 'Vector':
                return 'Vector'
        elif type(b).__name__ in ['float', 'int']:
            return 'Number'
        else:
            return 'Unsupport'

    def __add__(self, b):
        ''' + '''
        type_b = self.var_type(b)
        print type_b
        if type_b == 'Vector':
            return Vector( self.x + b.x, self.y + b.y, self.z + b.z )
        elif type_b == 'Number':
            return Vector( self.x + b, self.y + b, self.z + b )
        else:
            return None

    def __iadd__(self, b):
        ''' += '''
        print 'iadd'
        print b
        print self.x
        type_b = self.var_type(b)
        print type_b
        if type_b == 'Vector':
            self.x, self.y, self.z = self.x + b.x, self.y + b.y, self.z + b.z
            return self
        elif type_b == 'Number':
            self.x, self.y, self.z = self.x + b, self.y + b, self.z + b
            return self
        else:
            return None
        
    def __sub__(self, b):
        ''' - '''
        type_b = self.var_type(b)
        if type_b == 'Vector':
            return Vector( self.x - b.x, self.y - b.y, self.z - b.z )
        elif type_b == 'Number':
            return Vector( self.x - b, self.y - b, self.z - b )
        else:
            return None

    def __isub__(self, b):
        ''' -= '''
        type_b = self.var_type(b)
        if type_b == 'Vector':
            self.x, self.y, self.z = self.x - b.x, self.y - b.y, self.z - b.z
            return self
        elif type_b == 'Number':
            self.x, self.y, self.z = self.x - b, self.y - b, self.z - b
            return self
        else:
            return None

    def __mul__(self, b):
        ''' * '''
        type_b = self.var_type(b)
        if type_b == 'Vector':
            return Vector( self.x * b.x, self.y * b.y, self.z * b.z )
        elif type_b == 'Number':
            return Vector( self.x * b, self.y * b, self.z * b )
        else:
            return None

    def __imul__(self, b):
        ''' *= '''
        type_b = self.var_type(b)
        if type_b == 'Vector':
            self.x, self.y, self.z = self.x * b.x, self.y * b.y, self.z * b.z
            return self
        elif type_b == 'Number':
            self.x, self.y, self.z = self.x * b, self.y * b, self.z * b
            return self
        else:
            return None

    def __pow__(self, b):
        ''' ** '''
        type_b = self.var_type(b)
        if type_b == 'Vector':
            return Vector( self.x ** b.x, self.y ** b.y, self.z ** b.z )
        elif type_b == 'Number':
            return Vector( self.x ** b, self.y ** b, self.z ** b )
        else:
            return None

    def __div__(self, b):
        ''' / '''
        type_b = self.var_type(b)
        if type_b == 'Vector':
            return Vector( self.x / b.x, self.y / b.y, self.z / b.z )
        elif type_b == 'Number':
            return Vector( self.x / b, self.y / b, self.z / b )
        else:
            return None

    def DotProduct(self, b):
        ''' . '''
        return self.x * b.x + self.y * b.y + self.z * b.z

    def crossProduct(self, b):
        x = self.y * b.z - self.z * b.y
        y = self.z * b.x - self.x * b.z
        z = self.x * b.y - self.y * b.x
        self.x, self.y, self.z = x, y, z

    def norm(self):
        return sqrt(self.x**2  + self.y**2 + self.z**2)

    def squarNorm(self):
        return self.x**2  + self.y**2 + self.z**2

#----------------------------------------------------------------------
def get_jointsHierarchy( obj, order= 'hierarchy' ):
    '''
    Return a list of joints in Hierarchical order.
    Get all the child joints of a given object with himself if it was a joint

    :param obj: The name of the first joint
    :type obj: string
    
    :param order: Define the order of the return list 'hierarchy' or 'invert'
    :type order: string
    
    :return: A list of joints in hierarchy order or invert
    :rtype: list
    '''
    if not mc.objExists( obj ):
        return None
    
    # --- Get children of in Object
    children = mc.listRelatives( obj, children=True, allDescendents=True ) or list()
    children.reverse()
    
    children_jnt = []
    for child in children:
        if mc.nodeType(child) == 'joint':
            children_jnt.append( child )
    
    # --- Create list joints to return
    joints = []
    if mc.nodeType( obj ) == 'joint':
        joints.append( obj )
    joints.extend( children_jnt )
    
    # --- Invert list joint to return if order is 'invert'
    if order == 'invert':
        joints.reverse()
        
    return joints

jnts = get_jointsHierarchy( obj= mc.ls( sl= True)[0], order= 'invert' )

if len(jnts) == 3:
    vA = Vector( A= jnts[2], B= jnts[0] )
    vB = Vector( A= jnts[2], B= jnts[1] )

loc = mc.ls( sl= True )[0]

attr = ['translateX', 'translateY', 'translateZ']
value = [ vB.x, vB.y, vB.z ]

for i in range(0, 3):
    mc.setAttr( loc +'.'+ attr[i], value[i] )

'''
for k in kids:
    print k
    if mc.listRelatives(k, children=True, type="joint") is None:
        for attr in [".jointOrientX", ".jointOrientY", ".jointOrientZ"]:
            mc.setAttr(k+attr, 0)
        print "Zeroed '" + k + ".jointOrient'"
'''
