# stolen from: http://gis.stackexchange.com/questions/103668/using-union-on-multiple-shapefiles-to-output-single-result
# works for any binary processing algorithm in the form of:
# processing.runalg("algorithm_name", file1, file2, outputfile)
# now works on Shapefiles (because of hardcoding the extensions)
# paste this script into the QGIS Python console to import all modules (scope problem with python on mac)
import os
import tempfile
import shutil
import processing
import glob

def delete_shape(shape_file):
    shape_file_no_ext=os.path.splitext(shape_file)[0]
    ext_list=('shx','dbf','qpj','prj','shp','cpg')
    for extension in ext_list:
        try:
            os.remove(shape_file_no_ext+'.'+extension)
            print "Deleted following file: ",shape_file
        except:
            print "could not delete following file: ",shape_file
            pass

def copy_shape(shape_file,destination_shape_file):
    delete_shape(destination_shape_file)
    shape_file_no_ext=os.path.splitext(shape_file)[0]
    destination_shape_file_no_ext=os.path.splitext(destination_shape_file)[0]
    ext_list=('shx','dbf','qpj','prj','shp','cpg')
    for extension in ext_list:
        try:
            shutil.copyfile(shape_file_no_ext+'.'+extension ,destination_shape_file_no_ext+'.'+extension)
            print "copied following file:" ,shape_file_no_ext, destination_shape_file_no_ext
        except:
            print "Did NOT copied following file:" ,shape_file_no_ext, destination_shape_file_no_ext
            pass

def wrapped_alg(algorithm_name,file_name_list, output_file):
    #Copy files to temp directory
    temp_file_list=[]
    for src_file in file_name_list:
        dst_file=os.path.join(tempfile.gettempdir(),os.path.basename(src_file))
        copy_shape(src_file,dst_file)
        temp_file_list.append(dst_file)
        print "Tempfile list is: \n",temp_file_list

    #binary process on files in temp directory
    while len(temp_file_list)>1:
        temp_file=os.path.join(tempfile.gettempdir(),'multi_merge_temp_file.shp')
        ultimate_file=temp_file_list.pop()
        print ultimate_file,len(temp_file_list)
        penultimate_file=temp_file_list.pop()
        processing.runalg(algorithm_name, ultimate_file, penultimate_file, temp_file)
        delete_shape(penultimate_file)
        copy_shape(temp_file,penultimate_file)
        delete_shape(temp_file)
        delete_shape(ultimate_file)
        temp_file_list.append(penultimate_file)

    #copy over final file
    copy_shape(temp_file_list.pop(),output_file)

dir_to_process="/Users/Valentin/Desktop/TEST/"
output_file="/Users/Valentin/Desktop/output/output1.shp"
file_name_list = [shp for shp in glob.glob(dir_to_process + "*.shp")]
#alg_name="qgis:mergevectorlayers"
alg_name="qgis:union"
wrapped_alg(alg_name,file_name_list, output_file)
