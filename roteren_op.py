import bpy
import math








pi=math.pi

class MESH_OT_roteren(bpy.types.Operator):
    """roteer object in xy vlak rond het gekozen object"""
    bl_idname = "mesh.roteren"# komy in de afdeling mesh en heet planken
    bl_label = "roteren"
    bl_options = {'REGISTER', 'UNDO'} # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven
    
    straal:bpy.props.FloatProperty(
        name="straal(cm)",
        default=100,
    )
    aantal:bpy.props.IntProperty(
        name="aantal",
        default=4,
        min=1, soft_max=20,
    )
    verdraaing:bpy.props.FloatProperty(
        name="verdraaing(gra)",
        default=0,
    )
    #wel of niet om eigen as draaien
    knop:bpy.props.BoolProperty(
        name="draai",
        default=True,
    )    
    
    def execute(self, context):
        straal=self.straal/100
        aantal=self.aantal
        draai=(self.verdraaing*2*pi)/360
        if self.knop == True:
            fact=1
        else:
            fact=0
        plaats=bpy.context.object.location

        for t in range (0, aantal):
            
            hoek=(2*pi/aantal)*t+draai
            print('hoek=',hoek)
            y=math.sin(hoek)*straal+plaats.y
            x=math.cos(hoek)*straal+plaats.x
            z=plaats.z
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
            bpy.context.object.location=(x,y,z)
            if t>0:
                bpy.ops.transform.rotate(value=(fact*(2*pi)/aantal),orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False) 
                
                
            else:
                bpy.ops.transform.rotate(value=(draai), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        return{'FINISHED'}









def register():
    bpy.utils.register_class(MESH_OT_roteren)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_roteren)
    
if __name__ == '__main__':
    register()            