import functions.cstr as cstr
reload( cstr )
import functions.connection as connection
reload( connection )

sel= mc.ls(sl= True)

for i in range( 0, len(sel), 2):
    # Do Cstr
    #cstr.constraint( source= sel[i], target= sel[i+1], mode= ['rotate'])
    
    # Do Connection
    connection.connect_Attribute( source= sel[i], target= sel[i+1], attribute= ['translate', 'rotate'])