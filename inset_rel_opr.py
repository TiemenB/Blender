# Maakt een array van de indexen van de geslecteerde vlakken
import bpy
import bmesh
from random import random


class MESH_OT_inset_rel(bpy.types.Operator):
    """ Relatieve inset naar kortst lijn"""
    bl_idname = "mesh.rel_inset"
    bl_label = "relative inset"
    bl_options = {'REGISTER', 'UNDO'}

    verhouding: bpy.props.FloatProperty(
        name="verhouding",
        default=10,
    )

    def execute(self, context):
        verhouding = self.verhouding

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()
        ges_vlakken = []
        for f in bm.faces:
            if f.select:
                vlak_kortste = []
                vlak_kortste.append(f.index)
                lijnlengte = 0
                # kijken wat de kortste lijn van een vlak is
                for lijn in f.edges:
                    if lijnlengte == 0:
                        kortste = lijn.calc_length()
                    lijnlengte = lijn.calc_length()
                    if lijnlengte < kortste:
                        kortste = lijnlengte
                vlak_kortste.append(kortste)
                ges_vlakken.append(vlak_kortste)

        print('Geselecteerde vlakken zijn; ', ges_vlakken)
        bpy.ops.mesh.select_all(action='DESELECT')
        for vk in ges_vlakken:
            dikte = vk[1]/verhouding
            bm.faces[vk[0]].select_set(True)
            bpy.ops.mesh.inset(thickness=dikte, depth=0)

            bm.faces.ensure_lookup_table()
            bm.faces[vk[0]].select_set(False)
        for vk in ges_vlakken:
            bm.faces[vk[0]].select_set(True)

        return{'FINISHED'}


def register():
    bpy.utils.register_class(MESH_OT_inset_rel)


def unregister():
    bpy.utils.unregister_class(MESH_OT_inset_rel)


if __name__ == '__main__':
    register()
