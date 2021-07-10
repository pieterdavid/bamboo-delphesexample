cmake_minimum_required(VERSION 3.12)

project(DelphesIO LANGUAGES CXX)

if(NOT DEFINED Delphes_VERSION)
  message(FATAL_ERROR "No Delphes version passed, please call CMake with -DDelphes_VERSION=X.Y.Z (a valid git tag)")
endif()

find_package(ROOT REQUIRED COMPONENTS MathCore Physics)

set(DELPHES_INC
  "${CMAKE_CURRENT_BINARY_DIR}/include/DelphesClasses.h"
  "${CMAKE_CURRENT_BINARY_DIR}/include/DelphesFactory.h"
  "${CMAKE_CURRENT_BINARY_DIR}/include/SortableObject.h"
  )
set(DELPHES_SRC
  "src/DelphesClasses.cc"
  "src/DelphesFactory.cc"
  "src/ExRootTreeBranch.cc"
  )
add_custom_target(delphessources
  COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/getSources.sh ${Delphes_VERSION}
  COMMENT "Copying classes from Delphes ${Delphes_VERSION}"
  BYPRODUCTS ${DELPHES_SRC} ${DELPHES_INC}
    "src/ExRootTreeBranch.h"
    "src/ClassesLinkDef.h"
  )

add_library(DelphesIO SHARED ${DELPHES_SRC})
target_include_directories(DelphesIO PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include> $<INSTALL_INTERFACE:include> PRIVATE $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/src>)
target_link_libraries(DelphesIO ROOT::MathCore ROOT::Physics)
set_target_properties(DelphesIO PROPERTIES SOVERSION ${Delphes_VERSION})
add_dependencies(DelphesIO delphessources)

ROOT_GENERATE_DICTIONARY(G__DelphesIO
  "${CMAKE_CURRENT_BINARY_DIR}/include/DelphesClasses.h"
  LINKDEF "${CMAKE_CURRENT_BINARY_DIR}/src/ClassesLinkDef.h"
  MODULE DelphesIO
  )

install(TARGETS DelphesIO LIBRARY DESTINATION lib)
install(FILES ${DELPHES_INC} DESTINATION include)
