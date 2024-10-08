set(ARENA_SOURCE_FILES
        main.cpp
        )

list(TRANSFORM ARENA_SOURCE_FILES PREPEND "${SUBPROJ_ARENA_SRC_DIR}/")

add_executable (arena ${ARENA_SOURCE_FILES})
target_link_libraries(arena PUBLIC Stratega)

set_target_properties(arena PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY  ${CMAKE_CURRENT_BINARY_DIR}/lib
        RUNTIME_OUTPUT_DIRECTORY  ${CMAKE_CURRENT_BINARY_DIR}/bin
        ARCHIVE_OUTPUT_DIRECTORY  ${CMAKE_CURRENT_BINARY_DIR}/lib
        EXECUTABLE_OUTPUT_DIRECTORY  ${CMAKE_CURRENT_BINARY_DIR}/bin

        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${LIBRARY_OUTPUT_DIRECTORY}
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${RUNTIME_OUTPUT_DIRECTORY}
        ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${ARCHIVE_OUTPUT_DIRECTORY}
        EXECUTABLE_OUTPUT_DIRECTORY_RELEASE ${EXECUTABLE_OUTPUT_DIRECTORY}
        
        LIBRARY_OUTPUT_DIRECTORY_DEBUG ${LIBRARY_OUTPUT_DIRECTORY}
        RUNTIME_OUTPUT_DIRECTORY_DEBUG ${RUNTIME_OUTPUT_DIRECTORY}
        ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${ARCHIVE_OUTPUT_DIRECTORY}
        EXECUTABLE_OUTPUT_DIRECTORY_DEBUG ${EXECUTABLE_OUTPUT_DIRECTORY}
)