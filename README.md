# LSD-SLAM: Large-Scale Direct Monocular SLAM

This fork started from [Thomas Whelan's fork](https://github.com/mp3guy/lsd_slam) which "relieves the user of the horrors of a ROS dependency and uses the much nicer lightweight [Pangolin](https://github.com/stevenlovegrove/Pangolin) framework instead."

Here is Jakob's original description:

> LSD-SLAM is a novel approach to real-time monocular SLAM. It is fully direct (i.e. does not use keypoints / features) and creates large-scale,
> semi-dense maps in real-time on a laptop. For more information see
> [http://vision.in.tum.de/lsdslam](http://vision.in.tum.de/lsdslam)
> where you can also find the corresponding publications and Youtube videos, as well as some
> example-input datasets, and the generated output as rosbag or .ply point cloud.

This repo contains my experiments with LSD-SLAM, for performance, functionality
and structure.   As of March 2016, it diverges significantly from either Jakob
or Thomas's branches in structure (I refactored as a way of learning the code),
but not significantly in terms of functionality.   


**master**  is my working / stable-ish branch.   **aaron_dev** is my
**really** unstable branch.   Other branches are for hardware-specific ports
although in the long run I try to merge those functionalities into master
and use CMake to turn hardware-specific elements on and off.

# 1. Quickstart / Minimal Setup

**This build uses CMake ExternalProjects to build a number of non-standard
(non-apt-gettable) dependencies.   CMake will not resolve these dependencies
correctly when building in parallel ('make -j').
On the first build, use just 'make'.   Once the dependencies have been made
(they should be reasonably stable), you can 'make -j' when rebuilding just LSD-SLAM.**

Requires these "standard" dependencies: OpenCV 2.4 (with nonfree if you want FABMAP), [TCLAP](http://tclap.sourceforge.net/), Boost, Eigen.

Requires these "non-standard" dependencies: Pangolin, g2o, [g3log](https://github.com/KjellKod/g3log),
and optionally the [StereoLabs Zed](https://www.stereolabs.com/) SDK and
[Google Snappy](https://github.com/google/snappy) for file compression.
By default, LSD-SLAM It will use CMake ExternalProjects to build each of these
dependencies automatically.
Set the appropriate CMake variable `BUILD_LOCAL_* = OFF` to disable local building.

My targeted environments are Ubuntu 14.04.2, [NVidia Jetpack 2.0](https://developer.nvidia.com/embedded/jetpack) for Jetson TX1, and OS X 10.11 with Homebrew.

# 2. Installation

Install everything from apt repos if you can, otherwise there are githubs for Pangolin and g2o.

## On Jetson TX1

I have not tested this on a clean install, but on the Jetson, from a clean
install of Jetpack 2.1, and with the Zed 0.93 API installed, I needed to:

    apt-get --yes install cmake git libeigen3-dev \
      libboost-filesystem1.55-dev libboost-thread1.55-dev \
      libboost-system1.55-dev libopencv-dev libtclap-dev \
      libglm-dev autoconf

(autoconf is needed by Google Snappy, if enabled)

You then need to manually build [Pangolin](https://github.com/stevenlovegrove/Pangolin) and [g2o](https://github.com/RainerKuemmerle/g2o) using the standard CMake build procedure.  For both I made "Release" and installed in /usr/local.   For g2o I needed to install:

    apt-get --yes install libgomp1 libsuitesparse-dev

Then:

    git clone -b jetson https://github.com/amarburg/lsd_slam.git
    mkdir build_jetson
    cd build_jetson

I then needed to manually specify the path to the Boost libs which seems
strange

    BOOST_LIBRARYDIR=/usr/lib/arm-linux-gnueabihf/  cmake ..


## On Mac

or on the Mac using [Homebrew]()

    brew install eigen boost ...

Then usual cmake building process.


## Common problems

    ../lib/lsd_core/liblsdslam.so: undefined reference to `g2o::csparse_extension::cs_chol_workspace(cs_di_sparse const*, cs_di_symbolic const*, int*, double*)'
    ../lib/lsd_core/liblsdslam.so: undefined reference to `g2o::csparse_extension::cs_cholsolsymb(cs_di_sparse const*, double*, cs_di_symbolic const*, double*, int*)'
    ../lib/lsd_core/liblsdslam.so: undefined reference to `g2o::csparse_extension::writeCs2Octave(char const*, cs_di_sparse const*, bool)'

g2o should be built with the system libcsparse provided by the libsuitesparse-dev package.  Ensure the CMake variable  BUILD_CSPARSE=OFF, and that CSPARSE_INCLUDE_DIR and CSPARSE_LIBRARY point to system libraries, not the libraries included in the g2o source code.

    ../lib/lsd_core/liblsdslam.so: undefined reference to `pangolin::CreateGlutWindowAndBind(std::string, int, int, unsigned int)'

Thomas' Pangolin wrapper assumes Glut has been installed.  I needed to

    cmake -DFORCE_GLUT=ON ..



# 3. Running

Supports directories or sets of raw PNG images. For example, you can down any dataset from [here](http://vision.in.tum.de/lsdslam) in PNG format, and run like;

./LSD --calib datasets/LSD_machine/cameraCalibration.cfg  datasets/LSD_machine/images/

I've started to record my performance results in [Performance.md](Performance.md)

# 4. Related Papers

* **LSD-SLAM: Large-Scale Direct Monocular SLAM**, *J. Engel, T. Schöps, D. Cremers*, ECCV '14

* **Semi-Dense Visual Odometry for a Monocular Camera**, *J. Engel, J. Sturm, D. Cremers*, ICCV '13

# 5. License

LSD-SLAM is licensed under the GNU General Public License Version 3 (GPLv3), see http://www.gnu.org/licenses/gpl.html.
