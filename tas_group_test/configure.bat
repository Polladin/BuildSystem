
mkdir build
cd build

cmake .. -G "Visual Studio 14 2015 Win64" -DWITH_SOURCES=common;common_lib

cd ..