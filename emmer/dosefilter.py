import numpy as np
import mrcfile
import sys

def calculate_frequency_map_2D_real(map):
    per_axis_freq = [np.fft.fftfreq(N) for N in map.shape[:-1]]
    per_axis_freq.append(np.fft.rfftfreq(map.shape[-1]))
    i,j = np.meshgrid(*per_axis_freq, indexing='ij', sparse=True)
    return np.sqrt(i**2+j**2)

def critical_exposure(spatial_frequency):
    return 0.245*spatial_frequency**(-1.665)+2.81 #Grant,Grigorieff 2015

def dose_weighting(accumulated_dose, spatial_frequency, pixelsize):
    spatial_frequency_1overAngstrom = spatial_frequency / pixelsize
    return np.exp(-accumulated_dose/(2*critical_exposure(spatial_frequency_1overAngstrom)))

def doseweight_image(img):
    img_fft          = np.fft.rfft2(img)
    img_freq         = calculate_frequency_map_2D_real(img)
    img_exp_filter   = dose_weighting(np.float(sys.argv[3]), img_freq, np.float(sys.argv[4]))
    img_fft_filtered = img_fft * img_exp_filter
    img_filtered     = np.fft.irfft2(img_fft_filtered)
    return img_filtered
 

if __name__ == "__main__":
    if len(sys.argv)<5:
        print("Usage: python dosefilter.py input.mrc output.mrc accumulated_dose apix")
        sys.exit()

    with mrcfile.open(sys.argv[1], permissive=True) as mrc:
        img = mrc.data
        
    img_doseweighted = doseweight_image(img)

    with mrcfile.new(sys.argv[2]) as mrc:
        mrc.set_data(img_doseweighted.astype(np.float32))

