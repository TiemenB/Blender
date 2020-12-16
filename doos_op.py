import bpy






class MESH_OT_doos(bpy.types.Operator):
    """maak een doos met opgegeven maten"""
    bl_idname = "mesh.doos"# komy in de afdeling mesh en heet planken
    bl_label = "doos"
    bl_options = {'REGISTER', 'UNDO'} # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven
    naam:bpy.props.StringProperty(
        name="naam",
        default='doos',
    )



    
    x:bpy.props.FloatProperty(
        name="x-maat(cm)",
        default=100,
    )
    y:bpy.props.FloatProperty(
        name="y-maat(cm)",
        default=20,
    )
    z:bpy.props.FloatProperty(
        name="z-maat(cm)",
        default=20,
    )
    def execute(self,context):
        naam=self.naam
        x=self.x
        y=self.y
        z=self.z
        bpy.ops.mesh.primitive_cube_add(size=(1))
        bpy.context.object.name=naam
        bpy.ops.transform.resize(value=(x/100,y/100,z/100), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) 
        
        return{'FINISHED'}       


def register():
    bpy.utils.register_class(MESH_OT_doos)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_doos)
    
if __name__ == '__main__':
    register()        