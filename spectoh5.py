import numpy as np
import pandas as pd
from astropy.io import fits
import glob
import time

namelist = []
specdata = []
specdata2 = []
epicnum = []
epicnum2 = []
obj = []
obj2 = []

specerr = []
wav = []
speclamb = np.linspace(5101.13,5101.13+(2.93*1571), 1571)
specerr2 = []
speclamb2 = np.linspace(3301.06,3301.06+(2.38*778), 778)
wav2 = []
headers = []
images = []
images2 = []
headers2 = []

#for SNIFS
for name in glob.glob('spec_C*.fits'):
    namelist.append(name)

    
namelist = sorted(namelist)    
print(len(namelist))
    
for i in range(len(namelist)):
    hdulist = fits.open(namelist[i], memmap=False)
    try:
        errlist = fits.open('var_'+namelist[i], memmap=False)
    except:
        print('no error file')
        errlist = fits.open('var_spec_C18_090_033_003_17_B.fits', memmap=False)
        errlist[0].data = errlist[0].data * np.zeros_like(errlist[0].data)
    try:
        imalist = fits.open('ima_T'+namelist[i][5:], memmap=False)
    except:
        print('no image file')
        imalist = fits.open('ima_TC18_090_033_003_17_B.fits', memmap=False)
        imalist[0].data = imalist[0].data * np.zeros_like(imalist[0].data)
        #print(imalist[0].data)
    if namelist[i][-6] == 'R':
        specdata.append(hdulist[0].data)
        try:
            specerr.append(np.sqrt(errlist[0].data))
        except:
            print('huh',errlist[0].data)
        wav.append(speclamb)
        epicnum.append(float(hdulist[0].header['JD'])) #now JD, not epicnum
        obj.append(hdulist[0].header['object'])
        headers.append(hdulist[0].header)
        #print(imalist[0].data)
        images.append(imalist[0].data)
        #print(namelist[i])
    elif namelist[i][-6] == 'B':
        specdata2.append(hdulist[0].data)
        try:
            specerr2.append(np.sqrt(errlist[0].data))
        except:
            print('huh',errlist[0].data)
        wav2.append(speclamb2)
        #print(namelist[i])
        epicnum2.append(float(hdulist[0].header['JD']))
        obj2.append(hdulist[0].header['object'])
        headers2.append(hdulist[0].header)
        images2.append(imalist[0].data)
    #print(hdulist[0].header['object'])
    hdulist.close()
    errlist.close()
    imalist.close()
    del hdulist
    del errlist
    del imalist


print(len(specdata), len(specdata2), len(epicnum))
print(epicnum, epicnum2)

d1 = pd.DataFrame(data=[obj2,headers2,images2,wav2,specdata2,specerr2,epicnum2]).T
d1.columns = ['object', 'header','SNIFS_BIMAGE','SNIFS_BWAV','SNIFS_BFLUX','SNIFS_BERROR','obstime']
d2 = pd.DataFrame(data=[obj,headers,images,wav,specdata,specerr,epicnum]).T
d2.columns = ['object', 'header','SNIFS_RIMAGE','SNIFS_RWAV','SNIFS_RFLUX','SNIFS_RERROR', 'obstime']
d = pd.merge(d1,d2, on=['obstime'])#, how='inner')
d = d.drop(['object_x', 'object_y', 'obstime', 'header_y'], axis=1)

print(d.iloc[0])
#print(d1['#'], d2['#'], d['#'])
print(len(d1),len(d2),len(d))
#print(d1['header']['DATE-OBS'])

for i in range(len(epicnum2)):
    for j in range(len(epicnum)):
        if abs(float(epicnum2[i])-float(epicnum[j])) < 0.005:
            #print(float(epicnum2[i]),float(epicnum[j]))
            epicnum2[i] == epicnum[j]

d3 = d1.copy()
#d3.index = [float(i) for i in epicnum2]
d4 = d2.copy()
#d4.index = [float(i) for i in epicnum]
d5 = pd.merge(d3,d4, on=['obstime'])#left_index=True, right_index=True)
d5 = d5.drop(['object_x', 'object_y', 'obstime', 'header_y'], axis=1)

#print(d3.index,d4.index)
#print(len(d3),len(d4),len(d5))
print(d5.columns)
#print([d5['header_x'][i]['object'] for i in d5.index])

#indexed = d5.set_index('obstime')

#print(indexed.loc['HD188875'])
#print(indexed.loc['HD188875']['SNIFS_BIMAGE'])

#d.columns = ['bwav','b','berr','rwav','r','rerr','#']
df = d5.drop(d[pd.isnull(d['SNIFS_BFLUX'])].index) #remove extra entries without spectral data
#df = d5

#change epicunms
#s2 = pd.Series([df['#'][i][4:] for i in range(len(df))])
#df['#'] = s2
#print(s2)
#print(d)

print([df['header_x'][i]['object'] for i in df.index])


#remove stds
#s = pd.Series([df['#'].values[i][0]=='E' for i in range(len(df))])
s = pd.Series([df['header_x'][i]['object'] =='BD+174708' \
               or df['header_x'][i]['object'] =='BD+254655' \
               or df['header_x'][i]['object'] =='BD+284211' \
               or df['header_x'][i]['object'] =='BD+332642' \
               or df['header_x'][i]['object'] =='BD+75325' \
               or df['header_x'][i]['object'] =='CD-32d9927' \
               or df['header_x'][i]['object'] =='EG131' \
               or df['header_x'][i]['object'] =='Feige110' \
               or df['header_x'][i]['object'] =='Feige34' \
               or df['header_x'][i]['object'] =='Feige56' \
               or df['header_x'][i]['object'] =='Feige66' \
               or df['header_x'][i]['object'] =='Feige67' \
               or df['header_x'][i]['object'] =='G191B2B' \
               or df['header_x'][i]['object'] =='GD153' \
               or df['header_x'][i]['object'] =='GD71' \
               or df['header_x'][i]['object'] =='HD93521' \
               or df['header_x'][i]['object'] =='HR1544' \
               or df['header_x'][i]['object'] =='HR3454' \
               or df['header_x'][i]['object'] =='HR4468' \
               or df['header_x'][i]['object'] =='HR4963' \
               or df['header_x'][i]['object'] =='HR5501' \
               or df['header_x'][i]['object'] =='HR718' \
               or df['header_x'][i]['object'] =='HR7596' \
               or df['header_x'][i]['object'] =='HR7950' \
               or df['header_x'][i]['object'] =='HR8634' \
               or df['header_x'][i]['object'] =='HR9087' \
               or df['header_x'][i]['object'] =='HZ21' \
               or df['header_x'][i]['object'] =='HZ44' \
               or df['header_x'][i]['object'] =='LTT1020' \
               or df['header_x'][i]['object'] =='LTT1788' \
               or df['header_x'][i]['object'] =='LTT2415' \
               or df['header_x'][i]['object'] =='LTT377' \
               or df['header_x'][i]['object'] =='LTT3864' \
               or df['header_x'][i]['object'] =='LTT6248' \
               or df['header_x'][i]['object'] =='LTT9239' \
               or df['header_x'][i]['object'] =='LTT9491' \
               or df['header_x'][i]['object'] =='NGC7293' \
               or df['header_x'][i]['object'] =='P041C' \
               or df['header_x'][i]['object'] =='P177D' \
               for i in df.index])

df.columns = ['header','SNIFS_BIMAGE','SNIFS_BWAV','SNIFS_BFLUX','SNIFS_BERROR', 'SNIFS_RIMAGE','SNIFS_RWAV','SNIFS_RFLUX','SNIFS_RERROR']

#df = df[s.values]
stds = df[s.values] #save stds if needed
stds = stds.reset_index()
print('len(stds):', len(stds))

df.to_hdf('SNIFS_all_072418.h5', 'table')
stds.to_hdf('SNIFS_stds_072418.h5', 'table')

## ## For SpeX

## epicnum = []
## namelist = []
## specdata = []
## wav = []
## err = []

## for name in glob.glob('*_merge.fits'):
##     namelist.append(name)

## for i in range(len(namelist)):
##     hdulist = fits.open(namelist[i])
##     wav.append(hdulist[0].data[0])
##     specdata.append(hdulist[0].data[1])
##     err.append(hdulist[0].data[2])
##     epicnum.append(hdulist[0].header['object'])

## d = pd.DataFrame(data=[wav,specdata,err,epicnum]).T
## d.columns = ['wav','flux', 'err','#']

## d.to_hdf('072017_SpeX.h5', 'table')



## #To merge and save as 1 star, all spectra file:

## spex = pd.read_hdf('*_SpeX.h5', 'table')
## snifs = pd.read_hdf('*_SNIFS.h5', 'table')

## merged = pd.merge(spex,snifs, on='#')

## merged.to_hdf('hd175884.h5', 'table')
