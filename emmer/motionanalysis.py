import os
import numpy as np
import matplotlib.pyplot as plt

def run_motioncor(filenames, format='tif'):
    """MotionCor Version 1.0 assumed. Gives a txt file per image with stdout as contents."""
    #_ = os.popen("module load motioncor2/1.0") does not work somehow
    for f in filenames:
        if format=='tif':
            _ = os.popen('MotionCor2 -InTiff %s -OutMrc /dev/null > %s'%(f,f[:-4]+'.txt')).read()
            print('File %s processed'%f)
        else:
            _ = os.popen('MotionCor2 -InMrc %s -OutMrc /dev/null > %s'%(f,f[:-4]+'.txt')).read()
            print('File %s processed'%f)
                         
def load_motioncor_trajectories(filenames, pixelsize):
    """Using stdout from Motioncor2 1.0. One textfile per image."""
    trajectories = []
    for filename in filenames:
        data = np.array(open(filename).read().split('\n'))
        n_frames = int(data[np.where(data=='Stack mode: 1')[0][0]-1].split()[4])
        trajectory_start_index = np.where(data=='Full-frame alignment shift')[0][0]
        trajectory = [[i.split()[5],i.split()[6]] for i in data[trajectory_start_index+1:trajectory_start_index+n_frames]]
        trajectory = np.array(trajectory).astype(np.float)
        trajectories.append(trajectory)
    trajectories = np.array(trajectories) * pixelsize
    return trajectories

def load_cryosparc_trajectories(filenames, pixelsize):
    rigid_trajs = []
    for file in filenames:
        content = np.load(file)
        rigid_trajs.append(content[0]-content[0][0])
    rigid_trajs = np.array(rigid_trajs)*pixelsize
    return rigid_trajs
                         
def plot_trajectories_per_angle(angles, trajectories, sorted=False, shift=2, save=False, dpi=150):
    if sorted:
        sort_indices = np.argsort(angles)
        trajectories = trajectories[sort_indices]
        angles = np.sort(angles)
    fig,ax=plt.subplots(figsize=(3.5,7),dpi=dpi)
    for i,(a,t) in enumerate(zip(angles,trajectories)):
        yshift = -i * shift
        plt.scatter(t[0,0], t[0,1]+yshift, color='k', s=1)
        plt.plot(*(t+[0,yshift]).T, linewidth=0.5, color='k')
        plt.text(t[0,0]+7, t[0,1]+yshift, "%.0f°"%a, fontsize=6, color='red')
    plt.gca().set_aspect(1)
    plt.xlabel('Shift [Å]'); plt.ylabel('Shift [Å]')
    if save!=False:
        plt.savefig(save)
    return fig,ax

def plot_trajectories_hairball(trajectories, ax=None, xylim = 70, dpi=150):
    if ax is None:
        fig,ax = plt.subplots(figsize=(3.5,5.5), dpi=dpi)
    for traj in trajectories:
        ax.plot(*traj.T, alpha=0.2, color='k', linewidth=0.5)
    ax.set_xlabel('x [Angstrom]'); ax.set_ylabel('y [Angstrom]')
    ax.grid(color='k', ls = '-.', lw = 0.25)
    ax.set_aspect('equal'); ax.set_xlim(-xylim, xylim); ax.set_ylim(-xylim, xylim); 
    return ax
                         
def plot_trajectories_rmsd(trajectories):
    """Uses trajectories """
    pass
                        