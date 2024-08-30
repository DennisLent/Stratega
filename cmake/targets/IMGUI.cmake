set(IMGUI_SOURCE_FILES
        imgui-SFML.cpp
)

list(TRANSFORM IMGUI_SOURCE_FILES PREPEND "${imgui-sfml_SOURCE_DIR}/")

add_library(IMGUII STATIC ${IMGUI_SOURCE_FILES})
target_include_directories(IMGUII PUBLIC ${imgui-sfml_SOURCE_DIR})

target_link_libraries(IMGUII
        PRIVATE
        imgui::imgui

        PRIVATE
        OpenGL::GL

        sfml-system
        sfml-graphics
        sfml-window      
)