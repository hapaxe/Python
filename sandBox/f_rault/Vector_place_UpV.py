#----------------------------------------------------------------------
# math.Vector Class
# Author : felixlechA.com
# Date   : March 2015
# Ver    : 0.5
#----------------------------------------------------------------------
import maya.cmds as mc
from math import sqrt

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
                x, y, z = x - posB[0], y - posB[1], z - posB[2]
                
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        '''printable'''
        return str([self.x, self.y, self.z])

    def __repr__(self):
        ''' evaluatable '''
        return str([self.x, self.y, self.z])

    def __getitem__(self, iIndex):
        """get the index value

        :param iIndex: the index of the value to access
        :type iIndex: int
        """

        # return
        return self.values[iIndex]

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

    def normalize(self):
        # get vector norm
        fNorm = self.norm()
        return self / fNorm

#-----------------------------------------------------
sel= mc.ls(sl= True)

A= Vector(A= sel[0])
B= Vector(A= sel[1])
C= Vector(A= sel[2])

vBone1= B - A
vBone2= C - B
vBase= C - A

scale_value = vBone1.norm() + vBone2.norm()

# Calculate a vB Tangente Vector
vResult = (vBone1 - vBase * vBone1.DotProduct(vBase) / float( vBase.squarNorm())).normalize() * scale_value + B

mc.xform( 'Locator1', t= [vResult.x, vResult.y, vResult.z] )

