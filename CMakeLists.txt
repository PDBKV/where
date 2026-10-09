cmake_minimum_required(VERSION 3.21...4.4)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(Python COMPONENTS NumPy Interpreter Development.Module REQUIRED)
find_package(Cython MODULE REQUIRED VERSION 3.0)
include(UseCython)
include(UseF2Py)

set(EXT "${CMAKE_CURRENT_SOURCE_DIR}/external")

f2py_object_library(f2py_object OBJECT)

# ----- SOFA -----
set(SOFA_CONF "${CMAKE_CURRENT_SOURCE_DIR}/config/download_sofa.conf")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${SOFA_CONF}")
set(SOFA "${EXT}/sofa/src")
if("${SOFA_CONF}" IS_NEWER_THAN "${SOFA}/sofa.pyf")
    execute_process(
        COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/download.py" "sofa"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        RESULT_VARIABLE _rc
    )

    if(_rc)
        message(FATAL_ERROR "download.py failed (${_rc})")
    endif()
    file(TOUCH "${SOFA}/sofa.pyf")
endif()
file(GLOB SOFA_SRCS "${SOFA}/*.for")
f2py_generate_module("${SOFA}/sofa.pyf" ${SOFA_SRCS} OUTPUT_VARIABLE SOFA_FILES)
python_add_library(sofa MODULE "${SOFA_FILES}" WITH_SOABI)
target_link_libraries(sofa PRIVATE f2py_object)
install(TARGETS sofa DESTINATION where/ext)

# ----- HF_EOP -----
set(HFEOP_CONF "${CMAKE_CURRENT_SOURCE_DIR}/config/download_hf_eop.conf")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${HFEOP_CONF}")
set(HFEOP "${EXT}/iers/hfeop")
if("${HFEOP_CONF}" IS_NEWER_THAN "${HFEOP}/hfeop_xyu_mod.pyf")
    execute_process(
        COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/download.py" "hf_eop"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        RESULT_VARIABLE _rc
    )
    if(_rc)
        message(FATAL_ERROR "download.py failed (${_rc})")
    endif()
    file(TOUCH "${HFEOP}/hfeop_xyu_mod.pyf")
endif()
set(HFEOP_SRCS "${HFEOP}/hfeop_xyu_mod.f90")
configure_file("${HFEOP}/hfeop_xyu_mod.pyf" "${CMAKE_CURRENT_BINARY_DIR}/hf_eop.pyf" COPYONLY)
f2py_generate_module("${CMAKE_CURRENT_BINARY_DIR}/hf_eop.pyf" ${HFEOP_SRCS} OUTPUT_VARIABLE HFEOP_FILES)
python_add_library(hf_eop MODULE "${HFEOP_FILES}" WITH_SOABI)
target_link_libraries(hf_eop PRIVATE f2py_object)
install(TARGETS hf_eop DESTINATION where/ext)

# ----- IERS -----
set(IERS_CONF "${CMAKE_CURRENT_SOURCE_DIR}/config/download_iers.conf")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${IERS_CONF}")
set(IERS "${EXT}/iers/src_2010")
if("${IERS_CONF}" IS_NEWER_THAN "${IERS}/iers_2010.pyf")
    execute_process(
        COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/download.py" "iers_2010"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        RESULT_VARIABLE _rc
    )

    if(_rc)
        message(FATAL_ERROR "download.py failed (${_rc})")
    endif()
    file(TOUCH "${IERS}/iers_2010.pyf")
endif()
set(DEHANT_DIR  "${IERS}/libiers-dehant")
set(HARDISP_DIR "${IERS}/libiers-hardisp")
add_library(iers_dehant STATIC
    ${DEHANT_DIR}/CAL2JD.F    ${DEHANT_DIR}/DAT.F      ${DEHANT_DIR}/NORM8.F
    ${DEHANT_DIR}/SPROD.F     ${DEHANT_DIR}/ST1IDIU.F  ${DEHANT_DIR}/ST1ISEM.F
    ${DEHANT_DIR}/ST1L1.F     ${DEHANT_DIR}/STEP2DIU.F ${DEHANT_DIR}/STEP2LON.F
    ${DEHANT_DIR}/ZERO_VEC8.F)

add_library(iers_hardisp STATIC
    ${HARDISP_DIR}/ADMINT.F   ${HARDISP_DIR}/ETUTC.F   ${HARDISP_DIR}/EVAL.F
    ${HARDISP_DIR}/JULDAT.F   ${HARDISP_DIR}/LEAP.F    ${HARDISP_DIR}/MDAY.F
    ${HARDISP_DIR}/RECURS.F   ${HARDISP_DIR}/SHELLS.F  ${HARDISP_DIR}/SPLINE.F
    ${HARDISP_DIR}/TOYMD.F    ${HARDISP_DIR}/TDFRPH.F)

set_target_properties(iers_dehant iers_hardisp PROPERTIES POSITION_INDEPENDENT_CODE ON)
file(GLOB IERS_SRCS "${IERS}/*.F")
f2py_generate_module("${IERS}/iers_2010.pyf" ${IERS_SRCS} OUTPUT_VARIABLE IERS_FILES)
python_add_library(iers_2010 MODULE "${IERS_FILES}" WITH_SOABI)
target_link_libraries(iers_2010 PRIVATE f2py_object iers_dehant iers_hardisp)
install(TARGETS iers_2010 DESTINATION where/ext)

# ----- GPT2W -----
set(GPT_CONF "${CMAKE_CURRENT_SOURCE_DIR}/config/download_gpt2w.conf")
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${GPT_CONF}")
set(GPT "${EXT}/gpt2w/src")
if("${GPT_CONF}" IS_NEWER_THAN "${GPT}/gpt2w.pyf")
    execute_process(
        COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/download.py" "gpt2w"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        RESULT_VARIABLE _rc
    )

    if(_rc)
        message(FATAL_ERROR "download.py failed (${_rc})")
    endif()
    file(TOUCH "${GPT}/gpt2w.pyf")
endif()
set(GPT_SRCS "${GPT}/vmf1_ht.f" "${GPT}/saasthyd.f" "${GPT}/asknewet.f" "${GPT}/gpt2_1w.f")
f2py_generate_module("${GPT}/gpt2w.pyf" ${GPT_SRCS} OUTPUT_VARIABLE GPT2W_FILES)
python_add_library(gpt2w MODULE "${GPT2W_FILES}" WITH_SOABI)
target_link_libraries(gpt2w PRIVATE f2py_object)
install(TARGETS gpt2w DESTINATION where/ext)
#FROM HERE ON OUT EVERYTHING NEEDS CHECKING EXTRA MUCH MORE
# cython_transpile falls back to this variable when CYTHON_ARGS isn't given per call
set(CYTHON_ARGS --annotate -X language_level=3 -X boundscheck=False -X cdivision=True)

file(GLOB PYX_FILES CONFIGURE_DEPENDS
  "${CMAKE_CURRENT_SOURCE_DIR}/where/models/orbit/*.pyx"
  "${CMAKE_CURRENT_SOURCE_DIR}/where/integrators/*.pyx")

foreach(_pyx IN LISTS PYX_FILES)
  get_filename_component(_name "${_pyx}" NAME_WE)                     # e.g. kepler
  get_filename_component(_dir  "${_pyx}" DIRECTORY)
  file(RELATIVE_PATH _rel "${CMAKE_CURRENT_SOURCE_DIR}" "${_dir}")    # where/models/orbit
  string(REPLACE "/" "." _pkg "${_rel}")                              # where.models.orbit
  file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${_rel}")

  cython_transpile("${_pyx}" LANGUAGE C
    MODULE_NAME "${_pkg}.${_name}"
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/${_rel}/${_name}.c"
    OUTPUT_VARIABLE _c)

  python_add_library(${_pkg}.${_name} MODULE "${_c}" WITH_SOABI)
  set_target_properties(${_pkg}.${_name} PROPERTIES OUTPUT_NAME "${_name}")
  target_link_libraries(${_pkg}.${_name} PRIVATE Python::NumPy)
  install(TARGETS ${_pkg}.${_name} DESTINATION "${_rel}")
endforeach()
target_compile_definitions(where.models.orbit._orbit PRIVATE CYTHON_TRACE_NOGIL=1)
