
import bpy
import mathutils
import bmesh

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
        me=obj.data
        
        bm=bmesh.from_edit_mesh(me)
        hist=bm.select_history

        bpy.ops.mesh.edge_face_add()
        plaats_object = obj.location
        for vlak in bm.faces:
            
            if vlak.select:
                norm = vlak.normal
                lengte = norm.length
                factor = verplaats/lengte
                vert_ind = vlak.verts[0].index
                cord = vlak.verts[0].co+plaats_object
                cord.x=cord.x+(norm.x*factor)
                cord.y=cord.y+(norm.y*factor)
                cord.z=cord.z+(norm.z*factor)
                break
                
                
        
        
        
         # doe de bisect 
        if knop_3:
            bpy.ops.mesh.delete(type='FACE')# haal vlak weer weg
            #bpy.ops.mesh.separate(type='SELECTED')
            bpy.ops.mesh.select_all(action='SELECT')
            
        else:
            
            bpy.ops.mesh.delete(type='FACE')# haal vlak weer weg
            #bpy.ops.mesh.separate(type='SELECTED')
            bm.verts.ensure_lookup_table()
            bm.verts[vert_ind].select = True
            
            bpy.ops.mesh.select_linked()            

   
        #bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=cord,
                            clear_inner=knop,
                            clear_outer=not knop,
                            use_fill=knop_2,
                            plane_no=norm)       
        #bpy.ops.mesh.dissolve_limited()
        bm.to_mesh
        bm.free
     
        
        return{'FINISHED'}

def register():
    bpy.utils.register_class(MESH_OT_hakken)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_hakken)
    
if __name__ == '__main__':
    register()             