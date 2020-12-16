import bpy
import mathutils

class MESH_OT_hakken(bpy.types.Operator):
    """Snij het object in gekozen vlak"""
    bl_idname = "mesh.hakken"  # komy in de afdeling mesh en heet planken
    bl_label = "hakken"
    bl_options = {'REGISTER', 'UNDO'}  # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven
    # wel of niet om eigen as draaien
    knop: bpy.props.BoolProperty(
        name="binnen/buiten",
        default=True,
    )
    knop_2: bpy.props.BoolProperty(
        name="dicht/open",
        default=True,
    )

    knop_3: bpy.props.BoolProperty(
        name="alles/selectie",
        default=True,
    )
    
    verplaats: bpy.props.FloatProperty(
        name="verplaatsing",
        default=0,
    )
    
    def execute(self,context):
        knop=self.knop
        knop_2=self.knop_2
        knop_3=self.knop_3
        verplaats=-self.verplaats
        
        obj=bpy.context.object
        p=obj.data.polygons
        bpy.ops.mesh.edge_face_add()# maak vlak door punten
        bpy.ops.object.editmode_toggle()
        # welk vlak is gesecteerd?
        for t in p:
            if t.select:
                
                norm=t.normal
                lengte=norm.length
                factor=verplaats/lengte
                vert_ind=t.vertices[0]# het krijgen van de index van de nulde vertice van de polygon.
                punt_onhouden=vert_ind
                cord=obj.data.vertices[vert_ind].co+bpy.context.object.location
                cord.x=cord.x+(norm.x*factor)
                cord.y=cord.y+(norm.y*factor)
                cord.z=cord.z+(norm.z*factor)
                
                
        bpy.ops.object.editmode_toggle()
        
        
         # doe de bisect 
        if knop_3:
            bpy.ops.mesh.delete(type='FACE')# haal vlak weer weg
            bpy.ops.mesh.select_all(action='SELECT')
            
        else:
            
            bpy.ops.mesh.delete(type='FACE')# haal vlak weer weg
            
            bpy.ops.mesh.select_linked_pick(deselect=False, delimit={'SEAM'}, index=punt_onhouden)

            

   
        #bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=cord,clear_inner=knop,clear_outer=not knop,use_fill=knop_2, plane_no=norm, xstart=195, xend=495, ystart=358, yend=360)  
        #bpy.ops.mesh.dissolve_limited()
     
        
        return{'FINISHED'}

def register():
    bpy.utils.register_class(MESH_OT_hakken)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_hakken)
    
if __name__ == '__main__':
    register()             