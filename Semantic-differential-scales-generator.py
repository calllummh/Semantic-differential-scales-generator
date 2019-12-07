import matplotlib.pyplot as plt
import numpy as np
import random as r
import math as m
import os

class Material():
    "Class for a material"
    def __init__(self, material):
        self.material = material

    def __repr__(self):
        return str(self.material)


class Property():
    "Class for a material property"
    def __init__(self, name):
        self.name = name
        self.materials = {}

    def __repr__(self):
        return str(self.name)

    def add_a_material(self,material,avg,std_dev):
        "Adds a material to the materials list for that property"
        property_values = PropertyValues(avg,std_dev)
        #updates the materials dictionary with the material and its values.
        self.materials.update( {str(material) : property_values.values() } )
    
    def mat_values(self,material):
        "returns the materials' values from the materials dictionary"
        return list(self.materials.get(material))
        # return (str(material) + " has the average value " + str(values[0]) + " and a standard deviation of " + str(values[1]) + " for the property " + str(self.name) + "." , values)
    
    def gen_array(self):
        "Generates the array of data for numpy to make graphs for that property"
        array_list = []
        header_list = []
        #iterates over the materials in the materials list
        for mat in self.materials.keys():
            #creates an array_row list and appends the material to it
            array_row = []
            header_list.append(mat)
            #iterates over the values generated by the mat_values method
            for value in self.mat_values(mat):
                #appends the values to the array row
                array_row.append(value)
            #appends the row to the list, for each material.
            array_list.append(array_row)
        #generates the array from the array list. 
        return np.array(array_list), header_list


class PropertyValues():
    "Class for property values to generate lists on the fly."
    def __init__(self,avg,std_dev):
        self.property_values = [avg,std_dev]
        
    def values(self):
        return self.property_values


def y_or_n(yn):
    "Default method for answering yes or no to questions."
    if yn == "y":
        return True
    elif yn == "n":
        return False
    else:
        print("Please only enter y or n!")
        return None

def y_n_loop(string):
    y_n = True
    while y_n:
        print(string)
        ans = input()
        if y_or_n(ans) is None:
            y_n = True
        else:
            if y_or_n(ans):
                return True
            elif not y_or_n(ans):
                return False
            y_n = False

def add_thing(thing_class,thing_list):
    "adds things to their respected lists in the __main__ function"
    print("Please enter a " + thing_class.__name__.lower() + ".")
    #creates a thing of thing_class via the input
    this_thing = thing_class(input())
    #appends the thing to the list of things
    thing_list.append(this_thing)
    #asks if you want to make more things?
    if y_n_loop("Do you want to add another " + thing_class.__name__.lower() + "? (y/n)"):
        return False
    else:
        return True


def make_graph(array,prprty,max_min):
    "Makes an error bar graph based on the array and other parameters supplied."
    x = np.arange(1,len(array[0][:,0])+1)
    y = array[0][:,0] 
    plt.xticks(x, array[1])
    e = array[0][:,1]
    plt.ylabel(str(prprty), fontweight="bold")
    plt.xlabel("Materials", fontweight="bold")
    plt.ylim(float(max_min[0]),float(max_min[1]))
    plt.xlim(min(x)-0.2*len(x),max(x)+0.2*len(x))
    plt.grid(linestyle='dashed')
    return plt.errorbar(x, y, yerr=e, fmt = "o", capsize=2)

def only_num(string):
    "Checks whether a user input is a numeric value, if not, loops around the specified previous question."
    only_num = True
    while only_num:
        print(string)
        try:
            thing = float(input())
            only_num = False
            return thing
        except ValueError:
            print("Please only enter numeric values!")
            only_num = True

if __name__ == '__main__':
    material_list = []
    property_list = []
    adding_materials = True
    adding_properties = False
    adding_values = False
    draw_graphs = False
    gen_random = 0
    within_limits = True
    the_headers = ["Material", "Average", "Standard Deviation"]
    newpath = os.path.join(os.getcwd(), "semantic-differential-scales")
    max_min = []


    max_min.append(only_num("Please enter the minimum rating limit:"))
    max_min.append(only_num("Please enter the maximum rating limit:"))

    if y_n_loop("Do you want to generate totally random values for your material properties and standard deviations? (y/n)"):
        if y_n_loop("WARNING!!! These values are completely and totally random. No guarantee can be made for their relevance to the materials specfied. Do you still want to proceed? (y/n)"):
            gen_random = 2
        else:
            if y_n_loop("Would you like to add a small amount of randomness to inputted values? (y/n)"):
                gen_random = 1
    else:
        if y_n_loop("Would you like to add a small amount of randomness to inputted values? (y/n)"):
            gen_random = 1

    while adding_materials:
        if add_thing(Material, material_list):
            adding_materials = False
            adding_properties = True

    while adding_properties:
        if add_thing(Property, property_list):
            adding_properties = False
            adding_values = True
    #Adding values to the properties and the materials.
    #Iterates over the list of properties
    for prprty in property_list:
        #iterates over the list of materials for each property
        for mat in material_list:
            #If total randomness was selected
            if gen_random == 2:
                #adds properties with random values based on maximum and minimum limits.
                prprty.add_a_material(mat,r.uniform(float(max_min[0]),float(max_min[1])),r.uniform(float(max_min[0]), float(max_min[1])/4))
            else:
                while within_limits:
                    avg = only_num("Enter a value for average " + str(prprty) + "-ness, of " + str(mat) + ":")
                    if gen_random==1:
                        avg *= r.uniform(0.8,1.2)

                    std_dev = only_num("Enter a value for standard deviation around " + str(mat) + "'s " + str(prprty) + "-ness:")
                    if gen_random ==1:
                        std_dev *= r.uniform(0.8,1.2)
                    if avg > max_min[1] or avg < max_min[0] or std_dev > max_min[1] or std_dev < max_min[0]:
                        if y_n_loop("WARNING!!! The values specified for average and standard deviation of " + str(mat) + "'s " + str(prprty) + "-ness are outside of the maximum and minimum values. Do you wish to continue? (y/n)"):
                            within_limits = False
                        else:
                            within_limits = True
                #adds a material to the property with the avg and std dev values specified
                prprty.add_a_material(mat,avg,std_dev)
        if len(property_list) < 3:
            num_cols = 1
        else:
            num_cols = m.ceil(len(property_list)/3)
        # plt.subplot(3, num_cols, property_list.index(prprty)+1, aspect = len(material_list)/(float(max_min[1])*2))
        plot = make_graph(prprty.gen_array(), prprty, max_min)

        newfilename = str(prprty) + "-differential-scales.png"
        if os.path.exists(newpath):
            print("semantic-differential-scales found!")
        else:
            print("semantic-differential-scales directory not found. Making a new directory...")
            os.makedirs(newpath)
            if os.path.exists(newpath):
                print("Directory successfuly made")

        print("saving a semantic differential scale graph for " + str(prprty) + " as " + newfilename + "...")
        plt.savefig(os.path.join(newpath, (newfilename)),dpi = 300, bbox_inches ="tight")
        plt.clf()
        print("Your data for " + str(prprty) + " is ")

        no_headers = np.insert(prprty.gen_array()[0].astype(str), 0, prprty.gen_array()[1], 1 )

        print(str(np.insert(no_headers, 0, the_headers, 0)))
    print("Your graphs have been saved in " + str(newpath))
    print("Your materials are " + str(material_list))
    print("Your properties are " + str(property_list))
    # plt.show()
