try:
    from openalea.plantgl.gui.curve2deditor import Curve2DEditor,FuncConstraint
except ImportError as e:
    Curve2DEditor = None
from openalea.lpy.gui.abstractobjectmanager import *
from curve2dmanager import displayLineAsThumbnail
from openalea.plantgl.gui.qt import QtGui, QtWidgets

class FunctionManager(AbstractPglObjectManager):
    """see the doc of the objectmanager abtsract class to undesrtand the implementation of the functions"""
    def __init__(self):
        AbstractPglObjectManager.__init__(self,"Function")
        
    def displayThumbnail(self,obj,i,focus,objectthumbwidth):
        displayLineAsThumbnail(self,obj,i,objectthumbwidth,(1,0,1,1))
        
    def createDefaultObject(self,subtype=None):
        import openalea.plantgl.all as pgl
        nbP = 4
        return pgl.NurbsCurve2D(pgl.Point3Array([(float(i)/(nbP-1),0) for i in range(nbP)],1) )

    def getEditor(self,parent):
        if Curve2DEditor:
            return Curve2DEditor(parent,FuncConstraint())
        else: return None

    def setObjectToEditor(self,editor,obj):
        """ ask for edition of obj with editor """
        from copy import deepcopy        
        editor.setCurve(deepcopy(obj))

    def retrieveObjectFromEditor(self,editor):
        """ ask for current value of object being edited """
        return editor.getCurve()
    
    def writeObjectToLsysContext(self,obj):
        return 'pgl.QuantisedFunction('+obj.name+')'
    
    def canImportData(self,fname):
        from os.path import splitext
        ext = splitext(fname)[1]
        return  ext == '.fset' or ext == '.func'
    
    def importData(self,fname):
        from openalea.lpy.cpfg_compat.data_import import import_functions, import_function
        from os.path import splitext
        ext = splitext(fname)[1]
        if ext == '.fset':  return import_functions(fname)
        else: return import_function(fname)
    
    def fillEditorMenu(self,menubar,editor):
        """ Function call to fill the menu of the editor """
        menu = QtWidgets.QMenu('Theme',menubar)
        menu.addAction('Black',lambda : editor.applyTheme(editor.BLACK_THEME))
        menu.addAction('White',lambda : editor.applyTheme(editor.WHITE_THEME))
        menubar.addMenu(menu)
        
def get_managers():
    return FunctionManager()
