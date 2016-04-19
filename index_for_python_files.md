basis.py
-----

This file is part of the Ptolemy Layer for Google Earth project.
 It implements a method to compute unknown coordinates from known modern coordinates for locations given in Ptolemy. It is currently focused on book 7 (India region), but can and will be extended to other regions. 

This particular program works by viewing the nearest three known neighbors as a basis for each unknown, and then doing a change of basis to the modern coordinates for those three known places.

###function:   
    change_basis(ax, bx, cx, tx, ay, by, cy): return ty
      Find the position ty based on basis formed by vectors ay, by and ay, cy   
      by finding its coordinates using tx on the basis formed by vectors ax, bx, and ax, cx.

###class:   
    Basis(object): trainX, trainY, neighbors
    predict(self, X): return y
     Compute unknown modern coordinates from known ones using the given triangulation.

##basis_test.py

### function:   
    coords(data, cols, name): return data.loc[data.name == name, cols].values[0]  
     
    nulti_coords(data,cols, names): return tuple(coords(data, cols, name) for name in names)  
    
    change_basis(ax, bx, cx, tx, ay, by, cy): return ty
    
    show_points(points):   
    
    add_point(kml, name, coords, color):
    
    load_data(filename): return data   
    
    write_kml(filename, ax, bx, cx, tx, ay, by, cy, ty):   
    
##baysian_adjust.py
 Initial attempt at getting a Bayesian prior in and a posterior out for the Ptolemy problem.
 ### function:
    load_image(filename):return io.imread(os.path.join(PTOL_HOME, 'Images', filename))   
    Initial attempt at getting a Bayesian prior in and a posterior out for the Ptolemy problem.   
       
    load_gray_image(filename):return skimage.color.rgb2gray(image)   
    Load an image from the images directory in grayscale.   
        
    save_image(filename, image):
    Save an image to the images directory.   
         
    save_prob_image(p1, filename):    
    Save a probability grid as an image, adjusting so that the point with maximum probability is full white.   

    coord_space(a, b, res): return np.tile(np.linspace(a, b, res), (res, 1))       
    Create a grid of res values from a to b, repeated res times.   
###class   
     ImagePrior(object): image_filename, lat_lim, lon_lim, res 
     
     multivariate_point(self, lat, lon):  return prob.transpose()
      Create a grid approximation representation of the given lat and lon coordinates. This returns a multivariate normal distribution over the grid represented by this state.    
                
    center_mass(self, p1): return plat.sum(), plon.sum()
      Given the lat/lon in p1 as a grid approximation, find the 'center of mass' of the weighted grid to estimate the   
      multivariate mean (letting us extract the adjusted point).    
      This one seems to give less aestetically pleasing results than the map_latlon below.    
        
    grid_to_latlon(self, g):return ((self.lat_lim[0] - (g[0] / self.lat_parts)), ((g[1] / self.lon_parts) + self.lon_lim[0]))
      Convert a screen y/x pair in g, convert back to a lat/lon pair based on the parameters of the grid approximation state.
    

    map_latlon(self, p):return self.grid_to_latlon(np.unravel_index(p.argmax(), p.shape))   
      Compute the MAP (maximum a-posteriori) point (i.e., the point in the grid with the highest probability), and return the lat/lon coordinate pair it represents.
        

    adjust_point(self, lat, lon, ptol_id=None):return self.map_latlon(p2)
      Main driver routine which takes in a predicted lat/lon coordinate pair, and returns it after adjusting by the given prior. If given
      the ptol_id along with the lat/lon pair, then will render images representing the multivariate normal for the point and the posterior
      for debugging purposes. Either map_latlon or center_mass may be specified in the final return statement to adjust the method used
        
    bayesian_adjust(self, p):return pd.Series({'modern_lat': alat, 'modern_lon': alon})
      An adapter routine to make the adjustment method compatible with pandas dataframe apply and merge approach.
      
    different(mlat, mlon, alat, alon, epsilon):return abs(mlat - alat) >= epsilon or abs(mlon - alon) >= epsilon
      A debugging routine to determine whether the given 2 coordinate pairs are different by more than epsilon.
    
    bayesian_adjust_file(prior_filename, data_file, output_base, res):
      Adjust the file given in data file using a Bayesian approach, treating the given prior_filename as an image representing the prior,
      and computing a new modern coordinate pair as the MAP of the posterior resulting, all using grid approximation.
      
##combine.py
  Given the .tab files from Stuckelberger and Grasshoff, some associated metadata and translation files, prepare a training set we can use to 
  prepare a model.
  
##common.py
  Contains the common configuration constants and function definitions for the various place estimation modules we are trying for the Ptolemy
  project.
###functions:
    construct_model(modelname):return getattr(__import__(mname, cname), cname)()
    
    read_places(id_starts_with):return places
      Read places for this script.
      
    read_places_xlsx(filename):return places
      Read a set of places from an Excel spreadsheet, formatted the way we've adopted during this project.
    
    split_places(places): return known, unknown
      Split places into known and unknown places.
      
    report_places(places):
      A debugging function to report lat/lon pairs for each place.
      
    report_simplices(tri, points):
      A debugging function to report the triangulation computed.
      
    write_points(kml, places, name_col, lon_col, lat_col, color):
      Write a series of placemarks into kml from places, using the name, lon and lat columns specified by the corresponding col parameters, and
      using the specified color.
