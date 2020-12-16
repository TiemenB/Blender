import bpy

class MESH_OT_spiegel(bpy.types.Operator):
    """Spiegelen in een vlak"""
    bl_idname = "mesh.spiegel"  # komy in de afdeling mesh en heet planken
    bl_label = "spiegel"
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
    
    def execute(self,context):
        context = bpy.context
        override = context.copy() # dictionary of context
        tool=bpy.context.scene.tool_settings.transform_pivot_point #actieve tool opslaan
        bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'

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
        
        
        
        return{'FINISHED'}
    
def register():
    bpy.utils.register_class(MESH_OT_spiegel)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_spiegel)
    
if __name__ == '__main__':
    register()   