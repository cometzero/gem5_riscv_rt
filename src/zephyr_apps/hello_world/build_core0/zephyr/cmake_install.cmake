# Install script for directory: /home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr/zephyr

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "TRUE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/home/ubuntu/zephyr-sdk-0.16.8/riscv64-zephyr-elf/bin/riscv64-zephyr-elf-objdump")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/arch/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/lib/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/soc/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/boards/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/subsys/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/drivers/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/acpica/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/cmsis/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/cmsis-dsp/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/cmsis-nn/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/cmsis_6/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/fatfs/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/adi/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_afbr/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_ambiq/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/atmel/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_bouffalolab/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_espressif/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_ethos_u/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_gigadevice/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_infineon/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_intel/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/microchip/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_nordic/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/nuvoton/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_nxp/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/openisa/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/quicklogic/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_renesas/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_rpi_pico/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_sifli/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_silabs/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_st/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_stm32/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_tdk/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_telink/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/ti/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_wch/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hal_wurthelektronik/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/xtensa/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/hostap/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/liblc3/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/libmctp/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/libmetal/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/libsbc/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/littlefs/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/lora-basics-modem/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/loramac-node/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/lvgl/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/mbedtls/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/mcuboot/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/mipi-sys-t/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/nanopb/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/nrf_wifi/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/open-amp/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/openthread/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/percepio/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/picolibc/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/segger/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/trusted-firmware-a/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/trusted-firmware-m/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/uoscore-uedhoc/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/zcbor/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/modules/nrf_hw_models/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/kernel/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/cmake/flash/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/cmake/usage/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/ubuntu/work/gem5/gem5_riscv_rt/src/zephyr_apps/hello_world/build_core0/zephyr/cmake/reports/cmake_install.cmake")
endif()

