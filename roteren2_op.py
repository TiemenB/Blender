import bpy
import math
pi = math.pi


class MESH_OT_roteren(bpy.types.Operator):
    """Roteer rond actief element"""
    bl_idname = "mesh.roteren"  # komy in de afdeling mesh en heet planken
    bl_label = "roteren"
    bl_options = {'REGISTER', 'UNDO'}  # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven
    
    knop: bpy.props.BoolProperty(
        name="kopieren",
        default=True,
    )
    
    
    
    aantal: bpy.props.IntProperty(
        name = "aantal",
        default = 2
    )
    As: bpy.props.IntProperty(
        name = "As: 1=X,2-Y,3=Z",
        default = 1
    )    
    
    
    def execute(self,context):
        aantal = self.aantal
        hoek = 360/aantal
        As=self.As
        richt_as = 'X'
        if As == 2:richt_as='Y'
        if As == 3:richt_as='Z'


        context = bpy.context
        override = context.copy() # dictionary of context
        tool=bpy.context.scene.tool_settings.transform_pivot_point #actieve tool opslaan
        
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                override["area"] = area
                override["space_data"] = area.spaces.active
                override["region"] = area.regions[-1] # rule of thumb r.type == 'WINDOW'
                break

        #bpy.ops.view3d.snap_cursor_to_active()

        for t in range (0,aantal-1):
            bpy.ops.mesh.duplicate()                         
            bpy.ops.transform.rotate(override,value=hoek/360*2*pi,
                                        orient_axis=richt_as, orient_type='CURSOR',
                                        orient_matrix_type='CURSOR',
                                        constraint_axis=(False, True, False),
                                        mirror=True, use_proportional_edit=False,
                                        proportional_edit_falloff='SMOOTH',
                                        proportional_size=1,
                                        use_proportional_connected=False,
                                        use_proportional_projected=False)
                                        
        bpy.context.scene.tool_settings.transform_pivot_point = tool #actieve tool terugzetten
                                        
        return{'FINISHED'}                                        
                                        
def register():
    bpy.utils.register_class(MESH_OT_roteren)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_roteren)
    
if __name__ == '__main__':
    register()                                            
                                        