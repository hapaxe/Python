__author__ = 'youcaidi'

import math
import maya.api.OpenMaya as om
import maya.cmds as cmds

#
# Fonction de recherche de la camera a updater
#
def ccc_findCamera(pcamName):
    for pcam in cmds.ls(type='camera', v=True):
        print pcam
        if pcam == pcamName:
            return pcam

#
# Fonction qui dit si oui ou non l'objet est dans le cone de la camera
#
def ccc_isMeshinCone(pmesh, pcamUpVec, pcamHzVec, pcamFrVec, pcamPos, pcamVfv, pcamHfv):
    # On recupere la bbox du mesh
    pbbox = cmds.exactWorldBoundingBox(pmesh)
    pbboxInf = om.MVector([pbbox[0], pbbox[1], pbbox[2]])
    pbboxSup = om.MVector([pbbox[3], pbbox[4], pbbox[5]])

    # On calcule le centre de la bbox et son rayon
    pcentrBbox = (pbboxSup + pbboxInf) / 2.0
    prayBbox = om.MVector(pbboxSup - pbboxInf).length() / 2.0

    # On teste d'abord si la bbox est devant ou derriere la camera
    pVecCamBbox = pcentrBbox - pcamPos
    if pVecCamBbox * pcamFrVec < 0:
        if om.MVector(pVecCamBbox).length() > prayBbox:
            return False
        else:
            return True

    # On est devant la camera, on va tester le cone...
    # A la verticale
    if (math.fabs(pcamUpVec * pVecCamBbox) * math.cos(pcamVfv * 0.5) -  math.fabs(pcamFrVec * pVecCamBbox) * math.sin(pcamVfv * 0.5)) > prayBbox:
        return False

    # Sinon on teste a l'horizontale
    if (math.fabs(pcamHzVec * pVecCamBbox) * math.cos(pcamHfv * 0.5) -  math.fabs(pcamFrVec * pVecCamBbox) * math.sin(pcamHfv * 0.5)) > prayBbox:
        return False

    return True

#	
# Fonction corps du Plugins
#
def cull(pcamName, nodes_to_test):
    # On recupere la camera
    pcam = pcamName
    #pcam = ccc_findCamera(pcamName)
    
    # On sort en cas d'echec
    if not pcam:
        raise(RuntimeError("Failed to find camera !"))

    # Verbose
    print "Frustum : Culling for camera '%s' ..." % pcam

    # On recupere les parametres de PlayBack et on se place au debut
    pstart = cmds.playbackOptions(query=True, minTime=True)
    pend = cmds.playbackOptions(query=True, maxTime=True)
    pby = cmds.playbackOptions(query=True, by=True)
	
    # On se place au debut
    cmds.currentTime(pstart, edit=True)

    # On recupere la liste des meshs visible et non intermediaire et on initialise le tableau des mesh a tester a la frame suivante
    pmeshs = nodes_to_test
	
    # On boucle sur l'ensemble des frames du playback
    ptime = pstart
    while ptime <= pend:
        # On update la scene
        cmds.currentTime(ptime, edit=True)

        # On recupere les infos de la camera
        pcamUpVec = om.MVector(cmds.camera(pcam, q=True, wup=True))
        pcamPos = om.MVector(cmds.camera(pcam, q=True, p=True))
        pcamWci = om.MVector(cmds.camera(pcam, q=True, wci=True))
        pcamFrVec = om.MVector(pcamWci - pcamPos).normal()
        pcamHzVec = pcamFrVec ^ pcamUpVec
        pcamVfv = cmds.camera(pcam, q=True, vfv=True) / 180.0 * math.pi
        pcamHfv = cmds.camera(pcam, q=True, hfv=True) / 180.0 * math.pi
        
        # On boucle a l'envers sur l'ensemble des mesh qui reste a tester
        pitmp = len(pmeshs) - 1
        while pitmp >= 0:
            # Test si dans cone
            if ccc_isMeshinCone(pmeshs[pitmp], pcamUpVec, pcamHzVec, pcamFrVec, pcamPos, pcamVfv, pcamHfv):
                # Supprime de la liste des oblets a cacher
                pmeshs.remove(pmeshs[pitmp])
            # Decremente Index
            pitmp = pitmp - 1

        # On change d'image
        ptime = ptime + pby

        #print 'ptime:\t%s' % ptime
        #print 'A la fin on a %s pmeshs' % len(pmeshs)

    # Verbose
    print "Frustum : %s nodes culled !" % len(pmeshs)
    # Renvoie les mesh a cacher
    return pmeshs

if __name__ == "__main__":
    #
    # On lance !
    #
    # Recupere les Meshes a tester
    meshes_to_test = cmds.ls(et=('mesh'), v=True, ni=True)
    # Reupere les Meshes a cacher
    meshes_to_hide  = cull('CAM_a:finalShape', meshes_to_test)
    # On set la Visibility a off pour les objects non vue de la camera
    for pmesh in meshes_to_hide:
        cmds.setAttr('%s.visibility' % pmesh, False)
    # Verbose
    print "C'est bon!\n"
