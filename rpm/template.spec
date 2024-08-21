%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-mola-lidar-odometry
Version:        0.3.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS mola_lidar_odometry package

License:        GPLv3
URL:            https://docs.mola-slam.org/
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-iron-mola-common
Requires:       ros-iron-mola-input-kitti-dataset
Requires:       ros-iron-mola-input-kitti360-dataset
Requires:       ros-iron-mola-input-mulran-dataset
Requires:       ros-iron-mola-input-paris-luco-dataset
Requires:       ros-iron-mola-input-rawlog
Requires:       ros-iron-mola-input-rosbag2
Requires:       ros-iron-mola-kernel
Requires:       ros-iron-mola-launcher
Requires:       ros-iron-mola-navstate-fuse
Requires:       ros-iron-mola-pose-list
Requires:       ros-iron-mola-viz
Requires:       ros-iron-mp2p-icp
Requires:       ros-iron-mrpt2
Requires:       ros-iron-ros-workspace
BuildRequires:  cmake3
BuildRequires:  ros-iron-ament-cmake
BuildRequires:  ros-iron-ament-cmake-gtest
BuildRequires:  ros-iron-ament-cmake-xmllint
BuildRequires:  ros-iron-mola-common
BuildRequires:  ros-iron-mola-input-kitti-dataset
BuildRequires:  ros-iron-mola-input-kitti360-dataset
BuildRequires:  ros-iron-mola-input-mulran-dataset
BuildRequires:  ros-iron-mola-input-paris-luco-dataset
BuildRequires:  ros-iron-mola-input-rawlog
BuildRequires:  ros-iron-mola-input-rosbag2
BuildRequires:  ros-iron-mola-kernel
BuildRequires:  ros-iron-mola-navstate-fuse
BuildRequires:  ros-iron-mola-pose-list
BuildRequires:  ros-iron-mp2p-icp
BuildRequires:  ros-iron-mrpt2
BuildRequires:  ros-iron-ros-environment
BuildRequires:  ros-iron-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-iron-ament-lint-auto
BuildRequires:  ros-iron-ament-lint-cmake
BuildRequires:  ros-iron-mola-metric-maps
BuildRequires:  ros-iron-mola-test-datasets
BuildRequires:  ros-iron-rosbag2-storage-mcap
%endif

%description
LIDAR odometry system based on MOLA and MRPT components

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Thu Aug 22 2024 Jose-Luis Blanco-Claraco <joseluisblancoc@gmail.com> - 0.3.1-1
- Autogenerated by Bloom

* Wed Aug 14 2024 Jose-Luis Blanco-Claraco <joseluisblancoc@gmail.com> - 0.3.0-1
- Autogenerated by Bloom

