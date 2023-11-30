import subprocess
import numpy as np
import unittest,os

from numpy.core.numeric import True_


# CubitPy imports.
from cubitpy import CubitPy, cubit_group, cupy, get_surface_center
from cubitpy.mesh_creation_functions import extrude_mesh_normal_to_tri_surface
from cubitpy.mesh_creation_functions import create_brick, extrude_mesh_normal_to_surface

testing_path = os.path.abspath(os.path.dirname(__file__))
testing_input = os.path.join(testing_path, "input-files-ref")
testing_temp = os.path.join(testing_path, "testing-tmp")



class TestStringMethods(unittest.TestCase):
    
    file='/home/a11bmafr/software/vmtk/vmtk2baci/049/Case_cut_49_fluid.msh'
    #file='/home/a11bmafr/software/baci/simulations/start_modeling/049/40_coarse.msh'    
    
    def test_stl_import(self):
        cubit = CubitPy()
        cubit.Import_Fluent_Geometry(self.file)
        self.assertFalse(cubit.was_last_cmd_undoable())

    def test_feature_angle(self):

        cubit = CubitPy()
        cubit.Import_Fluent_Geometry(self.file,100)
        a=cubit.get_entities("surface")
        
        # test if we really have 4 surfaces 
        self.assertTrue(len(a)==4)
   

    def test_wall_extrusion_quad(self):

        cubit = CubitPy()
        cubit.Import_Fluent_Geometry(self.file,100)
        # Surface 3 = big surface
        cubit.cmd("delete mesh")
        cubit.cmd("surface 3 Scheme Auto")
        
        cubit.cmd("mesh surface 3")
        cubit.cmd("refine surface 3")
        #cubit.cmd("refine surface 3")
        #cubit.cmd("refine surface 3")
        #cubit.cmd("refine surface 3")

        volume = extrude_mesh_normal_to_surface(
             cubit,
             [cubit.surface(3)],
             0.05,
             n_layer=3,
             extrude_dir="outside",
             offset=[0 ,0, 0],
         )
        cubit.display_in_cubit()
        # TODO define testcriteria

    def driver_fsi(self):
        # this a the test driver for the a fsi simulation
        test_file='/home/a11bmafr/software/vmtk/vmtk2baci/049/Case_cut_49_fluid.msh'
        cubit = CubitPy()
        cubit.Import_Fluent_Geometry(test_file,100)
        # Surface 3 = big surface
        cubit.cmd("delete mesh")
        cubit.cmd("surface 3 Scheme Auto")
        
        cubit.cmd("mesh surface 3")
        cubit.cmd("refine surface 3")


        volume = extrude_mesh_normal_to_surface(
             cubit,
             [cubit.surface(3)],
             0.05,
             n_layer=3,
             extrude_dir="outside",
             offset=[0 ,0, 0],
         )
            
        cubit.cmd("delete volume 2")
        cubit.Import_Fluent_Geometry(test_file,100)

        # create blocks 
        cubit.cmd("block 1 volume 1")
        cubit.cmd("block 2 volume 2")

        # you can replace this easily with a touple(name, id) -> print
        # also you would need to add here the search alg
        # add structure nodesets
        cubit.cmd("nodeset 11 Surface 9")
        cubit.cmd("nodeset 11 name \"artery_wall_surf_outside\" ")

        cubit.cmd("nodeset 12 Surface 2")
        cubit.cmd("nodeset 12 name \"artery_wall_surf_inside\" ")

        cubit.cmd("nodeset 13 Surface 8")
        cubit.cmd("nodeset 13 name \"artery_wall_surf_inflow\" ")

        cubit.cmd("nodeset 14 Surface 1")
        cubit.cmd("nodeset 14 name \"artery_wall_surf_outflow1\" ")

        cubit.cmd("nodeset 15 Surface 7")
        cubit.cmd("nodeset 15 name \"artery_wall_surf_outflow2\" ")

        # add fluid nodesets
        cubit.cmd("nodeset 21 Surface 3")
        cubit.cmd("nodeset 21 name \"artery_fluid_surf\" ")

        cubit.cmd("nodeset 23 Surface 6")
        cubit.cmd("nodeset 23 name \"artery_fluid_surf_inflow\" ")

        cubit.cmd("nodeset 24 Surface 4")
        cubit.cmd("nodeset 24 name \"artery_fluid_surf_outflow1\" ")

        cubit.cmd("nodeset 25 Surface 5")
        cubit.cmd("nodeset 25 name \"artery_fluid_surf_outflow2\" ")


        cubit.cmd("export mesh \"049_artery_fluid.e\" dimension 3 block all overwrite")

        #cubit.display_in_cubit()


    def test_export_normal(self):
        
        cubit = CubitPy()
        cubit.Import_Fluent_Geometry(self.file,100)
        surf_id=cubit.get_entities("surface")
        


    
    # def test_wall_extrudion(self):

    #     cubit = CubitPy()
    #     cubit.Import_Fluent_Geometry(self.file,100)
    #     cubit.cmd("refine volume 2")
    #     # Surface 3 = big surface
    #     cubit.cmd("delete mesh")
    #     cubit.cmd("surface 3 Scheme Auto")
    #     cubit.cmd("refine surface 3")
    #     cubit.cmd("mesh surface 3")
    #     volume = extrude_mesh_normal_to_surface(
    #         cubit,
    #         [cubit.surface(3)],
    #         0.05,
    #         n_layer=2,
    #         extrude_dir="outside",
    #         #offset=[0 0 0],
    #     )
    #     #cubit.cmd("delete volume 2")
    #     #cubit.Import_Fluent_Geometry(self.file,100)
    #     #cubit.cmd("refine volume 2")
    #     cubit.display_in_cubit()


    def test_connectivity(self):
        cubit = CubitPy()
        cubit.cmd('brick x 1 y 1 z 1')
        cubit.cmd('surface 1  Scheme TriMesh geometry approximation angle 15 ')
        cubit.cmd('Trimesher surface gradation 1.3')
        #cubit.cmd('surface 1 size 1')
        cubit.cmd('mesh surface 1 ')

        volume = extrude_mesh_normal_to_tri_surface(
            cubit,
            #[cubit.surface(i) for i in surface_ids],
            [cubit.surface(1)],
            1,
            n_layer=1,
            extrude_dir="symmetric",
            #offset=[1, 1, 1],
        )
        cubit.display_in_cubit()
        self.assertFalse(cubit.was_last_cmd_undoable())
        
        
       # cubit.cmd('volume 1 redistribute nodes off ')
       # cubit.cmd('volume 1 Scheme Sweep  source surface 1    target surface 2   sweep transform least squares  ')
       # cubit.cmd('volume 1 autosmooth target on  fixed imprints off  smart smooth on  tolerance 0.2  nlayers 5')

        # cubit.cmd('volume 1  sizing function constant ')
        # cubit.cmd('delete mesh volume 1  propagate')
        # cubit.cmd('volume 1  size 1 ')
        # cubit.cmd('mesh volume 1 ')
        # cubit.cmd('nodeset 1 volume 1')
        # nodal_coordinates=[]
        # quad_nodes = cubit.get_connectivity("wedge", 1)
        # for node in quad_nodes:
        #     nodal_coordinates.append(cubit.get_nodal_coordinates(node))
        # print("here,",nodal_coordinates) 
        # print("here,", cubit.get_connectivity("wedge", 1))

''' 
    def test_extrude_mesh_function(self):
        """Test the extrude mesh function."""

        # Initialize cubit.
        cubit = CubitPy()
        # Create dummy geometry to check, that the extrude functions work with
        # already existing geometry.
        cubit.cmd("create surface circle radius 1 zplane")
        cubit.cmd("surface 1  Scheme TriMesh geometry approximation angle 15")
        cubit.cmd("surface 1  size 4")
        cubit.cmd("mesh surface 1")
        #cubit.display_in_cubit()
        # cubit.cmd("create brick x 1")
        # cubit.cmd("mesh volume 2")

        # # Create and cut torus.
        # cubit.cmd("create torus major radius 1.0 minor radius 0.5")
        # torus_vol_id = cubit.get_entities(cupy.geometry.volume)[-1]
        # cut_text = "webcut volume {} with plane {}plane offset {} imprint merge"
        # cubit.cmd(cut_text.format(torus_vol_id, "x", 1.0))
        # cubit.cmd(cut_text.format(torus_vol_id, "y", 0.0))
        surface_ids = cubit.get_entities(cupy.geometry.surface)

        # cut_surface_ids = [surface_ids[-4], surface_ids[-1]]
        # cut_surface_ids_string = " ".join(map(str, cut_surface_ids))
        # cubit.cmd("surface {} size auto factor 9".format(cut_surface_ids_string))
        # cubit.cmd("mesh surface {}".format(cut_surface_ids_string))
        print("empty?",cubit.surface(surface_ids[0]))
        # Extrude the surface.
        volume = extrude_mesh_normal_to_surface(
            cubit,
            #[cubit.surface(i) for i in surface_ids],
            [cubit.surface(1)],
            1,
            n_layer=1,
            extrude_dir="symmetric",
            offset=[1, 1, 1],
        )

        # Check the created volume.
        # self.assertTrue(
        #     np.abs(
        #         cubit.get_meshed_volume_or_area("volume", [volume.id()])
        #         - 0.6917559630511103
        #     )
        #     < 1e-10
        # )
        
        # Set the mesh for output.
        #cubit.add_element_type(volume, cupy.element_type.hex8)
        cubit.display_in_cubit()
        # Compare the input file created for baci.
        #self.compare(cubit, single_precision=False)



    def test_create_boundary_mesh(self):

        cubit = CubitPy()
        cubit.Import_Fluent_Geometry(self.file,100)
        cubit.cmd("delete mesh")
        cubit.cmd("surface 3 Scheme Auto")
        cubit.cmd('mesh surface 3')
        #cubit.cmd('refine surface 3')
        # create boundary layer
        cubit.cmd("create boundary_layer 1")
        cubit.cmd("modify boundary_layer 1 uniform height 0.05 growth 1.2 layers 4 ")
        cubit.cmd("modify boundary_layer 1 add surface 3 volume 2 ")
        cubit.cmd("modify boundary_layer 1 continuity on")
        cubit.cmd("undo group end")

        # create volume mesh
        cubit.cmd('tri mesh volume 2')
       
        cubit.cmd('volume 2  Scheme Tetmesh proximity layers off geometry approximation angle 15 ')
        cubit.cmd('volume 2  tetmesh growth_factor 1 ')
        cubit.cmd('Trimesher surface gradation 1.3')
        cubit.cmd('mesh volume 2')
        print("xes")
        cubit.display_in_cubit()
        self.assertTrue(0)

''' 
       


if __name__ == "__main__":
    unittest.main()