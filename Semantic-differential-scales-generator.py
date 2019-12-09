import matplotlib.pyplot as plt
import numpy as np
import random as r
import math as m
import os
import string

class Material():
    "Class for a material"
    def __init__(self, material):
        "Instantiates a material."
        self.material = material

    def __repr__(self):
        return str(self.material)


class Property():
    "Class for a material property."
    def __init__(self, name):
        "Instantiates a property."
        self.name = name
        self.materials = {}
        self.headers = ["Material", "Average", "Standard Deviation"]
    def __repr__(self):
        return str(self.name)

    def add_a_material(self,material,avg,std_dev):
        "Adds a material to the materials dictionary for that property. with average, and standard deviation values"
        property_values = PropertyValues(avg,std_dev)
        # Updates the materials dictionary with the material and its values.
        self.materials.update( {str(material) : property_values.values() } )
    
    def gen_array(self):
        "Generates the array of data for numpy to make graphs for that property."
        array_list = []
        material_list = []
        # Iterates over the materials in the materials list
        for mat in self.materials.keys():
            # Creates an array_row list and appends the material to it
            array_row = []
            material_list.append(mat)
            # Iterates over the values for avg and std deviation for each material
            for value in self.materials[mat]:
                # Appends the values to the array row
                array_row.append(value)
            # Appends the row to the list, for each material.
            array_list.append(array_row)
        # Returns a generated array from the array list, and the header list. 
        return np.array(array_list), material_list
        
    def make_graph(self,max_min):
        "Makes an error bar graph based on the array and other parameters supplied."
        data = self.gen_array()[0]
        mat_names = self.gen_array()[1]
        # Generates a range of x values for each value in first column of the array
        x = np.arange(1,len(data[:,0])+1)
        # Assigns y to equal the first column data array
        y = data[:,0]
        # Makes x-ticks for the graph from the mat_headers
        plt.xticks(x, mat_names, rotation = 30)
        # Adds error bars from the second coulmn of the data array
        e = data[:,1]
        plt.ylabel(str(self.name), fontweight="bold")
        plt.xlabel("Materials", fontweight="bold")
        plt.ylim(float(max_min[0]),float(max_min[1]))
        plt.xlim(min(x)-0.2*len(x),max(x)+0.2*len(x))
        plt.grid(linestyle='dashed')
        return plt.errorbar(x, y, yerr=e, fmt = "o", capsize=2)
    
    def gen_csv(self, file_path):
        "Method to generate a CSV file for the property."
        data = self.gen_array()[0]
        mat_names = self.gen_array()[1]
        no_headers = np.insert(data.astype(str), 0, mat_names, 1 )
        csv_array = np.insert(no_headers, 0, self.headers, 0)
        return np.savetxt(file_path, csv_array, fmt="%s", delimiter= ",")


class PropertyValues():
    "Class for property values to generate lists on the fly."
    def __init__(self,avg,std_dev):
        "Instnatiates a property value."
        self.property_values = [avg,std_dev]
        
    def values(self):
        return self.property_values

class FilePath():
    "Class for generating safe file paths and names."
    def __init__(self, new_folder_name, file_name):
        self.safe_file_name = self.make_name_safe(str(file_name))
        self.new_folder = os.path.join(os.getcwd(), new_folder_name)
    
    def make_name_safe(self,file_name):
        'Makes the file name safe for computer consumption by replacing all punctuation to be a "-"'
        for char in file_name: 
            if char in string.punctuation: 
                file_name = file_name.replace(char, "-") 
        return file_name

    def safe_file_path(self, file):
        '''Returns the safe file path with the file'''
        return str(os.path.join(self.new_folder, file))

    def add_extras(self, file_extension, *extras):
        '''Adds extra words and a file extension to the safe file name attribute.
        The method will separate extras with a "-" and add a "." before the file extension.'''
        extra_file_name = self.safe_file_name
        for extra in extras:
            extra_file_name += ( "-" + str(extra))
        extra_file_name += ("." + str(file_extension))
        return extra_file_name

def y_or_n(yn):
    "Default method for answering yes or no to questions. Returns None when user makes a false input."
    if yn == "y":
        return True
    elif yn == "n":
        return False
    else:
        print("Please only enter y or n!")
        return None

def y_n_loop(string):
    "Yes no loop function for resolving conflicts with false y/n input."
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
        #Uses the add_thing function to add Material instances to the material_list
        if add_thing(Material, material_list):
            adding_materials = False
            adding_properties = True

    while adding_properties:
        #Uses the add_thing function to add property instances to the material_list
        if add_thing(Property, property_list):
            adding_properties = False
            adding_values = True
    #Adding values to the properties and the materials.
        
    print("Your materials are " + str(material_list))
    print("Your properties are " + str(property_list))
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
                    # If the user wants some randomness
                    if gen_random==1:
                        # Multiplies the avg by a small randomness factor
                        avg *= r.uniform(0.8,1.2)
                    std_dev = only_num("Enter a value for standard deviation around " + str(mat) + "'s " + str(prprty) + "-ness:")
                    # If the user wants some randomness
                    if gen_random ==1:
                        # Multiplies the avg by a small randomness factor
                        std_dev *= r.uniform(0.8,1.2)
                    # Checks whether  the average and standard deviation values are within the max and min values.
                    if avg > max_min[1] or avg < max_min[0] or std_dev > max_min[1] or std_dev < max_min[0]:
                        # Queries a yes or no loop to check whether they want to continue with the out of max_min range values.
                        if y_n_loop("WARNING!!! The values specified for average and standard deviation of " + str(mat) + "'s " + str(prprty) + "-ness are outside of the maximum and minimum values. Do you wish to continue? (y/n)"):
                            # If they do wish to continue, Breaks the within_limits loop
                            within_limits = False
                        else:
                            # If they don't want continue, keeps within_limits loop, forcing user to re-enter maerial property values.
                            within_limits = True
                    else:
                        # Breaks the within limits loop as they have entered values within the limits of the max_min values.
                        within_limits = False
                # Resets the within limits loop to true so that they are queried about material properties for the next material in the list.
                within_limits = True
                #adds a material to the property with the avg and std dev values specified
                prprty.add_a_material(mat,avg,std_dev)
        plot = prprty.make_graph(max_min)

        # Makes a new file name based on the string of the property
        new_file_name = str(prprty) + "-differential-scales"
        # Makes the file name safe for computer consumption by changing all punctuation to a -

        the_path = FilePath("semantic-differential-scales", prprty)
        the_file_png = the_path.add_extras("png")
        the_file_csv = the_path.add_extras("csv","csv","file")

        if os.path.exists(the_path.new_folder):
            print("semantic-differential-scales found!")
        else:
            print("semantic-differential-scales directory not found. Making a new directory")
            print("...")
            os.makedirs(the_path.new_folder)
            print("Done!")
            if os.path.exists(the_path.new_folder):
                print("Directory successfuly made")

        print("Saving a semantic differential scale graph for " + str(prprty) + " as " + the_file_png )
        print("...")
        plt.savefig(the_path.safe_file_path(the_file_png), dpi = 300, bbox_inches ="tight")
        print("Done!")
        plt.clf()

        no_headers = np.insert(prprty.gen_array()[0].astype(str), 0, prprty.gen_array()[1], 1 )
        print("Saving a CSV file of semantic differential data for " + str(prprty) + " as " + the_file_csv )
        print("...")
        prprty.gen_csv(the_path.safe_file_path(the_file_csv))
        # np.savetxt(the_path.safe_file_path(the_file_csv), np.insert(no_headers, 0, the_headers, 0), fmt="%s", delimiter= ",")
        print("Done!")

        print("Your graph and CSV file have been saved in " + the_path.new_folder)