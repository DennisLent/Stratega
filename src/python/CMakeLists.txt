set(BINDING_SOURCE_FILES
    actions.cpp
    basic_structures.cpp
    buff.cpp
    default_methods.cpp
    entity.cpp
    forwardmodel.cpp
    game.cpp
    gamestate.cpp
    heuristic.cpp
    misc.cpp
    parameter.cpp
    player.cpp
    technology.cpp
    tile.cpp
    vector2.cpp
    binding.cpp
)

list(TRANSFORM BINDING_SOURCE_FILES PREPEND "${SUBPROJ_PYBINDING_SRC_DIR}/")
#find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
# find_package(Python COMPONENTS Interpreter Development.Module)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
#set(PYBIND11_FINDPYTHON TRUE)
if(DEFINED ${pybind11_SEARCH_PATH})
    find_package(pybind11 CONFIG PATHS ${pybind11_SEARCH_PATH} REQUIRED)
else()
    find_package(pybind11 REQUIRED)
endif()

pybind11_add_module(stratega ${BINDING_SOURCE_FILES})
message("\nAdding pybind11 module.\n")
target_link_libraries(stratega PUBLIC Stratega)
set_target_properties(stratega PROPERTIES
    #LIBRARY_OUTPUT_DIRECTORY  ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
    RUNTIME_OUTPUT_DIRECTORY  ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/python
    ARCHIVE_OUTPUT_DIRECTORY  ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
    EXECUTABLE_OUTPUT_DIRECTORY  ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python

    #LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
    RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/python
    ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
    EXECUTABLE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
    
    #LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
    RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/python
    ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
    EXECUTABLE_OUTPUT_DIRECTORY_DEBUG ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/python
)