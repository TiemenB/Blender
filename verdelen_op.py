import bpy
from mathutils import Vector


class Verdeel_array(bpy.types.Operator):
    """twee objecten kieren"""
    bl_idname = "mesh.verdelen"
    bl_label= "verdelen"
    bl_options = {'REGISTER','UNDO'}
    
    aantal:bpy.props.IntProperty(
        name="aantal",
        default=2,
        min=2, soft_max=30,
    )
    
    def execute(self,context):
        def uitvoer(deler):
            v=[]
            dingen=[]
            for item in bpy.context.selected_objects:
                v.append(item.location)
                dingen.append(item)
                
            afst_x = v[1].x-v[0].x
            afst_y = v[1].y-v[0].y
            afst_z = v[1].z-v[0].z   
            print('de afstand over de x-as=',afst_x)
            verpl_x=afst_x/deler
            verpl_y=afst_y/deler
            verpl_z=afst_z/deler
            print(dingen[0])
            bpy.ops.object.select_all(action='DESELECT')
            dingen[0].select_set(True)


            for kopie in range(deler-1):
                bpy.ops.object.duplicate_move(
                    OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
                     TRANSFORM_OT_translate={"value":(verpl_x, verpl_y, verpl_z),
                      "orient_type":'GLOBAL', 
                      "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1))}) 
                       





        deler=self.aantal            
        selectie=bpy.context.selected_objects
            

        if len(selectie)==2:
            uitvoer(deler)
        else:
            pass
        return{'FINISHED'}

def register():
    bpy.utils.register_class(Verdeel_array)
    
def unregister():
    bpy.utils.unregister_class(Verdeel_array)
    
if __name__ == '__main__':
    register()     