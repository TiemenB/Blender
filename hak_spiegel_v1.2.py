import bpy

import math
import bmesh
import mathutils

class VIEW_PT_mir_div(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "mir/div"
    
    bl_label = "Belangrijke zaken"
    bl_context_mode = 'EDIT'

    def draw(self, context):

       
        self.layout.operator('mesh.spiegel',
                            text = 'spiegelen',
                            icon='MOD_MIRROR')
        self.layout.operator('mesh.hakken',
                            text = 'hakken',
                            icon = 'SCULPTMODE_HLT')                    
                            





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
            bpy.ops.mesh.select_all(action='SELECT')
            
        else:
            
            bpy.ops.mesh.delete(type='FACE')# haal vlak weer weg
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
  
    
class MESH_OT_spiegel(bpy.types.Operator):
    """Spiegelen in een vlak"""
    bl_idname = "mesh.spiegel"  # komy in de afdeling mesh en heet planken
    bl_label = "spiegel"
    bl_options = {'REGISTER', 'UNDO'}  # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven
    # wel of niet om eigen as draaien
    knop: bpy.props.BoolProperty(
        name="merge",
        default=False)
    
    
    
    def execute(self,context):
        knop=self.knop
        
        context = bpy.context
        override = context.copy() # dictionary of context
        tool=bpy.context.scene.tool_settings.transform_pivot_point #actieve tool opslaan
        bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
        # oude automerge opslaan en later terugzetten
        autom = bpy.context.scene.tool_settings.use_mesh_automerge
        if knop:
            bpy.context.scene.tool_settings.use_mesh_automerge = True
        else:
            bpy.context.scene.tool_settings.use_mesh_automerge = False


        bpy.ops.mesh.select_linked()
        bpy.ops.mesh.duplicate()
        
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                override["area"] = area
                override["space_data"] = area.spaces.active
                override["region"] = area.regions[-1] # rule of thumb r.type == 'WINDOW'
                break

        bpy.ops.transform.resize(override,
                                 value=(1, 1, -1),
                                 constraint_axis=(True, False, False),
                                 orient_type='NORMAL'
                                 )
                                 
        bpy.ops.mesh.normals_make_consistent(inside=False)
        

        bpy.context.scene.tool_settings.transform_pivot_point = tool #actieve tool terugzetten
        
        #auto merge terugzetten
        bpy.context.scene.tool_settings.use_mesh_automerge = autom

        return{'FINISHED'}


def register():
    bpy.utils.register_class(VIEW_PT_mir_div)

    bpy.utils.register_class(MESH_OT_spiegel)
    bpy.utils.register_class(MESH_OT_hakken)

def unregister():
    bpy.utils.unregister_class(VIEW_PT_mir_div)

    bpy.utils.unregister_class(MESH_OT_spiegel)
    bpy.utils.unregister_class(MESH_OT_hakken)

if __name__ == '__main__':
    register()