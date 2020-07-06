"""
Created at 10:41 on 22.06.20
@course dozent: Ardit Sulce.
@author: lingsun
"""

from ftplib import FTP, error_perm
import os
import glob
import pandas
import numpy
import patoolib
from matplotlib import pyplot as plt
import simplekml
#import datetime

#print(datetime.datetime.now())

def ftpDownloader(stationId,startYear,endYear,url="ftp.pyclass.com",user="student@pyclass.com",passwd="student123"):
    ftp=FTP(url)
    ftp.login(user,passwd)
    if not os.path.exists("ftpFiles"):
        os.makedirs("ftpFiles")
    os.chdir("ftpFiles")
    for year in range(startYear,endYear+1):
        fullpath='/Data/%s/%s-%s.gz' % (year,stationId,year)
        filename=os.path.basename(fullpath)
        try:
            with open(filename,"wb") as file:
                ftp.retrbinary('RETR %s' % fullpath, file.write)
            print("%s succesfully downloaded" % filename)
        except error_perm:
            print("%s is not available" % filename)
            os.remove(filename)
    ftp.close()

def extractFiles(indir="ftp_files", out="ftp_files/extracted"):
    #os.chdir("./Data_Processing_with_Python")
    os.chdir("./data_files")
    if not os.path.exists(out):
        os.makedirs(out)
    os.getcwd()
    os.chdir(indir)
    archive = glob.glob("*.gz")
    files = os.listdir("extracted")
    for arch in archive:
        if arch[:-3] not in files:
            patoolib.extract_archive(arch, outdir=out)
    os.chdir("..")
    os.chdir("..")

def addField(indir="add_field_files"):
    os.chdir("./Data_Processing_with_Python")
    if not os.path.exists(indir):
        os.makedirs(indir)
    os.getcwd()
    os.chdir(indir)
    fileList = glob.glob("*")
    for filename in fileList:
        df = pandas.read_csv(filename, sep='\s+', header=None)
        df["Station"] = [filename.rsplit("-", 1)[0]] * df.shape[0]
        df.to_csv(filename + ".csv", index=None, header=None)
    os.chdir("..")

def concatenate(indir="./concatenate_multiple_csvfiles",outfile="./concanated.csv"):
    os.chdir(indir)
    fileList = glob.glob("*.csv")
    dfList=[]
    columns = ["Year","Month","Day","Hour","Temp","DewTemp","Pressure",\
                "WindDir","WindSpeed","Sky","Precip1","Precip6","ID"]
    for filename in fileList:
        print(filename)
        df=pandas.read_csv(filename,header=None)
        dfList.append(df)
    concatDf=pandas.concat(dfList,axis=0)
    concatDf.columns=columns
    concatDf.to_csv(outfile,index=None)
    os.chdir("..")

def merge(left="./Concatenated.csv",right="./station-info.txt",output="./Concatenated-Merged.csv"):
    leftDf=pandas.read_csv(left)
    rightDf=pandas.read_fwf(right,converters={"USAF":str,"WBAN":str})
    rightDf["USAF_WBAN"]=rightDf["USAF"]+"-"+rightDf["WBAN"]
    print(rightDf.columns)
    mergedDf=pandas.merge(leftDf,rightDf.loc[:,["USAF_WBAN","STATION NAME","LAT","LON"]],left_on="ID",right_on="USAF_WBAN")
    mergedDf.to_csv(output)

# concatDf = pandas.read_csv("./IncomeByStateByYear.csv")
# nodupl = concatDf.T.drop_duplicates().T
# nodupl.to_csv("./IncomeByStateByYearNoDupl.csv",index=0)

def pivot(infile="./Concatenated-Merged.csv",outfile="./Pivoted.csv"):
    df=pandas.read_csv(infile)
    df=df.replace(-9999,numpy.nan)
    df['Temp']=df["Temp"]/10.0
    table=pandas.pivot_table(df,index=["ID","LAT","LON","STATION NAME"],columns="Year",values="Temp")
    table.to_csv(outfile)
    return table

def plot(outfigure="./Ploted.png"):
    df=pivot()
    df.T.plot(subplots=True,kind='bar')
    plt.savefig(outfigure,dpi=200)

# def kml(input="./Pivoted.csv",out="./Weather.kml"):
#     kml=simplekml.Kml()
#     df=pandas.read_csv(input,index_col=["ID","LON","LAT","STATION NAME"])
# 	for lon,lat,name in zip(df.index.get_level_values("LON"),df.index.get_level_values("LAT"),df.index.get_level_values("STATION NAME")):
# 		kml.newpoint(name=name,coords=[(lon,lat)])
# 		kml.save(out)


def kml(input="./Pivoted.csv",out="./Weather.kml"):
    kml=simplekml.Kml()
    df=pandas.read_csv(input,index_col=["ID","LON","LAT","STATION NAME"])
    for lon,lat,name in zip(df.index.get_level_values("LON"),df.index.get_level_values("LAT"),df.index.get_level_values("STATION NAME")):
        kml.newpoint(name=name,coords=[(lon,lat)])
        kml.save(out)

def milesToKm(miles):
    km=miles*1.60934
    print(km, "km")

# m=input("Please enter miles: ")
# m=float(m)
# milesToKm(m)

if __name__=="__main__":
    stationsIdString=input("Enter station names divided by commans: ")
    startingYear=int(input("Enter the starting yera of the data: "))
    endingYear=int(input("Enter the ending year of the data: "))
    stationIdList=stationsIdString.split(',')

    for station in stationIdList:
        ftpDownloader(station,startingYear,endingYear)

    extractFiles()
    addField()
    os.chdir("./Data_Processing_with_Python/LS_util")
    concatenate()
    merge()
    pivot()
    kml()
    plot()

