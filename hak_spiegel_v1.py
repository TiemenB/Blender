import bpy

import math

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
            
            bpy.ops.mesh.select_linked_pick(deselect=False, delimit=set(), index=punt_onhouden)            
            print('punt=',punt_onhouden)
            
            

   
        #bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=cord,clear_inner=knop,clear_outer=not knop,use_fill=knop_2, plane_no=norm)  
       
     
        
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