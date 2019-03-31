cmake_minimum_required(VERSION 3.6)
project(IndoorMapEditor)

set(CMAKE_CXX_STANDARD 11)
# Tell CMake to run moc when necessary:
set(CMAKE_AUTOMOC ON)
# As moc files are generated in the binary dir, tell CMake
# to always look for includes there:
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Create code from a list of Qt designer ui files
set(CMAKE_AUTOUIC ON)
# qrc resource files
set(CMAKE_AUTORCC ON)

#find_package(Qt5Widgets CONFIG REQUIRED)
#find_package(Qt5Core CONFIG REQUIRED)
#find_package(Qt5Gui CONFIG REQUIRED)
#find_package(Qt5PrintSupport CONFIG REQUIRED)

find_package(Qt5 REQUIRED
    Core
    PrintSupport
    Gui
    Widgets)

set(PROJECT_SOURCE_DIR src)
file(GLOB_RECURSE SOURCE_FILES
        "${PROJECT_SOURCE_DIR}/*.cpp"
        "${PROJECT_SOURCE_DIR}/*.h"
        "${PROJECT_SOURCE_DIR}/*.qrc"
        "${PROJECT_SOURCE_DIR}/*.ui")

set(QT_LIBRARIES
        Qt5::Widgets
        Qt5::Core
        Qt5::Gui
        Qt5::PrintSupport)

add_executable(IndoorMapEditor ${SOURCE_FILES})
target_link_libraries(IndoorMapEditor ${QT_LIBRARIES})
