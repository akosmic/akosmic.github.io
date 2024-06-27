import pandas as pd


# DATA FORMAT: ra, dec, radius
aprg = pd.read_csv('C:/Users/akash/Downloads/APRG_All-part1/coords.csv')

for i in range(20):

    ra, dec = aprg['ra'][i], aprg['dec'][i]
    ra, dec = round(Decimal(ra),6), round(Decimal(dec),6) # due to filename
    radec = "%f" % (aprg['ra'][i])+"%+f" % (aprg['dec'][i]) #due to filename
    print(i/aprg.shape[0])
    ds9 = subprocess.Popen('C:\SAOImageDS9\ds9.exe \
                          -rgb -fits \
                          C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_spitzer_seipirac4(2.4)_reproj.fits -scale ZScale \
                          -rgb channel green -fits \
                          C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_spitzer_seipirac2(2.4)_reproj.fits -scale ZScale \
                          -rgb channel blue -fits \
                         C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_spitzer_seipirac1(2.4)_reproj.fits \
                          -scale ZScale -zoom to fit -colorbar no \
                          -export C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE/'+radec+'_glimpse.jpeg 100')
    time.sleep(5.0)
    ds9.terminate()
    #export vs print
    ds9 = subprocess.Popen('C:\SAOImageDS9\ds9.exe \
                          -rgb -fits \
                          C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_wise_4_reproj.fits -scale ZScale \
                          -rgb channel green -fits \
                          C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_wise_2_reproj.fits -scale ZScale \
                          -rgb channel blue -fits \
                         C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_wise_1_reproj.fits \
                          -scale ZScale -zoom to fit -colorbar no \
                          -export C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/WISE/'+radec+'_wise.jpeg 100')
    time.sleep(5.0)
    ds9.terminate()

    ds9 = subprocess.Popen('C:\SAOImageDS9\ds9.exe \
                          -rgb -fits \
                          C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_2mass_k_reproj.fits -scale ZScale \
                          -rgb channel green -fits \
                          C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_2mass_h_reproj.fits -scale ZScale \
                          -rgb channel blue -fits \
                         C:/Users/akash/Downloads/APRG_All-part1/'+radec+'/fc_'+radec+'_2mass_j_reproj.fits \
                          -scale ZScale -zoom to fit -colorbar no \
                          -export C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/2MASS/'+radec+'_2mass.jpeg 100')
    time.sleep(5.0)
    ds9.terminate()


################### 
#GLIMPSE data plot#
###################

fig, ax = plt.subplots(4,5, figsize=(25,20))
for i in range(aprg.shape[0]):
    size=150/3600
    ra, dec = aprg['ra'][i], aprg['dec'][i]
    ra, dec = round(Decimal(ra),6), round(Decimal(dec),6)
    radec = "%f" % (aprg['ra'][i])+"%+f" % (aprg['dec'][i])
    gc = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='fk5', unit='deg')
    l, b = gc.galactic.l.value, gc.galactic.b.value
    
    img = Image.open('C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE/'+radec+'_glimpse.jpeg')
    j=i+1
    if i<5:
        ax[0,i].imshow(img, extent=(l-size*0.5,l+size*0.5, b-0.5*size,b+0.5*size))
        ax[0,i].set_title('APRG %d' % j+' (%0.4f' % l+', %0.4f)' %b, fontsize=15)
    elif 5<=i<10:
        ax[1,i-5].imshow(img, extent=(l-size*0.5,l+size*0.5, b-0.5*size,b+0.5*size))
        ax[1,i-5].set_title('APRG %d' % j+' (%0.4f' % l+', %0.4f)' %b, fontsize=15)
    elif 10<=i<15:
        ax[2,i-10].imshow(img, extent=(l-size*0.5,l+size*0.5, b-0.5*size,b+0.5*size))
        ax[2,i-10].set_title('APRG %d' % j+' (%0.4f' % l+', %0.4f)' %b, fontsize=15)
    elif 15<=i<20:
        ax[3,i-15].imshow(img, extent=(l-size*0.5,l+size*0.5, b-0.5*size,b+0.5*size))
        ax[3,i-15].set_title('APRG %d' % j+' (%0.4f' % l+', %0.4f)' %b, fontsize=15)
    elif 20<=i<25:
        ax[4,i-20].imshow(img, extent=(l-size*0.5,l+size*0.5, b-0.5*size,b+0.5*size))
        ax[4,i-20].set_title('APRG %d' % j+' (%0.4f' % l+', %0.4f)' %b, fontsize=15)
plt.tight_layout()
plt.savefig("C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE_APRG.pdf")