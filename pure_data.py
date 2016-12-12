import pandas as pd


class Data_parse(object):
    """
    Data_parse read the dppr_file to get_values properties from a component
    """
    
    def read_dppr(self, dppr_file):
        #self.dppr_data = pd.read_excel(dppr_file).head().set_index('Name').ix[:, 1:12]

        self.dppr_data = pd.read_excel(dppr_file).set_index("Name").ix[:, 1:12]
        # component_names = dppr_data.index.get_values()
        return self.dppr_data
        
    def selec_component(self, dppr_file, component):
        self.name = str(component)
        self.properties = self.read_dppr(dppr_file).loc[self.name]
        self.label = {self.name : self.properties}

        #print(self.properties.index)
        #print ('name = {0}'.format(self.name))
        #print ('acentric_factor = {0}'.format(self.properties['Omega']))
        #print ('critical_Temperature = {0}'.format(self.properties['Tc']))
        #print ('critical_Pressure = {0}'.format(self.properties['Pc']))
        #print ('compressibility_factor_Z = {0}'.format(self.properties['Zc']))
        #print(self.label.keys())
        #print(self.label.values())

        return self.name, self.properties

        def fun(self):
            pass

    


def show(component, properties_component):
    print ('Component = {0}'.format(component))
    print ('Acentric_factor = {0}'.format(properties_component[1]['Omega']))
    print ('Critical_Temperature = {0} K'.format(properties_component[1]['Tc']))
    print ('Critical_Pressure = {0} Bar'.format(properties_component[1]['Pc']))
    print ('Critical_Volume = {0} cm3/mol'.format(properties_component[1]['Vc']))
    print ('Compressibility_factor_Z = {0}'.format(properties_component[1]['Zc']))
    
        

def main():
    
    dppr_file = "PureFull.xls"
    #component = "METHANE"
    #component = "ISOBUTANE"
    component = "TRIPHENYLMETHANE"
    #component = "PYRENE"
    component = "CARBON DIOXIDE"
    #component = "CARBON"
    
    properties_table = Data_parse()    
    #component, properties_component = properties_table.selec_component(dppr_file, component)

    #print(properties_component["Omega"])
    #print(component)

    properties_component = properties_table.selec_component(dppr_file, component)

    print(properties_component)

    #show_properti(component, properties_component)


if __name__ == "__main__":
    # execute only if run as a script
    main()
