cmake_minimum_required(VERSION 3.12)
project(jacro)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME} SCRIPTS_DESTINATION
                             lib/${PROJECT_NAME})

install(
  DIRECTORY
    ${CMAKE_CURRENT_BINARY_DIR}/ament_cmake_python/${PROJECT_NAME}/scripts/
  DESTINATION bin/
  USE_SOURCE_PERMISSIONS)

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_jacro tests/jacro_test.py WORKING_DIRECTORY
                        ${CMAKE_CURRENT_SOURCE_DIR})
endif()

ament_package()
