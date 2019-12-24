# cozy - 4k executable gfx entry by NR4/Team210, shown at Under Construction 2k19
# Copyright (C) 2019 Alexander Kraus <nr4@z10.info>
# Copyright (C) 2019 DaDummy <c.anselm@paindevs.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

cmake_minimum_required(VERSION 3.12)

project(cozy)

find_package(OpenGL REQUIRED COMPONENTS OpenGL)

if(WIN32)
    find_program(MINIFIER_EXECUTABLE NAMES shader_minifier.exe HINTS "${PROJECT_SOURCE_DIR}/bin")
    message("Found CTRL-ALT-TEST minifier: ${MINIFIER_EXECUTABLE}")
    add_custom_command(TARGET cozy COMMAND ${MINIFIER_EXECUTABLE} "${PROJECT_SOURCE_DIR}/gfx.h")
endif()

set(SHADER_HEADER gfx.h)
add_custom_target(gfx.h
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/
    COMMAND "${MINIFIER_EXECUTABLE}" underground.frag -o ${SHADER_HEADER}
    SOURCES underground.frag
    BYPRODUCTS ${SHADER_HEADER}
)

add_executable(cozy cozy.c ${SHADER_HEADER})
target_compile_options(cozy PRIVATE /Gy /O1 /fp:fast /GR- /GS- /MT )
target_include_directories(cozy SYSTEM PRIVATE "${OPENGL_INCLUDE_DIR}")
