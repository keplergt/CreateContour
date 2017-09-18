# -*- coding: cp936 -*-

#第一步 提取 excel 生成 点shp
#第二步 点shp 插值为 点栅格
#第三步 点栅格 提取等值线


import linecache
import os,sys
import arcpy
from arcpy import env
from arcpy import *
from arcpy.sa import *
import shutil  
import traceback

def CreateContour(csvFile):

    #第一步 提取 excel 生成 点shp
    # Description: Creates an XY layer and exports it to a layer file
    # import system modules

    # Set the local variables
    
    if not os.path.exists(csvFile):
        raise Exception(csvFile+"不存在！")
    filename=GetFileNameAndExt(csvFile)

    x_coords = "x"
    y_coords = "y"
    z_coords = ""
    
    out_Layer= filename
    
    # Set the spatial reference
    spRef = r""

    # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(csvFile, x_coords, y_coords, out_Layer, spRef, z_coords)

    # Print the total rows
##    print arcpy.GetCount_management(out_Layer)

    # Save to a layer file
    #arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)

    # Execute FeatureClassToGeodatabase
    #arcpy.FeatureClassToShapefile_conversion(out_Layer, tempPath)

    print "已完成#第一步 提取 excel 生成 点shp"

    #第二步 点shp 插值为 点栅格
    
    # Set local variables
    
    inFeatures = out_Layer
    field = "eta"
    cellSize = ""
    outVarRaster = tempPath+ r'\\' + filename+ r"_Kriging.tif"

    if  os.path.exists(outVarRaster):
        os.remove(outVarRaster)

    desc = arcpy.Describe(out_Layer)
    if(desc.extent.height >= desc.extent.width):
        cellsize = desc.extent.width/250 
    else:
        cellsize = desc.extent.height/250 

    lagSize = cellsize
    majorRange = None
    partialSill = None
    nugget = None

    kModelOrdinary = KrigingModelOrdinary("CIRCULAR",lagSize,
                                          majorRange,partialSill,nugget)
    kRadius = RadiusFixed(5*cellsize,0)
    
    arcpy.CheckOutExtension("Spatial")

    # Execute Kriging
    outKriging = Kriging(inFeatures, field, kModelOrdinary, cellSize,
                         kRadius, None)

    # Save the output 
    outKriging.save(outVarRaster)
    
    print "已完成#第二步 点shp 插值为 点栅格"

    # Set local variables
    
    inRaster = outVarRaster
    contourInterval = 3
    baseContour = 0
    
    #outContours =r"C:\Users\demo\Desktop\1\temp\fsd_C.shp"
    outContours =resuPath+ r'\\' + filename+ r"_Contour.shp"
    
    if  os.path.exists(outContours):
        os.remove(outContours)
        
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute Contour
    outContour =Contour(inRaster, outContours, contourInterval, baseContour)

    print "已完成#第三步 点栅格 提取等值线"
    return
   
def GetFileNameAndExt(filename2):  
    (filepath,tempfilename) = os.path.split(filename2);  
    (shotname,extension) = os.path.splitext(tempfilename);  
    return shotname

def Rmtree(tempPath1):
    if not os.path.exists(tempPath1):
       os.makedirs(tempPath1)
       
    shutil.rmtree(tempPath1)  
    os.makedirs(tempPath1)
    return


# 获取当前文件夹 设置为工作空间
csvpath= sys.path[0]+r"\data"
tempPath=sys.path[0]+r"\temp"
resuPath=sys.path[0]+r"\result"


if __name__ == "__main__":
    try:
        if not os.path.exists(tempPath):
           os.makedirs(tempPath)
        if not os.path.exists(resuPath):
           os.makedirs(resuPath)

        Rmtree(tempPath)

        print "                                  "
        print "                                  "
        print "                                  "
        print "                                  "
        print "****** 数据csv目录" + csvpath 
        print "****** 数据临时目录" + tempPath
        print "****** 数据结果目录" + resuPath
        filecount=0
        
        for filename in os.listdir(csvpath): 
            if os.path.splitext(filename)[1] == '.csv':
                in_Table =csvpath+r"\\"+filename

                print "                                  "
                print "                                  "
                print "******" + in_Table
                print "**********************************"
                
    ##            Rmtree(tempPath)
    ##            print in_Table
                
                CreateContour(in_Table)
    ##            CreateContour(in_Table)
    ##            filecount=filecount+1

    ##    in_Table =csvpath+r"\point.csv"
    ##    CreateContour(in_Table)

    ##    print "共处理+"+filecount+"个文件！"
        print "ok!"
        
    except arcpy.ExecuteError:
        ##    print arcpy.GetMessages()
        print arcpy.GetMessages()
    except arcpy.ExecuteWarning:
        ##    print arcpy.GetMessages()
        print arcpy.GetMessages()
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        print 'traceback.print_exc():'; traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()







    
    
