
import bpy
import bmesh
from mathutils import Vector
import mathutils
import math



class MESH_OT_gaten(bpy.types.Operator):
    """Hier moet iets"""
    bl_idname = "mesh.gaten"# komy in de afdeling mesh en heet planken
    bl_label = "gaten"
    bl_options = {'REGISTER', 'UNDO'} # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven
    
    vaste_richting:bpy.props.BoolProperty(
        name="vast richting",
        default=False
    )
    diameter_groot:bpy.props.FloatProperty(
        name="gat diameter groot(cm)",
        default=10,
    )
    diepte_groot:bpy.props.FloatProperty(
        name="diepte groot(cm)",
        default=10,
    )
    diameter_klein:bpy.props.FloatProperty(
        name="gat diameter klein(cm)",
        default=8,
    )
    diepte_klein:bpy.props.FloatProperty(
        name="diepte klein(cm)",
        default=100,
    )
    resolutie:bpy.props.IntProperty(
        name="resolutie",
        default=32,
    )
    draaing:bpy.props.FloatProperty(
        name="draaing(graden)",
        default=0,
    )    
    
    def execute(self, context):
        dia_groot=self.diameter_groot/200
        dia_klein=self.diameter_klein/200 
        diepte_klein=self.diepte_klein/50
        diepte_groot=self.diepte_groot/50
        zijden=self.resolutie
        hoek=self.draaing
        vaste_richting=self.vaste_richting
        draaingZ=math.pi*(hoek/180)




        ob = bpy.context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        
        hist=bm.select_history
        plaats_abs=ob.location

        vect=[] #array om de punten uit de selectie in op te slaan
        #daarna de array vullen met de punten
        for t in range (0,len(hist)):
            vect.append(hist[(-t-1)])
        # alle waardes in een tabel zetten omdat je dan de punten behoud na de boolean    
        waardes=[]    
        for u in vect:
            v1 =Vector((0,0,1))
            normaal=u.normal
            if vaste_richting == True:normaal=Vector((0,0,1))
            hoek=normaal.angle(v1)    #hoek tussen normaal van het vlak en de en vector recht omhoog
            axis=v1.cross(normaal)    #vector loodrecht op het vlak v1-normal(draaias voor tranformtie)
            euler=mathutils.Matrix.Rotation(hoek,4,axis).to_euler()  #eule rotatie berekenen
            euler.rotate_axis('Z', draaingZ)
            waardes.append(u.co)
            waardes.append(euler)
            
           


        for t in range (0,len(waardes),2):
            plaats=waardes[t]
            euler=waardes[t+1]
            bpy.ops.mesh.primitive_cylinder_add(vertices=zijden,
                                                radius=dia_klein, 
                                                depth=diepte_klein, 
                                                enter_editmode=False, 
                                                location=(plaats+plaats_abs),
                                                rotation=(euler))

            bpy.ops.mesh.intersect_boolean()
            plaats=waardes[t]
            euler=waardes[t+1]
            print('plaats=',plaats)
            bpy.ops.mesh.primitive_cylinder_add(vertices=zijden,
                                                radius=dia_groot, 
                                                depth=diepte_groot, 
                                                enter_editmode=False, 
                                                location=(plaats+plaats_abs),
                                                rotation=(euler))
            bpy.ops.mesh.intersect_boolean()
            
        return{'FINISHED'}
        
def register():
    bpy.utils.register_class(MESH_OT_gaten)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_gaten)
    
if __name__ == '__main__':
    register()        