import bpy
import random
import math
import bmesh
from random import random
pi = math.pi


class VIEW_PT_tiemen(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "tiemen"
    bl_label = "Belangrijke zaken"

    def draw(self, context):

        self.layout.operator('mesh.doos',
                             text='doos')
        self.layout.operator('mesh.roteren',
                             text='roteren')
        self.layout.operator('mesh.verdelen',
                             text='verdelen')
        self.layout.operator('mesh.plakken',
                             text='plakken')
        self.layout.operator('mesh.rel_inset',
                             text='relatieve inset')

        props = self.layout.operator('mesh.primitive_cube_add',
                                     text='random')
        x = random.random()*20
        y = random.random()*20
        z = random.random()*20
        props.location = (x, y, z)


class MESH_OT_roteren(bpy.types.Operator):
    """roteer object in xy vlak rond het gekozen object"""
    bl_idname = "mesh.roteren"  # komy in de afdeling mesh en heet planken
    bl_label = "roteren"
    bl_options = {'REGISTER', 'UNDO'}  # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven

    straal: bpy.props.FloatProperty(
        name="straal(cm)",
        default=100,
    )
    aantal: bpy.props.IntProperty(
        name="aantal",
        default=4,
        min=1, soft_max=20,
    )
    verdraaing: bpy.props.FloatProperty(
        name="verdraaing(gra)",
        default=0,
    )
    # wel of niet om eigen as draaien
    knop: bpy.props.BoolProperty(
        name="draai",
        default=True,
    )
    link: bpy.props.BoolProperty(
        name="gelinked",
        default=False,
    )

    def execute(self, context):
        straal = self.straal/100
        aantal = self.aantal
        link = self.link
        draai = (self.verdraaing*2*pi)/360
        if self.knop == True:
            fact = 1
        else:
            fact = 0
        plaats = bpy.context.object.location

        for t in range(0, aantal):

            hoek = (2*pi/aantal)*t+draai
            print('hoek=', hoek)
            y = math.sin(hoek)*straal+plaats.y
            x = math.cos(hoek)*straal+plaats.x
            z = plaats.z
            bpy.ops.object.duplicate_move(
                OBJECT_OT_duplicate={"linked": link, "mode": 'TRANSLATION'})
            bpy.context.object.location = (x, y, z)
            if t > 0:
                bpy.ops.transform.rotate(value=(fact*(2*pi)/aantal), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
                    False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

            else:
                bpy.ops.transform.rotate(value=(draai), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
                    False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        return{'FINISHED'}


class Verdeel_array(bpy.types.Operator):
    """twee objecten kieren"""
    bl_idname = "mesh.verdelen"
    bl_label = "verdelen"
    bl_options = {'REGISTER', 'UNDO'}

    aantal: bpy.props.IntProperty(
        name="aantal",
        default=2,
        min=2, soft_max=30,
    )
    link: bpy.props.BoolProperty(
        name="gelinkt",
        default=False,
    )

    def execute(self, context):
        def uitvoer(deler, link):
            v = []
            dingen = []
            for item in bpy.context.selected_objects:
                v.append(item.location)
                dingen.append(item)

            afst_x = v[1].x-v[0].x
            afst_y = v[1].y-v[0].y
            afst_z = v[1].z-v[0].z
            print('de afstand over de x-as=', afst_x)
            verpl_x = afst_x/deler
            verpl_y = afst_y/deler
            verpl_z = afst_z/deler
            print(dingen[0])
            bpy.ops.object.select_all(action='DESELECT')
            dingen[0].select_set(True)

            for kopie in range(deler-1):
                bpy.ops.object.duplicate_move(
                    OBJECT_OT_duplicate={
                        "linked": link, "mode": 'TRANSLATION'},
                    TRANSFORM_OT_translate={"value": (verpl_x, verpl_y, verpl_z),
                                            "orient_type": 'GLOBAL',
                                            "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1))})

        deler = self.aantal
        link = self.link
        selectie = bpy.context.selected_objects

        if len(selectie) == 2:
            uitvoer(deler, link)
        else:
            pass
        return{'FINISHED'}


class MESH_OT_doos(bpy.types.Operator):
    """maak een doos met opgegeven maten"""
    bl_idname = "mesh.doos"  # komy in de afdeling mesh en heet planken
    bl_label = "doos"
    bl_options = {'REGISTER', 'UNDO'}  # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven
    naam: bpy.props.StringProperty(
        name="naam",
        default='doos',
    )

    x: bpy.props.FloatProperty(
        name="x-maat(cm)",
        default=100,
    )
    y: bpy.props.FloatProperty(
        name="y-maat(cm)",
        default=20,
    )
    z: bpy.props.FloatProperty(
        name="z-maat(cm)",
        default=20,
    )

    def execute(self, context):
        naam = self.naam
        x = self.x
        y = self.y
        z = self.z
        bpy.ops.mesh.primitive_cube_add(size=(1))
        bpy.context.object.name = naam
        bpy.ops.transform.resize(value=(x/100, y/100, z/100), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True,
                                 use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)

        return{'FINISHED'}


class MESH_OT_plakken(bpy.types.Operator):
    """Hier moet iets"""
    bl_idname = "mesh.plakken"  # komy in de afdeling mesh en heet planken
    bl_label = "Plakken"
    bl_options = {'REGISTER', 'UNDO'}  # nodig voor menu in beeld te krijgen
    # hier staan waardes die je mee kan geven

    plank_dikte: bpy.props.FloatProperty(
        name="plank dikte(cm)",
        default=2,
    )
    sleuf: bpy.props.FloatProperty(
        name="sleuf(cm)",
        default=4,
    )

    def execute(self, context):
        dikte_hout = self.plank_dikte/100
        dikte_sleuf = self.sleuf/100
        x_maat = bpy.context.object.dimensions.x
        y_maat = bpy.context.object.dimensions.y
        z_maat = bpy.context.object.dimensions.z
        # nulpunt van het object in centrum geometry zetten
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        x_pos = bpy.context.object.location.x
        y_pos = bpy.context.object.location.y
        # naam van het object(moet id_name zijn)
        naam = bpy.context.object.id_data.name
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.editmode_toggle()

        aantal_lagen = int(z_maat/(dikte_hout+dikte_sleuf))
        maat = x_maat*1.1
        if y_maat > x_maat:
            maat = y_maat*1.1
        onder = (bpy.context.object.location.z)-(z_maat/2)

        # eerste vlak maken in object mode
        bpy.ops.mesh.primitive_plane_add(
            size=maat, enter_editmode=False, location=(x_pos, y_pos, onder-1))
        # naar edit mode voor vervolg zodat het een object wordt
        bpy.ops.object.editmode_toggle()
        for z in range(aantal_lagen+2):

            bpy.ops.mesh.primitive_plane_add(size=maat,
                                             enter_editmode=False,
                                             location=(x_pos, y_pos, onder))
            onder = onder+dikte_hout+dikte_sleuf
        bpy.ops.mesh.select_all(action='DESELECT')  # alle lagen deselecteren
        bpy.ops.object.editmode_toggle()  # weer in objectmode
        # het te versnijden object selecteren
        bpy.data.objects[naam].select_set(True)
        bpy.ops.object.join()  # verbinden met de lagen
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.intersect_boolean(operation='INTERSECT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={
                                         "use_normal_flip": False, "mirror": False}, TRANSFORM_OT_translate={"value": (0, 0, dikte_hout), })
        bpy.ops.object.editmode_toggle()

        return{'FINISHED'}


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
    bpy.utils.register_class(VIEW_PT_tiemen)
    bpy.utils.register_class(MESH_OT_roteren)
    bpy.utils.register_class(Verdeel_array)
    bpy.utils.register_class(MESH_OT_doos)
    bpy.utils.register_class(MESH_OT_plakken)
    bpy.utils.register_class(MESH_OT_inset_rel)


def unregister():
    bpy.utils.unregister_class(VIEW_PT_tiemen)
    bpy.utils.unregister_class(MESH_OT_roteren)
    bpy.utils.unregister_class(Verdeel_array)
    bpy.utils.unregister_class(MESH_OT_doos)
    bpy.utils.unregister_class(MESH_OT_plakken)
    bpy.utils.unregister_class(MESH_OT_inset_rel)


if __name__ == '__main__':
    register()
