macro(run_conan)

#     Download the latest version of conan.cmake if not already downloaded
    if (NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
        message(
                STATUS
                "Downloading conan.cmake from https://raw.githubusercontent.com/conan-io/cmake-conan/develop2/conan_provider.cmake")
        file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/develop2/conan_provider.cmake"
                "${CMAKE_BINARY_DIR}/conan.cmake")
    endif ()

    include(${CMAKE_BINARY_DIR}/conan.cmake)
    
    message(STATUS "Manually adding bincrafters remote repository")
    execute_process(COMMAND ${CONAN_PATH} remote add bincrafters https://center.conan.io)
    
    # Set SSL verification explicitly
    message(STATUS "Setting SSL verification to True")
    execute_process(COMMAND ${CONAN_PATH} config set general.ssl_verify=True)

    message(STATUS "Running conan_cmake_run")
    conan_cmake_run(
            # Uncomment if building for M1 Apple
            # ARCH armv8
            CONANFILE ${DEPENDENCY_DIR}/${CONANFILE}
            CONAN_COMMAND ${CONAN_PATH}
            ${CONAN_EXTRA_REQUIRES}
            OPTIONS ${CONAN_EXTRA_OPTIONS}
            BASIC_SETUP NO_OUTPUT_DIRS
            CMAKE_TARGETS # individual targets to link to
            BUILD missing
            PROFILE default
    )
endmacro()
