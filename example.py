"""
Loads all the example fault trees which have the entire FT in a single file.
"""
import os
from pathlib import Path
from ft_2_quantum_sat.fault_tree import FaultTree

image_folder = 'images/'


def image_name(filepath):
    """
    Get a name for the image from the file path (models/ABC/abc.xml -> abc.png).
    """
    file_name = os.path.basename(filepath)
    return image_folder + file_name[:-4] + '.png'


def analyze_fault_tree(filepath, m=1, method='classical'):

    # load the fault tree
    print(f"Loading {filepath}... ", end='')
    ft = FaultTree.load_from_xml(filepath)
    print(f"(has {ft.number_of_nodes()} nodes)")

    # vizualize
    ft.save_as_image(image_name(filepath))

    # compute minimal cutsets
    print(f"Computing the {m} smallest minimal cut sets with method = '{method}'...")
    cutsets = ft.compute_min_cutsets(m, method)
    print(f"{cutsets}\n")


if __name__ == '__main__':
    Path(image_folder).mkdir(parents=True, exist_ok=True)

    # analyze FTs (other FTs can't be loaded because they have e.g. this 
    # <!-- Transfer-In --> thing
    analyze_fault_tree('models/Theatre/theatre.xml', m=2)
    analyze_fault_tree('models/Theatre/theatre.xml', m=2, method='grover')
    analyze_fault_tree('models/SmallTree/SmallTree.xml', m=2)
    analyze_fault_tree('models/BSCU/BSCU.xml', m=3)
    analyze_fault_tree('models/Lift/lift.xml', m=5)
